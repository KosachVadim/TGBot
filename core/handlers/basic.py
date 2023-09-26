from aiogram import  Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from core.utils.statesform import StepsForm
from core.utils.utils import get_vacancies
import core.keyboards.reply as kb
from core.keyboards.reply import (
    get_kb_countries,
    get_kb_cities,
    get_kb_specializations_filter,
    get_kb_specializations,
    get_kb_specializations_filter_by_country
)

router = Router()

# Глобальные переменные для отслеживания текущей страницы и блоков вакансий
current_index = 0
vacancy_blocks = ""

# Обработчик команды /start
@router.message(F.text == '/start')
async def get_start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}, ты можешь узнать информацию о моей работе или же приступить к поиску нажав на конпоку "Вакансии"', reply_markup=kb.main)

# Обработчик команды "Вакансии"
@router.message(F.text == 'Вакансии')
async def bt_vacancy(message: Message):
    await message.answer(f'Выберите Страну, просмотор всех вакансий или же можете пропустить выбор страны и города и перейти сразу к выбору специализации нажав на кнопку', reply_markup=kb.country)

# Обработчик команды "Страна"
@router.message(F.text == 'Страна')
async def bt_country(message: Message, state: FSMContext):
    await message.answer(f'Выберите страну', reply_markup=get_kb_countries())
    await state.set_state(StepsForm.GET_COUNTRY)

# Обработчик команды "Специализация"
@router.message(F.text == 'Специализация')
async def bt_specialization(message: Message, state: FSMContext):
    await message.answer(f'Выберите специализацию', reply_markup=get_kb_specializations())
    await state.set_state(StepsForm.GET_SPECIALIZATION)

# Обработчик команды "Все вакансии"
@router.message(F.text == 'Все вакансии')
async def all_vacancies(message: Message, state: FSMContext):
    global vacancy_blocks
    vacancy_blocks = get_vacancies()
    global current_index
    current_index = 0

    if vacancy_blocks:
        await message.answer("Вакансии:", reply_markup=kb.vacancy)
        await send_vacancies(message, state)
    else:
        await message.answer("По вашему запросу ничего не найдено.")



# Обработчик состояния выбора города
@router.message(StepsForm.GET_COUNTRY)
async def bt_city(message: Message, state: FSMContext):
    if message.text == 'Специализация':
        await bt_specialization(message, state)
    else:
        await message.answer(f'Выберите город или Не важно', reply_markup=get_kb_cities(message.text))
        await state.update_data(country=message.text)
        await state.set_state(StepsForm.GET_CITY)

# Обработчик состояния выбора фильтрации специализации
@router.message(StepsForm.GET_CITY)
async def bt_specialization_filter(message: Message, state: FSMContext):
    if message.text == 'Специализация':
        await bt_specialization(message, state)
    else:
        if message.text == 'Не важно':
            context_data = await state.get_data()
            country_name = context_data.get('country')
            await message.answer(f'Выберите специализацию или выберите Не важно', reply_markup=get_kb_specializations_filter_by_country(country_name))
        else:
            await message.answer(f'Выберите специализацию или выберите Не важно', reply_markup=get_kb_specializations_filter(message.text))
            await state.update_data(city=message.text)
        await state.set_state(StepsForm.GET_SPECIALIZATION)

# Обработчик состояния выбора специализации
@router.message(StepsForm.GET_SPECIALIZATION)
async def bt_vacancy(message: Message, state: FSMContext):
    context_data = await state.get_data()
    country, city = context_data.get('country'), context_data.get('city')
    specialization = message.text
    await state.clear()

    global vacancy_blocks
    #vacancy_blocks = get_vacancies_filter(country, city, specialization)
    vacancy_blocks = get_vacancies(country, city, specialization)

    global current_index
    current_index = 0

    await message.answer(f'Вакансии : {specialization}', reply_markup=kb.vacancy)
    await send_vacancies(message, state)

# Обработчик команды "Просмотреть ещё"
@router.message(F.text == 'Просмотреть ещё')
async def bt_cont(message: Message, state: FSMContext):
    global current_index
    global vacancy_blocks

    current_index += 5

    await send_vacancies(message, state)

# Функция для отправки блоков вакансий
async def send_vacancies(message: Message, state: FSMContext):
    global current_index
    global vacancy_blocks

    if current_index >= len(vacancy_blocks):
        await message.answer("Вакансии закончились.")
        return

    for i in range(current_index, min(current_index + 5, len(vacancy_blocks))):
        await message.answer(f'Вакансия {i + 1}:\n{vacancy_blocks[i]}', reply_markup=kb.vacancy)

    if current_index < len(vacancy_blocks):
        await message.answer("Для продолжения нажмите 'Просмотреть ещё'", reply_markup=kb.vacancy)

# Обработчик команды "Назад в меню"
@router.message(F.text == 'Назад в меню')
async def restart_bot(message: Message):
    await get_start(message)

# Обработчик неизвестных команд
@router.message()
async def answer(message: Message):
    await message.reply('Я тебя не понимаю')
