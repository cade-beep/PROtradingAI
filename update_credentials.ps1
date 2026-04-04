# Update credentials in .env file
# Usage: .\update_credentials.ps1

Write-Host "🔐 PROtradingAI 자격증 업데이트 스크립트" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GitHub에 노출된 API 키/웹훅을 새로운 것으로 교체합니다`n" -ForegroundColor Yellow

# 백업 생성
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupPath = ".env.backup_$timestamp"
Copy-Item ".env" $backupPath -Force
Write-Host "✓ 백업 생성됨: $backupPath`n" -ForegroundColor Green

# 새 자격증 입력
Write-Host "🔑 새로운 자격증을 입력하세요 (GitHub에서 발급받은 것):`n"

$appKey = Read-Host "Kiwoom APP_KEY"
$appSecret = Read-Host "Kiwoom APP_SECRET"
$discordWebhook = Read-Host "Discord Webhook URL"
$accountNo = Read-Host "Kiwoom 계좌번호 (선택사항, 엔터하면 기존값 유지)"

# 기존 .env 파일 읽기
$envContent = Get-Content ".env" -Raw

# 새 값으로 교체
$envContent = $envContent -replace 'KIWOOM_APP_KEY=.*', "KIWOOM_APP_KEY=$appKey"
$envContent = $envContent -replace 'KIWOOM_APP_SECRET=.*', "KIWOOM_APP_SECRET=$appSecret"
$envContent = $envContent -replace 'DISCORD_WEBHOOK_URL=.*', "DISCORD_WEBHOOK_URL=$discordWebhook"

if ($accountNo) {
    $envContent = $envContent -replace 'KIWOOM_ACCOUNT_NO=.*', "KIWOOM_ACCOUNT_NO=$accountNo"
}

# 새 값으로 .env 파일 저장
$envContent | Set-Content ".env" -Encoding UTF8
Write-Host "`n✅ .env 파일이 업데이트되었습니다!" -ForegroundColor Green

# 검증
Write-Host "`n🔍 설정 검증 중...`n"
python -c "
from config.settings import settings
print(f'✓ App Key loaded: {len(settings.kiwoom_app_key)} characters')
print(f'✓ Webhook loaded: {len(settings.discord_webhook_url)} characters')
print(f'✓ Account No: {settings.kiwoom_account_no}')
print(f'✓ Trading enabled: {settings.live_trading_enabled}')
print(f'✓ All settings loaded successfully!')
"

Write-Host "`n⚠️  중요 안내:`n" -ForegroundColor Yellow
Write-Host "1. .env 파일은 절대 GitHub에 업로드하면 안 됩니다 (.gitignore에 포함됨)"
Write-Host "2. LIVE_TRADING_ENABLED=false 상태에서 테스트 후 거래를 시작하세요"
Write-Host "3. 백업 파일: $backupPath`n"
