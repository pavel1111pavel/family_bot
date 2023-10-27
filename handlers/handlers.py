from aiogram import F, Router, Dispatcher, types
from database import SessionLocal, Task, UserResponse, Category
from aiogram import Dispatcher
from aiogram import Dispatcher
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from sqlalchemy.orm import Session


router: Router = Router()

class FSMFillForm(StatesGroup):
    choose_or_input_category = State()
    fill_task = State()
    add_task_in_bd = State()
    choose_category = State()
    waiting_for_category_name = State()
    create_category = State()


@router.message(Command(commands=['command_1']), lambda message: message.text)
async def choose_or_input_category(message: Message, state: FSMContext):
    # Предложите пользователю выбрать или ввести категорию

    choose_button = InlineKeyboardButton(text="Выбрать категорию", callback_data="choose_category")
    markup = InlineKeyboardMarkup(inline_keyboard=[[choose_button]])

    await message.answer("Выберите действие:", reply_markup=markup)



@router.message(Command(commands=['command_3']), lambda message: message.text)
async def add_task(message: Message, state: FSMContext):
    # Получите сессию базы данных
    db = SessionLocal()

    categories = db.query(Category).all()

    # Если есть доступные категории, предложите пользователю выбрать или создать
    if not categories:

        await message.answer("У вас пока нет категорий для задач. Вы можете создать новую, написав ее название.")
        await message.answer("Пожалуйста, напишите название новой категории:")
        # Создайте кнопку "Создать новую категорию"
        await state.set_state(FSMFillForm.waiting_for_category_name)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"* 10)
    else:
        categories = db.query(Category).all()
        choose_button = [InlineKeyboardButton(text=category.name, callback_data=f"choose_category:{category.id}") for category in categories]
        markup = InlineKeyboardMarkup(inline_keyboard=[choose_button])

        await message.answer("Выберите действие:", reply_markup=markup)
    # Завершите состояние ожидания выбора категории
        await state.set_state(FSMFillForm.choose_category)