import logging
from aiogram.types import InputFile
from aiogram.utils import executor
from dotenv import load_dotenv
from keyboards import *
from settings import GROUP_ID
from work import *
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup

storage = MemoryStorage()

load_dotenv()

TOKEN = '5752484871:AAH21ewpQSV-5bQh6wC7d52JHT-KoY1mqBM'
bot = Bot(TOKEN, parse_mode='HTML')

# dp = Dispatcher(bot, storage=storage)
dp = Dispatcher(bot, storage=storage)

database = sqlite3.connect('myhelper.db')
cursor = database.cursor()
user_data = {}
group = GROUP_ID
logging.basicConfig(level=logging.INFO)
admin = get_admins_list()
# print(admin)
# print(admin)

boss = (1043144098, 89645973, 431473067, 6578322428)
# shaxzod jaxongiraka voxidaka sifat meneger
# boss = [1043144098]
# print(boss)
ru = ('ru',)
uz = ('uz',)


class ProfileStatesGroup(StatesGroup):
    name = State()
    contact = State()
    branch = State()
    house_id = State()
    address = State()


class ClientsGroup(StatesGroup):
    name = State()
    contact = State()


class AdminsGroup(StatesGroup):
    name = State()
    user_name = State()
    telegram_id = State()
    contact = State()
    branch = State()
    master = State()


class ServiceGroup(StatesGroup):
    branch = State()
    title = State()


class AnswerGroup(StatesGroup):
    ID = State()
    title = State()


class Answer_Photo_Group(StatesGroup):
    ID = State()
    title = State()


class NewStateGroup(StatesGroup):
    new_name = State()
    new_contact = State()
    new_house_id = State()
    new_address = State()
    offer = State()
    service = State()
    master = State()
    guest = State()
    branch = State()
    new_branch = State()


@dp.message_handler(commands=['start'])
async def command_start(message: Message):
    chat_id = message.from_user.id
    print(chat_id)
    typo = get_type(chat_id)
    print(typo)
    print(typo == 'client')
    if typo == 'client':
        lang = get_client_lang(chat_id)
        if lang == ru:
            await message.answer('Вы вернулись в главное меню:',
                                 reply_markup=generate_main_menu('Russian 🇷🇺', 'client'))
        elif lang == uz:
            await message.answer('Siz asosiy menyuga qaytasiz:',
                                 reply_markup=generate_main_menu('Özbekcha 🇺🇿', 'client'))
    elif typo == 'resident':
        lang = get_lang(chat_id)
        if lang == ru:
            await message.answer('Вы вернулись в главное меню:',
                                 reply_markup=generate_main_menu('Russian 🇷🇺', 'resident'))
        elif lang == uz:
            await message.answer('Siz asosiy menyuga qaytasiz:',
                                 reply_markup=generate_main_menu('Özbekcha 🇺🇿', 'resident'))
    else:
        await bot.send_message(chat_id, 'Выберите язык | Tilni tanlang', reply_markup=generate_language_menu())


none = (None,)


@dp.message_handler(commands=['register'])
async def cmd_create(message: types.Message) -> None:
    user_id = message.from_user.id
    language = get_lang_by_id(user_id)
    user = first_select_users(user_id)
    user_name = message.from_user.username
    phone = get_phone(user_id)
    address = get_address(user_id)
    name = message.from_user.full_name
    # print(language)
    # print(address)
    if address == ('None',) or address is None or address == none:
        if language == ru:
            await message.reply("Давайте зарегистрируем вас, для начала пришлите свое имя!",
                                reply_markup=generate_name(name))
            # reply_markup=get_cancel_kb("Russian 🇷🇺"))
            await ProfileStatesGroup.name.set()
        elif language == uz:
            await message.reply("Keling, sizni ro'yxatdan o'tkazamiz, avval ismingizni yuboring!",
                                reply_markup=generate_name(name))
            # reply_markup=get_cancel_kb("Özbekcha 🇺🇿"))
            await ProfileStatesGroup.name.set()
    elif not address == ('None',) or address is None or address == none:
        if language == ru:
            await message.answer('Вы уже зарегистрированы, вы можете изменить данные с настроек',
                                 reply_markup=generate_settings_menu("Russian 🇷🇺", 'resident'))
        elif language == uz:
            await message.answer(
                "Siz allaqachon ro'yxatdan o'tgansiz, sozlamalardan ma'lumotlarni o'zgartirishingiz mumkin",
                reply_markup=generate_settings_menu("Özbekcha 🇺🇿", 'resident'))


@dp.message_handler(state=ProfileStatesGroup.name)
async def load_name(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    language = get_lang_by_id(user_id)
    async with state.proxy() as data:
        data['name'] = message.text
    if language == ru:
        await message.reply('А теперь пришли свой контакт', reply_markup=generate_phone('Russian 🇷🇺'))
        await ProfileStatesGroup.next()
    elif language == uz:
        await message.reply('Endi kontaktingizni yuboring', reply_markup=generate_phone('Özbekcha 🇺🇿'))
        await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.contact, content_types=['contact'])
async def load_house_id(message: types.message, state: FSMContext) -> None:
    user_id = message.from_user.id
    language = get_lang_by_id(user_id)
    ru = 'ru',
    uz = 'uz',
    async with state.proxy() as data:
        data['contact'] = message.contact.phone_number
    if language == ru:
        await bot.send_message(chat_id=user_id, text='А теперь пришлите место проживания',
                               reply_markup=generate_branch_menu())
        await ProfileStatesGroup.next()
    if language == uz:
        await bot.send_message(chat_id=user_id, text='Endi yashash manzilingizni yuboring',
                               reply_markup=generate_branch_menu())
        await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.branch)
async def load_branch(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    language = get_lang_by_id(user_id)
    async with state.proxy() as data:
        data['branch'] = message.text
    if not message.text == 'Пропустить' or "Oʻtkazib yuborish":
        if language == ru:
            await message.reply('Теперь пришлите номер своего лицевого счета')
            await message.answer('Если не знаете номер лицевого счета пропустите его',
                                 reply_markup=generate_latere_menu('ru'))
            await ProfileStatesGroup.next()
        if language == uz:
            await message.reply('Endi shaxsiy hisob raqamingizni yuboring')
            await message.answer("Shaxsiy hisob raqamingizni bilmasangiz, uni o'tkazib yuboring",
                                 reply_markup=generate_latere_menu('uz'))
            await ProfileStatesGroup.next()
    else:
        await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.house_id)
