import sqlite3
from types import NoneType


class TextExtractsStorage:
    def create_db(self):
        pass

    def does_extract_exist(
        self, img_name: str, model_name: str, segment_type: int
    ) -> bool:
        return False

    def create_or_update_extract(
        self,
        img_name: str,
        model_name: str,
        card_type: int,
        segment_type: int,
        text: str,
    ):
        pass


class TextExtractsSQLiteStorage(TextExtractsStorage):
    db_name: str

    def __init__(self, db_name: str):
        self.db_name = db_name

    def create_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(
                """CREATE TABLE IF NOT EXISTS extracts (
                img_name TEXT NOT NULL,
                model_name TEXT NOT NULL,
                card_type INT NOT NULL,
                segment_type INT NOT NULL,
                text TEXT NOT NULL,
                PRIMARY KEY (img_name, model_name, card_type, segment_type))"""
            )

    def does_extract_exist(
        self, img_name: str, model_name: str, segment_type: int
    ) -> bool:
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT 1 FROM extracts
                WHERE img_name = ? AND model_name = ? AND segment_type = ?
                """,
                (img_name, model_name, segment_type),
            )
            result = cur.fetchone()
            return result is not None

    def create_or_update_extract(
        self,
        img_name: str,
        model_name: str,
        card_type: int,
        segment_type: int,
        text: str,
    ) -> None:
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT OR REPLACE INTO extracts 
                (img_name, model_name, card_type, segment_type, text) 
                VALUES (?, ?, ?, ?, ?)
                """,
                (img_name, model_name, card_type, segment_type, text),
            )
            conn.commit()
