import sqlite3
import traceback

path = 'dbot/db.sqlite3'
con = sqlite3.connect(path)
cur = con.cursor()

def create_roles() -> bool:
    try:
        cur.execute(f"INSERT OR REPLACE INTO webapp_roomprofilerole VALUES ('1','Student')")
        cur.execute(f"INSERT OR REPLACE INTO webapp_roomprofilerole VALUES ('2','Mentor')")
        cur.execute(f"INSERT OR REPLACE INTO webapp_roomprofilerole VALUES ('3','Super Mentor')")
        con.commit()
        print("added the three roles successfully")
        return True
    except Exception:
        print(traceback.format_exc())
    return False


if __name__ == '__main__':
    create_roles()