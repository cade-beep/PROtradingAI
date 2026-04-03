import logging
from typing import Dict, Any, List
import httpx
from config.settings import settings
from auth.token_manager import TokenManager
from db.orders import OrderDatabase

logger = logging.getLogger(__name__)

class OrderReconciler:
    """
    주문/체결 상태 동기화 (Reconciler)
    네트워크 타임아웃, 웹소켓 유실 등에 대비하여 REST API로 당일 미체결 내역을 확실하게 재조회합니다.
    """
    def __init__(self, token_manager: TokenManager):
        self.host = settings.kiwoom_api_host
        self.token_manager = token_manager
        self.db = OrderDatabase()
        
    async def init_db(self):
        await self.db.init_db()
        
    async def fetch_open_orders(self, account_no: str) -> List[Dict[str, Any]]:
        """
        해당 계좌의 미체결 내역(Open Orders)을 조회합니다.
        *주의: API 엔드포인트와 TR 코드는 키움증권 최신 공식 문서(예: 주식일별주문체결조회)를 확인해야 합니다.
        """
        token = await self.token_manager.issue_token()
        # 임시 엔드포인트 및 파라미터 구성
        url = f"{self.host}/uapi/domestic-stock/v1/trading/inquire-daily-ccld" 
        
        headers = {
            "Authorization": f"Bearer {token}",
            "appkey": settings.kiwoom_app_key,
            "appsecret": settings.kiwoom_app_secret,
            "tr_id": "TTTC8001R"  # 예시 TR 코드 (미체결/체결 내역 조회)
        }
        
        params = {
            "CANO": account_no[:8],          # 종합계좌번호 앞 8자리
            "ACNT_PRDT_CD": account_no[8:],  # 계좌상품코드
            "INQR_STRT_DT": "",              # 조회시작일자 (보통 공백 시 당일)
            "INQR_END_DT": "",               # 조회종료일자
            "SLL_BUY_DVSN_CD": "00",         # 전체 매수/매도
            "INQR_DVSN": "00",               # 조회구분
            "PDNO": "",                      # 종목코드 (공백 시 전체)
            "CCLD_DVSN": "02"                # 체결구분 (02: 미체결)
        }

        try:
            async with httpx.AsyncClient() as client:
                logger.info(f"요청: 미체결 내역 재조회 - 계좌: {account_no}")
                response = await client.get(url, headers=headers, params=params, timeout=10.0)
                response.raise_for_status()
                
                data = response.json()
                # 응답 구조는 API 문서에 따라 output1, output2 등으로 나뉠 수 있습니다.
                open_orders = data.get("output1", [])
                logger.info(f"성공: 미체결 내역 {len(open_orders)}건 확인됨")
                return open_orders
                
        except httpx.HTTPError as e:
            logger.error(f"실패: 미체결 내역 조회 통신 오류 - {str(e)}")
            # 네트워크 오류 시, 주문 로직에 안전하게 "상태 불명"임을 알리기 위해 예외를 전파합니다.
            raise

    async def reconcile_orders(self, account_no: str):
        """
        로컬 주문 상태를 브로커의 미체결 내역과 동기화합니다.
        """
        try:
            fetched_orders = await self.fetch_open_orders(account_no)
            local_open = await self.db.get_open_orders()
            
            # fetched 주문의 order_no 목록 (API 응답 키에 따라 조정 필요, 예: 'ord_no')
            fetched_order_nos = {order.get('ord_no', order.get('order_no')) for order in fetched_orders}
            
            # 로컬 오픈 주문 중 fetched에 없는 것은 체결된 것으로 간주
            for local_order in local_open:
                if local_order['order_no'] not in fetched_order_nos:
                    await self.db.update_order_status(local_order['order_no'], 'filled')
                    logger.info(f"주문 체결 확인: {local_order['order_no']}")
            
            # fetched에 있는 주문은 오픈 상태로 업데이트
            for fetched_order in fetched_orders:
                order_no = fetched_order.get('ord_no', fetched_order.get('order_no'))
                if order_no:
                    await self.db.update_order_status(order_no, 'open')
            
            logger.info("주문 상태 동기화 완료")
        except Exception as e:
            logger.error(f"주문 동기화 실패: {str(e)}")
            raise

    async def store_order(self, order_no: str, symbol: str, qty: int, price: int, order_type: str):
        """
        주문 실행 시 로컬 DB에 저장합니다.
        """
        await self.db.insert_order(order_no, symbol, qty, price, order_type, 'pending')
        logger.info(f"주문 저장: {order_no}")