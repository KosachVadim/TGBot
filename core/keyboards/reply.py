from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from core.utils.utils import get_countries, get_cities, get_specializations
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



def get_kb_specializations(country_name=None, city_name=None):
    kb_buld = ReplyKeyboardBuilder()

    if country_name is not None:
        unique_specialization = set(get_specializations(country_name))
    elif city_name is not None:
        unique_specialization = set(get_specializations(None, city_name))
    else:
        unique_specialization = set(get_specializations())


    for specialization in unique_specialization:
        kb_buld.button(text=specialization)

    kb_buld.button(text='Не важно')
    kb_buld.adjust(1)

    return kb_buld.as_markup(resize_keyboard=True)


