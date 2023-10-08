from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, callback_query


def generate_language_menu():
    return ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(*
                                                                      [
                                                                          KeyboardButton(text='Русский 🇷🇺'),
                                                                          KeyboardButton(text='Özbekcha 🇺🇿')
                                                                      ])


def generate_latere_menu(lang):
    if lang == "ru":
        return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*
                                                                      [
                                                                          KeyboardButton(text='Пропустить'),
                                                                      ])
    elif lang == 'uz':
        return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*
                                                                      [
                                                                          KeyboardButton(text="Oʻtkazib yuborish"),
                                                                      ])


def generate_get_number(lang):
    if lang == "Russian 🇷🇺":
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(*
                                                                      [
                                                                          KeyboardButton(text='Дом 93-3'),
                                                                          KeyboardButton(text='Дом 95-2'),
                                                                          KeyboardButton(text='Дом 95-3'),
                                                                          KeyboardButton(text='Дом 97-1'),
                                                                          KeyboardButton(text='Дом 97-2'),
                                                                          KeyboardButton(text='🔙')
                                                                      ])
    elif lang == 'Özbekcha 🇺🇿':
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(*
                                                                          [
                                                                              KeyboardButton(text='Dom 93-3'),
                                                                              KeyboardButton(text='Dom 95-2'),
                                                                              KeyboardButton(text='Dom 95-3'),
                                                                              KeyboardButton(text='Dom 97-1'),
                                                                              KeyboardButton(text='Dom 97-2'),
                                                                              KeyboardButton(text='⬅')
                                                                          ])


def generate_phone(lang):
    if lang == "Russian 🇷🇺":
        return ReplyKeyboardMarkup([
            [KeyboardButton(text='Отправить мой контакт ☎️', request_contact=True)]
        ], resize_keyboard=True, one_time_keyboard=True)
    elif lang == 'Özbekcha 🇺🇿':
        return ReplyKeyboardMarkup([
            [KeyboardButton(text='Mening kontaktimni yuborish ☎️', request_contact=True, )]
        ], resize_keyboard=True, one_time_keyboard=True)


def generate_main_menu(lang):
    if lang == 'Russian 🇷🇺':
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(*
                                                                          [
                                                                              KeyboardButton(text='👨🏻‍💻Связатся с Админом 📞'),
                                                                              KeyboardButton(text='Выбрать сервис ⛑️'),
                                                                              KeyboardButton(text='📓 Узнать о лицевом счете 🧮'),
                                                                              KeyboardButton(text='Аварийная ситуация 🚨'),
                                                                              # KeyboardButton(text='Дополнительная информация'),
                                                                              KeyboardButton(text='Настройки ⚙️')


                                                                          ])
    elif lang == 'Özbekcha 🇺🇿':
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(*
                                                                          [
                                                                              KeyboardButton(text='👨🏻‍💻Admin bilan boglanish📞'),
                                                                              KeyboardButton(text='Xizmatni tanlang ⛑️'),
                                                                              KeyboardButton(text='📓 Shaxsiy hisob haqida bilib olish 🧮'),
                                                                              KeyboardButton(text='Favqulodda vaziyat 🚨'),
                                                                              # KeyboardButton(text='Qoshimcha malumot'),
                                                                              KeyboardButton(text='Sozlamalar ⚙️'),

                                                                          ])


def generate_settings_menu(lang):
    if lang == "Russian 🇷🇺":
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True).add(*
                                                                          [
                                                                              KeyboardButton(text='Сменить имя 👤'),
                                                                              KeyboardButton(text='Изменить адрес 🏘️'),
                                                                              KeyboardButton(text='Изменить лицевой счет 🧮'),
                                                                              KeyboardButton(text='📞 Сменить номер телефона ☎️'),
                                                                              KeyboardButton(text='Изменить язык 🇷🇺 🔀 🇺🇿'),
                                                                              KeyboardButton(text='🔙')
                                                                          ])
    elif lang == 'Özbekcha 🇺🇿':
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True).add(*
                                                                          [
                                                                              KeyboardButton(text='Ismimni ozgartirish 👤'),
                                                                              KeyboardButton(text="Manzilni o'zgartirish 🏘️"),
                                                                              KeyboardButton(text="Shaxsiy hisobni o'zgartirish 🧮"),
                                                                              KeyboardButton(text="📞 Telefon raqamini o'zgartirish ☎️"),
                                                                              KeyboardButton(text="Tilni o'zgartirish 🇺🇿 🔀 🇷🇺"),
                                                                              KeyboardButton(
                                                                                  text='⬅')
                                                                          ])