async def load_branch(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    language = get_lang_by_id(user_id)
    house_id = message.text
    if not house_id == 'Пропустить' and not house_id == "Oʻtkazib yuborish":
        if house_id.startswith('139') or house_id.startswith('138'):
            async with state.proxy() as data:
                data['house_id'] = message.text
            if language == ru:
                await message.reply('А теперь пришлите адрес с указанием дома этажа и номером квартиры!',
                                    reply_markup=types.ReplyKeyboardRemove())
                await ProfileStatesGroup.next()
            if language == uz:
                await message.reply("Endi uyning qavati va xonadon raqamini ko'rsatgan holda manzilni yuboring!",
                                    reply_markup=types.ReplyKeyboardRemove())
                await ProfileStatesGroup.next()
        else:
            if language == ru:
                await message.answer('Пожалуйста пришлите действительный номер лицевого счета')
            elif language == uz:
                await message.answer("Iltimos, haqiqiy shaxsiy hisob raqamini yuboring")
    else:
        async with state.proxy() as data:
            data['house_id'] = '❌'
            if language == ru:
                await message.answer('Но не забудьте добавить лицевой счет в настройках после того как узнате')
                await message.reply('А теперь пришлите адрес с указанием дома этажа и номером квартиры!',
                                    reply_markup=types.ReplyKeyboardRemove())
                await ProfileStatesGroup.next()
            elif language == uz:
                await message.answer(
                    "Lekin buni bilib olganingizdan so'ng sozlamalarga shaxsiy hisobingizni qo'shishni unutmang")
                await message.reply("Endi uyning qavati va xonadon raqamini ko'rsatgan holda manzilni yuboring!",
                                    reply_markup=types.ReplyKeyboardRemove())
                await ProfileStatesGroup.next()
        # await message.answer('Oxshavotdi nop ne do konsa')
        # await load_address(message, state)


@dp.message_handler(state=ProfileStatesGroup.address)
async def load_address(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    language = get_lang_by_id(user_id)
    user_name = message.from_user.username
    async with state.proxy() as data:
        user_id = message.from_user.id
        data['address'] = message.text
        name = data['name']
        phone = data['contact']
        branch = data['branch']
        house_id = data['house_id']
        address = data['address']
        update_data(name, user_id, address, branch, phone, house_id, user_name)
        # print(house_id)
        #     phone = message.contact.phone _number
        # if not message.text == 'Пропустить' or "Oʻtkazib yuborish":

        if house_id == str('Пропустить') or house_id == str("Oʻtkazib yuborish"):
            no = '❌'
            if language == ru:
                await message.reply(
                    f"Имя: {name},\nТелефон номер: +{phone}\nЮзер @{user_name}\nМесто проживания: {branch},\nЛицевой счет: {no},\nАдрес:{address}\nЕсли вы что то указали не верно то его можно изменить в настройках",
                    reply_markup=generate_main_menu('Russian 🇷🇺', 'resident'))
            elif language == uz:
                await message.reply(
                    f"Ism: {name},\nTelefon raqami: +{phone}\nYuzer @{user_name}\nYashash joyi: {branch},\nShaxsiy hisob: {no},\nManzil: {address}\nAgar biror narsani noto'g'ri ko'rsatgan bo'lsangiz, uni sozlamalarda o'zgartirishingiz mumkin",
                    reply_markup=generate_main_menu('Özbekcha 🇺🇿', 'resident'))
            if language == ru:
                await message.reply('Ваша анкета успешно создана!')
                await state.finish()
            elif language == uz:
                await message.reply('Profilingiz muvaffaqiyatli yaratildi!')
                await state.finish()
        else:
            if language == ru:
                await message.reply(
                    f"Имя: {name},\nТелефон номер: +{phone}\nЮзер @{user_name}\nМесто проживания: {branch},\nЛицевой счет: {house_id},\nАдрес:{address}\nЕсли вы что то указали не верно то его можно изменить в настройках",
                    reply_markup=generate_main_menu('Russian 🇷🇺', 'resident'))
            elif language == uz:
                await message.reply(
                    f"Ism: {name},\nTelefon raqami: +{phone}\nYuzer @{user_name}\nYashash joyi: {branch},\nShaxsiy hisob: {house_id},\nManzil: {address}\nAgar biror narsani noto'g'ri ko'rsatgan bo'lsangiz, uni sozlamalarda o'zgartirishingiz mumkin",
                    reply_markup=generate_main_menu('Özbekcha 🇺🇿', 'resident'))
            if language == ru:
                await message.reply('Ваша анкета успешно создана!')
                await state.finish()
            elif language == uz:
                await message.reply('Profilingiz muvaffaqiyatli yaratildi!')
                await state.finish()


# Обработчик команды /register_admin
@dp.message_handler(commands=['register_admin'])
async def register_admin(message: types.Message):
    name = message.from_user.full_name
    chat_id = message.chat.id
    user_id = message.from_user.id
    member = await bot.get_chat_member(chat_id=group, user_id=message.from_user.id)
    # if user_id in admin:
    #     await message.answer('Siz adminsiz')
    # else:
    if member.is_chat_member():
        # if chat_id == group:
        # await message.forward(message_thread_id=group, chat_id=message.from_user.id)
        await bot.send_message(chat_id=message.from_user.id, text="Ismingizni yozing:",
                               reply_markup=generate_name(name))
        await AdminsGroup.name.set()

    else:
        await message.answer('Siz administrator guruhida emassiz')
        # else:
    #     await message.answer('Not group')


# Обработчик ответа с именем
@dp.message_handler(state=AdminsGroup.name)
async def process_name(message: types.Message, state: FSMContext):
    # Сохранение имени в контексте
    await state.update_data(name=message.text)
    chat_id = message.from_user.id

    user = message.from_user.username
    await message.reply("User_name kiriting:", reply_markup=generate_user_name(user))
    await AdminsGroup.user_name.set()


# Обработчик ответа с user_name
@dp.message_handler(state=AdminsGroup.user_name)
async def process_user_name(message: types.Message, state: FSMContext):
    # Сохранение user_name в контексте
    await state.update_data(user_name=message.text)

    # Запрос следующего поля
    await message.reply("Telefon raqamingizni kiriting:", reply_markup=generate_phone("Özbekcha 🇺🇿"))
    await AdminsGroup.contact.set()


# Обработчик ответа с телефоном
@dp.message_handler(state=AdminsGroup.contact, content_types=['contact'])
async def process_phone(message: types.Message, state: FSMContext):
    # Сохранение телефона в контексте
    await state.update_data(phone=message.contact.phone_number)
    # Запрос следующего поля
    id = message.from_user.id
    await message.reply("Telegram_id kiriting:", reply_markup=generate_id(id))
    await AdminsGroup.telegram_id.set()


# Обработчик ответа с telegram_id
@dp.message_handler(state=AdminsGroup.telegram_id)
async def process_telegram_id(message: types.Message, state: FSMContext):
    # Сохранение telegram_id в контексте
    await state.update_data(telegram_id=message.text)
    # Запрос следующего поля
    await message.reply("Xizmat yonalishi:", reply_markup=generate_admin_work())
    await AdminsGroup.master.set()


# Обработчик ответа с master
@dp.message_handler(state=AdminsGroup.master)
async def process_master(message: types.Message, state: FSMContext):
    # Сохранение master в контексте
    await state.update_data(master=message.text)
    # Запрос следующего поля
    await message.reply("Xizmat ko'rsatish joyi:", reply_markup=generate_branch())
    await AdminsGroup.branch.set()


# Обработчик ответа с веткой
@dp.message_handler(state=AdminsGroup.branch)
async def process_branch(message: types.Message, state: FSMContext):
    # Сохранение ветки в контексте
    await state.update_data(branch=message.text)
    # Получение всех данных из контекста
    data = await state.get_data()
    # Регистрация администратора в таблице admins
    register_admin_base(name=data['name'], user_name=data['user_name'], phone=data['phone'],
                        telegram_id=data['telegram_id'], master=data['master'], branch=data['branch'])

    # Очистка контекста
    await state.finish()
    # Отправка сообщения об успешной регистрации
    await message.reply("Administrator muvaffaqiyatli ro'yxatdan o'tdi!")


@dp.message_handler(state=AdminsGroup.name)
async def load_name(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    print('ol')
    language = get_lang_by_id(user_id)
    async with state.proxy() as data:
        data['admin_name'] = message.text
        await message.reply('Endi kontaktingizni yuboring', reply_markup=generate_phone('Russian 🇷🇺'))
        await ProfileStatesGroup.next()


@dp.message_handler(state=AdminsGroup.branch)
async def load_branch(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    language = get_lang_by_id(user_id)
    async with state.proxy() as data:
        data['branch'] = message.text
    if not message.text == 'Пропустить' or message.text == "Oʻtkazib yuborish":
        if language == ru:
            await message.reply('Теперь пришлите номер своего лицевого счета')
            await message.answer('Если не знаете номер лицевого счета пропустите его',
                                 reply_markup=generate_latere_menu('ru'))
            await AdminsGroup.next()
        if language == uz:
            await message.reply('Endi shaxsiy hisob raqamingizni yuboring')
            await message.answer('Agar litsevoy schet raqamingizni bilmasez, otkazib yuboring',
                                 reply_markup=generate_latere_menu('uz'))
            await AdminsGroup.next()
    else:
        await AdminsGroup.next()


@dp.message_handler(commands=['delete'])
async def delete(message: Message):
    user_id = message.from_user.id
    # delete_user(user_id)
    # delete_client(user_id)
    if user_id in boss:
        delete_user(user_id)
        delete_client(user_id)
        await message.answer(' ✅', reply_markup=generate_language_menu())
    # elif user_id in boss:
    #     text = message.text.strip('delete_admin')[1]
    #     delete_user(text)
    #     await message.reply('Вы удалили его из базы данных')
    #     await message.answer(' ✅', reply_markup=generate_language_menu())


@dp.message_handler(commands=['delete_admin'])
async def delete_admin_command(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if chat_id == group:
        admin_id = message.from_user.id  # Получение айди админа, которого нужно удалить
        delete_admin(admin_id)
        await message.reply("Siz administratorlar roʻyxatidan oʻchirildingiz.")
    elif user_id in boss:
        text = message.text.strip('delete_admin')[1]
        delete_admin(text)
        await message.reply("Вы удалили админа из списка админов.")


@dp.message_handler(commands=['id'])
async def get_user_id(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    language = get_lang_by_id(user_id)
    if language == ru:
        await message.answer(f'Ваш user_id = {user_id}')
        await message.answer(f'Ваш chat_id = {chat_id}')
    elif language == uz:
        await message.answer(f'Sizning user_id = {user_id}')
        await message.answer(f'Sizning chat_id = {chat_id}')


# ✅
@dp.message_handler(regexp='👨🏻‍💻Admin bilan boglanish📞|👨🏻‍💻Связатся с Админом 📞')
async def admin(message: Message):
    chat_id = message.from_user.id
    typo = get_type(chat_id)
    if typo == 'resident':
        if message.text == '👨🏻‍💻Admin bilan boglanish📞':
            await bot.send_contact(chat_id, first_name='Jahongiraka', last_name='1 nomer',
                                   phone_number='+998 95 388 88 01',
                                   reply_markup=generate_main_menu('Özbekcha 🇺🇿', 'resident'))
            await bot.send_contact(chat_id, first_name='Jahongiraka', last_name='2 nomer',
                                   phone_number='+998 93 505 01 81',
                                   reply_markup=generate_main_menu('Özbekcha 🇺🇿', 'resident'))
        elif message.text == '👨🏻‍💻Связатся с Админом 📞':
            await bot.send_contact(chat_id, first_name='Жахонгирака', last_name='1 номер',
                                   phone_number='+998 95 388 88 01',
                                   reply_markup=generate_main_menu("Russian 🇷🇺", 'resident'))
            await bot.send_contact(chat_id, first_name='Жахонгирака', last_name='2 номер',
                                   phone_number='+998 93 505 01 81',
                                   reply_markup=generate_main_menu("Russian 🇷🇺", 'resident'))
    elif typo == 'client':
        if message.text == '👨🏻‍💻Admin bilan boglanish📞':
            await bot.send_contact(chat_id, first_name='Jahongiraka', last_name='1 nomer',
                                   phone_number='+998 95 388 88 01',
                                   reply_markup=generate_main_menu('Özbekcha 🇺🇿', 'client'))
            await bot.send_contact(chat_id, first_name='Jahongiraka', last_name='2 nomer',
                                   phone_number='+998 93 505 01 81',
                                   reply_markup=generate_main_menu('Özbekcha 🇺🇿', 'client'))
        elif message.text == '👨🏻‍💻Связатся с Админом 📞':
            await bot.send_contact(chat_id, first_name='Жахонгирака', last_name='1 номер',
                                   phone_number='+998 95 388 88 01',
                                   reply_markup=generate_main_menu("Russian 🇷🇺", 'client'))
            await bot.send_contact(chat_id, first_name='Жахонгирака', last_name='2 номер',
                                   phone_number='+998 93 505 01 81',
                                   reply_markup=generate_main_menu("Russian 🇷🇺", 'client'))


@dp.message_handler(regexp='Я житель|Men rezidentman')
async def inhabitant(message: Message):
    user_id = message.from_user.id
    address = get_address(user_id)
    lang = get_lang(user_id)
    if address == ('None',) or address == none or address is None:
        await cmd_create(message)
    else:
        if lang == ru:
            await generate_main_menu('Russian 🇷🇺', 'resident')
        elif lang == uz:
            await generate_main_menu('Özbekcha 🇺🇿', 'resident')


@dp.message_handler(regexp='Гость|Mehmon')
async def guest(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_lang(user_id)
    if lang == ('uz',):
        await message.answer("Iltimos kelayotgan odamingizni filialini talang",
                             reply_markup=generate_branch_menu())
        await NewStateGroup.branch.set()
        # reply_markup=generate_back_menu('Özbekcha 🇺🇿'))
    if lang == ('ru',):
        await message.answer('Пожалуйста выберите филиал к кому вы едите', reply_markup=generate_branch_menu())
        await NewStateGroup.branch.set()


@dp.message_handler(state=NewStateGroup.branch)
async def loc(message: Message, state: FSMContext):
    user_id = message.from_user.id
    branch = message.text
    lang = get_lang(user_id)
    if branch == 'GreenPark':
        await message.answer('https://yandex.uz/maps/-/CDUty4Pf')
        await bot.send_location(message.chat.id, latitude=41.305242, longitude=69.324845)
        await state.finish()
        if lang == ru:
            await message.answer('Вот локация место проживания людей живуших в GreenPark',
                                 reply_markup=generate_back_menu('ru'))
        elif lang == uz:
            await message.answer('GreenPark aholisning turar joy lakatsiyasi', reply_markup=generate_back_menu('uz'))
    elif branch == 'Adliya':
        await message.answer('https://yandex.uz/maps/-/CDUtyYjT')
        await bot.send_location(message.chat.id, latitude=41.304994, longitude=69.322362)
        await state.finish()
        if lang == ru:
            await message.answer('Вот локация место проживания людей живуших в Adliya',
                                 reply_markup=generate_back_menu('ru'))
        elif lang == uz:
            await message.answer('Adliya aholisning turar joy lakatsiyasi', reply_markup=generate_back_menu('uz'))

    # 41.304994, 69.322362

    # await send_location(message)


# @dp.message_handler(commands=['send_location'])
# async def send_location(message: types.Message):
#     user_id = message.from_user.id
#     branch = get_user_branch(user_id)
#     lang = get_lang(user_id)
#     if branch == ('GreenPark',):
#         await bot.send_location(message.chat.id, latitude=41.305242, longitude=69.324845)
#     elif branch == ('Adliya',):
#         await bot.send_location(message.chat.id, latitude=41.305242, longitude=69.324845)
#     else:
#         if lang == ru:
#             await message.answer('My Helper не подерживает это место')
#         elif lang == uz:
#             await message.answer('My Helper siz yozgan joyga qaramaydi')


@dp.message_handler(regexp='Пропустить|Otqazib yuborish')
async def skip(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_lang(user_id)
    if lang == ru:
        await message.answer('После того как узнаете ваш лицевой счет добавьте его в насторйках')
    elif lang == uz:
        await message.answer("Shaxsiy hisobingizni aniqlaganingizdan so'ng, uni sozlamalarga qo'shing")
    await ProfileStatesGroup.next()


# ✅


@dp.message_handler(regexp='Русский 🇷🇺|Özbekcha 🇺🇿')
async def set_language(message: Message):
    user_id = message.from_user.id
    adrs = ('None',)
    name = message.from_user.full_name
    house_id = get_home_id(user_id)
    lang = 'ru'
    typo = get_type(user_id)
    address = get_address(user_id)
    if message.text == 'Русский 🇷🇺':
        if not typo == 'unknown':
            if typo == 'resident':
                update_lang(lang, user_id)
                await bot.send_message(user_id,
                                       'Вы на главном меню',
                                       reply_markup=generate_main_menu('Russian 🇷🇺', 'resident')
                                       )
            elif typo == 'client':
                update_client_lang(lang, user_id)
                await bot.send_message(user_id,
                                       'Вы на главном меню',
                                       reply_markup=generate_main_menu('Russian 🇷🇺', 'client')
                                       )
        elif address == ('None',) or address == none or address is None:
            lang = 'ru'
            language = get_lang(user_id)
            if language == ru:

                await bot.send_message(user_id,
                                       'Здравствуйте, вас приветсвует бот Упровляюшей компании My helper, для продолжения '
                                       'пожалуйуста авторизируйтесь, /register',
                                       reply_markup=generate_later("Russian 🇷🇺")
                                       )
            else:
                register_lang(user_id, name, lang)
                await bot.send_message(user_id,
                                       'Здравствуйте, вас приветсвует бот Упровляюшей компании My helper, для продолжения '
                                       'пожалуйуста авторизируйтесь, /register',
                                       reply_markup=generate_later("Russian 🇷🇺")
                                       )
        elif address == adrs:
            update_lang(lang, user_id)
            await guest(message)
        else:
            update_lang(lang, user_id)
            await bot.send_message(user_id,
                                   'Вы на главном меню',
                                   reply_markup=generate_main_menu('Russian 🇷🇺', 'resident')
                                   )
    elif message.text == 'Özbekcha 🇺🇿':
        lang = 'uz'
        if not typo == 'unknown':
            typo = get_type(user_id)
            if typo == 'resident':
                update_lang(lang, user_id)
                await bot.send_message(user_id,
                                       'Siz asosiy menyudasiz',
                                       reply_markup=generate_main_menu('Özbekcha 🇺🇿', 'resident')
                                       )
            elif typo == 'client':
                update_client_lang(lang, user_id)
                await bot.send_message(user_id,
                                       'Siz asosiy menyudasiz',
                                       reply_markup=generate_main_menu('Özbekcha 🇺🇿', 'client')
                                       )
        elif address == ('None',) or address == none or address is None:
            lang = 'uz'
            language = get_lang(user_id)
            if language == uz:

                await bot.send_message(user_id,
                                       'Assalomu aleykum sizni  “My helper” boshqaruv kompaniyasi boti kutib oldi,\n iltimos registratsiyadan /register',
                                       reply_markup=generate_later("Özbekcha 🇺🇿")
                                       )
            else:
                register_lang(user_id, name, lang)
                await bot.send_message(user_id,
                                       'Assalomu aleykum sizni  “My helper” boshqaruv kompaniyasi boti kutib oldi,\n iltimos registratsiyadan /register',
                                       reply_markup=generate_later("Özbekcha 🇺🇿")
                                       )
        elif address == adrs:
            update_lang(lang, user_id)
            await guest(message)
        else:
            update_lang(lang, user_id)
            await bot.send_message(user_id,
                                   'Siz asosiy menyudasiz',
                                   reply_markup=generate_main_menu('Özbekcha 🇺🇿', 'resident')
                                   )


@dp.message_handler(regexp='⬅|🔙')
async def back(message: Message):
    user_id = message.from_user.id
    typo = get_type(user_id)
    lang = get_lang(user_id)
    if message.text == '🔙':
        if typo == 'client':
            await message.answer('Вы вернулись в главное меню:',
                                 reply_markup=generate_main_menu('Russian 🇷🇺', 'client'))
        elif typo == 'resident':
            await message.answer('Вы вернулись в главное меню:',
                                 reply_markup=generate_main_menu('Russian 🇷🇺', 'resident'))
    elif message.text == '⬅':
        if typo == 'client':
            await message.answer('Siz asosiy menyuga qaytasiz:',
                                 reply_markup=generate_main_menu('Özbekcha 🇺🇿', 'client'))
        elif typo == 'resident':
            await message.answer('Siz asosiy menyuga qaytasiz:',
                                 reply_markup=generate_main_menu('Özbekcha 🇺🇿', 'resident'))


# if typo is 'client':
#     if lang == ru:
#         if message.text == '🔙':
#             await message.answer('Вы вернулись в главное меню:',
#                                  reply_markup=generate_main_menu('Russian 🇷🇺', 'client'))
#     elif lang == uz:
#         # if message.text == '⬅':
#             await message.answer('Siz asosiy menyuga qaytasiz:',
#                                  reply_markup=generate_main_menu('Özbekcha 🇺🇿', 'client'))
# elif typo is 'resident':
#     if lang == ru:
#         # if message.text == '🔙':
#             await message.answer('Вы вернулись в главное меню:',
#                                  reply_markup=generate_main_menu('Russian 🇷🇺', 'resident'))
#     elif lang == uz:
#         # if message.text == '⬅':
#             await message.answer('Siz asosiy menyuga qaytasiz:',
#                                  reply_markup=generate_main_menu('Özbekcha 🇺🇿', 'resident'))


@dp.message_handler(regexp='Вернутся на главное меню|Asosiy menyuga qaytish')
async def bbb(message: Message):
    user_id = message.from_user.id
    typo = get_type(user_id)
    if typo == 'resident':
        lang = get_lang(user_id)
        if lang == ('ru',):
            await message.answer('Вы вернулись в главное меню:',
                                 reply_markup=generate_main_menu('Russian 🇷🇺', 'resident'))
        elif lang == ('uz',):
            await message.answer('Siz asosiy menyuga qaytasiz:',
                                 reply_markup=generate_main_menu('Özbekcha 🇺🇿', 'resident'))
    elif typo == 'client':
        lang = get_lang(user_id)
        if lang == ('ru',):
            await message.answer('Вы вернулись в главное меню:',
                                 reply_markup=generate_main_menu('Russian 🇷🇺', 'client'))
        elif lang == ('uz',):
            await message.answer('Siz asosiy menyuga qaytasiz:',
                                 reply_markup=generate_main_menu('Özbekcha 🇺🇿', 'client'))


@dp.message_handler(regexp='Выбрать сервис ⛑️|Xizmatni tanlang ⛑️')
async def service(message: Message):
    user_id = message.from_user.id
    typo = get_type(user_id)
    if typo == 'resident':
        if message.text == 'Выбрать сервис ⛑️':
            await message.answer('Выберите одно из сервисов:', reply_markup=generate_service_menu('Russian 🇷🇺', 'resident'))
        elif message.text == 'Xizmatni tanlang ⛑️':
            await message.answer('Xizmatlardan birini tanlang:',
                                 reply_markup=generate_service_menu('Özbekcha 🇺🇿', 'resident'))
    elif typo == 'client':
        if message.text == 'Выбрать сервис ⛑️':
            await message.answer('Выберите одно из сервисов:', reply_markup=generate_service_menu('Russian 🇷🇺', 'client'))
        elif message.text == 'Xizmatni tanlang ⛑️':
            await message.answer('Xizmatlardan birini tanlang:',
                                 reply_markup=generate_service_menu('Özbekcha 🇺🇿', 'client'))


@dp.message_handler(regexp='👨‍🔧 Сантехник 🪠|🪠Santexnik 👨‍🔧')
async def santexnik(message: Message, state: FSMContext):
    if message.text == '🪠Santexnik 👨‍🔧':
        caption = 'Chap tomonda xizmat kodi mavjud'
        await message.answer_photo(InputFile('media/usu.png'), caption=caption)
        await message.answer("Bu bizning santexnika xizmatlarimiz, ro'yxatdan o'tmoqchimisiz?",
                             reply_markup=generate_yes_no_menu('Özbekcha 🇺🇿'))
    elif message.text == '👨‍🔧 Сантехник 🪠':
        caption = 'Слева находится код сервиса'
        await message.answer_photo(InputFile('media/sss.png'), caption=caption)
        await message.answer(
            'Это наши сервисы сантехника, хотите оформить ?',
            reply_markup=generate_yes_no_menu('Russian 🇷🇺'))
    async with state.proxy() as data:
        master = data['master_service'] = message.text
    # print(master)


@dp.message_handler(regexp='🔌 Электрик ⚡|🔌 Elektrik ⚡')
async def electro(message: Message, state: FSMContext):
    if message.text == '🔌 Elektrik ⚡':
        caption = 'Chap tomonda xizmat kodi mavjud'
        await message.answer_photo(InputFile('media/ueu.png'), caption=caption)
        await message.answer("Bu bizning elektrchi xizmatlarimiz, ro'yxatdan o'tmoqchimisiz?",
                             reply_markup=generate_yes_no_menu('Özbekcha 🇺🇿'))
    elif message.text == '🔌 Электрик ⚡':
        caption = 'Слева находится код сервиса'
        await message.answer_photo(InputFile('media/eee.png'), caption=caption)
        await message.answer(
            'Это наши сервисы электрика, хотите оформить ?',
            reply_markup=generate_yes_no_menu('Russian 🇷🇺'))
    async with state.proxy() as data:
        master = data['master_service'] = message.text
    # print(master)


@dp.message_handler(regexp='🧹Химчистка 🧼|🧹Уборка 🧼|🧹Uborka 🧼')
async def uborka(message: Message, state: FSMContext):
    if message.text == '🧹Uborka 🧼':
        caption = 'Chap tomonda xizmat kodi mavjud'
        await message.answer_photo(InputFile('media/uzu.png'), caption=caption)
        await message.answer("Bu bizning tozalash xizmatlarimiz, ro'yxatdan o'tishni xohlaysizmi?",
                             reply_markup=generate_yes_no_menu('Özbekcha 🇺🇿'))
    elif message.text == '🧹Уборка 🧼':
        caption = 'Слева находится код сервиса'
        await message.answer_photo(InputFile('media/uuu.png'), caption=caption)
        await message.answer(
            'Это наши сервисы уборщицы , хотите оформить ?',
            reply_markup=generate_yes_no_menu('Russian 🇷🇺'))
    async with state.proxy() as data:
        master = data['master_service'] = message.text
    # print(master)


# ✅
# ✅

# print(master == '🧹Уборка 🧼' or '🧹Uborka 🧼')

@dp.message_handler(regexp='Продолжить|Davom etish')
async def dalshe(message: Message):
    user_id = message.from_user.id
    lang = get_lang(user_id)
    if lang == ('uz',):
        await message.answer(
            "Kirish qavati va xonadon raqamini bilish uchun kimga ketayotganingizni hisob raqamini so'rang va menga yuboring!\n(uning ro'yxatdan o'tganligi muhim)!")
        await NewStateGroup.guest.set()
    elif lang == ('ru',):
        await message.answer(
            'Чтобы узнать подъезд этаж  и номер квартиры спросите номер лицевого счета к кому вы едите, и пришлите его мне\n!(Важно чтоб он/она была зарегестрирована)!')
        await NewStateGroup.guest.set()


@dp.message_handler(regexp='Дa ✅|Ha ✅')
async def application(message: Message, state=FSMContext):
    user_id = message.from_user.id
    lang = get_lang(user_id)
    user = first_select_users(user_id)
    async with state.proxy() as data:
        master = data['master_service']
    if master == str('🔌 Электрик ⚡') or master == str('🔌 Elektrik ⚡'):
        if lang == ('uz',):
            await message.answer("Foydalanmoqchi bo'lgan elektrchining xizmat kodini tanlang ⬇️:",
                                 reply_markup=generate_electric_menu())
            await NewStateGroup.service.set()
        elif lang == ('ru',):
            await message.answer('Выберите код сервиса электрика которым хотите воспользоваться ⬇️:',
                                 reply_markup=generate_electric_menu())
            await NewStateGroup.service.set()
    elif master == '👨‍🔧 Сантехник 🪠' or master == '🪠Santexnik 👨‍🔧':
        if lang == ('uz',):
            await message.answer("Foydalanmoqchi bo'lgan sanitariya-tesisat kodini tanlang ⬇️",
                                 reply_markup=generate_santexnik_menu())
            await NewStateGroup.service.set()
        elif lang == ('ru',):
            await message.answer('Выберите код сервиса сантехника которым хотите воспользоваться ⬇️:',
                                 reply_markup=generate_santexnik_menu())
            await NewStateGroup.service.set()
    elif master == str('🧹Уборка 🧼') or str('🧹Uborka 🧼') == master:
        if lang == ('uz',):
            await message.answer("Foydalanmoqchi bo'lgan tozalash xizmati kodini tanlang ⬇️:",
                                 reply_markup=generate_uborka_menu())
            await NewStateGroup.service.set()
        elif lang == ('ru',):
            await message.answer('Выберите код сервиса уборки которым хотите воспользоваться ⬇️: ',
                                 reply_markup=generate_uborka_menu())
            await NewStateGroup.service.set()


@dp.message_handler(commands=['get_user'])
async def cmd_gets(message: Message):
    # user_id = message.text.strip('/get_user')[1]
    get_id = message.text.strip('/get_user ')
    print(get_id)
    full_name, user_name, telegram_id, phone, language, branch, house_id, address = get_info_iuser_id(get_id)
    user_id = message.from_user.id
    if user_id in boss:
        # print(user_id)
        text = f"---Информация---\n"
        text += f"---Юзера---\n"
        text += f'Имя: {full_name}\n'
        text += f'Юзер: @{user_name}\n'
        text += f'ID: {telegram_id}\n'
        text += f'Номер: +{phone}\n'
        text += f"Язык: {language}\n"
        text += f"Филиал: {branch}\n"
        text += f"Лицевой счет: {house_id}\n"
        text += f"Адресс: {address}\n"
        await bot.send_message(chat_id=message.chat.id, text=text)
    else:
        await message.answer('error 404')
        await message.answer('Пользователя нет в базе данных')


@dp.message_handler(commands=['get_admin'])
async def cmd_get_admin(message: Message):
    get_id = message.text.strip('/get_admin ')
    full_name, user_name, telegram_id, phone, master, branch = get_admin_info(get_id)
    chat_id = message.chat.id
    # hs_id = 'none'
    # user = first_select_users(user_id)
    # if user:
    user_id = message.from_user.id
    if user_id in boss:
        text = f"---Информация---\n"
        text += f"---Админа---\n"
        text += f'Имя: {full_name}\n'
        text += f'Юзер: {user_name}\n'
        text += f'ID: {get_id}\n'
        text += f'Номер: +{phone}\n'
        text += f"Мастер: {master}\n"
        text += f"Филиал: {branch}\n"
        await bot.send_message(chat_id, text=text)
    else:
        await message.answer('error 404')
        # await message.answer('Пользователя нет в базе данных')


@dp.message_handler(regexp='Информация про анкету|Anketa haqida malumot')
async def info(message: Message):
    chat_id = message.from_user.id
    lang = get_lang(chat_id)
    data = get_user_data(chat_id)
    name, user_id, phone, language, house_id, address = get_user_data(chat_id)
    if lang == ('uz',):
        await message.answer(
            f'~~~Anketa~~~\nIsm:\t{name}\nId:\t{user_id}\nTelefon nomer:\t+{phone}\nTil:\t{language}\nLitsevoy schet:\t{house_id}\nAddress:\t{address}')
        await message.answer(data)
    elif lang == ('ru',):
        await message.answer(
            f'~~~Анкета~~~\nИмя:\t{name}\nId:\t{user_id}\nТелефон номер:\t+{phone}\nЯзык:\t{language}\nЛицевой счет:\t{house_id}\nАддресс:\t{address}')


# ❌


@dp.message_handler(state=NewStateGroup.guest)
async def cmd_get_user(message: Message, state: FSMContext):
    user_id = message.from_user.id
    language = get_lang(user_id)
    try:
        house_id = message.text
        full_name, phone, language, address = get_phone_and_address_by_hs_id(house_id)
        hs_id = 'none',
        result = hs_id == house_id
        if not result:
            uz = str('uz')
            ru = str('ru')
            if language == ru:
                text = f"---Информация---\n"
                text += f'Имя: {full_name}\n'
                text += f'Номер: +{phone}\n'
                text += f"Язык: {language}\n"
                text += f"Адрес: {address}\n"
                # text += f"house_id: {house_id}\n"
                await message.answer(text=text, reply_markup=generate_back_menu('ru'))
                await message.answer('Данные нашлись ✅')
            elif language == uz:
                text = f"---Malumot---\n"
                text += f'Ism: {full_name}\n'
                text += f'Telefon raqam: +{phone}\n'
                text += f"til: {language}\n"
                text += f"address: {address}\n"
                # text += f"house_id: {house_id}\n"
                await message.answer(text=text, reply_markup=generate_back_menu('uz'))
                await message.answer(text='Malumotlar topildi ✅')
        # await guest(message)
        await state.finish()
    except Exception as e:
        if e:
            if language == ('ru',):
                await message.answer('Пользователя нет в базе данных перепроверьте')
                await guest(message)
            elif language == ('uz',):
                await message.answer("Foydalanuvchi ma'lumotlar bazasida yo'q, qayta tekshiring")
                await guest(message)
            # await message.answer('error 404')
            await state.finish()

    # await message.reply("Это команда должна быть ответом на сообщение !")
    # return
    # await bot.send_message(GROUP_ID, "Вы приняли сервис ! "
    #                                  " бегите в помощь !")
    # await bot.send_message(message.from_user.id, 'Ваш сервис был принят ждите !')


# ✅


@dp.message_handler(commands=['end'])
async def send_end(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if message.chat.id == group:
        await message.answer("Xabar yubormoqchi bo'lgan shaxsning identifikatorini yuboring")
        await AnswerGroup.ID.set()
    else:
        await message.answer('Это команда только для Админов')
        await state.finish()


@dp.message_handler(state=AnswerGroup.ID)
async def branch_sr(message: Message, state: FSMContext):
    async with state.proxy() as data:
        sender_id = data['sender_id'] = message.text
        print(sender_id)
        await message.answer(f'Endi kerakli xabarni yuboring\n{sender_id}')
        # await AnswerGroup.title.sext()
        await AnswerGroup.next()


@dp.message_handler(state=AnswerGroup.title, content_types=['photo'])
async def title_send(message: Message, state: FSMContext):
    chat_id = message.chat.id
    photo_file_id = message.photo[-1].file_id

    caption = message.caption
    message_id = message.message_id
    if chat_id == group:
        async with state.proxy() as data:
            sender_id = data['sender_id']
            print(sender_id)
            lang = get_lang(sender_id)
            # print(sender_id)
            # await bot.forward_message(chat_id=sender_id, from_chat_id=group, message=f'{message.photo+message.caption }'),
            if lang == ru:
                await bot.send_photo(chat_id=sender_id, photo=photo_file_id, caption=caption,
                                     reply_markup=generate_dov_menu('ru')),
                await bot.send_message(text='Оцените пожалуйста качество сервиса', chat_id=sender_id)
            elif lang == uz:
                await bot.send_photo(chat_id=sender_id, photo=photo_file_id, caption=caption,
                                     reply_markup=generate_dov_menu('uz')),
                await bot.send_message(text="Iltimos, xizmat sifatini baholang", chat_id=sender_id)
            await state.finish()
            await message.answer('Yuborildi ✅')


@dp.message_handler(commands=['answer'])
async def send_answer(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if message.chat.id == group:
        await message.answer("Xabar yubormoqchi bo'lgan shaxsning identifikatorini yuboring")
        await AnswerGroup.ID.set()
    else:
        await message.answer('Это команда только для Админов')
        await state.finish()


@dp.message_handler(state=AnswerGroup.ID)
async def branch_sr(message: Message, state: FSMContext):
    async with state.proxy() as data:
        sender_id = data['sender_id'] = message.text
        print(sender_id)
        await message.answer(f'Endi kerakli xabarni yuboring\n{sender_id}')
        await AnswerGroup.next()


@dp.message_handler(state=AnswerGroup.title)
async def title_send(message: Message, state: FSMContext):
    chat_id = message.chat.id
    text = message.text
    if chat_id == group:
        async with state.proxy() as data:
            sender_id = data['sender_id']
            print(sender_id)
            lang = get_lang(sender_id)
            # print(sender_id)
            # await bot.forward_message(chat_id=sender_id, from_chat_id=group, message=f'{message.photo+message.caption }'),
            if lang == ru:
                await bot.send_message(text=f'{text}', chat_id=sender_id)
            elif lang == uz:
                await bot.send_message(text=f'{text}', chat_id=sender_id)
            await state.finish()
            await message.answer('Yuborildi ✅')


@dp.message_handler(state=NewStateGroup.offer)
async def feedback(message: Message, state: FSMContext):
    # text = message.text.split(' ')[1]
    user_id = message.from_user.id
    language = get_lang_by_id(user_id)
    print(user_id)
    text = message.text
    await bot.send_message(group, f'{user_id}\nПредложение от жителя:\n{text}')
    if language == ru:
        await state.finish()
        await message.answer(f'{text}\nваше предложение отправлено ✅')


@dp.message_handler(regexp='📓 Shaxsiy hisob haqida bilib olish 🧮|📓 Узнать о лицевом счете 🧮')
async def personality(message: Message):
    if message.text == '📓 Shaxsiy hisob haqida bilib olish 🧮':
        await message.answer('Sizga mos keladigan elementni tanlang', reply_markup=generate_account_menu("Özbekcha 🇺🇿"))
    #     await message.answer('Qabul qilindi , adminimiz javobini kuting')
    #     await bot.send_message(group, f'{message.migrate_from_chat_id} Ozini shaxsiy hsobini soravoti')
    elif message.text == '📓 Узнать о лицевом счете 🧮':
        await message.answer('Выберите подходящий вам пункт', reply_markup=generate_account_menu("Russian 🇷🇺"))
    #     await message.answer('Принятоб ждите пока вам ответят ')
    #     await bot.send_message(group, f'{message.from_user} '
    #                                   f'Просит свои даные лицевого счета ')


# ❌


@dp.message_handler(state=NewStateGroup.service)
async def process_request(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.from_user.username
    typo = get_type(user_id)
    branch = get_user_branch(user_id)
    async with state.proxy() as data:
        master = data['master_service']
        print(master)
        print(master == '🧹Химчистка 🧼')

        # print(branch)
        # print(branch == ('GreenPark',))
        # print(branch == ('QUSHBEGI'))
        # print('o00o', master == str('👨‍🔧 Сантехник 🪠') or master == str('🪠Santexnik 👨‍🔧'))

    if typo == 'resident':
        if master == str('🔌 Электрик ⚡') or master == str('🔌 Elektrik ⚡'):
            master = 'Электрик'
            branch = '1/2'
            master_user = get_master(master, branch)
            await bot.send_message(chat_id=group,
                                   text=f"Yangi elektrchi so'rovi olindi, iltimos, xizmat ko'rsating:\n{master_user}")
        elif master == str('👨‍🔧 Сантехник 🪠') or master == str('🪠Santexnik 👨‍🔧'):
            master = 'Сантехник'
            branch = '1/2'
            master_user = get_master(master, branch)
            # print(f'E#########{master_user}')
            await bot.send_message(chat_id=group,
                                   text=f"Santexnikga yangi talab olindi,iltimos xizmat qiling:\n{master_user}")

        elif master == str('🧹Уборка 🧼') or master == str('🧹Uborka 🧼'):
            master = 'Уборщица'
            branch = '1/2'
            master_user = get_master(master, branch)
            print(master_user)
            await bot.send_message(chat_id=group,
                                   text=f"Yangi tozalash so'rovi olindi,iltimos xizmat qiling:\n{master_user}")
        full_name, phone, language, address, house_id, branchh = get_phone_and_address_by_id(user_id)
        text = f"---Rezidentdan xizmat ko'rsatishni so'rash---\n"
        text += f'Ism: {full_name}\n'
        text += f'Yuzer: @{user_name}\n'
        text += f'ID: <u>{user_id}</u>\n'
        text += f'Telefon raqami: +{phone}\n'
        text += f"Til: {language}\n"
        text += f"Manzil: {address}\n"
        text += f"Filial: {branchh}\n"
        text += f"Shaxsiy hisob: {house_id}\n"
        text += f"Xizmat: \t{message.text}"
        # text += f"User servise: \t{message.text.split(' ')[1]}"
        # await bot.send_message(group, text=text)
        await bot.send_photo(chat_id=group, photo=InputFile('media/servise.png'), caption=text)
        # await bot.send_photo(chat_id=group, photo=InputFile('media/93-3-2.png'))
        if language == 'ru':
            await message.answer('Ваша заявка принята ✅,\nскоро с вами свяжутся',
                                 reply_markup=generate_main_menu('Russian 🇷🇺', 'resident'))
        elif language == 'uz':
            await message.answer("Sizning arizangiz qabul qilindi ✅,\ntez orada siz bilan bog'lanamiz",
                                 reply_markup=generate_main_menu('Özbekcha 🇺🇿', 'resident'))
        await state.finish()
    elif typo == 'client':
        if master == str('🔌 Электрик ⚡') or master == str('🔌 Elektrik ⚡'):
            master = 'Электрик'
            branch = '1/2'
            master_user = get_master(master, branch)
            cleaned_users = [user[0].replace("('", "").replace("',)", "") for user in master_user]

            await bot.send_message(chat_id=group,
                                   text=f"Yangi elektrchi so'rovi olindi, iltimos, xizmat ko'rsating:\n{cleaned_users}")
        elif master == str('👨‍🔧 Сантехник 🪠') or master == str('🪠Santexnik 👨‍🔧'):
            master = 'Сантехник'
            branch = '1/2'
            master_user = get_master(master, branch)
            cleaned_users = [user[0].replace("[(''", "").replace("'',)]", "") for user in master_user]

            # print(f'E#########{master_user}')
            await bot.send_message(chat_id=group,
                                   text=f"Santexnikga yangi talab olindi,iltimos xizmat qiling:\n{cleaned_users}")

        elif master == str('🧹Химчистка 🧼') or str('🧹Уборка 🧼') or master == str('🧹Uborka 🧼'):
            master = 'Уборщица'
            branch = '1/2'
            master_user = get_master(master, branch)
            cleaned_users = [user[0].replace("('", "").replace("',)", "") for user in master_user]
            await bot.send_message(chat_id=group,
                                   text=f"Xaridordan xizmat so'rovi olindi, iltimos, xizmatni taqdim eting:\n{cleaned_users}")
        full_name, phone, language, user_name = get_client_info(user_id)
        text = f"---Xaridor info 👇🏻---\n"
        text += f'Ism: {full_name}\n'
        text += f'Yuzer: @{user_name}\n'
        text += f'ID: <u>{user_id}</u>\n'
        text += f'Telefon raqami: +{phone}\n'
        text += f"Til: {language}\n"
        text += f"Xizmat: \t{message.text}"
        await bot.send_photo(chat_id=group, photo=InputFile('media/servise.png'), caption=text)
        if language == 'ru':
            await message.answer('Ваша заявка принята ✅,\nскоро с вами свяжутся',
                                 reply_markup=generate_main_menu('Russian 🇷🇺', 'client'))
        elif language == 'uz':
            await message.answer("Sizning arizangiz qabul qilindi ✅,\ntez orada siz bilan bog'lanamiz",
                                 reply_markup=generate_main_menu('Özbekcha 🇺🇿', 'client'))
        await state.finish()
    else:
        await message.answer('None resident\nnot even customer')


@dp.message_handler(regexp='🤗 Qoniq topdim rahmat ✅|🤗Доволен спасибо ✅')
async def dovolen(message: Message):
    user_id = message.from_user.id
    lang = get_lang_by_id(user_id)
    if lang == ru:
        await message.answer('Спасибо за оценку качество,вы вернулись в главное меню:',
                             reply_markup=generate_main_menu('Russian 🇷🇺', 'resident'))
    elif lang == uz:
        await message.answer('Sifat reytingingiz uchun rahmat, siz asosiy menyuga qaytasiz:',
                             reply_markup=generate_main_menu('Özbekcha 🇺🇿', 'resident'))
    await bot.send_message(
        text=f'{message.from_user.full_name}dan\t- @{message.from_user.username}\t{message.text}\nrezidentdan minnatdorchilik bildirildi, MyHelper jamoasiga raxmat',
        chat_id=group)

    # else:
    #     await message.answer('error 404')
    #     await state.finish()

    # else:


@dp.message_handler(regexp='❌ Не довлен 😕|❌ Qoniqarli emas 😕')
async def nedovolen(message: Message):
    user_id = message.from_user.id
    lang = get_lang_by_id(user_id)
    if lang == ru:
        await message.answer('Спасибо за оценку качество,вы вернулись в главное меню:',
                             reply_markup=generate_main_menu('Russian 🇷🇺', 'resident'))
    elif lang == uz:
        await message.answer('Sifat reytingingiz uchun rahmat, siz asosiy menyuga qaytasiz:',
                             reply_markup=generate_main_menu('Özbekcha 🇺🇿', 'resident'))
    await bot.send_message(
        text=f'{message.from_user.full_name}dan\t- @{message.from_user.username}\t{message.text}\nrezidentdan servisdan maqulmasligini bildirildi, MyHelper jamoasiga',
        chat_id=group)


# ✅
@dp.message_handler(regexp='Нет ❌|Yoq ❌')
async def nope(message: Message):
    user_id = message.from_user.id
    typo = get_type(user_id)
    if typo == 'resident':
        lang = get_lang(user_id)
        if lang == uz:
            await message.answer('Siz xizmatlar menyusidasiz',
                                 reply_markup=generate_service_menu('Özbekcha 🇺🇿', "resident"))
        elif lang == ru:
            await message.answer('Вы в меню сервисов', reply_markup=generate_service_menu('Russian 🇷🇺', 'resident'))
    elif typo == 'client':
        lang = get_client_lang(user_id)
        if lang == uz:
            await message.answer('Siz xizmatlar menyusidasiz',
                                 reply_markup=generate_service_menu('Özbekcha 🇺🇿', "client"))
        elif lang == ru:
            await message.answer('Вы в меню сервисов', reply_markup=generate_service_menu('Russian 🇷🇺', 'client'))


# ✅ ❌
@dp.message_handler(regexp='Аварийная ситуация 🚨|Favqulodda vaziyat 🚨')
async def green(message: Message):
    user_id = message.from_user.id
    lang = get_lang(user_id)
    branch = get_user_branch(user_id)
    print(branch)
    if branch == ('GreenPark',):
        await bot.send_photo(chat_id=message.from_user.id, photo=InputFile('media/gp.jpg'),
                             caption='+998 90 957 60 56 -\tlift | лифт\n+998 95 388 88 06 -\t santexnik | сантехник\n+998 95 388 88 05 -\t elektrik | электрик\n+998 93 541 22 99 -\t'
                                     'domofon | домофон\n+998 95 388 88 04 -\tqorovul | охранник\n+998 95 388 88 07 - sifat menedjeri | менеджер по качеству'),
    elif branch == ('Adliya',):
        await bot.send_photo(chat_id=message.from_user.id, photo=InputFile('media/adl.jpg'),
                             caption='+998 90 957 60 56 -\tlift | лифт\n+998 95 388 88 06 -\t santexnik | сантехник\n+998 95 388 88 05 -\t elektrik | электрик\n+998 97 103 45 01 -\t'
                                     'domofon | домофон\n+998 95 388 88 03 -\tqorovul | охранник\n+998 95 388 88 07 - sifat menedjeri | менеджер по качеству'),
        # caption='90 957 60 56 -\tlift | лифт\n91 101 72 21 -\t santexnik | сантехник\n99 854 13 81 -\t elektrik | электрик\n+998971034501 -\t'
        # 'domofon | домофон\n+998 997919995 -\t qorovul | охранник'),


# ✅
@dp.message_handler(regexp='Номер лицевого счета|Hisob raqami')
async def get_num(message: Message):
    user_id = message.from_user.id
    branch = get_user_branch(user_id)
    lang = get_lang(user_id)
    if branch == ('GreenPark',):
        if message.text == 'Номер лицевого счета':
            await message.answer('Выберите номер здания', reply_markup=generate_get_number('Russian 🇷🇺'))
        elif message.text == 'Hisob raqami':
            await message.answer('Bino raqamini tanlang', reply_markup=generate_get_number('Özbekcha 🇺🇿'))
    elif branch == ('Adliya',):
        group_933 = [
            types.InputMediaPhoto(media=open('media/adliya1.jpg', 'rb')),
            types.InputMediaPhoto(media=open('media/adliya2.jpg', 'rb'))
        ]
        await bot.send_media_group(message.chat.id, media=group_933)
        if lang == uz:
            await message.answer("Adliya da yashovchilar ro'yxatidan shaxsiy hisobingizni qidiring",
                                 reply_markup=generate_main_menu('Özbekcha 🇺🇿', 'resident'))
        elif lang == ru:
            await message.answer("Найдите свой лицевой счет в списке живуших в Adliya",
                                 reply_markup=generate_main_menu('Russian 🇷🇺', 'resident'))


# ✅
@dp.message_handler(regexp='Dom 93-3|Dom 95-2|Dom 95-3|Dom 97-2|Dom 97-1')
async def personality(message: Message):
    if message.text == 'Dom 93-3':
        group_933 = [
            types.InputMediaPhoto(media=open('media/93-3-1.png', 'rb')),
            types.InputMediaPhoto(media=open('media/93-3-2.png', 'rb'),
                                  caption="93/3 da yashovchilar ro'yxatidan shaxsiy hisobingizni qidiring")
        ]
        await bot.send_media_group(message.chat.id, media=group_933)
    elif message.text == 'Dom 95-3':
        group_953 = [
            types.InputMediaPhoto(media=open('media/95-3-1.png', 'rb')),
            types.InputMediaPhoto(media=open('media/95-3-2.png', 'rb'),
                                  caption="95/3 da yashovchilar ro'yxatidan shaxsiy hisobingizni qidiring")
        ]
        await bot.send_media_group(message.chat.id, media=group_953)
    elif message.text == 'Dom 95-2':
        group_952 = [
            types.InputMediaPhoto(media=open('media/95-2-1.png', 'rb')),
            types.InputMediaPhoto(media=open('media/95-2-2.png', 'rb'),
                                  caption="95/2 da yashovchilar ro'yxatidan shaxsiy hisobingizni qidiring")
        ]
        await bot.send_media_group(message.chat.id, media=group_952)
    elif message.text == 'Dom 97-2':
        group_972 = [
            types.InputMediaPhoto(media=open('media/97-2-1.png', 'rb')),
            types.InputMediaPhoto(media=open('media/97-2-2.png', 'rb'),
                                  caption="97/2 da yashovchilar ro'yxatidan shaxsiy hisobingizni qidiring")
        ]
        await bot.send_media_group(message.chat.id, media=group_972)
    elif message.text == 'Dom 97-1':
        group_971 = [
            # types.InputMediaPhoto(media=open('media/97-1-1.png', 'rb')),
            types.InputMediaPhoto(media=open('media/97-1.png', 'rb'),
                                  caption="97/1 da yashovchilar ro'yxatidan shaxsiy hisobingizni qidiring")
        ]
        await bot.send_media_group(message.chat.id, media=group_971)


# ✅
@dp.message_handler(regexp='Дом 93-3|Дом 95-2|Дом 95-3|Дом 97-2|Дом 97-1')
async def personality(message: Message):
    # caption1 = 'Первый лист'
    # caption2 = 'Второй лист'
    if message.text == 'Дом 93-3':
        # await message.answer_photo(InputFile('media/93-3-1.png'), caption=caption1),
        # await message.answer_photo(InputFile('media/93-3-2.png'), caption=caption2),
        # await message.answer('Ищите))')
        group_933 = [
            types.InputMediaPhoto(media=open('media/93-3-1.png', 'rb')),
            types.InputMediaPhoto(media=open('media/93-3-2.png', 'rb'),
                                  caption="Ищите свой лицевой счет из списка живущих в 93/3")
        ]
        await bot.send_media_group(message.chat.id, media=group_933)
    if message.text == 'Дом 95-3':
        # await message.answer_photo(InputFile('media/95-3-1.png'), caption=caption1),
        # await message.answer_photo(InputFile('media/95-3-2.png'), caption=caption2),
        # await message.answer('Ищите))')
        group_953 = [
            types.InputMediaPhoto(media=open('media/95-3-1.png', 'rb')),
            types.InputMediaPhoto(media=open('media/95-3-2.png', 'rb'),
                                  caption="Ищите свой лицевой счет из списка живущих в 95/3")
        ]
        await bot.send_media_group(message.chat.id, media=group_953)
    if message.text == 'Дом 95-2':
        # await message.answer_photo(InputFile('media/95-2-1.png'), caption=caption1),
        # await message.answer_photo(InputFile('media/95-2-2.png'), caption=caption2),
        # await message.answer('Ищите))')
        group_952 = [
            types.InputMediaPhoto(media=open('media/95-2-1.png', 'rb')),
            types.InputMediaPhoto(media=open('media/95-2-2.png', 'rb'),
                                  caption="Ищите свой лицевой счет из списка живущих в 95/2")
        ]
        await bot.send_media_group(message.chat.id, media=group_952)
    if message.text == 'Дом 97-2':
        group_972 = [
            types.InputMediaPhoto(media=open('media/97-2-1.png', 'rb')),
            types.InputMediaPhoto(media=open('media/97-2-2.png', 'rb'),
                                  caption="Ищите свой лицевой счет из списка живущих в 97/2")
        ]
        await bot.send_media_group(message.chat.id, media=group_972)
    if message.text == 'Дом 97-1':
        group_971 = [
            # types.InputMediaPhoto(media=open('media/97-1-1.png', 'rb')),
            types.InputMediaPhoto(media=open('media/97-1.png', 'rb'),
                                  caption="Ищите свой лицевой счет из списка живущих в 97/1")
        ]
        await bot.send_media_group(message.chat.id, media=group_971)


# ✅
@dp.message_handler(regexp='Узнать мою задалжость|Mening qarzimni bilib oling')
async def duty(message: Message):
    user_id = message.from_user.id
    address = get_address(user_id)
    home_id = get_home_id(user_id)
    lang = get_lang(user_id)
    if lang == ru:
        await message.answer(
            'Информацию о своем лицевом счете вы можете узнать используя click, payme uzum итд, в разделе Mening Uyim',
            reply_markup=generate_main_menu('Russian 🇷🇺', 'resident'))
    elif lang == uz:
        await message.answer(
            "Shaxsiy kabinetingiz haqidagi ma'lumotlarni click, payme uzum va boshqalarlar yordamida bilib olishingiz mumkin, Mening Uyim servisida",
            reply_markup=generate_main_menu('Özbekcha 🇺🇿', 'resident'))


# ✅
@dp.message_handler(commands=['sendall'])
async def send_all(message: Message, state: FSMContext):
    user_id = message.from_user.id
    caption = message.text.split('/sendall')[1]
    users = mailing()
    if user_id in boss:
        await message.answer('Это команда только для Жахонгир Ака')
        await state.finish()
    else:
        if message.chat.id == group:
            print(users)
            for user_id in users:
                await bot.send_photo(chat_id=user_id, photo=InputFile('media/news.jpg'), caption=caption),
            await message.answer('Рассылка отправлена')


@dp.message_handler(commands=['send_branch'])
async def send_branch(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if message.chat.id == group:
        await message.answer('Выберите филиал которому хотите отправить рассылку', reply_markup=generate_branch_menu())
        await ServiceGroup.branch.set()
    else:
        await message.answer('Это команда только для Админов')
        await state.finish()


@dp.message_handler(state=ServiceGroup.branch)
async def branch_sr(message: Message, state: FSMContext):
    async with state.proxy() as data:
        branch = data['branch_sr'] = message.text
        # print(branch)
        await ServiceGroup.next()
        await message.answer(f'Теперь отправьте что хотите расслать {branch}')


@dp.message_handler(state=ServiceGroup.title)
async def title_send(message: Message, state: FSMContext):
    user_id = message.from_user.id
    caption = message.text
    async with state.proxy() as data:
        branch = data['branch_sr']
    # branch = get_user_branch(user_id)
    print(branch)
    users = get_branch(branch)
    # print(users)
    if message.chat.id == group:
        for user in users:
            await bot.send_photo(chat_id=user, photo=InputFile('media/news.jpg'), caption=f'{branch}\n{caption}'),
            await state.finish()
    await message.answer('Рассылка отправлена')


# ❌
@dp.message_handler(regexp='Sozlamalar ⚙️|Настройки ⚙️')
async def setting(message: Message):
    user_id = message.from_user.id
    typo = get_type(user_id)
    if typo == 'resident':
        if message.text == 'Sozlamalar ⚙️':
            await message.answer('Sozlamalar menyusi', reply_markup=generate_settings_menu('Özbekcha 🇺🇿', 'resident'))
        elif message.text == 'Настройки ⚙️':
            await message.answer('Меню настроек', reply_markup=generate_settings_menu('Russian 🇷🇺', 'resident'))
    elif typo == 'client':
        if message.text == 'Sozlamalar ⚙️':
            await message.answer('Sozlamalar menyusi', reply_markup=generate_settings_menu('Özbekcha 🇺🇿', 'client'))
        elif message.text == 'Настройки ⚙️':
            await message.answer('Меню настроек', reply_markup=generate_settings_menu('Russian 🇷🇺', 'client'))


# ✅
@dp.message_handler(regexp="Tilni o'zgartirish 🇺🇿 🔀 🇷🇺|Изменить язык 🇷🇺 🔀 🇺🇿")
async def change_lang(message: Message):
    if message.text == 'Изменить язык 🇺🇿 🔀 🇷🇺':
        await message.answer("Выберите язык", reply_markup=generate_language_menu())
    else:
        await message.answer("Tilni tanlang", reply_markup=generate_language_menu())


# ✅
async def get_user(user_id, message):
    user = first_select_users(user_id)
    if user:
        full_name, phone, language, address, house_id = get_phone_and_address_by_id(user_id)
        print(phone)
        text = f"*** Заявка ***\n~На информацию про задолжноть~:\n"
        text += f'имя: {full_name}\n'
        text += f'phone: +{phone}\n'
        text += f"language: {language}\n"
        text += f"Адрес: {address}\n"
        text += f"house_id: {house_id}\n"
        # text += f"User servise: \t{message.text.split(' ')[1]}"
        await bot.send_message(group, text=text)
    else:
        await message.answer('error 404')


@dp.message_handler(regexp='Сменить имя 👤|Ismimni ozgartirish 👤')
async def get_new_name(message: Message):
    user_id = message.from_user.id
    language = get_lang_by_id(user_id)
    ru = 'ru',
    uz = 'uz',

    if language == ru:
        await message.reply('Пришлите свое новое имя:')
        await NewStateGroup.new_name.set()
    elif language == uz:
        await message.reply('Yangi ismingizni yuboring:')
        await NewStateGroup.new_name.set()


@dp.message_handler(state=NewStateGroup.new_name)
async def load_new_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    typo = get_type(user_id)
    ru = 'ru',
    uz = 'uz',
    async with state.proxy() as data:
        new_name = data['name'] = message.text
        if typo == 'resident':
            language = get_lang_by_id(user_id)
            update_name(new_name, user_id)
            if language == ru:
                await message.reply('Ваше имя изменено!')
                await state.finish()
            if language == uz:
                await message.reply("Ismingiz o'zgartirildi!")
                await state.finish()
        elif typo == 'client':
            lang = get_client_lang(user_id)
            update_client_name(new_name, user_id)
            if lang == ru:
                await message.reply('Ваше имя изменено!')
                await state.finish()
            if lang == uz:
                await message.reply("Ismingiz o'zgartirildi!")
                await state.finish()


@dp.message_handler(regexp="📞 Telefon raqamini o'zgartirish ☎️|📞 Сменить номер телефона ☎️")
async def get_new_phone(message: Message):
    user_id = message.from_user.id
    language = get_lang_by_id(user_id)
    typo = get_type(user_id)
    # if typo == 'resident':
    if language == ru:
        await message.reply('Пришлите свой новый номер:', reply_markup=generate_phone('Russian 🇷🇺'))
        await NewStateGroup.new_contact.set()
    elif language == uz:
        await message.reply('Yangi raqamingizni yuboring:', reply_markup=generate_phone('Özbekcha 🇺🇿'))
        await NewStateGroup.new_contact.set()
    # elif typo == 'client':
    #     if language == ru:
    #         await message.reply('Пришлите свой новый номер:', reply_markup=generate_phone('Russian 🇷🇺'))
    #         await NewStateGroup.new_contact.set()
    #     elif language == uz:
    #         await message.reply('Yangi raqamingizni yuboring:', reply_markup=generate_phone('Özbekcha 🇺🇿'))
    #         await NewStateGroup.new_contact.set()


@dp.message_handler(state=NewStateGroup.new_contact, content_types=['contact'])
async def load_new_phone(message: Message, state: FSMContext):
    user_id = message.from_user.id
    language = get_lang_by_id(user_id)
    typo = get_type(user_id)
    ru = 'ru',
    uz = 'uz',
    async with state.proxy() as data:
        new_phone = data['contact'] = message.contact.phone_number
        # print(new_phone)
        if typo == 'resident':
            update_phone(new_phone, user_id)
            if language == ru:
                await message.reply('Ваш номер изменен!', reply_markup=generate_settings_menu('Russian 🇷🇺', 'resident'))
                await state.finish()
            if language == uz:
                await message.reply("Sizning raqamingiz o'zgartirildi!",
                                    reply_markup=generate_settings_menu('Özbekcha 🇺🇿', 'resident'))
                await state.finish()
        elif typo == 'client':
            update_client_phone(new_phone, user_id)
            if language == ru:
                await message.reply('Ваш номер изменен!', reply_markup=generate_settings_menu('Russian 🇷🇺', 'client'))
                await state.finish()
            if language == uz:
                await message.reply("Sizning raqamingiz o'zgartirildi!",
                                    reply_markup=generate_settings_menu('Özbekcha 🇺🇿', 'client'))
                await state.finish()


@dp.message_handler(regexp="Manzilni o'zgartirish 🏘️|Изменить адрес 🏘️")
async def add_address(message: Message):
    user_id = message.from_user.id
    language = get_lang_by_id(user_id)
    ru = 'ru',
    uz = 'uz',
    if language == ru:
        await message.reply('Пришлите свой филиал:', reply_markup=generate_branch_menu())
        await NewStateGroup.new_branch.set()
    elif language == uz:
        await message.reply('Filialingizni yuboring:', reply_markup=generate_branch_menu())
        await NewStateGroup.new_branch.set()


@dp.message_handler(state=NewStateGroup.new_branch)
async def new_branch_func(message: Message, state: FSMContext):
    user_id = message.from_user.id
    language = get_lang_by_id(user_id)
    async with state.proxy() as data:
        new_branch = data['new_branch_'] = message.text
        update_branch(new_branch, user_id)
        if language == ru:
            await message.reply('Пришлите свой адрес:')
            await NewStateGroup.new_address.set()
        elif language == uz:
            await message.reply('Manzilingizni yuboring:')
            await NewStateGroup.new_address.set()


@dp.message_handler(state=NewStateGroup.new_address)
async def load_new_address(message: Message, state: FSMContext):
    user_id = message.from_user.id
    language = get_lang_by_id(user_id)
    ru = 'ru',
    uz = 'uz',
    async with state.proxy() as data:
        new_address = data['new_address'] = message.text
        update_address(new_address, user_id)
        if language == ru:
            await message.answer(f"{new_address}\nадрес успешно изменен!",
                                 reply_markup=generate_settings_menu("Russian 🇷🇺", 'resident'))
            await state.finish()
        if language == uz:
            await message.answer(f"{new_address}\nmanzil ozgartirildi!",
                                 reply_markup=generate_settings_menu('Özbekcha 🇺🇿', 'resident'))
            await state.finish()


@dp.message_handler(regexp="Shaxsiy hisobni o'zgartirish 🧮|Изменить лицевой счет 🧮")
async def add_new_house_id(message: Message):
    user_id = message.from_user.id
    language = get_lang_by_id(user_id)
    ru = 'ru',
    uz = 'uz'
    if language == ru:
        await message.reply('Пришлите свой лицевой счет:')
        await NewStateGroup.new_house_id.set()
    else:
        await message.reply('Shaxsiy hisobingizni quyidagi manzilga yuboring:')
        await NewStateGroup.new_house_id.set()


@dp.message_handler(state=NewStateGroup.new_house_id)
async def load_new_new_house_id(message: Message, state: FSMContext):
    user_id = message.from_user.id
    language = get_lang_by_id(user_id)
    ru = 'ru',
    uz = 'uz',
    house_id = message.text
    if house_id.startswith('139') or house_id.startswith('138'):
        async with state.proxy() as data:
            new_house_id = data['new_house_id'] = message.text
            update_house_id(new_house_id, user_id)
            if language == ru:
                await message.answer(f"{new_house_id}\nЛицевой счет успешно изменен!")
                await state.finish()
            if language == uz:
                await message.answer(f"{new_house_id}\nShaxsiy hisob muvaffaqiyatli o'zgartirildi!")
                await state.finish()
    else:
        if language == ru:
            await message.answer('Пожалуйста пришлите действительный номер лицевого счета')
        elif language == uz:
            await message.answer("Iltimos, haqiqiy shaxsiy hisob raqamini yuboring")


@dp.message_handler(commands=['help'])
async def admin_help(message: Message):
    user_id = message.from_user.id
    # if user_id in boss:
    await message.reply(
        "/id - пришлет вам ваш телеграмм id\n/register_admin - зарегистрирует админа\n/delete_admin - если напишет сам то удалит себя а если Джахонгир ака то после ввода его id\n/delete - тоже самое, только юзеров\n/sendall- отправит всем что вы напишите кто хотяб просто когда либо нажимал /start\n/send_branch - отправит рассылку на филиал на который вы укажите\n/get_user - вытащит все о юзере из базы данных (надо ввести его Id)\n/get_admin - работает так же как и get_user только с админами")
    # else:
    #     await message.answer('error 404')


@dp.message_handler(content_types=['contact'])
async def contact_id(message: Message):
    conatctid = message.contact.user_id
    if message.from_user.id in boss:
        await message.answer(f'{conatctid}')


@dp.message_handler(regexp='Клиент|Haridor')
async def client_reg(message: Message):
    user_name = message.from_user.username
    print(user_name)
    # chat_id = message.chat
    user_id = message.from_user.id
    name = message.from_user.full_name
    ru = 'ru'
    uz = 'uz'
    if message.text == 'Клиент':
        register_client_lang(user_id, name, ru, user_name)
        await message.answer(
            "Уважаемый клиент, чтобы воспользоваться услугами MyHelper, нам необходимо пройти небольшую регистрацию.")
        await message.answer("Начинаем малую регистрацию,\nпришлите свое имя", reply_markup=generate_name(name))
        await ClientsGroup.name.set()
    else:
        register_client_lang(user_id, name, uz, user_name)
        await message.answer("Hurmatli mijoz, MyHelper xizmatlaridan foydalanish uchun kichik ro'yxatdan o'tamiz.")
        await message.answer("Biz kichik ro'yxatga olishni boshlaymiz,\nismingizni yuboring",
                             reply_markup=generate_name(name))
        await ClientsGroup.name.set()


@dp.message_handler(state=ClientsGroup.name)
async def client_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_client_lang(user_id)
    print('uuu')
    async with state.proxy() as data:
        name = data['name'] = message.text
    if lang == ru:
        await message.answer(f'{name} теперь отправьте пожалуйуста ваш номер',
                             reply_markup=generate_phone("Russian 🇷🇺"))
        await ClientsGroup.next()
    elif lang == uz:
        await message.answer(f'{message.text} endi nomerizni yuboring', reply_markup=generate_phone('Özbekcha 🇺🇿'))
        await ClientsGroup.next()


@dp.message_handler(state=ClientsGroup.contact, content_types=['contact'])
async def reg_phone(message: Message, state: FSMContext):
    user_id = message.from_user.id
    async with state.proxy() as data:
        phone = data['contact'] = message.contact.phone_number
        name = data['name']
        update_client_data(name, user_id, phone)
        lang = get_client_lang(user_id)
    if lang == ru:
        await message.answer(
            f'{message.text} наша минни регистрация прошла успешно теперь можете пользоваться услугами MyHelper',
            reply_markup=generate_main_menu("Russian 🇷🇺", 'client'))
        await ClientsGroup.next()
    elif lang == uz:
        await message.answer(
            f"{message.text} bizning minnie ro'yxatdan o'tishimiz muvaffaqiyatli o'tdi, endi siz MyHelper xizmatlaridan foydalanishingiz mumkin ",
            reply_markup=generate_main_menu('Özbekcha 🇺🇿', 'client'))
        await ClientsGroup.next()


# @dp.message_handler(commands=['location'], content_types='location')
# async def location(message: Message):
#     user_id = message.from_user.id
#     latitude = message.location.latitude
#     longitude = message.location.longitude


executor.start_polling(dp)
