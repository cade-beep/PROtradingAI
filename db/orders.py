import aiosqlite
import logging
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class OrderDatabase:
    """
    SQLite 기반 주문 데이터베이스 관리
    주문 상태를 로컬에 저장하고 동기화합니다.
    """
    def __init__(self, db_path: str = "orders.db"):
        self.db_path = db_path

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_no TEXT UNIQUE,
                    symbol TEXT,
                    qty INTEGER,
                    price INTEGER,
                    order_type TEXT,
                    status TEXT DEFAULT 'pending',
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            await db.commit()
        logger.info("주문 데이터베이스 초기화 완료")

    async def insert_order(self, order_no: str, symbol: str, qty: int, price: int, order_type: str, status: str = 'pending'):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT OR REPLACE INTO orders (order_no, symbol, qty, price, order_type, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (order_no, symbol, qty, price, order_type, status))
            await db.commit()
        logger.info(f"주문 저장: {order_no} - {status}")

    async def get_orders(self) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT * FROM orders ORDER BY timestamp DESC')
            rows = await cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in rows]

    async def get_open_orders(self) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT * FROM orders WHERE status = 'pending' OR status = 'open' ORDER BY timestamp DESC")
            rows = await cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in rows]

    async def update_order_status(self, order_no: str, status: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('UPDATE orders SET status = ? WHERE order_no = ?', (status, order_no))
            await db.commit()
        logger.info(f"주문 상태 업데이트: {order_no} -> {status}")

    async def delete_order(self, order_no: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('DELETE FROM orders WHERE order_no = ?', (order_no,))
            await db.commit()
        logger.info(f"주문 삭제: {order_no}")