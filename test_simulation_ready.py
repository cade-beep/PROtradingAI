# Automated simulation test for live trading readiness
# This script validates the entire system without executing real trades

import asyncio
import sys
from datetime import datetime
import json
from pathlib import Path

# Configuration
SIMULATION_DURATION_MINUTES = 5  # Quick validation run
SAFE_MODE_ENABLED = True

async def test_imports():
    """테스트 1: 모든 모듈 임포트 확인"""
    print("\n" + "="*60)
    print("🔍 TEST 1: Module Import Validation")
    print("="*60)
    
    modules_to_test = [
        "config.settings",
        "auth.token_manager",
        "broker_api.kiwoom_client",
        "market_data.quotes",
        "market_data.realtime",
        "order.validator",
        "order.reconciler",
        "strategy.strategy",
        "portfolio.portfolio",
        "risk.risk",
        "notifications.discord",
    ]
    
    failed = []
    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"  ✅ {module_name}")
        except Exception as e:
            print(f"  ❌ {module_name}: {e}")
            failed.append(module_name)
    
    if failed:
        print(f"\n⚠️  {len(failed)} modules failed to import")
        return False
    
    print(f"\n✅ All {len(modules_to_test)} modules imported successfully")
    return True

async def test_configuration():
    """테스트 2: 설정 로드 확인"""
    print("\n" + "="*60)
    print("🔍 TEST 2: Configuration Validation")
    print("="*60)
    
    try:
        from config.settings import settings
        
        print(f"  ✅ Kiwoom APP_KEY: {settings.kiwoom_app_key[:20]}... ({len(settings.kiwoom_app_key)} chars)")
        print(f"  ✅ Kiwoom APP_SECRET: {settings.kiwoom_app_secret[:20]}... ({len(settings.kiwoom_app_secret)} chars)")
        print(f"  ✅ Account Number: {settings.kiwoom_account_no}")
        print(f"  ✅ Discord Webhook: {settings.discord_webhook_url[:60]}...")
        print(f"  ✅ Live Trading Enabled: {settings.live_trading_enabled}")
        print(f"  ✅ Max Position Size: {settings.max_position_size}%")
        print(f"  ✅ Daily Loss Limit: {settings.daily_loss_limit:,} KRW")
        
        # Safety check
        if settings.live_trading_enabled:
            print(f"\n⚠️  WARNING: LIVE_TRADING_ENABLED=true")
            print(f"   This is a simulation. Set LIVE_TRADING_ENABLED=false in .env")
            return False
        else:
            print(f"\n✅ Safe mode active: LIVE_TRADING_ENABLED=false")
            
        return True
    except Exception as e:
        print(f"  ❌ Configuration error: {e}")
        return False

async def test_market_calendar():
    """테스트 3: 시장 캘린더 확인"""
    print("\n" + "="*60)
    print("🔍 TEST 3: Market Calendar Validation")
    print("="*60)
    
    try:
        from market_calendar import MarketCalendar
        
        calendar = MarketCalendar()
        is_open = calendar.is_market_open()
        current_time = calendar.get_current_kst_time()
        
        print(f"  ✅ Current KST Time: {current_time}")
        print(f"  ✅ Market Open Now: {is_open}")
        print(f"  ✅ Market Sessions: {calendar.sessions}")
        
        return True
    except Exception as e:
        print(f"  ❌ Market calendar error: {e}")
        return False

async def test_portfolio():
    """테스트 4: 포트폴리오 초기화 확인"""
    print("\n" + "="*60)
    print("🔍 TEST 4: Portfolio Initialization")
    print("="*60)
    
    try:
        from portfolio.portfolio import Portfolio
        
        portfolio = Portfolio(initial_cash=1000000)
        
        print(f"  ✅ Initial Cash: {portfolio.cash:,} KRW")
        print(f"  ✅ Total Value: {portfolio.get_total_value():,} KRW")
        print(f"  ✅ Positions: {len(portfolio.positions)}")
        print(f"  ✅ Daily PnL: {portfolio.daily_pnl:,} KRW")
        
        return True
    except Exception as e:
        print(f"  ❌ Portfolio error: {e}")
        return False

async def test_strategy():
    """테스트 5: 거래 전략 초기화"""
    print("\n" + "="*60)
    print("🔍 TEST 5: Trading Strategy Initialization")
    print("="*60)
    
    try:
        from strategy.strategy import TradingStrategy
        
        strategy = TradingStrategy()
        
        print(f"  ✅ Strategy Name: {strategy.name}")
        print(f"  ✅ Short MA Period: {strategy.short_ma_period}")
        print(f"  ✅ Long MA Period: {strategy.long_ma_period}")
        print(f"  ✅ Min Price: {strategy.min_price:,} KRW")
        
        return True
    except Exception as e:
        print(f"  ❌ Strategy error: {e}")
        return False

async def test_discord_notification():
    """테스트 6: Discord 알림 테스트"""
    print("\n" + "="*60)
    print("🔍 TEST 6: Discord Notification System")
    print("="*60)
    
    try:
        from notifications.discord import DiscordNotifier
        
        notifier = DiscordNotifier()
        
        # Send test notification
        await notifier.notify_order(
            symbol="TEST",
            qty=1,
            price=100000,
            side="BUY"
        )
        print(f"  ✅ Test order notification sent")
        
        await notifier.notify_error("This is a test error message")
        print(f"  ✅ Test error notification sent")
        
        print(f"\n✅ Discord webhook is working")
        print(f"   Check your Discord channel for 2 messages")
        
        return True
    except Exception as e:
        print(f"  ❌ Discord notification error: {e}")
        print(f"  ⚠️  Check your webhook URL in .env")
        return False

async def run_all_tests():
    """모든 테스트 실행"""
    print("\n")
    print("🚀" * 30)
    print("PROtradingAI - Live Trading System Simulation Test")
    print("시작 시간:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("🚀" * 30)
    
    results = {}
    
    # Run tests sequentially
    results["imports"] = await test_imports()
    results["config"] = await test_configuration()
    results["calendar"] = await test_market_calendar()
    results["portfolio"] = await test_portfolio()
    results["strategy"] = await test_strategy()
    results["discord"] = await test_discord_notification()
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name:20} {status}")
    
    print(f"\n결과: {passed}/{total} 통과")
    
    if passed == total:
        print("\n" + "🎉" * 30)
        print("✅ 모든 테스트 통과! 라이브 트레이딩 준비 완료!")
        print("🎉" * 30)
        print("\n다음 단계:")
        print("  1. Discord 채널에서 테스트 메시지 확인")
        print("  2. LIVE_TRADING_CHECKLIST.md 항목 완료")
        print("  3. runner/main.py 실행")
        print("  4. 포트폴리오 모니터링")
        return 0
    else:
        print("\n" + "⚠️ " * 30)
        print(f"❌ {total - passed}개의 테스트 실패")
        print("⚠️ " * 30)
        print("\n실패 항목:")
        for test_name, result in results.items():
            if not result:
                print(f"  - {test_name}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
