import sqlite3

# Підключення до бази даних
conn = sqlite3.connect('user.db')
cursor = conn.cursor()

# Перевірка наявності таблиці users
try:
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    print(users)
except sqlite3.OperationalError as e:
    print(e)

# Закриття з'єднання
conn.close()
