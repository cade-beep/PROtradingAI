import asyncio
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
from market_calendar import MarketCalendar
from auth.token_manager import TokenManager

logger = logging.getLogger(__name__)
KST = timezone('Asia/Seoul')

class TradingScheduler:
    """KST 기반 거래 스케줄러 - pre-market, regular, post-market 작업 관리"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone=KST)
        self.token_manager = TokenManager()
        self.market_cal = MarketCalendar()
        self.is_running = False
    
    async def pre_market_job(self):
        """Pre-market (08:30 KST): 시스템 준비/토큰 갱신/포지션 동기화"""
        logger.info("=== Pre-market Job Started (08:30 KST) ===")
        try:
            now_kst = datetime.now(KST)
            if not self.market_cal.is_market_open(now_kst, session='pre_market'):
                logger.warning("Pre-market session closed, skipping job")
                return
            
            # 토큰 재발급
            await self.token_manager.issue_token()
            logger.info("Token refreshed for the day")
            
            # 포지션 동기화 (REST 재쿼리)
            logger.info("Position sync scheduled for pre-market")
            
        except Exception as e:
            logger.error(f"Pre-market job failed: {str(e)}")
    
    async def intraday_job(self):
        """Regular session (09:00~15:20 KST): 전략 실행/신호 생성"""
        try:
            now_kst = datetime.now(KST)
            
            # 정규 세션만 실행
            if not self.market_cal.is_market_open(now_kst, session='regular'):
                logger.debug("Market closed for regular session")
                return
            
            # 마감 옥션 제외 (15:20~15:30)
            if self.market_cal.in_closing_auction(now_kst):
                logger.warning("In closing auction KILL zone, skipping orders")
                return
            
            logger.debug(f"Intraday job running at {now_kst.strftime('%H:%M:%S')}")
            
        except Exception as e:
            logger.error(f"Intraday job failed: {str(e)}")
    
    async def post_market_job(self):
        """Post-market (15:30 KST): 일일 정산/포지션 확인"""
        logger.info("=== Post-market Job Started (15:30 KST) ===")
        try:
            # 일일 정산 수행
            logger.info("Daily settlement and position reconciliation")
            
            # 주문 히스토리 로깅
            logger.info("Order history logged for the day")
            
        except Exception as e:
            logger.error(f"Post-market job failed: {str(e)}")
    
    def register_jobs(self):
        """스케줄 등록 (KST 기준)"""
        # Pre-market: 매일 08:30 KST
        self.scheduler.add_job(
            self.pre_market_job,
            CronTrigger(hour=8, minute=30, timezone=KST),
            id='job_pre_market',
            name='Pre-market preparation'
        )
        
        # Intraday: 매 5분마다 09:00~15:30 (정규 세션)
        self.scheduler.add_job(
            self.intraday_job,
            CronTrigger(hour='9-15', minute='*/5', timezone=KST),
            id='job_intraday',
            name='Intraday strategy execution'
        )
        
        # Post-market: 매일 15:30 KST
        self.scheduler.add_job(
            self.post_market_job,
            CronTrigger(hour=15, minute=30, timezone=KST),
            id='job_post_market',
            name='Post-market settlement'
        )
        
        logger.info("All jobs registered with KST timezone")
    
    async def start(self):
        """스케줄러 시작"""
        if self.is_running:
            logger.warning("Scheduler already running")
            return
        
        self.register_jobs()
        self.scheduler.start()
        self.is_running = True
        logger.info("Scheduler started successfully")
    
    async def stop(self):
        """스케줄러 중지"""
        if not self.is_running:
            logger.warning("Scheduler not running")
            return
        
        self.scheduler.shutdown()
        self.is_running = False
        logger.info("Scheduler stopped")