def generate_service_menu(lang):
    if lang == "Russian 🇷🇺":
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(*
                                                                          [
                                                                              KeyboardButton(text='🔌 Электрик ⚡'),
                                                                              KeyboardButton(text='👨‍🔧 Сантехник 🪠'),
                                                                              KeyboardButton(text='🧹Уборка 🧼'),
                                                                              KeyboardButton(text='🔙')
                                                                          ])
    elif lang == 'Özbekcha 🇺🇿':
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(*
                                                                          [
                                                                              KeyboardButton(
                                                                                  text='🔌 Elektrik ⚡'),
                                                                              KeyboardButton(
                                                                                  text='🪠Santexnik 👨‍🔧'),
                                                                              KeyboardButton(
                                                                                  text='🧹Uborka 🧼'),
                                                                              KeyboardButton(
                                                                                  text='⬅')
                                                                          ])


def generate_back_menu(lang):
    if lang == "ru":
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True).add(*[KeyboardButton(text='Я житель'), KeyboardButton(text='Продолжить')])
    elif lang == 'uz':
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True).add(*[KeyboardButton(text='Men rezidentman'), KeyboardButton(text='Davom etish')])


def generate_electric_menu():
    return ReplyKeyboardMarkup(resize_keyboard=True, row_width=5).add(*
                                                                      [
                                                                          KeyboardButton(text='Е0'),
                                                                          KeyboardButton(text='Е1'),
                                                                          KeyboardButton(text='Е2'),
                                                                          KeyboardButton(text='Е3'),
                                                                          KeyboardButton(text='Е4'),
                                                                          KeyboardButton(text='Е5'),
                                                                          KeyboardButton(text='Е6'),
                                                                          KeyboardButton(text='Е7'),
                                                                          KeyboardButton(text='Е8'),
                                                                          KeyboardButton(text='Е9'),
                                                                          KeyboardButton(text='Е10'),
                                                                          KeyboardButton(text='Е11'),
                                                                          KeyboardButton(text='Е12'),
                                                                          KeyboardButton(text='Е13'),
                                                                          KeyboardButton(text='Е14'),
                                                                          KeyboardButton(text='Е15'),
                                                                          KeyboardButton(text='Е16'),
                                                                          KeyboardButton(text='Е17'),
                                                                          KeyboardButton(text='Е18')
                                                                      ])


def generate_santexnik_menu():
    return ReplyKeyboardMarkup(resize_keyboard=True, row_width=7).add(*
                                                                      [
                                                                          KeyboardButton(text='S0'),
                                                                          KeyboardButton(text='S1'),
                                                                          KeyboardButton(text='S2'),
                                                                          KeyboardButton(text='S3'),
                                                                          KeyboardButton(text='S4'),
                                                                          KeyboardButton(text='S5'),
                                                                          KeyboardButton(text='S6'),
                                                                          KeyboardButton(text='S7'),
                                                                          KeyboardButton(text='S8'),
                                                                          KeyboardButton(text='S9'),
                                                                          KeyboardButton(text='S10'),
                                                                          KeyboardButton(text='S11'),
                                                                          KeyboardButton(text='S12'),
                                                                          KeyboardButton(text='S13'),
                                                                          KeyboardButton(text='S14'),
                                                                          KeyboardButton(text='S15'),
                                                                          KeyboardButton(text='S16'),
                                                                          KeyboardButton(text='S17'),
                                                                          KeyboardButton(text='S18'),
                                                                          KeyboardButton(text='S19'),
                                                                          KeyboardButton(text='S20')
                                                                      ])


def generate_uborka_menu():
    return ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(*
                                                                      [
                                                                          KeyboardButton(text='U0'),
                                                                          KeyboardButton(text='U1'),
                                                                          KeyboardButton(text='U2'),
                                                                          KeyboardButton(text='U3'),
                                                                          KeyboardButton(text='U4'),
                                                                          KeyboardButton(text='U5')
                                                                      ])


def generate_account_menu(lang):
    if lang == "Russian 🇷🇺":
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(*[
            KeyboardButton(text='Номер лицевого счета'),
            KeyboardButton(text='Узнать мою задалжость')
        ])
    elif lang == "Özbekcha 🇺🇿":
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(*[
            KeyboardButton(text='Hisob raqami'),
            KeyboardButton(text='Mening qarzimni bilib oling')
        ])


