from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import BOT_TOKEN, GROUP_CHAT_ID

bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

class Form(StatesGroup):
    city = State()
    name = State()
    debt = State()
    payment = State()
    overdue = State()
    income = State()
    credit = State()
    property = State()
    custom_property = State()
    phone = State()

@dp.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="Получить консультацию")],
        [KeyboardButton(text="О компании")],
        [KeyboardButton(text="Наши офисы")]
    ])
    await message.answer("Добрый день! Какую информацию Вы хотите получить?", reply_markup=keyboard)

@dp.message(F.text == "О компании")
async def about_company(message: Message):
    await message.answer("Подробнее о нас: https://avers-34.ru/")

@dp.message(F.text == "Наши офисы")
async def office_info(message: Message):
    await message.answer("Наш офис: https://yandex.ru/maps/org/yuk_avers/94070841340/?ll=44.468825%2C48.723016&z=16")

@dp.message(F.text == "Получить консультацию")
async def consultation_start(message: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="Волгоград")],
        [KeyboardButton(text="Краснодар")],
        [KeyboardButton(text="Невинномысск")],
        [KeyboardButton(text="Михайловка")]
    ])
    await message.answer("Выберите ваш город:", reply_markup=keyboard)
    await state.set_state(Form.city)

@dp.message(Form.city)
async def get_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Введите Ваше ФИО:")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="менее 300 000")],
        [KeyboardButton(text="Более 300 000")],
        [KeyboardButton(text="Более 500 000")],
        [KeyboardButton(text="Более 1 000 000")]
    ])
    await message.answer("Сумма Вашего долга:", reply_markup=keyboard)
    await state.set_state(Form.debt)

@dp.message(Form.debt)
async def get_debt(message: Message, state: FSMContext):
    await state.update_data(debt=message.text)
    await message.answer("Сколько составляет Ваш ежемесячный платеж?")
    await state.set_state(Form.payment)

@dp.message(Form.payment)
async def get_payment(message: Message, state: FSMContext):
    await state.update_data(payment=message.text)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="Да")],
        [KeyboardButton(text="Нет")]
    ])
    await message.answer("Были ли у Вас просрочка платежей?", reply_markup=keyboard)
    await state.set_state(Form.overdue)

@dp.message(Form.overdue)
async def get_overdue(message: Message, state: FSMContext):
    await state.update_data(overdue=message.text)
    await message.answer("Сколько составляет Ваш ежемесячный официальный доход?")
    await state.set_state(Form.income)

@dp.message(Form.income)
async def get_income(message: Message, state: FSMContext):
    await state.update_data(income=message.text)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="Да")],
        [KeyboardButton(text="Нет")]
    ])
    await message.answer("Есть ли у Вас Автокредит или Ипотека?", reply_markup=keyboard)
    await state.set_state(Form.credit)

@dp.message(Form.credit)
async def get_credit(message: Message, state: FSMContext):
    await state.update_data(credit=message.text)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="Есть только жилье")],
        [KeyboardButton(text="Есть Авто")],
        [KeyboardButton(text="Есть иное имущество")],
        [KeyboardButton(text="Перечислить самому")]
    ])
    await message.answer("Есть ли у Вас имущество?", reply_markup=keyboard)
    await state.set_state(Form.property)

@dp.message(Form.property)
async def get_property(message: Message, state: FSMContext):
    if message.text == "Перечислить самому":
        await message.answer("Перечислите имущество через запятую")
        await state.set_state(Form.custom_property)
    else:
        await state.update_data(property=message.text)
        await message.answer("Введите Ваш номер телефона в формате +7...")
        await state.set_state(Form.phone)

@dp.message(Form.custom_property)
async def get_custom_property(message: Message, state: FSMContext):
    await state.update_data(property=message.text)
    await message.answer("Введите Ваш номер телефона в формате +7...")
    await state.set_state(Form.phone)

@dp.message(Form.phone)
async def get_phone(message: Message, state: FSMContext):
    if not message.text.startswith("+7"):
        await message.answer("Пожалуйста, введите номер в формате +7...")
        return
    await state.update_data(phone=message.text)
    data = await state.get_data()

    text = (
        f"<b>Новая заявка на консультацию</b>

"
        f"📍 Город: {data['city']}
"
        f"👤 ФИО: {data['name']}
"
        f"💰 Долг: {data['debt']}
"
        f"📆 Платеж: {data['payment']}
"
        f"⏰ Просрочка: {data['overdue']}
"
        f"💸 Доход: {data['income']}
"
        f"🏦 Кредит/Ипотека: {data['credit']}
"
        f"🏠 Имущество: {data['property']}
"
        f"📞 Телефон: {data['phone']}"
    )

    await bot.send_message(GROUP_CHAT_ID, text)
    await message.answer("Отлично! Мы можем Вам помочь, ожидайте звонка.")
    await state.clear()
