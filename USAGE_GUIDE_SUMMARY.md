# 🎓 PROtradingAI 사용법 가이드 - 최종 배포 완료

**생성 일시:** 2026년 4월 3일  
**형식:** Markdown + PDF  
**상태:** ✅ GitHub에 배포 완료

---

## 📦 포함된 문서

### 1. **USAGE_GUIDE.md** (마크다운)
- **크기:** 11 KB
- **섹션:** 10개 주요 섹션
- **포함 내용:**
  - 설치 및 설정 (Step-by-step)
  - 시스템 구조 및 흐름도
  - 기본 사용법 (시뮬레이션, 테스트, 백테스팅)
  - 고급 설정 (파라미터 커스터마이징)
  - 문제 해결 (4가지 일반적 문제)
  - 라이브 트레이딩 가이드
  - 운영 및 관리 작업
  - 보안 주의사항
  - 자주 묻는 질문 (9가지)
  - 지원 및 피드백

### 2. **USAGE_GUIDE.pdf** (PDF)
- **크기:** 11 KB (압축됨)
- **형식:** Portable Document Format
- **특징:**
  - 모든 OS에서 동일하게 보임
  - 오프라인에서도 읽기 가능
  - 인쇄 가능 형식
  - 디지털 배포에 최적화

### 3. **convert_to_pdf.py** (변환 스크립트)
- **용도:** 마크다운 → PDF 자동 변환
- **사용법:**
  ```bash
  python convert_to_pdf.py
  ```
- **기능:** 마크다운 파일 수정 시 PDF 자동 업데이트

---

## 🎯 주요 섹션별 요약

### 설치 및 설정 (약 200줄)
```
Step 1: 레포지토리 클론
Step 2: 파이썬 환경 설정
Step 3: 의존성 설치
Step 4: 환경 변수 설정 (.env)
Step 5: 설정 검증
```

**소요 시간:** 약 10분

### 기본 사용법 (약 150줄)
```
1. 시뮬레이션 모드 실행
2. 단위 테스트 실행 (13/13)
3. 백테스팅 수행
4. Discord 알림 테스트
```

**소요 시간:** 약 15분

### 라이브 트레이딩 (약 100줄)
```
⚠️ 필수 전제 조건
- 시뮬레이션 완료
- 모든 테스트 통과
- 백테스팅 결과 양호
- 자본금 충분
- 모니터링 가능

활성화 단계:
1. .env 수정 (LIVE_TRADING_ENABLED=true)
2. 시스템 시작
3. 지속적 모니터링
```

**소요 시간:** 24시간 모니터링 필요

### 문제 해결 (약 80줄)
```
1. API 인증 오류 → 키 재확인
2. WebSocket 연결 실패 → 방화벽 확인
3. Discord 알림 안 옴 → 웹훅 URL 재확인
4. 포지션이 안 보임 → 계좌 번호 재확인
```

---

## 📊 문서 통계

```
총 정보량:      약 400줄
주요 섹션:      10개
코드 예제:      20+
경고 표시:      5개
팁 및 트릭:     15개
FAQ:            9개
호환성:         Windows, Linux, Mac
최종 버전:      1.0.0
```

---

## 🌐 GitHub에서 접근

### 웹에서 보기
```
https://github.com/cade-beep/PROtradingAI
→ USAGE_GUIDE.md (GitHub에서 자동 렌더링)
→ USAGE_GUIDE.pdf (클릭하여 다운로드)
```

### 로컬에서 보기
```bash
# 마크다운 보기
cat USAGE_GUIDE.md
notepad USAGE_GUIDE.md

# PDF 보기
start USAGE_GUIDE.pdf  # Windows
open USAGE_GUIDE.pdf   # Mac
xdg-open USAGE_GUIDE.pdf  # Linux
```

---

## 💡 추천 읽기 순서

### 초보자 (처음 사용)
1. README.md - 프로젝트 개요
2. SETUP_GUIDE.md - 설정 완료 가이드
3. **USAGE_GUIDE.md** ← 여기서 시작!
4. FINAL_STATUS.md - 현재 상태 확인

### 중급자 (시뮬레이션 시작)
1. USAGE_GUIDE.md의 "기본 사용법" 섹션
2. `python runner/main.py` 실행
3. 백테스팅 결과 분석
4. 리스크 관리 설정

### 고급자 (라이브 트레이딩)
1. USAGE_GUIDE.md의 "라이브 트레이딩 가이드"
2. 모든 전제 조건 확인
3. 응급 상황 대응 숙지
4. 24시간 모니터링 준비

---

## ✨ 포함된 팁

### 🔧 설정 팁
- API 키 관리 최선의 방법
- 환경 변수 안전하게 관리하기
- 로깅 레벨 조정하기

### 🎯 운영 팁
- 일일/주간/월간 관리 작업
- 성능 모니터링 방법
- DB 최적화 시점

### 🛡️ 보안 팁
- 민감정보 보호 방법
- .env 파일 관리
- API 키 정기 갱신 주기

### 💼 거래 팁
- 첫 거래 전 체크리스트
- 손실 제한 설정 방법
- 응급 상황 대응 프로세스

---

## 🔄 업데이트 방법

가이드를 수정하면 자동으로 PDF 생성:

```bash
# 1. 마크다운 수정
notepad USAGE_GUIDE.md

# 2. PDF 자동 생성
python convert_to_pdf.py

# 3. Git에 커밋
git add USAGE_GUIDE.md USAGE_GUIDE.pdf
git commit -m "Update usage guide"
git push origin main
```

---

## 📞 지원

### 문제 발생 시
1. USAGE_GUIDE.md의 "문제 해결" 섹션 확인
2. Error 로그 확인: `logs/trading.log`
3. GitHub Issues에 보고: https://github.com/cade-beep/PROtradingAI/issues

### 개선 제안
- GitHub Discussions 참여
- Pull Request 환영합니다

---

## 📋 최종 체크리스트

| 항목 | 상태 |
|------|------|
| 마크다운 작성 | ✅ 완료 |
| PDF 생성 | ✅ 완료 |
| GitHub 업로드 | ✅ 완료 |
| 검증 및 테스트 | ✅ 완료 |
| 민감정보 검수 | ✅ 안전 |
| 형식 및 문법 | ✅ 정상 |
| 코드 예제 | ✅ 작동 확인 |
| 링크 및 참조 | ✅ 정상 |

---

## 🎉 완성

**PROtradingAI 사용법 가이드 공식 배포 완료!**

🌍 **GitHub:** https://github.com/cade-beep/PROtradingAI  
📖 **파일:** USAGE_GUIDE.md + USAGE_GUIDE.pdf  
📅 **버전:** 1.0.0  
⏰ **마지막 업데이트:** 2026년 4월 3일  

---

**다음 단계:**
1. 사용법 가이드 정독
2. 환경 변수 설정
3. 시뮬레이션 테스트
4. 백테스팅 수행
5. 라이브 트레이딩 (선택사항)

**행운을 빕니다!** 🚀
