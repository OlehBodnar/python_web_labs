import sqlite3

# Підключення до бази даних
connection = sqlite3.connect("database.db")
cursor = connection.cursor()

# Вибірка всіх користувачів і їх ролей
cursor.execute("SELECT username, is_admin FROM users;")
users = cursor.fetchall()

for user in users:
    print("Ім'я користувача:", user[0], "Роль адміністратора:" if user[1] else "Звичайний користувач")

connection.close()
