import sqlite3

with sqlite3.connect("data_base.bd") as db:
    try:
        cursor = db.cursor()
        cursor.executescript("""CREATE TABLE IF NOT EXISTS data(
        id INTEGER PRIMARY KEY,
        id_user TEXT,
        joining_date VARCHAR,
        status TEXT
        )""")
        print('База данных успешно запустилась')
    except:
        print("Произошла ошибка...")

def Update_user():
    cursor.execute("SELECT * FROM data")
    print(cursor.fetchall())
    id_user = int(input('Введите порядковый номер пользователя: '))
    status = int(input("1 - статус User, 2 - статус Admin: "))
    if status == 1:
        cursor.execute(f"UPDATE data SET status = 'User' WHERE id = {id_user}")
        cursor.execute("SELECT * FROM data")
        print(cursor.fetchall())
        db.commit()
    elif status == 2:
        cursor.execute(f"UPDATE data SET status = 'Admin' WHERE id = {id_user}")
        cursor.execute("SELECT * FROM data")
        print(cursor.fetchall())
        db.commit()
    else:
        print("Такого статуса не существует!")

if __name__ == "__main__":

    op = int(input("Какую операцию Вы желаете совершить? \n 1 - просмотреть БД, 2 - обновить статус\n >>> "))
    if op == 1:
        cursor.execute("SELECT * FROM data")
        print(cursor.fetchall())
    elif op == 2:
        Update_user()
    else:
        print("Такой операции не существует.")
