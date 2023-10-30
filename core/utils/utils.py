# Импорт необходимых модулей
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.database.models import Base, Country, Vacancy, Applicant


# Создание соединения с базой данных
engine = create_engine("postgresql+psycopg2://postgres:1234@localhost/tg_bd")


# Создание таблиц в базе данных (если они ещё не существуют)
Base.metadata.create_all(engine)

# Создание сессии для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Функция для получения списка уникальных стран
def get_countries():
    distinct_countries = session.query(Country). \
        join(Vacancy, Country.id == Vacancy.country_id). \
        distinct().all()

    countries = [country.name for country in distinct_countries]
    return countries

# Функция для получения списка городов по имени страны
def get_cities(country_name):
    # Найдите страну по её имени
    country = session.query(Country).filter_by(name=country_name).first()

    if country:
        # Используйте отношение "vacancies" для получения городов
        cities = [vacancy.city for vacancy in country.vacancies]
        return cities
    else:
        return []


# Функция для получения списка специализаций

def get_specializations(country_name=None, city_name=None):
    query = session.query(Vacancy)

    if country_name:
        query = query.filter(Vacancy.country.has(Country.name == country_name))

    if city_name:
        query = query.filter_by(city=city_name)

    specializations = query.all()
    specializations = [vacancy.specialization for vacancy in specializations]
    return specializations

# Функция для получения списка вакансий с учетом фильтров
def get_vacancies(country_name=None, city_name=None, specialization_name=None):
    query = session.query(Vacancy)

    if country_name:
        query = query.filter(Vacancy.country.has(Country.name == country_name))

    if city_name:
        query = query.filter_by(city=city_name)

    if specialization_name and specialization_name != 'Не важно':
        query = query.filter_by(specialization=specialization_name)

    vacancies = query.all()


    # Генерация блоков вакансий
    vacancy_blocks = []

    for vacancy in vacancies:
        vacancy_block = f'Specialization: {vacancy.specialization}\nDescription: {vacancy.description}\nSalary: {vacancy.salary_range}\nManager account: {vacancy.manager_account}\nProfit type: {vacancy.profit_type}\nProfit amount: {vacancy.profit_amount}\nWorking conditions: {vacancy.working_conditions}'

        # Создайте инлайн кнопку для каждой вакансии
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Ответить на заявку", callback_data=f"vacancy_{vacancy.id}")
            ]
        ])

        # Добавьте текст блока вакансии и клавиатуру к результатам
        vacancy_blocks.append((vacancy_block, keyboard))

    return vacancy_blocks


def fill_data_in_database(vacancy_id, fio, number):
    if fio is not None and number is not None:
        vacancy = Applicant(vacancy_id=vacancy_id, name=fio, phone=number)
        session.add(vacancy)
        session.commit()


# Закрытие сессии
session.close()
