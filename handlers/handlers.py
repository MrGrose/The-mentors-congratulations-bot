from telegram import KeyboardButton, ParseMode, ReplyKeyboardMarkup, Update
from telegram.error import BadRequest, TelegramError, Unauthorized
from telegram.ext import CallbackContext

from libs.api_client.api_requests import (Mentor, Postcard,
                                          ResponseFormatError, ServerError,
                                          response_mentors, response_postcards)
from utils.format_long_name import format_long_name
from utils.insert_name import insert_name
from utils.long_message import long_message
from utils.start_role import start_role


def handle_errors(update: Update, context: CallbackContext, error: Exception) -> None:
    if isinstance(error, BadRequest):
        update.message.reply_text(
            "Ошибка: пользователь не найден. "
            "Проверьте данные и попробуйте снова."
        )
    elif isinstance(error, Unauthorized):
        update.message.reply_text("Ошибка: бот заблокирован пользователем")
    elif isinstance(error, ResponseFormatError):
        update.message.reply_text(
            "Ошибка получения формата данных. "
            "Проверьте, что данные передаются в правильном формате."
        )
    elif isinstance(error, ServerError):
        update.message.reply_text(
            "Ошибка на стороне сервера при получении данных. "
            "Попробуйте повторить запрос позже."
        )
    else:
        update.message.reply_text(
            "Произошла неизвестная ошибка."
            "Пожалуйста, обратитесь к разработчикам за помощью."
        )


def handle_start(update: Update, context: CallbackContext) -> None:
    try:
        user = update.effective_user
        if user is None:
            update.message.reply_text("Ошибка: пользователь не найден")
            return

        username = user.username
        role = start_role(username)
        keyboard = [
            [KeyboardButton('Показать менторов'),
             KeyboardButton('Показать открытки')]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        welcome_message = (
            f"{role}\n\nПриветствует тебя dvmn бот.\n\n"
            "Это бот, который поздравляет менторов dvmn с праздниками."
        )
        update.message.reply_text(welcome_message, reply_markup=reply_markup)
    except Exception as error:
        handle_errors(update, context, error)


def handle_mentors(update: Update, context: CallbackContext, mentors: list[Mentor]) -> None:
    if context.user_data is None:
        context.user_data = {}

    if mentors:
        text = "\n".join([
            "🌟 *Наши менторы:*",
            *[
                f"✨ *{num}.* {format_long_name(mentor.name)} ([{mentor.tg_username}](https://t.me/{mentor.tg_username[1:]}))"
                for num, mentor in enumerate(mentors, start=1)
            ]
        ])
        context.user_data['mentors'] = mentors
        context.user_data['awaiting_mentor'] = True
        update.message.reply_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
        update.message.reply_text(
            "*Введите номер ментора:*",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        update.message.reply_text("Список менторов пуст.\nПовторите попытку позже.")


def handle_postcards(update: Update, context: CallbackContext, cards: list[Postcard]) -> None:
    if context.user_data is None:
        context.user_data = {}

    if cards:
        text = "*Выберите номер открытки для отправки:*\n\n"
        for i, card in enumerate(cards, start=1):
            text += f"{i}. *{card.name_ru}* {card.body}\n"
        messages = long_message(text)
        for message in messages:
            update.message.reply_text(
                text=message,
                parse_mode=ParseMode.MARKDOWN
            )
        context.user_data['available_cards'] = cards
        context.user_data['awaiting_card'] = True
    else:
        update.message.reply_text("Список открыток пуст.\nПовторите попытку позже.")


def handle_mentor_choice(update: Update, context: CallbackContext) -> None:
    if context.user_data is None:
        context.user_data = {}

    message_text = update.message.text
    if message_text.isdigit():
        index = int(message_text) - 1
        mentors = context.user_data.get('mentors', [])
        if 0 <= index < len(mentors):
            context.user_data['selected_mentor'] = mentors[index]
            context.user_data['postcards_after_mentor'] = True
            handle_message(update, context)
        else:
            update.message.reply_text("Неверный номер ментора.")
        context.user_data['awaiting_mentor'] = False
    else:
        update.message.reply_text("Пожалуйста, введите номер ментора.")


def handle_card_choice(update: Update, context: CallbackContext) -> None:
    if context.user_data is None:
        context.user_data = {}

    message_text = update.message.text

    if not message_text.isdigit():
        update.message.reply_text("Пожалуйста, введите номер открытки.")
        return

    index = int(message_text) - 1
    cards = context.user_data.get('available_cards')

    if not cards or not (0 <= index < len(cards)):
        update.message.reply_text("Неверный номер открытки.")
        return

    selected_card = cards[index]
    selected_mentor = context.user_data.get('selected_mentor')

    if not selected_mentor:
        update.message.reply_text("Ментор не выбран.")
        return

    try:
        text = insert_name(selected_card.body, selected_mentor.name.first)
        context.bot.send_message(
            chat_id=selected_mentor.tg_chat_id,
            text=text,
            parse_mode=ParseMode.MARKDOWN
        )
        update.message.reply_text("Открытка отправлена!")
    except TelegramError as e:
        handle_errors(update, context, e)

    context.user_data['awaiting_card'] = False


def handle_show_mentors(update: Update, context: CallbackContext) -> None:
    mentors_data = response_mentors()
    handle_mentors(update, context, mentors_data)


def handle_show_postcards(update: Update, context: CallbackContext) -> None:
    cards_data = response_postcards()
    handle_postcards(update, context, cards_data)


def handle_message(update: Update, context: CallbackContext) -> None:
    try:
        if context.user_data is None:
            context.user_data = {}

        text = update.message.text
        if text == 'Показать менторов':
            handle_show_mentors(update, context)
        elif text == 'Показать открытки' or context.user_data.get(
                'postcards_after_mentor', False):
            handle_show_postcards(update, context)
            context.user_data['postcards_after_mentor'] = False
        elif context.user_data.get('awaiting_mentor', False):
            handle_mentor_choice(update, context)
        elif context.user_data.get('awaiting_card', False):
            handle_card_choice(update, context)
        else:
            handle_start(update, context)
    except Exception as error:
        handle_errors(update, context, error)
