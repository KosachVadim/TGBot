import json
from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.utils.statesform import StepsForm
from core.utils.utils import get_vacancies, check_in_database_flag, get_details, get_text, get_language_code, get_buttons_data_emoji, add_user, add_resume
import core.keyboards.reply as kb
from core.keyboards.reply import create_main_kb, create_details_kb, create_vacancy_kb, create_search_kb, create_countries_kb, create_info_kb

router = Router()
# Глобальные переменные для отслеживания текущей страницы и блоков вакансий
current_index = 0
vacancy_blocks = ""



with open(f'core/locales/default.json', 'r', encoding='utf-8') as file:
    default_data = json.load(file)


# Обработчик команды /start
@router.message(F.text == '/start')
async def get_start(message: Message, state: FSMContext):
    await message.answer(default_data.get("start_message"), reply_markup=kb.language)
    await state.set_state(StepsForm.LANGUAGE)

#Обработчик выбора языка
@router.message(StepsForm.LANGUAGE)
async def bt_language(message: Message, state: FSMContext):
    await get_language_code(message.text)
    await message.answer(get_text('choose_name'), reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(StepsForm.GET_NAME)


#Обработчик имени пользователя
@router.message(StepsForm.GET_NAME)
async def bt_name(message: Message, state: FSMContext):
    name = message.text
    await add_user(name)
    await state.clear()
    await state.update_data(name=name)
    await message.answer(get_text('continue'), reply_markup=create_main_kb())


@router.message(F.text.rsplit(' ', 1)[-1] == get_buttons_data_emoji("main_kb", 2))
async def bt_nationality_resume(message: Message, state: FSMContext):
    await message.answer(get_text('nationality'))
    await state.set_state(StepsForm.GET_NATIONALITY)
@router.message(StepsForm.GET_NATIONALITY)
async def bt_experience_job_title_resume(message: Message, state: FSMContext):
    await state.update_data(nationality=message.text)
    await message.answer(get_text('experience_job_title'))
    await state.set_state(StepsForm.GET_EXPERIENCE_JOB_TITLE)

@router.message(StepsForm.GET_EXPERIENCE_JOB_TITLE)
async def bt_experience_duration_years_resume(message: Message, state: FSMContext):
    await state.update_data(experience_job_title=message.text)
    await message.answer(get_text('experience_duration_years'))
    await state.set_state(StepsForm.GET_EXPERIENCE_DURATION_YEARS)

@router.message(StepsForm.GET_EXPERIENCE_DURATION_YEARS)
async def bt_experience_description_resume(message: Message, state: FSMContext):
    await state.update_data(experience_duration_years=message.text)
    await message.answer(get_text('experience_description'))
    await state.set_state(StepsForm.GET_EXPERIENCE_DESCRIPTION)

@router.message(StepsForm.GET_EXPERIENCE_DESCRIPTION)
async def bt_add_data_resume(message: Message, state: FSMContext):
    experience_description = message.text
    context_data = await state.get_data()
    name, nationality, experience_job_title, experience_duration_years = context_data.get('name'), context_data.get('nationality'), context_data.get('experience_job_title'), context_data.get('experience_duration_years')
    await add_resume(name, nationality, experience_job_title, experience_duration_years, experience_description)
    await message.answer(get_text('add_data'), reply_markup=create_main_kb())
    await state.clear()


# Обработчик команды "О боте"
@router.message(F.text.rsplit(' ', 1)[-1] == get_buttons_data_emoji("main_kb",0))
async def bt_info(message: Message):
    await message.answer(get_text('about_bot'), reply_markup=create_info_kb())
    await message.answer(get_text('choose_option'), reply_markup=create_search_kb())

# Обработчик команды "Вакансии"

@router.message(F.text.rsplit(' ', 1)[-1] == get_buttons_data_emoji("main_kb", 1))
async def bt_country(message: Message, state: FSMContext):
    await message.answer(get_text('search_vacancy'), reply_markup=create_countries_kb())
    await state.set_state(StepsForm.GET_COUNTRY)

# Обработчик команды "Страна"
@router.message(StepsForm.GET_COUNTRY)
async def bt_vacancy(message: Message, state: FSMContext):
    flag = message.text.split()[1]
    if await check_in_database_flag(flag) and flag != get_buttons_data_emoji("vacancy_kb", 1):
        await message.answer(get_text('no_vacancies'), reply_markup=create_countries_kb())
        return
    if flag == get_buttons_data_emoji("vacancy_kb", 1):
        await state.clear()
        await restart_bot(message)
        return
    global vacancy_blocks
    vacancy_blocks = get_vacancies()
    global current_index
    current_index = 0
    await state.clear()
    await message.answer(get_text('here_is_what_we_have'), reply_markup=create_vacancy_kb())
    await send_vacancies(message, state)


# Обработчик команды "Просмотреть ещё"
@router.message(F.text.rsplit(' ', 1)[-1] == get_buttons_data_emoji("vacancy_kb", 0))
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
        await message.answer(get_text('vacancies_finished'))
        return

    for i in range(current_index, min(current_index + 5, len(vacancy_blocks))):

        vacancy_block, keyboard = vacancy_blocks[i]
        await message.answer(f'{get_text("vacancy_prefix")} {i + 1}:\n{vacancy_block}', reply_markup=keyboard)


    if current_index < len(vacancy_blocks):
        await message.answer(get_text('view_more'), reply_markup=create_vacancy_kb())


@router.callback_query(F.data.startswith("details_"))
async def details(query: CallbackQuery):
    vacancy_id = int(query.data.split('_')[1])
    vacancy_block, keyboard = get_details(vacancy_id)


    for part in vacancy_block:
        await query.message.answer(part, reply_markup=keyboard)
    await query.message.answer(get_text('back'), reply_markup=create_details_kb())


@router.message(F.text.rsplit(' ', 1)[-1] == get_buttons_data_emoji("details_kb", 0))
async def restart_bot_vacancy(message: Message, state: FSMContext):
    await message.answer(get_text('here_is_what_we_have'), reply_markup=create_vacancy_kb())
    await send_vacancies(message, state)

# Обработчик команды "Назад в меню"
@router.message(F.text.rsplit(' ', 1)[-1] == get_buttons_data_emoji("vacancy_kb", 1))
async def restart_bot(message: Message):
    await message.answer(get_text('back_to_menu'), reply_markup=create_main_kb())

# Обработчик неизвестных команд
@router.message()
async def answer(message: Message):
    await message.reply(get_text('unknown_command'))
