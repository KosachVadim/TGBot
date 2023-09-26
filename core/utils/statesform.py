from aiogram.fsm.state import StatesGroup, State

class StepsForm(StatesGroup):
    GET_COUNTRY = State()
    GET_CITY = State()
    GET_SPECIALIZATION = State()
    GET_VACANCY = State()