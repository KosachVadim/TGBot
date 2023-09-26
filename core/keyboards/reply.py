from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from core.utils.utils import get_countries, get_cities, get_specialization_filter_by_city, get_specialization, get_specialization_by_country
main_kb = [
    [KeyboardButton(text='О боте'),
     KeyboardButton(text='Вакансии')]

]

country_kb = [

    [KeyboardButton(text='Страна'),
     KeyboardButton(text='Специализация'),
     KeyboardButton(text='Все вакансии')]

]

vacancy_kb = [

    [KeyboardButton(text='Просмотреть ещё'),
     KeyboardButton(text='Назад в меню')]

]

vacancy = ReplyKeyboardMarkup(keyboard=vacancy_kb, resize_keyboard=True)
main = ReplyKeyboardMarkup(keyboard=main_kb, resize_keyboard=True)
country = ReplyKeyboardMarkup(keyboard=country_kb, resize_keyboard=True)


def get_kb_countries():
    kb_buld = ReplyKeyboardBuilder()
    for country in get_countries():
        kb_buld.button(text=country)
    kb_buld.adjust(1)
    return kb_buld.as_markup(resize_keyboard=True)

def get_kb_cities(country_name):
    kb_buld = ReplyKeyboardBuilder()
    unique_cities = set(get_cities(country_name))  # Создаем множество уникальных городов
    for city in unique_cities:
        kb_buld.button(text=city)

    kb_buld.button(text='Не важно')
    kb_buld.adjust(1)
    return kb_buld.as_markup(resize_keyboard=True)


def get_kb_specializations():
    kb_buld = ReplyKeyboardBuilder()
    unique_specialization = set(get_specialization())
    for specialization in unique_specialization:
        kb_buld.button(text=specialization)
    kb_buld.adjust(1)
    return kb_buld.as_markup(resize_keyboard=True)

def get_kb_specializations_filter(city_name):
    kb_buld = ReplyKeyboardBuilder()
    unique_specialization = set(get_specialization_filter_by_city(city_name))
    for specialization in unique_specialization:
        kb_buld.button(text=specialization)

    kb_buld.button(text='Не важно')
    kb_buld.adjust(1)
    return kb_buld.as_markup(resize_keyboard=True)

def get_kb_specializations_filter_by_country(country_name):
    kb_buld = ReplyKeyboardBuilder()
    unique_specialization = set(get_specialization_by_country(country_name))
    for specialization in unique_specialization:
        kb_buld.button(text=specialization)

    kb_buld.button(text='Не важно')
    kb_buld.adjust(1)
    return kb_buld.as_markup(resize_keyboard=True)