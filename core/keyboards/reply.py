from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import json
from core.utils.utils import get_buttons_data_kb, get_buttons_data
with open(f'core/locales/default.json', 'r', encoding='utf-8') as file:
    default_data = json.load(file)



language_kb_texts = [button["text"] for button in default_data.get("language_kb", [])]

language = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=button_text) for button_text in language_kb_texts]],
    resize_keyboard=True
)

def create_main_kb():
    main_kb_texts = [button["text"] for button in get_buttons_data_kb("main_kb")]
    main = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=button_text) for button_text in main_kb_texts]],
        resize_keyboard=True
    )
    return main

def create_vacancy_kb():
    vacancy_kb_texts = [button["text"] for button in get_buttons_data_kb("vacancy_kb")]
    vacancy = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=button_text) for button_text in vacancy_kb_texts]],
        resize_keyboard=True
    )
    return vacancy

def create_details_kb():
    details_kb_texts = get_buttons_data("details_kb", 0)
    details = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=details_kb_texts)]], resize_keyboard=True)
    return details

def create_countries_kb():
    countries_kb_texts = [button["text"] for button in get_buttons_data_kb("countries")]
    countries = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=country_text)] for country_text in countries_kb_texts],
        resize_keyboard=True
    )
    return countries

def create_info_kb():
    info_text = get_buttons_data("info", 1)
    info_url = 'https://t.me/AlekseiDeshko'
    info = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=info_text, url=info_url)]])
    return info

def create_search_kb():
    search_vacancy_text = get_buttons_data("info", 0)
    search_vacancy = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=search_vacancy_text)]], resize_keyboard=True)
    return search_vacancy


