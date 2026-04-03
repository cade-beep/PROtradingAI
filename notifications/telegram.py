import logging
import httpx
from config.settings import settings

logger = logging.getLogger(__name__)

class TelegramNotifier:
    """
    Telegram 알림 모듈
    주요 이벤트(주문, 오류 등)를 Telegram으로 전송합니다.
    """
    def __init__(self):
        self.bot_token = settings.telegram_bot_token
        self.chat_id = settings.telegram_chat_id
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    async def send_message(self, message: str):
        """
        메시지를 Telegram으로 전송합니다.
        """
        if not self.bot_token or not self.chat_id:
            logger.warning("Telegram 토큰 또는 채팅 ID가 설정되지 않았습니다.")
            return

        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=10.0)
                response.raise_for_status()
                logger.info("Telegram 알림 전송 성공")
        except httpx.HTTPError as e:
            logger.error(f"Telegram 알림 전송 실패: {str(e)}")

    async def notify_order(self, action: str, symbol: str, qty: int, price: float):
        """
        주문 알림을 전송합니다.
        """
        message = f"📈 주문 실행: {action.upper()} {qty}주 {symbol} @ {price}원"
        await self.send_message(message)

    async def notify_error(self, error_msg: str):
        """
        오류 알림을 전송합니다.
        """
        message = f"🚨 오류 발생: {error_msg}"
        await self.send_message(message)

    async def notify_pnl(self, pnl: float):
        """
        손익 알림을 전송합니다.
        """
        message = f"💰 현재 손익: {pnl:,.0f}원"
        await self.send_message(message)