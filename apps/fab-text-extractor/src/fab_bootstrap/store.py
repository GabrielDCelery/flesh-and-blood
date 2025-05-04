import sqlite3


def create_db(db_name: str):
    with sqlite3.connect(db_name) as conn:
        cur = conn.cursor()

        try:
            cur.execute(
                """CREATE TABLE IF NOT EXISTS extracts (
                card_name TEXT NOT NULL,
                model_name TEXT NOT NULL,
                segment INT NOT NULL,
                text TEXT NOT NULL,
                PRIMARY KEY (card_name, model_name, segment)

            )"""
            )
            pass
        except:
            pass
