# PROtradingAI 사용법 가이드

## 목차

1. 설치 및 설정
2. 시스템 구조
3. 기본 사용법
4. 고급 설정
5. 문제 해결
6. 보안 주의사항
7. 라이선스

---

## 1. 설치 및 설정

### 1.1 사전 요구사항

- **OS**: Windows 10/11 또는 Linux
- **Python**: 3.11 이상
- **Git**: 최신 버전
- **Kiwoom 계정**: 증권사 계좌 필요
- **Discord 서버**: 알림 수신용

### 1.2 설치 단계

#### Step 1: 레포지토리 클론
```bash
git clone https://github.com/cade-beep/PROtradingAI.git
cd PROtradingAI
```

#### Step 2: 파이썬 환경 설정
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (Linux/Mac)
source venv/bin/activate
```

#### Step 3: 의존성 설치
```bash
pip install -r requirements.txt
```

#### Step 4: 환경 변수 설정

`.env.example`을 참조하여 `.env` 파일 생성:

```bash
# .env 파일 생성
cp .env.example .env
```

`.env` 파일에 다음 정보 입력:

```env
# Kiwoom API 인증정보
KIWOOM_APP_KEY=your_app_key_from_kiwoom
KIWOOM_APP_SECRET=your_app_secret_from_kiwoom
KIWOOM_ACCOUNT_NO=your_account_number

# Discord 웹훅 URL (알림용)
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN

# 거래 모드 (false=시뮬레이션, true=실제거래)
LIVE_TRADING_ENABLED=false
```

#### Step 5: 설정 검증
```bash
python -c "from config.settings import settings; print(settings)"
```

정상 출력되면 설정 완료!

---

## 2. 시스템 구조

### 2.1 주요 모듈

```
PROtradingAI/
├── auth/              → Kiwoom API 인증 및 토큰 관리
├── broker_api/        → REST API 호출 및 응답 처리
├── market_data/       → 실시간 시장 데이터 수신
├── strategy/          → 매매 신호 생성 로직
├── portfolio/         → 포지션 및 손익 추적
├── risk/              → 리스크 관리 및 제한
├── order/             → 주문 검증 및 동기화
├── notifications/     → Discord 알림
├── runner/            → 시스템 실행 엔진
├── backtest/          → 백테스팅 도구
└── tests/             → 단위 테스트
```

### 2.2 거래 흐름도

```
1. 토큰 발급
   ↓
2. 계좌 정보 조회
   ↓
3. 시장 데이터 수신 (WebSocket)
   ↓
4. 전략 분석
   ↓
5. Pre-trade 검증
   ↓
6. 주문 실행
   ↓
7. 주문 상태 동기화
   ↓
8. 포지션 업데이트 및 알림
```

---

## 3. 기본 사용법

### 3.1 시뮬레이션 모드 실행

**가장 안전한 첫 번째 테스트:**

```bash
# 활성 환경 확인
echo $LIVE_TRADING_ENABLED  # false 이어야 함

# 시스템 시작
python runner/main.py
```

**출력 예시:**
```
[INFO] === 시스템 시작: 통합 테스트 ===
[INFO] 안내: 현재 모의/테스트 모드입니다.
[INFO] --- 실시간 웹소켓 & Pub/Sub 백그라운드 구동 ---
[INFO] WebSocket 연결 성공
[INFO] 시장 데이터 컨슈머 태스크 시작
```

### 3.2 단위 테스트 실행

모든 모듈이 정상 작동하는지 확인:

```bash
pytest tests/ -v
```

**기대 결과:**
```
test_auth.py::test_issue_token_success PASSED
test_portfolio.py::test_portfolio_buy PASSED
test_strategy.py::test_trading_strategy_buy_signal PASSED
... (13/13 통과)
```

### 3.3 백테스팅 수행

과거 데이터로 전략 검증:

```bash
python backtest/backtest.py
```

**출력 예시:**
```
[BACKTEST] 초기 자본금: 1,000,000원
[BACKTEST] 총 거래 횟수: 12회
[BACKTEST] 승률: 66.67%
[BACKTEST] 누적 수익: 125,000원
[BACKTEST] 최대 낙폭: -32,500원
```

### 3.4 Discord 알림 테스트

알림 시스템이 정상 작동하는지 확인:

```bash
python -c "
import asyncio
from notifications.discord import DiscordNotifier

