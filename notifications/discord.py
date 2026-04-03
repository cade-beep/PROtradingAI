import logging
import httpx
from config.settings import settings

logger = logging.getLogger(__name__)

class DiscordNotifier:
    """
    Discord 알림 모듈
    주요 이벤트(주문, 오류 등)를 Discord 웹훅으로 전송합니다.
    """
    def __init__(self):
        self.webhook_url = settings.discord_webhook_url

    async def send_message(self, message: str, embed_color: int = 0x00b4d8):
        """
        메시지를 Discord로 전송합니다.
        """
        if not self.webhook_url:
            logger.warning("Discord 웹훅 URL이 설정되지 않았습니다.")
            return

        payload = {
            "embeds": [
                {
                    "description": message,
                    "color": embed_color
                }
            ]
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.webhook_url, json=payload, timeout=10.0)
                response.raise_for_status()
                logger.info("Discord 알림 전송 성공")
        except httpx.HTTPError as e:
            logger.error(f"Discord 알림 전송 실패: {str(e)}")

    async def notify_order(self, action: str, symbol: str, qty: int, price: float):
        """
        주문 알림을 전송합니다.
        """
        message = f"📈 주문 실행: {action.upper()} {qty}주 {symbol} @ {price}원"
        await self.send_message(message, embed_color=0x00b4d8)

    async def notify_error(self, error_msg: str):
        """
        오류 알림을 전송합니다.
        """
        message = f"🚨 오류 발생: {error_msg}"
        await self.send_message(message, embed_color=0xff006e)

    async def notify_pnl(self, pnl: float):
        """
        손익 알림을 전송합니다.
        """
        color = 0x06ffa5 if pnl >= 0 else 0xff006e  # 수익이면 초록색, 손실이면 빨간색
        symbol = "📈" if pnl >= 0 else "📉"
        message = f"{symbol} 현재 손익: {pnl:,.0f}원"
        await self.send_message(message, embed_color=color)
