import httpx
import logging
from typing import Dict, Any
from config.settings import settings
from auth.token_manager import TokenManager

logger = logging.getLogger(__name__)

class MarketDataClient:
    """
    키움증권 REST API 시장 데이터(현재가 등) 조회 클라이언트
    """
    def __init__(self, token_manager: TokenManager):
        self.host = settings.kiwoom_api_host
        self.token_manager = token_manager

    async def get_current_price(self, symbol: str) -> Dict[str, Any]:
        """
        특정 종목의 현재가를 조회합니다.
        *주의: 실제 API 엔드포인트와 파라미터는 키움증권 공식 문서를 반드시 확인하여 수정해야 합니다.
        """
        token = await self.token_manager.issue_token()
        
        # 임시 엔드포인트 및 파라미터 (공식 문서에 맞게 수정 필요)
        url = f"{self.host}/uapi/domestic-stock/v1/quotations/inquire-price"
        headers = {
            "Authorization": f"Bearer {token}",
            "appkey": settings.kiwoom_app_key,
            "appsecret": settings.kiwoom_app_secret,
            "tr_id": "FHKST01010100"  # 예시 TR 코드
        }
        params = {"FID_INPUT_ISCD": symbol}

        try:
            async with httpx.AsyncClient() as client:
                logger.info(f"요청: 현재가 조회 - 종목: {symbol}")
                response = await client.get(url, headers=headers, params=params, timeout=5.0)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"현재가 조회 API 통신 오류: {str(e)}")
            raise