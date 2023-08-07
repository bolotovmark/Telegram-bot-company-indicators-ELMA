import sqlite3
import os

from dotenv import load_dotenv
load_dotenv()

FIRST_USER_ID = os.getenv("FIRST_USER_ID")
FIRST_USER_NAME = os.getenv("FIRST_USER_NAME")

db_file = "db.sqlite"

if not os.path.exists(db_file):
    try:
        open(db_file, 'w').close()
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()

        with open('code.sql', 'r') as sql_file:
            sql_code = sql_file.read()

        cursor.executescript(sql_code)

        conn.commit()

        id_name = (FIRST_USER_ID, FIRST_USER_NAME)
        cursor.execute(f"INSERT INTO users(telegram_id_user, name) "
                       f"VALUES (?, ?);", id_name)
        conn.commit()
        cursor.close()

        print("База данных успешно создана из файла code.sql.")
    except Exception as e:
        print(e)
else:
    conn = sqlite3.connect('db.sqlite')
    print("База данных уже существует.")
