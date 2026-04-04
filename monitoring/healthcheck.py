import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional

logger = logging.getLogger(__name__)

class HealthCheck:
    """시스템 헬스 체크 - WebSocket 연결, 토큰 상태, 리소스 모니터링"""
    
    def __init__(self, heartbeat_interval: int = 30):
        self.heartbeat_interval = heartbeat_interval
        self.last_heartbeat: Optional[datetime] = None
        self.ws_connected = False
        self.token_valid = False
        self.last_order_time: Optional[datetime] = None
        self.consecutive_errors = 0
        self.max_consecutive_errors = 5
        self.is_healthy = True
    
    async def heartbeat(self, ws_client=None):
        """주기적 핸들셰이크 (기본: 30초 간격)"""
        while True:
            try:
                await asyncio.sleep(self.heartbeat_interval)
                
                now = datetime.now()
                self.last_heartbeat = now
                
                # WebSocket 상태 확인
                if ws_client:
                    self.ws_connected = ws_client.is_connected
                    if not self.ws_connected:
                        logger.warning("WebSocket disconnected, attempting reconnect")
                        self.consecutive_errors += 1
                    else:
                        self.consecutive_errors = 0
                
                # 연속 오류 카운트 확인
                if self.consecutive_errors >= self.max_consecutive_errors:
                    self.is_healthy = False
                    logger.critical(f"System unhealthy: {self.consecutive_errors} consecutive errors")
                else:
                    self.is_healthy = True
                
                logger.debug(f"[Heartbeat] WS: {self.ws_connected}, Token: {self.token_valid}, Health: {self.is_healthy}")
                
            except asyncio.CancelledError:
                logger.info("Heartbeat cancelled")
                break
            except Exception as e:
                logger.error(f"Heartbeat error: {str(e)}")
                self.consecutive_errors += 1
    
    def record_token_status(self, valid: bool):
        """토큰 상태 기록"""
        self.token_valid = valid
        if valid:
            self.consecutive_errors = 0
        else:
            self.consecutive_errors += 1
    
    def record_order(self):
        """주문 기록 (마지막 주문 시간 업데이트)"""
        self.last_order_time = datetime.now()
    
    def get_status(self) -> dict:
        """현재 시스템 상태 반환"""
        return {
            "is_healthy": self.is_healthy,
            "ws_connected": self.ws_connected,
            "token_valid": self.token_valid,
            "last_heartbeat": self.last_heartbeat.isoformat() if self.last_heartbeat else None,
            "last_order_time": self.last_order_time.isoformat() if self.last_order_time else None,
            "consecutive_errors": self.consecutive_errors,
            "uptime_minutes": self._calculate_uptime()
        }
    
    def _calculate_uptime(self) -> float:
        """시스템 가동 시간 (분 단위)"""
        if not self.last_heartbeat:
            return 0
        return (datetime.now() - self.last_heartbeat).total_seconds() / 60
