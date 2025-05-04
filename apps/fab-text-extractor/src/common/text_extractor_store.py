import sqlite3


class TextExtractsStorage:
    def create_db(self):
        pass

    def does_extract_exist(
        self, img_name: str, model_name: str, card_type: int, segment_type: int
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
    _db_name: str
    _connection: sqlite3.Connection | None

    def __init__(self, db_name: str):
        self._db_name = db_name
        self._connection = None

    def _get_connection(self) -> sqlite3.Connection:
        if self._connection is None:
            self._connection = sqlite3.connect(self._db_name)
        return self._connection

    def close(self):
        if self._connection is not None:
            try:
                self._connection.close()
            finally:
                self._connection = None

    def create_db(self):
        try:
            conn = self._get_connection()
            cur = conn.cursor()
            cur.execute(
                """CREATE TABLE IF NOT EXISTS extracts (
                img_name TEXT NOT NULL,
                model_name TEXT NOT NULL,
                card_type INT NOT NULL,
                segment_type INT NOT NULL,
                text TEXT NOT NULL,
                PRIMARY KEY (img_name, model_name, card_type, segment_type))
                """
            )
        except sqlite3.Error as e:
            self.close()
            raise e

    def does_extract_exist(
        self, img_name: str, model_name: str, card_type: int, segment_type: int
    ) -> bool:
        try:
            conn = self._get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                SELECT 1 FROM extracts
                WHERE img_name = ? AND model_name = ? AND card_type = ? AND segment_type = ?
                """,
                (img_name, model_name, card_type, segment_type),
            )
            result = cur.fetchone()
            return result is not None
        except sqlite3.Error as e:
            self.close()
            raise e

    def create_or_update_extract(
        self,
        img_name: str,
        model_name: str,
        card_type: int,
        segment_type: int,
        text: str,
    ) -> None:
        try:
            conn = self._get_connection()
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
        except sqlite3.Error as e:
            self.close()
            raise e
