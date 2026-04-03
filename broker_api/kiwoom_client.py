import httpx
import logging
from config.settings import settings
from auth.token_manager import TokenManager

logger = logging.getLogger(__name__)

class KiwoomClient:
    """
    키움증권 REST API 클라이언트
    """
    def __init__(self, token_manager: TokenManager):
        self.host = settings.kiwoom_api_host
        self.token_manager = token_manager

    async def _get_headers(self) -> dict:
        token = await self.token_manager.issue_token()
        return {
            "Authorization": f"Bearer {token}",
            "appkey": settings.kiwoom_app_key,
            "appsecret": settings.kiwoom_app_secret,
            "Content-Type": "application/json; charset=utf-8"
        }

    async def get_account_info(self, account_no: str) -> dict:
        """
        [ka00001] Account number lookup
        실제 엔드포인트 경로는 공식 문서를 확인하여 수정해야 합니다.
        """
        url = f"{self.host}/uapi/domestic-stock/v1/trading/inquire-account" # 예시 경로
        params = {
            "account_no": account_no
            # 추가적으로 필요한 파라미터들 (TR코드 등)
        }

        try:
            headers = await self._get_headers()
            # TR 코드가 헤더에 필요한 경우 추가
            headers["tr_id"] = "ka00001"
            
            async with httpx.AsyncClient() as client:
                logger.info(f"요청: 계좌번호 조회 (ka00001) - Account: {account_no}")
                response = await client.get(url, headers=headers, params=params, timeout=10.0)
                response.raise_for_status()
                
                data = response.json()
                logger.info("성공: 계좌번호 조회 완료")
                return data

        except httpx.HTTPStatusError as e:
            logger.error(f"실패: 계좌조회 HTTP 오류 - {e.response.status_code} {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"실패: 계좌조회 중 예외 발생 - {str(e)}")
            raise