async def test():
    notifier = DiscordNotifier()
    await notifier.notify_order('BUY', 'AAPL', 10, 150.0)
    await notifier.notify_error('테스트 오류')

asyncio.run(test())
"
```

Discord 채널에 메시지 2개가 도착하면 성공!

---

## 4. 고급 설정

### 4.1 리스크 관리 파라미터 조정

`config/settings.py` 또는 `.env` 파일에서 설정:

```python
# 설정 예시
MAX_POSITION_SIZE = 10  # 최대 포지션: 10주
MAX_DAILY_LOSS = 100000  # 일일 손실 한도: 100,000원
MAX_TRADES_PER_DAY = 10  # 일일 최대 거래: 10회
```

### 4.2 전략 커스터마이징

`strategy/strategy.py`에서 이동평균 설정 변경:

```python
class TradingStrategy:
    def __init__(self):
        self.short_window = 5   # 단기 이동평균 (기본: 5)
        self.long_window = 20   # 장기 이동평균 (기본: 20)
        self.data = {}
```

### 4.3 로깅 레벨 조정

`config/logging.py` 수정:

```python
# DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = 'INFO'
LOG_FILE = 'logs/trading.log'
```

### 4.4 데이터베이스 마이그레이션

SQLite에서 PostgreSQL로 변경:

```python
# db/db.py 수정
DB_TYPE = 'postgresql'
DB_URL = 'postgresql://user:password@localhost/protradingai'
```

---

## 5. 문제 해결

### 5.1 API 인증 오류

**증상:** `401 Unauthorized` 오류

**해결방법:**
1. Kiwoom 개발자 센터에서 APP_KEY 확인
2. `.env` 파일 기간 만료 확인
3. 새로운 키 발급 후 `.env` 업데이트
4. 가상환경 재시작

```bash
# 완전 재시작
deactivate
venv\Scripts\activate
python runner/main.py
```

### 5.2 WebSocket 연결 실패

**증상:** `Connection refused` 또는 `Network timeout`

**해결방법:**
1. 인터넷 연결 확인
2. 방화벽 설정 확인 (포트 443 열려있어야 함)
3. Kiwoom 서버 상태 확인
4. 다시 시작

```bash
python runner/main.py
```

### 5.3 Discord 알림 안 옴

**증상:** 주문 후 알림이 없음

**해결방법:**
1. Discord 웹훅 URL 확인
2. 웹훅 CHANNEL 권한 확인
3. 새 웹훅 생성하여 `.env` 업데이트
4. 테스트 알림 재전송

```bash
python -c "import asyncio; from notifications.discord import DiscordNotifier; asyncio.run(DiscordNotifier().notify_order('TEST', 'TEST', 1, 100))"
```

### 5.4 포지션이 보이지 않음

**증상:** 주문 후 포지션 미업데이트

**해결방법:**
1. 계좌 번호 정확성 확인
2. `.env` KIWOOM_ACCOUNT_NO 재확인
3. Kiwoom 웹에서 직접 확인
4. 로그에서 오류 메시지 확인

```bash
# 로그 확인
tail logs/trading.log
```

---

## 6. 라이브 트레이딩 가이드

### ⚠️ 중요: 전제 조건 체크리스트

라이브 트레이딩을 시작하기 전에 반드시 확인하세요:

- [ ] 시뮬레이션 모드 테스트 완료 및 성공
- [ ] 모든 단위 테스트 통과 (13/13)
- [ ] 백테스팅 결과 양호 (승률 40% 이상)
- [ ] Discord 알림 정상 작동
- [ ] 최소 필요 자본금 준비 (권장: 1,000,000원 이상)
- [ ] 손실 한도 설정 (권장: -100,000원)
- [ ] 모니터링 시간 확보 (거래시간: 09:00-15:30 KST)

### 6.1 라이브 모드 활성화

```bash
# 1. .env 파일 수정
LIVE_TRADING_ENABLED=true

# 2. 시스템 시작
python runner/main.py

