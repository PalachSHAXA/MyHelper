import sqlite3

database = sqlite3.connect('myhelper.db')
cursor = database.cursor()


def create_users_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        user_name TEXT,
        telegram_id BIGINT NOT NULL UNIQUE, 
        phone TEXT,
        language TEXT DEFAULT uz,
        branch TEXT,
        house_id TEXT,
        address TEXT
    )
    ''')

def create_clients_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        user_name TEXT,
        telegram_id BIGINT NOT NULL UNIQUE, 
        phone TEXT,
        language TEXT DEFAULT uz
    )
    ''')


def create_admins_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS admins(
        full_name TEXT,
        user_name TEXT,
        telegram_id BIGINT NOT NULL UNIQUE, 
        phone TEXT,
        master TEXT,
        branch TEXT
    )
    ''')
# todo команда обсуживающея 1/2 2/2
def delete():
    cursor.execute('''
     DROP TABLE IF EXISTS users''')


def delete_clients():
    cursor.execute('''
     DROP TABLE IF EXISTS clients''')

# create_users_table()
# create_admins_table()
delete_clients()
create_clients_table()






database.commit()
database.close()

