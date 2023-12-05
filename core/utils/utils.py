# Импорт необходимых модулей
import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.database.models import Base, Country, Vacancy, User, Resume
import json


# Создание соединения с базой данных
engine = create_engine("postgresql+psycopg2://postgres:1234@localhost/tg_test")


# Создание таблиц в базе данных (если они ещё не существуют)
Base.metadata.create_all(engine)

# Создание сессии для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()

lang_code = "ru"

async def get_language_code(language_name):
    file_path = 'core/locales/languages.json'

    # Проверяем, существует ли файл
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден.")
        return None

    with open(file_path, 'r', encoding='utf-8') as file:
        language_mapping = json.load(file)

    # Проверяем, есть ли такой язык в словаре
    if language_name in language_mapping:
        global lang_code
        lang_code = language_mapping[language_name]

    else:
        return None  # Возвращаем None, если язык не найден

def get_text(key):
    try:
        with open(f'core/locales/{lang_code}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data.get(key, f'[{key}] not found for language {lang_code}')
    except FileNotFoundError:
        return f'Language file not found for {lang_code}'

def get_buttons_data_emoji(key, number):
    try:
        with open(f'core/locales/{lang_code}.json', 'r', encoding='utf-8') as file:
            buttons_data = json.load(file)

        return buttons_data.get(key, [{}])[number].get("text").rsplit(' ', 1)[-1]
    except FileNotFoundError:
        # Обработка ошибки, если файл не найден
        return {}

def get_buttons_data(key, number: int):
    try:
        with open(f'core/locales/{lang_code}.json', 'r', encoding='utf-8') as file:
            buttons_data = json.load(file)
        return buttons_data.get(key, [{}])[number].get("text")
    except FileNotFoundError:
        # Обработка ошибки, если файл не найден
        return {}

def get_buttons_data_kb(key):
    try:
        with open(f'core/locales/{lang_code}.json', 'r', encoding='utf-8') as file:
            buttons_data = json.load(file)
        return buttons_data.get(key, [])
    except FileNotFoundError:
        # Обработка ошибки, если файл не найден
        return {}


# Функция для проверки в ДБ

def get_all_countries_from_file():
    with open(f'core/locales/ru.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    countries = {}
    for country_info in json_data.get("countries", []):
        # Извлекаем текст страны из JSON-объекта
        country_text = country_info.get("text", "")

        # Извлекаем флаг и название страны из текста
        country_parts = country_text.split()
        country_flag = country_parts[-1]
        country_name = ' '.join(country_parts[:-1])

        countries[country_flag] = country_name

    return countries

def check_name_in_db(name):
    existing_user = session.query(User).filter(User.name == name).first()
    if existing_user:
        return
    else:
        return False

async def check_in_database_flag(flag):
    all_countries = get_all_countries_from_file()
    # Ищем флаг в списке стран
    if flag in all_countries:
        global db_country_name
        db_country_name = all_countries[flag]
    result = session.query(Vacancy).join(Country).filter(Country.name == db_country_name).first()
    return result is None

# Функция для получения списка вакансий с учетом фильтров
def get_vacancies():
    global db_country_name
    vacancies = session.query(Vacancy).filter(Vacancy.country.has(Country.name == db_country_name)).all()

    # Генерация блоков вакансий
    vacancy_blocks = []

    for vacancy in vacancies:
        vacancy_block = f'{get_text("title")}: #{vacancy.unique_id}\n{get_text("city")}: {vacancy.city}\n{get_text("language")}: {vacancy.language}\n{get_text("specialization")}: {vacancy.specialization}\n{get_text("salary")}: {vacancy.salary}\n{get_text("manager")}: {vacancy.manager_account}'

        # Создайте инлайн кнопку для каждой вакансии
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=get_buttons_data("details_kb", 1), callback_data=f"details_{vacancy.id}")]
        ])


        vacancy_blocks.append((vacancy_block, keyboard))

    return vacancy_blocks

def get_details(vacancy_id):
    vacancy = session.query(Vacancy).filter_by(id=vacancy_id).first()


    details_text = (
        f'{get_text("title")}: #{vacancy.unique_id}\n{get_text("city")}: {vacancy.city}\n{get_text("language")}: {vacancy.language}\n'
        f'{get_text("specialization")}: {vacancy.specialization}\n{get_text("salary")}: {vacancy.salary}\n{get_text("manager")}: {vacancy.manager_account}\n\n'
        f'{get_text("for_whom")}: 👥\n{vacancy.for_whom}\n\n{get_text("schedule")}:\n{vacancy.chart}\n\n{get_text("housing")}:\n{vacancy.housing}\n\n'
        f'{get_text("work_clothes")}:\n{vacancy.work_clothes}\n\n{get_text("getting_to_work")}:\n{vacancy.getting_to_work}\n\n'
        f'{get_text("responsibilities")}:\n{vacancy.responsibilities}\n\n{get_text("requirements")}:\n{vacancy.requirements}'
    )


    max_length = 4096
    details_parts = [details_text[i:i+max_length] for i in range(0, len(details_text), max_length)]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_buttons_data("info", 1), url='https://t.me/AlekseiDeshko')]
    ])

    return details_parts, keyboard

async def add_user(name):
    user = User(name=name)
    session.add(user)
    session.commit()


async def add_resume(name, nationality, job_title, duration_years, description):
    user = session.query(User).filter_by(name=name).first()
    if user:
        resume = Resume(user_id=user.id, nationality=nationality, experience_job_title=job_title, experience_duration_years=duration_years, experience_description=description)
        session.add(resume)
        session.commit()
        return resume
    else:
        return None



# Создание клавиатур


# Закрытие сессии
session.close()
