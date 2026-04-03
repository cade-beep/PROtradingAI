import httpx
import logging
from datetime import datetime, timedelta
from typing import Optional
from config.settings import settings
from market_calendar import MarketCalendar

logger = logging.getLogger(__name__)

class TokenManager:
    """
    키움증권 REST API 토큰 발급 및 관리 (au10001)
    """
    def __init__(self):
        self.host = settings.kiwoom_api_host
        self.app_key = settings.kiwoom_app_key
        self.app_secret = settings.kiwoom_app_secret
        self._access_token: Optional[str] = None
        self._expires_at: Optional[datetime] = None

    async def issue_token(self) -> str:
        """
        [au10001] Access token issuance
        """
        # 만료 전이면 캐시된 토큰 반환 (보수적으로 10분 전 만료 처리)
        if self._access_token and self._expires_at and MarketCalendar.get_current_kst_time() < self._expires_at - timedelta(minutes=10):
            return self._access_token

        url = f"{self.host}/oauth2/token"
        payload = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "scope": "oob" # 통상적인 scope 값
        }

        try:
            async with httpx.AsyncClient() as client:
                logger.info(f"요청: 토큰 발급 (au10001) - URL: {url}")
                response = await client.post(url, json=payload, timeout=10.0)
                response.raise_for_status()
                
                data = response.json()
                self._access_token = data.get("access_token")
                expires_in = int(data.get("expires_in", 3600))
                
                if not self._access_token:
                    raise ValueError("응답에 access_token이 없습니다.")
                
                self._expires_at = MarketCalendar.get_current_kst_time() + timedelta(seconds=expires_in)
                logger.info("성공: 토큰 발급 완료")
                return self._access_token

        except httpx.HTTPStatusError as e:
            logger.error(f"실패: 토큰 발급 HTTP 오류 - {e.response.status_code} {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"실패: 토큰 발급 중 예외 발생 - {str(e)}")
            raise
