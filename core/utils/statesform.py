from aiogram.fsm.state import StatesGroup, State

class StepsForm(StatesGroup):
    GET_COUNTRY = State()
    GET_CITY = State()
    GET_SPECIALIZATION = State()
<<<<<<< HEAD
    GET_VACANCY = State()
=======
    GET_VACANCY = State()
    GET_FIO = State()
    GET_NUMBER = State()
    GET_VACANCY_ID = State()
>>>>>>> 6302428 (new change2)
