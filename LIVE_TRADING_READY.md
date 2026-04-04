# 🎯 라이브 트레이딩 준비 - 최종 실행 가이드

**작성:** 2026년 4월 5일  
**상태:** ✅ 모든 준비 완료, 사용자 입력 대기 중

---

## 📋 현재 상황

```
프로젝트 상태: 100% 완료 (Step 1~8)
테스트 상태: 13/13 통과 ✅
보안 상태: GitHub 히스토리 정제됨 ✅
새로운 도구: 5개 파일 생성 ✅
```

---

## 🚀 당신이 지금 해야 할 일 (3단계)

### **Step 1️⃣: 새 API 키 발급 (15분) - 수동**

#### Kiwoom 새 키 발급
```
🌐 접속: https://developers.kiwoom.com
👤 로그인
🔧 메뉴: 앱 관리
❌ 기존 앱 비활성화 (GitHub 노출됨)
✨ 새 앱 생성
📝 발급받기: APP_KEY, APP_SECRET 복사
```

#### Discord 새 웹훅 생성
```
📱 Discord 서버 접속
⚙️ 채널 설정 → 웹훅
❌ 기존 웹훅 삭제
✨ 새 웹훅 생성
📝 URL 복사: https://discord.com/api/webhooks/...
```

---

### **Step 2️⃣: .env 파일 업데이트 (2분) - 자동 또는 수동**

**선택지 A: 자동** (더 쉬움)
```powershell
cd c:\Users\rbflr\Desktop\PROtradingAI
.\update_credentials.ps1

# 프롬프트에 위에서 복사한 값 입력:
# 1. APP_KEY
# 2. APP_SECRET
# 3. Discord Webhook URL
# 4. 계좌번호 (선택)
```

**선택지 B: 수동**
```powershell
notepad .env

# 4개 줄 수정:
KIWOOM_APP_KEY=새발급값
KIWOOM_APP_SECRET=새발급값
DISCORD_WEBHOOK_URL=새생성값
KIWOOM_ACCOUNT_NO=계좌번호

# Ctrl+S → 저장
```

---

### **Step 3️⃣: 검증 & 자동 테스트 (5분) - 자동**

```powershell
cd c:\Users\rbflr\Desktop\PROtradingAI

# 전체 시스템 검증
python test_simulation_ready.py
```

**기대 결과:**
```
✅ Module imports
✅ Configuration  
✅ Market calendar
✅ Portfolio
✅ Trading strategy
✅ Discord notification

결과: 6/6 통과!
모든 테스트 통과! 라이브 트레이딩 준비 완료!
```

**Discord에 도착해야 할 메시지:** 2개
- [TEST ORDER] Order placed for TEST
- [TEST ERROR] This is a test error message

---

## 📈 다음 단계 (선택)

### Mode A: 시뮬레이션 (권장) ⭐
```powershell
python runner/main.py

# 안전 모드 (LIVE_TRADING_ENABLED=false)
# 실제 거래는 일어나지 않음
# 1~2시간 실행하여 안정성 확인
```

### Mode B: 각 모듈 개별 테스트
```powershell
python -m pytest tests/ -v    # 단위 테스트
python backtest/backtest.py   # 백테스팅
```

### Mode C: 라이브 트레이딩 (주의!) ⚠️
```powershell
# Step 1: .env 수정
LIVE_TRADING_ENABLED=false → true

# Step 2: 시스템 시작
python runner/main.py

# Step 3: 실시간 모니터링
# Discord + 로그 파일 확인
```

---

## 📊 생성된 파일 설명

| 파일 | 용도 | 명령어 |
|------|------|--------|
| `update_credentials.ps1` | API 키 자동 업데이트 | `.\update_credentials.ps1` |
| `test_live_setup.py` | Discord 웹훅 테스트 | `python test_live_setup.py` |
| `test_simulation_ready.py` | 전체 시스템 검증 | `python test_simulation_ready.py` |
| `LIVE_TRADING_CHECKLIST.md` | 출시 전 체크리스트 | 참고용 문서 |
| `QUICK_START.md` | 빠른 시작 가이드 | 참고용 문서 |

---

## ✅ 최종 체크리스트

```
[ ] 새 Kiwoom API 키 발급받음
[ ] 새 Discord 웹훅 생성함
[ ] update_credentials.ps1 또는 수동으로 .env 업데이트
[ ] test_simulation_ready.py 모두 통과 (6/6)
[ ] Discord 채널에 2개 메시지 도착 확인
[ ] 시뮬레이션 모드에서 최소 30분 이상 테스트
```

---

## 🎯 성공의 징표

✅ 모두 완료되면:
- Python 오류 없음
- Discord 알림 정상 작동
- 포트폴리오 업데이트 정상
- 거래 신호 생성 중

---

## 📞 문제 해결

### 문제: 테스트 실패
```
→ requirements.txt 재설치
pip install -r requirements.txt

→ 다시 테스트
python test_simulation_ready.py
```

### 문제: Discord 알림 안 옴
```
→ 웹훅 URL 확인
python -c "from config.settings import settings; print(settings.discord_webhook_url)"

→ Discord 서버 권한 확인
→ 채널에서 웹훅 메시지 수신 가능한지 확인
```

### 문제: "Market is closed" 오류
```
→ 한국 거래소 개장 시간: 09:00~15:30 KST
→ 개장 중에 다시 시도하세요
```

---

## 🎉 준비 완료!

**다음 명령어를 순서대로 실행하세요:**

```powershell
# 1. 자동 업데이트 (위의 자격증 입력)
.\update_credentials.ps1

# 2. 전체 검증
python test_simulation_ready.py

# 3. Discord 확인
# → Discord 채널에 메시지 도착 확인

# 4. 시뮬레이션 시작 (안전)
python runner/main.py
```

**모두 통과하면 라이브 트레이딩 준비 완료!** 🚀

---

**궁금한 점이 있으면:**
1. QUICK_START.md 참고
2. LIVE_TRADING_CHECKLIST.md 확인
3. 문서의 문제 해결 섹션 검토

**행운을 빕니다!** ✨
