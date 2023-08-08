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
        user = rez.fetchone()
        cur.close()
        return user
    except Exception as e:
        print(e)
        return False