# 🎯 PROtradingAI - 실행 계획서

## 현재 상태 (2026년 4월 3일)

| 영역 | 진행도 | 상태 |
|------|--------|------|
| **코드 개발** | 95% | ✅ 완료 |
| **단위 테스트** | 100% | ✅ 13/13 통과 |
| **시스템 통합** | 90% | ✅ 거의 완료 |
| **보안 조치** | 100% | ✅ GitHub 히스토리 정제 |
| **Discord 알림** | 100% | ✅ 작동 중 |

---

## 🚨 [긴급 우선] API 키 & 웹훅 재발급

### 왜 필요한가?
- GitHub에 실제 API 키와 Discord 웹훅이 노출되었음
- 히스토리는 정제했지만, 누군가 이미 봤을 가능성 있음
- **현재 키/웹훅은 즉시 비활성화 필요**

### 작업 순서

#### **Step 1: Kiwoom API 키 재발급** (5분)
```
1. Kiwoom 개발자 센터 접속 (https://developers.kiwoom.com)
2. 앱 관리 → 기존 APP 비활성화
3. 새로운 앱 등록
4. 새 APP_KEY, APP_SECRET 발급받기
```

#### **Step 2: Discord 웹훅 재생성** (3분)
```
1. Discord 서버 → 채널 설정 → 웹훅
2. 기존 웹훅 삭제
3. 새 웹훅 생성
4. 웹훅 URL 복사
```

#### **Step 3: 로컬 .env 파일 업데이트** (2분)
```bash
# 터미널에서 실행:
cd c:\Users\rbflr\Desktop\PROtradingAI

# .env 파일 열기
notepad .env

# 다음 내용으로 업데이트:
KIWOOM_APP_KEY=새_발급받은_키
KIWOOM_APP_SECRET=새_발급받은_시크릿
KIWOOM_ACCOUNT_NO=123456789012
DISCORD_WEBHOOK_URL=새_생성한_웹훅_URL
LIVE_TRADING_ENABLED=false

# 저장 후 닫기
```

#### **Step 4: 로컬 .env 검증** (2분)
```bash
# 설정이 제대로 로드되는지 확인
python -c "from config.settings import settings; print(f'✓ Key loaded: {settings.kiwoom_app_key[:20]}...'); print(f'✓ Webhook loaded: {settings.discord_webhook_url[:50]}...')"
```

**예상 소요 시간: 12분**

---

## 📊 [다음 우선] 시뮬레이션 테스트

새 키/웹훅이 정상 작동하는지 확인

### 작업 순서

#### **Test 1: Discord 알림 재테스트** (2분)
```bash
python -c "
import asyncio
from notifications.discord import DiscordNotifier

async def test():
    notifier = DiscordNotifier()
    print('[TEST] Discord 알림 테스트 시작...')
    await notifier.notify_order('BUY', 'AAPL', 10, 150.0)
    await notifier.notify_error('테스트 오류')
    await notifier.notify_pnl(50000)
    print('[SUCCESS] 모든 알림 전송 완료!')

asyncio.run(test())
"
```

**기대 결과:** Discord에 3개의 메시지 도착 → ✅

#### **Test 2: 시스템 통합 테스트** (5분)
```bash
# 안전 모드 (LIVE_TRADING_ENABLED=false)에서 실행
python runner/main.py

# 실행 후 확인:
# - WebSocket 연결 성공
# - 시장 데이터 수신
# - Discord 알림 정상
# - 오류 없음
```

**기대 결과:** 모든 모듈 정상 작동 → ✅

#### **Test 3: 전체 테스트 재실행** (3분)
```bash
pytest tests/ -v

# 결과: 13/13 통과 확인
```

**예상 소요 시간: 10분**

---

## 📈 [선택] 백테스팅 수행

전략의 역사적 성능 검증

### 작업 순서

```bash
# 백테스트 실행
python backtest/backtest.py

# 출력 확인:
# - 총 거래 횟수
# - 승배 (매매 수익률)
# - 누적 수익
# - 최대 낙폭 (MDD)
```

