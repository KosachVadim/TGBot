from aiogram.fsm.state import StatesGroup, State

class StepsForm(StatesGroup):
    GET_COUNTRY = State()
    GET_NAME = State()
    LANGUAGE = State()
    GET_NATIONALITY = State()
    GET_EXPERIENCE_JOB_TITLE = State()
    GET_EXPERIENCE_DURATION_YEARS = State()
    GET_EXPERIENCE_DESCRIPTION = State()