# 3. 모니터링 (필수)
# → Discord 알림 수신 확인
# → 포지션 변화 모니터링
# → 오류 발생 시 즉시 종료
```

### 6.2 응급 상황 대응

**즉시 모든 거래 중지:**

```bash
# 1. 터미널에서 Ctrl+C 누르기
# 또는

# 2. 수동으로 포지션 정리
# → Kiwoom 웹/앱에서 직접 매도
```

### 6.3 데일리 리포트

매일 거래 후 확인:

```bash
# 오늘의 거래 내역 조회
python -c "
import sqlite3
conn = sqlite3.connect('orders.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM orders WHERE created_at >= date(\"now\")')
for row in cursor.fetchall():
    print(row)
"
```

---

## 7. 운영 가이드

### 7.1 일일 관리 작업

**아침 8:50 (거래 전)**
```bash
# 시스템 시작
python runner/main.py
```

**종료 후 16:00 (거래 후)**
```bash
# Ctrl+C로 중지

# 로그 확인
cat logs/trading.log

# DB 백업
cp orders.db orders_backup_$(date +%Y%m%d).db
```

### 7.2 주간 관리 작업

**매주 월요일:**
1. 지난주 거래 분석
2. 백테스팅 재수행
3. 전략 파라미터 검토
4. 리스크 한도 재조정

### 7.3 월간 관리 작업

**매달 1일:**
1. 전전월 거래 내역 아카이빙
2. DB 최적화
   ```sql
   VACUUM;
   ```
3. 성과 보고서 작성

---

## 8. 보안 주의사항

### 8.1 API 키 보호

- ❌ API 키를 코드에 하드코딩 금지
- ❌ API 키를 GitHub에 업로드 금지
- ✅ `.env` 파일 사용 (`.gitignore`에 포함)
- ✅ API 키 정기적 갱신

### 8.2 .env 파일 관리

```bash
# .env는 절대 git에 올리지 않기
git rm --cached .env  # .env가 git에 있다면

# .gitignore에 .env 포함 확인
cat .gitignore | grep "^.env$"
```

### 8.3 자산 보호

- 자동 거래 한도 설정 (일일 손실 제한)
- 주문 전 자동 검증 (Pre-trade 체크)
- 포지션 크기 제한
- 거래 시간 제한 (09:00-15:20)

---

## 9. FAQ

### Q: 어떤 전략이 사용되나요?
**A:** 이동평균 크로스오버 전략입니다. 단기 이동평균(5일)이 장기 이동평균(20일)을 상향 돌파하면 매수, 하향 돌파하면 매도합니다.

### Q: 24시간 거래 가능한가요?
**A:** 아니요. 한국 주식시장 시간(09:00-15:30 KST)에만 거래 가능합니다. 관련 코드는 `market_calendar.py`에 있습니다.

### Q: 손실이 나면 어떻게 되나요?
**A:** 설정된 일일 손실 한도에 도달하면 자동으로 모든 신규 주문이 중지됩니다. 기존 포지션은 매도 명령만 실행됩니다.

### Q: 휴일에도 실행되나요?
**A:** 아니요. KRX 공휴일은 자동 감지되어 거래가 차단됩니다.

### Q: 여러 계좌로 운영 가능한가요?
**A:** 현재는 단일 계좌만 지원합니다. 추후 버전에서 멀티 계좌 지원 예정입니다.

---

## 10. 지원 및 피드백

### 문제 보고
- GitHub Issues: https://github.com/cade-beep/PROtradingAI/issues
- 상세한 로그와 함께 리포트 부탁드립니다

### 개선 제안
- GitHub Discussions 참여
- Pull Request 환영합니다

### 추가 문서
- [FINAL_STATUS.md](FINAL_STATUS.md) - 전체 상태 보고서
- [NEXT_STEPS.md](NEXT_STEPS.md) - 다음 단계 가이드
- [README.md](README.md) - 프로젝트 개요

---

## 라이선스

MIT License - 자유롭게 사용 가능합니다.

---

**마지막 업데이트:** 2026년 4월 3일  
**버전:** 1.0.0  
**상태:** Production Ready (API 키 발급 필수)
