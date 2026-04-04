# Quick Start Guide for Live Trading

## 🚀 빠른 시작 (5분)

### 1️⃣ API 키 업데이트 (선택지 A 또는 B)

#### 선택지 A: 자동 업데이트 (권장)
```powershell
cd c:\Users\rbflr\Desktop\PROtradingAI
.\update_credentials.ps1

# 프롬프트 나타나면:
# 1. Kiwoom APP_KEY 입력
# 2. Kiwoom APP_SECRET 입력  
# 3. Discord Webhook URL 입력
# 4. Kiwoom 계좌번호 입력 (선택)
```

#### 선택지 B: 수동 업데이트
```powershell
notepad .env

# 다음 4줄 수정:
KIWOOM_APP_KEY=새발급받은키
KIWOOM_APP_SECRET=새발급받은시크릿
DISCORD_WEBHOOK_URL=새생성한웹훅URL
KIWOOM_ACCOUNT_NO=계좌번호

# Ctrl+S 저장 후 닫기
```

### 2️⃣ 설정 검증
```powershell
python -c "from config.settings import settings; print('✓ Settings OK')"
```

### 3️⃣ 전체 시스템 테스트 (자동)
```powershell
python test_simulation_ready.py
```

**기대 결과:** ✅ 모든 테스트 통과

---

## 🎯 3가지 실행 모드

### Mode 1: 시뮬레이션 (안전 테스트) ⭐ 권장
```powershell
# .env에서 LIVE_TRADING_ENABLED=false 확인

python runner/main.py

# 또는 백그라운드 실행
$job = Start-Job -ScriptBlock { 
    cd "c:\Users\rbflr\Desktop\PROtradingAI"
    python runner/main.py 
}

# 상태 확인
Get-Job

# 종료
Stop-Job -Id $job.Id
```

**용도:** 
- 시스템 안정성 테스트 (1~2시간)
- 실제 시장 데이터 수신 확인
- Discord 알림 정상 작동 확인
- 거래 신호 정상 생성 확인

---

### Mode 2: 백테스팅 (과거 데이터 검증)
```powershell
python backtest/backtest.py
```

**용도:**
- 전략의 과거 성능 검증
- 수익성 검증
- 최대 손실 확인

**결과 해석:**
- Return: 양수면 수익성 있음
- Max Drawdown: 작을수록 안정적
- Sharpe Ratio: 높을수록 위험 조정 수익 좋음

---

### Mode 3: 라이브 트레이딩 (실제 거래) ⚠️ 주의
```powershell
# ⚠️ 절대 급할 필요 없음. Mode 1 최소 2시간 충분히 테스트 후!

# Step 1: .env 파일 수정
notepad .env
# LIVE_TRADING_ENABLED=false → true 변경

# Step 2: 시스템 시작
python runner/main.py

# Step 3: 모니터링
# - Discord 실시간 거래 알림 확인
# - 포트폴리오 손익 변화 확인
# - 로그 파일 실시간 감시

# Step 4: 문제 발생 시 즉시 중단
# Ctrl+C 누르면 거래 중단 (진행 중인 주문은 완료됨)
```

**주의사항:**
- 처음 거래는 최소 자금으로 시작
- 손실 한도 설정하기 (예: -100,000원 넘으면 자동 중단)
- 모니터링 가능한 시간에만 실행

---

## 📊 모니터링

### 실시간 모니터링 (Mode 1, 2, 3 모두 적용)
```powershell
# Discord에서 실시간 알림 수신
# - 거래 신호 발생
# - 주문 체결
# - 손익 업데이트

# 또는 로그 파일 감시
Get-Content "monitoring/logs/protrading_app.log" -Tail 50 -Wait
```

### 성능 메트릭
```powershell
# 포트폴리오 현황
python -c "
from portfolio.portfolio import Portfolio
p = Portfolio(1000000)
print(f'Total Value: {p.get_total_value():,}')
print(f'Daily PnL: {p.daily_pnl:,}')
print(f'Positions: {len(p.positions)}')
"
```

---

## 🚨 문제 해결

### 문제: ImportError 또는 ModuleNotFoundError
```powershell
# Step 1: 의존성 설치
pip install -r requirements.txt

# Step 2: 다시 테스트
python test_simulation_ready.py
```

### 문제: Discord 알림 안 옴
```powershell
# Step 1: 웹훅 URL 확인
python -c "from config.settings import settings; print(settings.discord_webhook_url)"

# Step 2: 웹훅 유효성 테스트
python test_live_setup.py

# Step 3: Discord 서버 권한 확인
# - 채널이 웹훅 메시지 수신 가능한가?
# - 봇이 메시지 작성 권한이 있는가?
```

### 문제: "Market is closed" 오류
```
정상 동작입니다!
시스템이 한국 거래소 개장 시간 (09:00~15:30 KST)을 확인 중입니다.

개장 중에 다시 실행하세요.
```

### 문제: Kiwoom API 연결 실패
```powershell
# Step 1: API 키 확인
python -c "from config.settings import settings; print(f'Key: {settings.kiwoom_app_key[:20]}...')"

# Step 2: 네트워크 연결 확인
Invoke-WebRequest -Uri "https://api.kiwoom.com" -UseBasicParsing | Select-Object StatusCode

# Step 3: 방화벽 확인
# - Windows Defender + 기타 방화벽이 api.kiwoom.com 차단하고 있지 않은가?
```

---

## ✅ 체크리스트 (라이브 출시 전)

#### 보안
- [ ] 새 API 키 발급받음
- [ ] 새 Discord 웹훅 생성함
- [ ] .env 파일이 .gitignore에 포함됨
- [ ] git status에서 .env가 보이지 않음

#### 기능
- [ ] test_simulation_ready.py 모두 통과
- [ ] pytest tests/ 모두 통과
- [ ] 시뮬레이션 모드 2시간 이상 안정
- [ ] 백테스팅 결과 만족

#### 자금 & 위험
- [ ] Kiwoom 계좌에 거래 자금 입금
- [ ] 최대 포지션 크기 설정 (5~10%)
- [ ] 일일 손실 한도 설정 (-100,000원 이상)
- [ ] 모니터링 가능 시간 확보

#### 운영
- [ ] Discord 채널 준비 (실시간 알림 확인)
- [ ] 로그 파일 위치 확인 (monitoring/logs/)
- [ ] 긴급 중단 방법 숙지 (Ctrl+C)

---

## 📞 지원

**첫 실행이 불안하면:**
1. 모든 단위 테스트 통과 확인: `python -m pytest tests/ -v`
2. 시뮬레이션 테스트 완료: `python test_simulation_ready.py`
3. 시뮬레이션 모드 1시간 실행: `python runner/main.py`
4. 로그 파일 에러 없음 확인: 에러가 있으면 해결 후 라이브

**장애 시:**
- 로그 파일: `monitoring/logs/protrading_*.log`
- 에러 메시지: JSON 형식으로 상세 기록됨
- 복구: LIVE_TRADING_ENABLED=false로 변경 → 재시작

---

**준비 완료?** 👇

```
1. update_credentials.ps1 실행 (또는 수동 .env 수정)
2. python test_simulation_ready.py 실행
3. 모두 통과하면 python runner/main.py
```

**화이팅!** 🚀
