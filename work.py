import sqlite3


def get_phone_and_address_by_id(user_id):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute("SELECT full_name, phone, language, address, house_id, branch FROM users WHERE telegram_id=?", (user_id,))
    result = cursor.fetchone()
    database.commit()
    database.close()
    return result


def get_info_iuser_id(user_id):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute("SELECT full_name, user_name, telegram_id, phone, language, branch, house_id, address FROM users WHERE telegram_id=?", (user_id,))
    result = cursor.fetchone()
    database.commit()
    database.close()
    return result


def get_admin_info(user_id):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute("SELECT full_name, user_name, telegram_id,  phone, master, branch FROM admins WHERE telegram_id=?", (user_id,))
    result = cursor.fetchone()
    database.commit()
    database.close()
    return result


def get_phone_and_address_by_hs_id(house_id):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute("SELECT full_name, phone, language, address FROM users WHERE house_id=?", (house_id,))
    result = cursor.fetchone()
    database.commit()
    database.close()
    return result


def get_lang_by_id(user_id):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute("SELECT language FROM users WHERE telegram_id=?", (user_id,))
    result = cursor.fetchone()
    database.commit()
    database.close()
    return result


def get_client_lang(user_id):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute("SELECT language FROM clients WHERE telegram_id=?", (user_id,))
    result = cursor.fetchone()
    database.commit()
    database.close()
    return result


def update_name(name: str, user_id: int):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute(f'''
    UPDATE users
    SET full_name = '{name}'
    WHERE telegram_id = ?
    ''', (user_id, ))
    database.commit()
    database.close()


def update_lang(lang: str, user_id: int):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute(f'''
    UPDATE users
    SET language = '{lang}'
    WHERE telegram_id = ?
    ''', (user_id, ))
    database.commit()
    database.close()


def update_client_lang(lang: str, user_id: int):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute(f'''
    UPDATE clients
    SET language = '{lang}'
    WHERE telegram_id = ?
    ''', (user_id, ))
    database.commit()
    database.close()


def first_select_users(user_id: int):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute(f'''
    SELECT * FROM users WHERE telegram_id = ?
    ''', (user_id, ))
    database.commit()
    database.close()


def update_house_id(house_id: int, user_id: int):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute(f'''
    UPDATE users
    SET house_id = '{house_id}'
    WHERE telegram_id = ?
    ''', (user_id, ))

    database.commit()
    database.close()


def update_phone(phone: int, user_id: int):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute(f'''
    UPDATE users
    SET phone = '{phone}'
    WHERE telegram_id = ?
    ''', (user_id, ))
    database.commit()
    database.close()


def request(name: str, user_id: int, address: str, phone: int):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute(f'''
    SELECT {name}, {address}{phone} FROM users
    SET full_name = '{name}'
    WHERE telegram_id = ?
    ''', (user_id, ))
    database.commit()
    database.close()


def update_data(name: str, user_id: int, address: str, branch, phone: int, house_id, user_name):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute(f'''
    UPDATE users
    SET full_name = '{name}', address = '{address}', branch = '{branch}', phone = '{phone}', house_id = '{house_id}', 
    user_name = '{user_name}'
    WHERE telegram_id = ?
    ''', (user_id, ))
    database.commit()
    database.close()
# {name}{address}{phone}{house_id}


def register_lang(chat_id, full_name, language):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO users(telegram_id, full_name, language)
     VALUES (?, ?, ?)
    ''', (chat_id, full_name, language))
    database.commit()
    database.close()


def register_client_lang(chat_id, full_name, language, user_name):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO clients(telegram_id, full_name, language, user_name)
     VALUES (?, ?, ?, ?)
    ''', (chat_id, full_name, language, user_name))
    database.commit()
    database.close()


def get_phone(chat_id):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT phone FROM users WHERE telegram_id = ?;
    ''', (chat_id,))
    phone = cursor.fetchone()
    database.commit()
    database.close()
    return phone

    # user = cursor.fetchone()


def register_user(phone, address, house_id, telegram_id):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute(f'''
    INSERT INTO users(phone, address, house_id)
     WHERE telegram_id = {telegram_id} VALUES (?, ?, ?, ?)
    ''', (phone, address, house_id, telegram_id))
    database.commit()
    database.close()


def register_client(phone, address, house_id, telegram_id):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute(f'''
    INSERT INTO users(phone, address, house_id)
     WHERE telegram_id = {telegram_id} VALUES (?, ?, ?, ?)
    ''', (phone, address, house_id, telegram_id))
    database.commit()
    database.close()


def register_admin_base(name, user_name, telegram_id, phone, master, branch):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute(f'''
    INSERT INTO admins(full_name, user_name, telegram_id, phone, master, branch ) VALUES ( ?, ?, ?, ?, ?, ?)
    ''', (name, user_name, telegram_id, phone, master, branch))
    database.commit()
    database.close()


def first_select_admins(user_id: int):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute(f'''
    SELECT * FROM admins WHERE telegram_id = ?
    ''', (user_id, ))


def is_admin(username):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute('SELECT * FROM admins WHERE user_name = ?', (username,))
    result = cursor.fetchone()
    database.commit()
    database.close()
    return result is not None


def reg_id(telegram_id):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute(f'''
    INSERT INTO admins(telegram_id) VALUES (?)''', telegram_id)
    database.commit()
    database.close()
#
# def register_lang(chat_id, full_name, language):
#     database = sqlite3.connect('myhelper.db')
#     cursor = database.cursor()
#     cursor.execute('''
#     INSERT INTO users(telegram_id, full_name, language)
#      VALUES (?, ?, ?)
#     ''', (chat_id, full_name, language))
#     database.commit()
#     database.close()


