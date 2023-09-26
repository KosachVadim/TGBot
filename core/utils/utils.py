# Импорт необходимых модулей
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.database.models import Base, Country, Vacancy

# Путь к файлу базы данных SQLite
PATH = 'C:\\Users\\Vadim\\PycharmProjects\\Vacancy\\db.sqlite3'

# Создание соединения с базой данных
engine = create_engine(f'sqlite:///{PATH}')

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
def get_specialization():
    specialization = session.query(Vacancy).all()
    specializations = [vacancy.specialization for vacancy in specialization]
    return specializations

# Функция для получения списка специализаций по имени города
def get_specialization_filter_by_city(city_name):
    specialization = session.query(Vacancy).filter_by(city=city_name).all()

    specializations = [vacancy.specialization for vacancy in specialization]
    return specializations

# Функция для получения списка специализаций по имени страны
def get_specialization_by_country(country_name):
    specialization = session.query(Vacancy).filter(Vacancy.country.has(Country.name == country_name)).all()

    specializations = [vacancy.specialization for vacancy in specialization]
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
    all_vacancy = ""
    for i, vacancy in enumerate(vacancies):
        vacancy_block = f'Specialization: {vacancy.specialization}\nDescription: {vacancy.description}\nSalary: {vacancy.salary_range}\nManager account: {vacancy.manager_account}\nProfit type: {vacancy.profit_type}\nProfit amount: {vacancy.profit_amount}\nWorking conditions: {vacancy.working_conditions}'

        # Добавление блока вакансии в результат
        all_vacancy += vacancy_block

        # Если это последний блок вакансии, удалите символы '\n\n' в конце
        if i == len(vacancies) - 1:
            all_vacancy = all_vacancy.rstrip()

        # Добавьте символы '\n\n' между блоками вакансий (кроме последнего)
        else:
            all_vacancy += '\n\n'

    return all_vacancy.split('\n\n')

# Закрытие сессии
session.close()
