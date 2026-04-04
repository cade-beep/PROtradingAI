# Test script to verify Discord webhook and settings

import asyncio
import httpx
from config.settings import settings
from notifications.discord import DiscordNotifier

async def test_discord_webhook():
    """Discord 웹훅이 정상 작동하는지 테스트"""
    print("🔍 Discord 웹훅 테스트 시작...\n")
    
    try:
        notifier = DiscordNotifier()
        
        # 테스트 1: 주문 알림
        print("📨 [Test 1] 주문 알림 전송...")
        await notifier.notify_order(symbol="AAPL", qty=10, price=150.0, side="BUY")
        print("   ✅ 주문 알림 전송 성공\n")
        
        # 테스트 2: 오류 알림  
        print("📨 [Test 2] 오류 알림 전송...")
        await notifier.notify_error("테스트 오류 메시지")
        print("   ✅ 오류 알림 전송 성공\n")
        
        # 테스트 3: PnL 알림
        print("📨 [Test 3] 손익 알림 전송...")
        await notifier.notify_pnl(realized_pnl=50000, unrealized_pnl=-10000)
        print("   ✅ 손익 알림 전송 성공\n")
        
        print("=" * 50)
        print("✅ 모든 Discord 테스트 통과!")
        print("=" * 50)
        print("\n💡 Discord 채널을 확인하세요. 위의 3개 메시지가 도착했어야 합니다.\n")
        
    except Exception as e:
        print(f"❌ Discord 테스트 실패: {e}\n")
        print("⚠️  웹훅 URL이 정확한지 확인하세요.\n")

async def main():
    print("🚀 PROtradingAI 라이브 준비 테스트\n")
    
    # 설정 검증
    print("📋 설정 검증:")
    print(f"   App Key: {settings.kiwoom_app_key[:20]}...({len(settings.kiwoom_app_key)} chars)")
    print(f"   App Secret: {settings.kiwoom_app_secret[:20]}...({len(settings.kiwoom_app_secret)} chars)")
    print(f"   Account No: {settings.kiwoom_account_no}")
    print(f"   Webhook: {settings.discord_webhook_url[:60]}...")
    print(f"   Live Trading: {settings.live_trading_enabled}\n")
    
    # Discord 테스트
    await test_discord_webhook()

if __name__ == "__main__":
    asyncio.run(main())
