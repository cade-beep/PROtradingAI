#!/usr/bin/env pwsh
# PROtradingAI 실행 가능한 체크리스트
# Windows PowerShell에서 직접 실행 가능

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PROtradingAI - 실행 체크리스트" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 환경 확인
Write-Host "[1/4] 환경 설정 확인..." -ForegroundColor Yellow
try {
    python -c "from config.settings import settings; print(f'    ✓ Kiwoom Account: {settings.kiwoom_account_no}'); print(f'    ✓ Discord Webhook: {settings.discord_webhook_url[:50]}...'); print(f'    ✓ Live Trading: {settings.live_trading_enabled}')" -ErrorAction Stop
} catch {
    Write-Host "    ✗ 환경 설정 로드 실패" -ForegroundColor Red
    Write-Host "    → .env 파일 확인 필요" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 2. 모듈 임포트 확인
Write-Host "[2/4] 핵심 모듈 확인..." -ForegroundColor Yellow
try {
    python -c "
from notifications.discord import DiscordNotifier
from strategy.strategy import TradingStrategy
from portfolio.portfolio import Portfolio
from risk.risk import RiskManager
print('    ✓ 모든 핵심 모듈 정상')
" -ErrorAction Stop
} catch {
    Write-Host "    ✗ 모듈 로드 실패" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 3. 테스트 실행
Write-Host "[3/4] 단위 테스트 실행..." -ForegroundColor Yellow
Write-Host "    (이 과정은 1분 정도 소요됩니다)"
$testOutput = pytest tests/ -q 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "    ✓ 모든 테스트 통과" -ForegroundColor Green
} else {
    Write-Host "    ✗ 테스트 실패" -ForegroundColor Red
    Write-Host $testOutput
    exit 1
}
Write-Host ""

# 4. Discord 알림 테스트
Write-Host "[4/4] Discord 알림 테스트..." -ForegroundColor Yellow
try {
    python -c "
import asyncio
from notifications.discord import DiscordNotifier

async def test():
    notifier = DiscordNotifier()
    await notifier.send_message('[TEST] PROtradingAI 시스템 준비 완료! 🚀')

asyncio.run(test())
print('    ✓ Discord 알림 전송 성공')
" -ErrorAction Stop
} catch {
    Write-Host "    ✗ Discord 알림 실패 (웹훅 URL 확인 필요)" -ForegroundColor Red
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ 시스템 준비 완료!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "다음 단계:" -ForegroundColor Cyan
Write-Host "  1. 새로운 API 키 발급"
Write-Host "  2. 새로운 Discord 웹훅 생성"
Write-Host "  3. 로컬 .env 파일 업데이트"
Write-Host "  4. python runner/main.py 실행 (시뮬레이션 모드)"
Write-Host ""
