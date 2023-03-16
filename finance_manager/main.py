import sqlite3

try:
    con = sqlite3.connect("DB_FM/account.db")
    cursor = con.cursor()

    cursor.execute("INSERT OR IGNORE INTO `users` (`user_id`) VALUES (?)", (1000,))

    users = cursor.execute("SELECT * FROM `users`")
    print(users.fetchall())

    con.commit()
except sqlite3.Error as error:
    print("Error", error)

finally:
    if(con):
        con.close()