**의의:** 
- 전략이 과거에 잘 작동했는지 확인
- 라이브 트레이딩 전 신뢰도 검증

**예상 소요 시간: 15분**

---

## ⚡ [라이브 준비] 라이브 트레이딩 활성화

**⚠️ 주의: 이 단계는 실제 자금이 움직입니다. 매우 신중히 진행하세요.**

### 전제 조건 (모두 만족해야 함)
- [ ] Step 1-3 (API 키 재발급) 완료
- [ ] Test 1-3 (시뮬레이션 테스트) 모두 통과
- [ ] 백테스팅 결과 양호
- [ ] 손실 한도 충분히 설정 (예: 일일 -100,000원)

### 활성화 절차

```bash
# 1. .env 파일에서 수정
notepad .env

# 다음 줄 변경:
# LIVE_TRADING_ENABLED=true

# 2. 소액 테스트 (예: 10만원 이하)
python runner/main.py

# 3. 모니터링
# - Discord 알림 수신 확인
# - 포지션 변화 모니터링
# - 오류 발생 즉시 종료
```

**예상 소요 시간: 1-2시간 (실시간 모니터링 필요)**

---

## 📋 체계별 실행 스케줄

### **오늘 할 것 (지금 바로)**
1. ✅ API 키 & 웹훅 재발급 (12분)
2. ✅ 시뮬레이션 테스트 (10분)
3. ✅ 백테스팅 (15분)

**총 37분 → 완료 후 상황 판단**

### **내일 할 것 (선택사항)**
1. 라이브 트레이딩 활성화
2. 추가 리스크 관리 규칙 설정
3. 마켓 캘린더 통합

### **추후 할 것 (장기)**
1. 웹 대시보드 개발
2. 고급 전략 추가
3. PostgreSQL 마이그레이션

---

## ✅ 시스템 점검 리스트

### 보안
- [ ] 새 API 키 발급했는가?
- [ ] 새 Discord 웹훅 생성했는가?
- [ ] 로컬 .env 파일은 GitHub에 업로드 금지 상태인가?
- [ ] `.gitignore`에 `.env` 포함되어 있는가?

### 기능성
- [ ] 13개 단위 테스트 모두 통과하는가?
- [ ] Discord 알림이 정상 작동하는가?
- [ ] 시뮬레이션 (LIVE_TRADING_ENABLED=false) 테스트 성공했는가?
- [ ] 백테스팅 결과 양호한가?

### 준비
- [ ] 손실 한도 설정했는가?
- [ ] 충분한 자본금이 있는가?
- [ ] 시장 시간이 맞는가 (09:00-15:30 KST)?
- [ ] 모니터링 시간을 확보했는가?

---

## 🆘 문제 발생 시 대응

| 문제 | 해결책 |
|------|--------|
| Discord 알림 실패 | 웹훅 URL 확인, 새 웹훅 생성 |
| 테스트 실패 (13개 중 일부) | pytest 오류 메시지 확인, 환경 변수 재설정 |
| API 키 인증 실패 | Kiwoom 개발자 센터에서 키 복사 재확인 |
| WebSocket 연결 실패 | 인터넷 연결 확인, 방화벽 설정 검토 |
| 포지션이 안 보임 | 계좌 번호 재확인, 주문 권한 확인 |

---

## 🎯 **지금 바로 시작할 것**

```
1. Kiwoom 개발자 센터 접속 → 새 API 키 발급
2. Discord → 새 웹훅 생성
3. 로컬 .env 파일 업데이트
4. 테스트 실행
5. 성공 보고 후 다음 단계 결정
```

---

**준비가 되면 터미널에서 다음 명령 실행하세요:**

```bash
cd c:\Users\rbflr\Desktop\PROtradingAI
python -c "from config.settings import settings; print('✓ System ready')"
```

성공 메시지가 나오면 다음 단계 진행 가능! 🚀
