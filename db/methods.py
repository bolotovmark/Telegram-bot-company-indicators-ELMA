import sqlite3

db_file = "db.sqlite"
conn = sqlite3.connect(db_file)


async def db_exists_user(user_id):
    try:
        cur = conn.cursor()
        rez = cur.execute(f"SELECT telegram_id_user, name FROM users "
                          f"WHERE telegram_id_user = {user_id};")
        user = rez.fetchone()
        cur.close()
        return user
    except Exception as e:
        print(e)
        return False


async def db_get_list_user():
    try:
        cur = conn.cursor()
        rez = cur.execute(f"SELECT * FROM users")
        user = rez.fetchall()
        cur.close()
        return user
    except Exception as e:
        print(e)
        return False


async def db_insert_new_user(user_id, name):
    cur = conn.cursor()
    data_insert = (user_id, name)
    cur.execute("INSERT INTO users(telegram_id_user, name) VALUES (?, ?);", data_insert)
    conn.commit()
    cur.close()


async def db_remove_user(user_id: str):
    cur = conn.cursor()
    cur.execute(f"DELETE FROM users WHERE telegram_id_user = {user_id};")
    conn.commit()
    cur.close()