def generate_yes_no_menu(lang):
    if lang == "Russian 🇷🇺":
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, selective=True).add(*
                                                                          [
                                                                              KeyboardButton(text='Дa ✅'),
                                                                              KeyboardButton(text='Нет ❌'),
                                                                              KeyboardButton(
                                                                                  text='Вернутся на главное меню')
                                                                          ])
    elif lang == "Özbekcha 🇺🇿":
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(*
                                                                          [
                                                                              KeyboardButton(text='Ha ✅'),
                                                                              KeyboardButton(text='Yoq ❌'),
                                                                              KeyboardButton(
                                                                                  text='Asosiy menyuga qaytish')
                                                                          ])


def generate_get_menu():
    return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True).add(*
                                                                      [
                                                                          KeyboardButton(text='/get'),
                                                                          KeyboardButton(text='#answer:')
                                                                      ])

def get_cancel_kb(lang):
    if lang == "Russian 🇷🇺":
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(*
                                                                          [
                                                                              KeyboardButton(text='Отменить'),
                                                                          ])
    elif lang == "Özbekcha 🇺🇿":
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(*
                                                                          [
                                                                              KeyboardButton(text='Otmen qilish'),
                                                                          ])



def generate_id(id):
        return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*
                                                                          [
                                                                              KeyboardButton(text=f'{id}'),
                                                                          ])


def generate_name(name):
        return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*
                                                                          [
                                                                              KeyboardButton(text=f'{name}'),
                                                                          ])


def generate_user_name(user):
        return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*
                                                                          [
                                                                              KeyboardButton(text=f'@{user}'),
                                                                          ])


def generate_admin_work():
        return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*
                                                                          [
                                                                              KeyboardButton(text=f'Электрик'),
                                                                              KeyboardButton(text=f'Сантехник'),
                                                                              KeyboardButton(text=f'Уборщица')
                                                                          ])


def generate_branch():
        return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*
                                                                          [
                                                                              KeyboardButton(text=f'1/2'),
                                                                              KeyboardButton(text=f'2/2'),
                                                                          ])


def generate_info_menu(lang):
    if lang == "Russian 🇷🇺":
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(*
                                                                          [
                                                                              # KeyboardButton(text='Узнать свой user_id'),
                                                                              KeyboardButton(text='Прделожить'),
                                                                              KeyboardButton(text='Информация про анкету'),
                                                                              KeyboardButton(text='🔙')
                                                                          ])
    elif lang == "Özbekcha 🇺🇿":
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(*
                                                                          [
                                                                              # KeyboardButton(text='user_id mni bilish'),
                                                                              KeyboardButton(text='Tavsiya qilish'),
                                                                              KeyboardButton(text='Anketa haqida malumot'),
                                                                              KeyboardButton(text='⬅')
                                                                    ])


def generate_branch_menu():
    return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True).add(*
                                                                                              [
                                                                                                  KeyboardButton(
                                                                                                      text='GreenPark'),
                                                                                                  KeyboardButton(
                                                                                                      text='Adliya')
                                                                                              ])


def generate_dov_menu(lang):
    if lang == 'ru':
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True).add(*
                                                                                              [
                                                                                                  KeyboardButton(
                                                                                                      text='🤗Доволен спасибо ✅'),
                                                                                                  KeyboardButton(
                                                                                                      text='❌ Не довлен 😕')
                                                                                              ])
    elif lang == 'uz':
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True).add(*
                                                                                              [
                                                                                                  KeyboardButton(
                                                                                                      text='🤗 Qoniq topdim rahmat ✅'),
                                                                                                  KeyboardButton(
                                                                                                      text='❌ Qoniqarli emas 😕')
                                                                                              ])


def generate_later(lang):
    if lang == "Russian 🇷🇺":
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True).add(*
                                                                                                  [
                                                                                                      # KeyboardButton(text='Потом'),
                                                                                                      KeyboardButton(text='/register'),
                                                                                                      KeyboardButton(text='Гость')



                                                                                                  ])
    elif lang == "Özbekcha 🇺🇿":
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True).add(*
                                                                                                  [
                                                                                                      # KeyboardButton(text='Keyin'),
                                                                                                      KeyboardButton(text='/register'),
                                                                                                      KeyboardButton(text='Mehmon')




                                                                                                  ])


def generate_secret_func():
    return ReplyKeyboardMarkup(resize_keyboard=True).add([
        KeyboardButton(text='#news'),
        KeyboardButton(text='#offer')

    ])