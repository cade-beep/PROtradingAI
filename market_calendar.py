import logging
from datetime import datetime, time, timedelta
from typing import Optional
import pytz

logger = logging.getLogger(__name__)


class MarketCalendar:
    """
    한국 증권시장 캘린더 모듈
    KST 타임존 기반 시장 운영시간 및 휴장일 관리
    """

    # KST 타임존
    KST = pytz.timezone('Asia/Seoul')

    # 시장 세션 시간 (KST)
    PRE_MARKET_START = time(8, 30)    # 08:30
    REGULAR_START = time(9, 0)        # 09:00
    REGULAR_END = time(15, 20)        # 15:20
    CLOSING_AUCTION_START = time(15, 20)  # 15:20
    CLOSING_AUCTION_END = time(15, 30)    # 15:30
    AFTER_HOURS_ODD_LOT_END = time(16, 0)  # 16:00
    AFTER_HOURS_BLOCK_END = time(18, 0)    # 18:00

    # KRX 공휴일 및 휴장일 (2024-2025년 기준 - 정기 업데이트 필요)
    HOLIDAYS_2024 = [
        "2024-01-01",  # 신정
        "2024-02-09", "2024-02-10", "2024-02-11", "2024-02-12",  # 설날
        "2024-03-01",  # 삼일절
        "2024-04-10",  # 국회의원 선거
        "2024-05-05", "2024-05-06",  # 어린이날 대체휴일
        "2024-05-15",  # 석가탄신일
        "2024-06-06",  # 현충일
        "2024-08-15",  # 광복절
        "2024-09-16", "2024-09-17", "2024-09-18",  # 추석
        "2024-10-03", "2024-10-09",  # 개천절, 한글날
        "2024-12-25",  # 성탄절
        "2024-12-31",  # 연말휴장
    ]

    HOLIDAYS_2025 = [
        "2025-01-01",  # 신정
        "2025-01-28", "2025-01-29", "2025-01-30",  # 설날
        "2025-03-01",  # 삼일절
        "2025-03-03",  # 대통령 선거
        "2025-05-05",  # 어린이날
        "2025-05-06",  # 석가탄신일
        "2025-06-06",  # 현충일
        "2025-08-15",  # 광복절
        "2025-10-03", "2025-10-05", "2025-10-06", "2025-10-07", "2025-10-08", "2025-10-09",  # 추석, 개천절, 한글날
        "2025-12-25",  # 성탄절
        "2025-12-31",  # 연말휴장
    ]

    HOLIDAYS_2026 = [
        "2026-01-01",  # 신정
        "2026-02-17", "2026-02-18", "2026-02-19",  # 설날
        "2026-03-01",  # 삼일절
        "2026-05-05",  # 어린이날
        "2026-05-25",  # 석가탄신일
        "2026-06-06",  # 현충일
        "2026-08-15",  # 광복절
        "2026-09-24", "2026-09-25", "2026-09-26", "2026-09-27",  # 추석
        "2026-10-03", "2026-10-09",  # 개천절, 한글날
        "2026-12-25",  # 성탄절
        "2026-12-31",  # 연말휴장
    ]

    @classmethod
    def get_current_kst_time(cls) -> datetime:
        """현재 KST 시간을 반환"""
        return datetime.now(cls.KST)

    @classmethod
    def is_market_open(cls, check_time: Optional[datetime] = None) -> bool:
        """
        주어진 시간에 시장이 열려있는지 확인
        check_time이 None이면 현재 시간 사용
        """
        if check_time is None:
            check_time = cls.get_current_kst_time()
        elif check_time.tzinfo is None:
            # 타임존 없는 datetime은 KST로 간주
            check_time = cls.KST.localize(check_time)

        # 휴장일 체크
        if cls.is_holiday(check_time.date()):
            return False

        # 요일 체크 (월-금)
        if check_time.weekday() >= 5:  # 5=토요일, 6=일요일
            return False

        # 시간 체크
        current_time = check_time.time()
        return (cls.REGULAR_START <= current_time <= cls.REGULAR_END or
                cls.PRE_MARKET_START <= current_time <= cls.CLOSING_AUCTION_END)

    @classmethod
    def is_regular_session(cls, check_time: Optional[datetime] = None) -> bool:
        """정규 세션 시간인지 확인"""
        if check_time is None:
            check_time = cls.get_current_kst_time()
        elif check_time.tzinfo is None:
            check_time = cls.KST.localize(check_time)

        if not cls.is_market_open(check_time):
            return False

        current_time = check_time.time()
        return cls.REGULAR_START <= current_time <= cls.REGULAR_END

    @classmethod
    def is_closing_auction(cls, check_time: Optional[datetime] = None) -> bool:
        """마감 경매 시간인지 확인 (주문 금지 구간)"""
        if check_time is None:
            check_time = cls.get_current_kst_time()
        elif check_time.tzinfo is None:
            check_time = cls.KST.localize(check_time)

        current_time = check_time.time()
        return cls.CLOSING_AUCTION_START <= current_time <= cls.CLOSING_AUCTION_END

    @classmethod
    def is_holiday(cls, check_date) -> bool:
        """휴장일인지 확인"""
        if isinstance(check_date, datetime):
            date_str = check_date.strftime("%Y-%m-%d")
        elif isinstance(check_date, str):
            date_str = check_date
        else:
            date_str = check_date.strftime("%Y-%m-%d")

        all_holidays = (cls.HOLIDAYS_2024 + cls.HOLIDAYS_2025 + cls.HOLIDAYS_2026)
        return date_str in all_holidays

    @classmethod
    def get_next_market_open(cls, from_time: Optional[datetime] = None) -> datetime:
        """다음 시장 개장 시간을 반환"""
        if from_time is None:
            from_time = cls.get_current_kst_time()
        elif from_time.tzinfo is None:
            from_time = cls.KST.localize(from_time)

        # 현재부터 30일 이내에서 다음 개장일 찾기
        for days_ahead in range(31):
            check_date = from_time + timedelta(days=days_ahead)
            market_open_time = cls.KST.localize(
                datetime.combine(check_date.date(), cls.REGULAR_START)
            )

            if check_date.date() == from_time.date():
                # 오늘인 경우 현재 시간 이후인지 확인
                if market_open_time > from_time and cls.is_market_open(market_open_time):
                    return market_open_time
            else:
                # 다른 날인 경우 개장하는 날인지 확인
                if cls.is_market_open(market_open_time):
                    return market_open_time

        raise ValueError("30일 이내에 개장하는 시장을 찾을 수 없습니다")

    @classmethod
    def get_market_status(cls) -> str:
        """현재 시장 상태를 문자열로 반환"""
        now = cls.get_current_kst_time()

        if cls.is_holiday(now.date()):
            return "휴장일"
        elif now.weekday() >= 5:
            return "주말"
        elif now.time() < cls.PRE_MARKET_START:
            return "장전 시간외"
        elif cls.PRE_MARKET_START <= now.time() < cls.REGULAR_START:
            return "장전 경매"
        elif cls.REGULAR_START <= now.time() <= cls.REGULAR_END:
            return "정규장"
        elif cls.CLOSING_AUCTION_START <= now.time() <= cls.CLOSING_AUCTION_END:
            return "마감 경매"
        elif cls.CLOSING_AUCTION_END < now.time() <= cls.AFTER_HOURS_ODD_LOT_END:
            return "시간외 단일가"
        elif cls.AFTER_HOURS_ODD_LOT_END < now.time() <= cls.AFTER_HOURS_BLOCK_END:
            return "시간외 대량"
        else:
            return "장마감"