def update_address(address: str, user_id: int):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute(f'''
    UPDATE users
    SET address = '{address}'
    WHERE telegram_id = ?
    ''', (user_id, ))
    database.commit()
    database.close()


def update_branch(branch: str, user_id: int):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute(f'''
    UPDATE users
    SET branch = '{branch}'
    WHERE telegram_id = ?
    ''', (user_id, ))
    database.commit()
    database.close()


def mailing():
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute('SELECT telegram_id FROM users')
    list_chat = cursor.fetchall()
    users = []
    for user_id in list_chat:
        users.append(*user_id)
    return users


def mailing_branch(branch):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    # cursor.execute(f'SELECT telegram_id FROM users WHERE branch = ?', (branch))
    # list_chat = cursor.fetchall()
    cursor.execute(f"SELECT telegram_id FROM users")
    list_chat = cursor.fetchall()

    # print(list_chat)
    users = []
    if f'{branch}' == list_chat[0]:
        for user_id in list_chat[1]:
            users.append(*user_id)
    return users


def get_admins_list():
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute('SELECT telegram_id FROM admins')
    list_chat = cursor.fetchall()
    admins = []
    for admins_id in list_chat:
        admins.append(*admins_id)
    return admins


def get_lang(user_id: int):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute(f'''
    SELECT language FROM users WHERE telegram_id = ?
    ''', (user_id,))
    lang = cursor.fetchone()
    database.commit()
    database.close()
    return lang


def get_name(user_id: int):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute(f'''
    SELECT full_name FROM users WHERE telegram_id = ?
    ''', (user_id,))
    name = cursor.fetchone()
    database.commit()
    database.close()
    return name


def get_result(user_id: int):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute(f'''
    SELECT address IS NULL or house_id IS NULL or phone IS NULL FROM users WHERE telegram_id = ?
    ''', (user_id,))
    result = cursor.fetchone()
    database.commit()
    database.close()
    return result


def get_address(user_id: int):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute(f'''
    SELECT address FROM users WHERE telegram_id = ?
    ''', (user_id,))
    address = cursor.fetchone()
    database.commit()
    database.close()
    return address


def get_branch(branch: str):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute(f'''
    SELECT telegram_id FROM users WHERE branch = ?
    ''', (branch,))
    list_chat = cursor.fetchall()
    users = []
    for user_id in list_chat:
        users.append(*user_id)
    # database.commit()
    # database.close()
    return users


# def get_master(branch: str):
#     database = sqlite3.connect('myhelper.db')
#     cursor = database.cursor()
#     cursor.execute(f'''
#     SELECT telegram_id FROM users WHERE branch = ?
#     ''', (branch,))
#     telegram_id = cursor.fetchall()
#     cursor.execute(f'''
#     SELECT user_name FROM admins WHERE telegram_id = ?
#     ''', (telegram_id,))
#     mas = cursor.fetchall()
#     database.commit()
#     database.close()
#     return mas


def get_master(master: str, branch):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute(f'''
    SELECT user_name FROM admins WHERE master = ? AND branch = ?
    ''', (master, branch))
    mas = cursor.fetchall()
    for row in mas:
        print(row[0])
    database.commit()
    database.close()
    return mas


def get_home_id(user_id):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute(f'''
    SELECT house_id FROM users WHERE telegram_id = ?
    ''', (user_id,))
    home_id = cursor.fetchone()
    database.commit()
    database.close()
    return home_id


def get_user_branch(user_id):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute(f'''
    SELECT branch FROM users WHERE telegram_id = ?
    ''', (user_id,))
    branch = cursor.fetchone()
    database.commit()
    database.close()
    return branch


def delete_user(user_id: int):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute("DELETE FROM users WHERE telegram_id = ?", (user_id,))
    database.commit()
    database.close()


# def delete_admin(user_id: int):
#     database = sqlite3.connect('myhelper.db')
#     cursor = database.cursor()
#     cursor.execute("DELETE admins WHERE telegram_id = ?", (user_id,))
#     database.commit()
#     database.close()

def delete_admin(admin_id):
    conn = sqlite3.connect('myhelper.db')  # Подключение к базе данных
    cursor = conn.cursor()

    # Удаление записи с указанным айди
    cursor.execute("DELETE FROM admins WHERE telegram_id = ?", (admin_id,))
    conn.commit()

    conn.close()


def get_user_data(user_id: int):
    database = sqlite3.connect('myhelper.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT full_name, telegram_id, phone, language, house_id, address FROM users WHERE telegram_id = ?''', (user_id,))
    data = cursor.fetchone()
    database.commit()
    database.close()
    return data
