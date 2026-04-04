# 🚀 라이브 트레이딩 시작 체크리스트

작성: 2026년 4월 5일  
시스템: PROtradingAI (Kiwoom Securities REST API)

---

## 📋 사전 체크리스트 (출시 전 필수)

### Phase 1: 보안 & 설정 (완료 후 체크)

- [ ] **API 키 재발급**
  - [ ] Kiwoom 새 APP_KEY 발급받음
  - [ ] Kiwoom 새 APP_SECRET 발급받음
  - [ ] Discord 새 웹훅 URL 생성함
  
- [ ] **.env 파일 업데이트**
  - [ ] `update_credentials.ps1` 실행 또는 수동 수정
  - [ ] `.env` 파일이 `.gitignore`에 포함되어 있음 확인
  - [ ] `git status`에서 `.env`이 표시되지 않는지 확인
  
- [ ] **설정 검증**
  ```powershell
  python -c "from config.settings import settings; print('✓ Settings loaded')"
  ```

### Phase 2: 기능 테스트

- [ ] **Discord 웹훅 테스트**
  ```powershell
  python test_live_setup.py
  ```
  기대 결과: Discord 채널에 3개 메시지 도착

- [ ] **모든 단위 테스트 통과**
  ```powershell
  python -m pytest tests/ -v
  ```
  기대 결과: 13/13 통과

- [ ] **시뮬레이션 모드 테스트**
  ```powershell
  # LIVE_TRADING_ENABLED=false 상태 확인
  python runner/main.py
  ```
  기대 결과: 오류 없이 실행, WebSocket 연결 성공, Discord 알림 수신

### Phase 3: 라이브 설정

- [ ] **거래 자금 준비**
  - [ ] Kiwoom 계좌에 거래 자금 입금 (추천: 1~5백만원)
  - [ ] 계좌번호 `.env`에 정확히 입력되어 있음 확인
  
- [ ] **위험 관리 설정**
  - [ ] `config/settings.py` 확인:
    - `MAX_POSITION_SIZE`: 계좌 자산의 5~10%
    - `DAILY_LOSS_LIMIT`: -100,000원 이상
    - `MAX_PER_SYMBOL_WEIGHT`: 20% 이상
  
- [ ] **거래 시간 확인**
  - [ ] 한국 거래소 개장 시간: 09:00~15:30 KST
  - [ ] 시스템이 KST 타임존 사용 중 확인: `market_calendar.py`

- [ ] **모니터링 준비**
  - [ ] Discord 채널이 실시간 알림 받을 상태
  - [ ] 거래 중 모니터링 가능한 시간 확보

---

## ⚠️ 안전 가드레일 (자동 활성화)

### 자동 제한 규칙

```
1. Market Hours Check
   - 현재 시각이 KRX 개장 시간 내인지 확인
   - 아니면 주문 거부
   
2. Pre-Trade Validation (order/validator.py)
   - 이용 가능 자금 충분한지 확인 ✓
   - 계좌 보유 통화 정확한지 확인 ✓
   - 최대 포지션 크기 초과 여부 확인 ✓
   - 최대 심볼 비중 초과 여부 확인 ✓
   - 일일 손실 한도 초과 여부 확인 ✓
   
3. Order Deduplication
   - 중복 주문 방지 (idempotency key 사용)
   
4. Fail-Safe Mode
   - API 연결 실패 → 자동 중단
   - 토큰 만료 → 자동 갱신 + 재연결
   - Discord 알림 실패 → 로그 기록 (거래는 진행)
```

---

## 🎯 첫 거래 실행 흐름

### Step 1: 시뮬레이션 확인 (권장 2시간)
```powershell
# LIVE_TRADING_ENABLED=false 상태에서
python runner/main.py

# 실시간 모니터링
# - 시장 데이터 수신 확인
# - 포트폴리오 업데이트 확인
# - 거래 신호 수신 확인 (가상 거래)
# - Discord 알림 도착 확인
```

**확인 항목:**
- WebSocket 연결 안정 (재연결 없이 30분 이상 유지)
- 거래 신호 정상 생성 (이동평균 크로스오버)
- 포트폴리오 손익 계산 정상
- Discord 모든 알림 수신

### Step 2: LIVE 모드 활성화 (신중하게)
```
1. .env 파일 열기
   LIVE_TRADING_ENABLED=false → true 로 변경
   
2. Python 다시 실행
   python runner/main.py
   
3. 첫 거래 감시
   - 첫 주문이 Kiwoom API로 전송되는지 확인
   - 주문 체결 상태를 Discord에서 확인
   - 포트폴리오 손익이 실제로 업데이트되는지 확인
```

### Step 3: 자동 모니터링 (장시간 운영)
```powershell
# 백그라운드에서 실행 (PowerShell)
$job = Start-Job -ScriptBlock { 
    cd "c:\Users\rbflr\Desktop\PROtradingAI"
    python runner/main.py 
}

# 상태 확인
Get-Job

# 종료 (필요시)
Stop-Job -Id $job.Id
```

---

## 🚨 장애 대응

### 문제: WebSocket 연결 끊김
```
증상: "WebSocket connection closed"
처리: 자동 재연결 (5초 대기 후)
상태: 정상 (재연결 시도 로그 확인)
```

### 문제: 주문 실패 (잔액 부족)
```
증상: "Insufficient funds" 에러
처리: 주문 취소, Discord 알림 발송
상태: 거래 자금 확인 필요
```

### 문제: API 토큰 만료
```
증상: "Token expired" 에러
처리: 자동 토큰 갱신 (token_manager.py)
상태: 정상 (갱신 후 재시도)
```

### 문제: Discord 알림 실패
```
증상: Discord 채널에 메시지 없음
처리: 로그 파일에 기록됨 (거래는 진행)
상태: 웹훅 URL 재확인 필요
```

---

## 📊 모니터링 지표

### 실시간 모니터링 (runner/main.py 실행 중)
- 현재 포트폴리오 가치
- 오늘의 손익 (실현 + 미실현)
- 활성 포지션 (심볼, 수량, 평균비)
- 거래 신호 신뢰도 (0~100%)

### 로그 파일 확인
```powershell
# 마지막 100줄 확인
Get-Content "monitoring/logs/protrading_app.log" -Tail 100

# 주문 관련 로그만 필터
Select-String "order" "monitoring/logs/protrading_app.log"
```

---

## ✅ 라이브 출시 최종 체크

```
[ ] Phase 1: 보안 & 설정 완료
    - API 키 재발급 ✓
    - .env 업데이트 ✓
    - 설정 검증 ✓

[ ] Phase 2: 기능 테스트 완료
    - Discord 테스트 ✓
    - 모든 단위 테스트 통과 ✓
    - 시뮬레이션 테스트 2시간 이상 ✓

[ ] Phase 3: 라이브 설정 완료
    - 거래 자금 입금 ✓
    - 위험 관리 설정 ✓
    - 모니터링 준비 ✓

[ ] LIVE_TRADING_ENABLED=true 설정
    - 첫 거래 신중하게 실행 ✓
    - 포트폴리오 실시간 감시 ✓
```

---

## 📞 비상연락

**문제 발생 시:**
1. 거래 중단 (Ctrl+C)
2. `.env`에서 `LIVE_TRADING_ENABLED=false`로 변경
3. 로그 파일 확인: `monitoring/logs/protrading_*.log`
4. 에러 메시지 Discord에 캡처

**지원:**
- GitHub Issues: 버그 보고
- 로그 분석: JSON 형식의 상세 로그 검토

---

**준비가 되셨으면 위 체크리스트를 하나씩 완료하세요!** ✨
