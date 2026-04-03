# PROtradingAI - Kiwoom Auto Trader

자동매매 시스템 for Kiwoom Securities API.

## 프로젝트 개요

이 프로젝트는 Kiwoom 증권 REST API를 활용한 자동매매 시스템입니다. Python 3.11+ 기반으로 구축되었으며, 실시간 시장 데이터 수신, 전략 기반 자동 주문, 리스크 관리, 포트폴리오 추적, Telegram 알림 기능을 제공합니다.

## 주요 기능

- **인증 및 토큰 관리**: Kiwoom API 토큰 자동 발급 및 갱신
- **시장 데이터**: 실시간 WebSocket 연결을 통한 시장 데이터 수신
- **주문 관리**: 사전 유효성 검사 및 자동 주문 실행
- **상태 동기화**: 로컬 DB를 통한 주문/체결 상태 동기화
- **전략 모듈**: 이동평균 크로스오버 기반 매매 전략
- **포트폴리오 관리**: 현금 및 포지션 추적
- **리스크 관리**: 포지션 사이즈 및 손실 제한
- **알림**: Telegram 봇을 통한 실시간 알림

## 설치 및 설정

### 요구사항
- Python 3.11+
- Git

### 설치
```bash
git clone <repository-url>
cd PROtradingAI
pip install -r requirements.txt
```

### 환경 변수 설정
`.env` 파일을 생성하고 다음 변수를 설정하세요:
```
KIWOOM_APP_KEY=your_app_key
KIWOOM_APP_SECRET=your_app_secret
KIWOOM_ACCOUNT_NO=your_account_no
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
LIVE_TRADING_ENABLED=false
```

## 사용법

### 테스트 실행
```bash
python runner/main.py
```

### 단위 테스트
```bash
pytest tests/
```

## 프로젝트 구조

```
PROtradingAI/
├── auth/                 # 인증 모듈
├── broker_api/           # Kiwoom API 클라이언트
├── config/               # 설정 관리
├── db/                   # 데이터베이스 모듈
├── market_data/          # 시장 데이터 모듈
├── notifications/        # 알림 모듈
├── order/                # 주문 관련 모듈
├── portfolio/            # 포트폴리오 관리
├── risk/                 # 리스크 관리
├── runner/               # 메인 실행 파일
├── strategy/             # 매매 전략
├── tests/                # 테스트 파일
├── .env                  # 환경 변수
├── requirements.txt      # 의존성
└── README.md             # 이 파일
```

## 안전 주의사항

- **LIVE_TRADING_ENABLED=false** 상태에서만 개발 및 테스트하세요.
- 실제 트레이딩 전 충분한 백테스트와 시뮬레이션 수행하세요.
- API 키 및 민감 정보는 .env 파일에서만 관리하세요.
- 리스크 관리 파라미터를 실제 자산 규모에 맞게 조정하세요.

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 기여

기여를 환영합니다. 이슈나 풀 리퀘스트를 통해 참여하세요.