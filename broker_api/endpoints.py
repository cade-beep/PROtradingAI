import httpx
import logging
from typing import Dict, Any
from config.settings import settings
from auth.token_manager import TokenManager

logger = logging.getLogger(__name__)

class OrderableAmountClient:
    """
    [kt00010] 출금가능/주문가능 금액 조회 클라이언트
    """
    def __init__(self, token_manager: TokenManager):
        self.host = settings.kiwoom_api_host
        self.token_manager = token_manager

    async def _get_headers(self, tr_id: str) -> dict:
        token = await self.token_manager.issue_token()
        return {
            "Authorization": f"Bearer {token}",
            "appkey": settings.kiwoom_app_key,
            "appsecret": settings.kiwoom_app_secret,
            "Content-Type": "application/json; charset=utf-8",
            "tr_id": tr_id
        }

    async def get_orderable_cash(self, account_no: str) -> Dict[str, Any]:
        """
        [kt00010] 주문 가능 금액 및 출금 가능 금액 조회
        *주의: 실제 API 엔드포인트와 파라미터는 키움증권 공식 문서를 반드시 확인하여 수정해야 합니다.
        """
        # 임시 엔드포인트 (공식 문서에 맞게 수정 필요)
        url = f"{self.host}/uapi/domestic-stock/v1/trading/inquire-balance" 
        
        params = {
            "account_no": account_no,
            # 기타 필수 파라미터 (비밀번호, 조회 구분 등 문서 참고)
        }

        try:
            headers = await self._get_headers(tr_id="kt00010")
            
            async with httpx.AsyncClient() as client:
                logger.info(f"요청: 출금/주문가능 금액 조회 (kt00010) - 계좌: {account_no}")
                response = await client.get(url, headers=headers, params=params, timeout=10.0)
                response.raise_for_status()
                
                data = response.json()
                logger.info("성공: 주문 가능 금액 조회 완료")
                return data

        except httpx.HTTPStatusError as e:
            logger.error(f"실패: 주문가능금액 조회 HTTP 오류 - {e.response.status_code} {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"실패: 주문가능금액 조회 중 예외 발생 - {str(e)}")
            raise
