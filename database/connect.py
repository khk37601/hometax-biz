from typing import List, Dict

from logger import logger_core


class DB:
    def __init__(self, conn, cursor) -> None:
        self.conn = conn
        self.cursor = cursor

    def __del__(self) -> None:
        self.conn.commit()
        self.conn.close()

    def execute(self, query: str) -> None:
        self.cursor.execute(str(query))
        self.conn.commit()

    def fetchone(self, query: str) -> List[Dict[str, any]]:
        self.execute(query)
        return self.cursor.fetchone()

    def fetchall(self, query: str) -> List:
        self.execute(query)
        return self.cursor.fetchall()
