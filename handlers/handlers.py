from telegram import KeyboardButton, ParseMode, ReplyKeyboardMarkup, Update
from telegram.error import BadRequest, TelegramError, Unauthorized
from telegram.ext import CallbackContext

from loads.response_data import response_data
from utils.format_long_name import format_long_name
from utils.start_role import start_role
from utils.insert_name import insert_name
from utils.long_message import long_message


def handle_errors(update: Update, context: CallbackContext, error: Exception) -> None:

    if isinstance(error, BadRequest):
        update.message.reply_text("Ошибка: пользователь не найден")
    elif isinstance(error, Unauthorized):
        update.message.reply_text("Ошибка: бот заблокирован пользователем")
    else:
        update.message.reply_text("Произошла неизвестная ошибка")


def handle_start(update: Update, context: CallbackContext) -> None:
    username = update.effective_user.username
    role = start_role(username)
    keyboard = [
        [KeyboardButton('Показать менторов')],
        [KeyboardButton('Показать открытки'), KeyboardButton('Показать праздники')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    welcome_message = (
        f"{role}\n\nПриветствует тебя dvmn бот.\n\n"
        "Это бот, который поздравляет менторов dvmn с праздниками."
    )
    update.message.reply_text(welcome_message, reply_markup=reply_markup)


def handle_holidays(update: Update, context: CallbackContext) -> None:
    holidays_data = response_data('holidays')

    if isinstance(holidays_data, list):
        update.message.reply_text("Произошла ошибка при получении данных.")
    else:
        holidays = holidays_data.get('holidays', [])
        if holidays:
            text = "*Список праздников:*\n\n"
            for i, holiday in enumerate(holidays, start=1):
                text += f"{i}. *{holiday.get('name')}*:  {holiday.get('name_ru')}\n"
            messages = long_message(text)
            for message in messages:
                update.message.reply_text(text=message, parse_mode=ParseMode.MARKDOWN)
            # хранения праздников
            context.user_data['holidays'] = holidays
            context.user_data['awaiting_holiday'] = True
        else:
            update.message.reply_text("Список праздников пуст.\nПовторите попытку позже.")


def handle_mentors(update: Update, context: CallbackContext) -> None:
    mentors_data = response_data('mentors')
    if isinstance(mentors_data, list):
        update.message.reply_text("Произошла ошибка при получении данных.")
    else:
        mentors = mentors_data.get('mentors', [])
        if mentors:
            text = "🌟 *Наши менторы:*\n\n"
            for i, mentor in enumerate(mentors, start=1):
                full_name = mentor.get('name')
                formatted_name = format_long_name(full_name)
                tg_id = mentor.get('tg_username')
                text += f"✨ *{i}.* {formatted_name} ([{tg_id}](https://t.me/{tg_id[1:]}))\n"
            # хранения менторов
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


def handle_poscards(update: Update, context: CallbackContext) -> None:
    cards_data = response_data('postcards')
    if isinstance(cards_data, list):
        update.message.reply_text("Произошла ошибка при получении данных.")
    else:
        cards = cards_data.get('postcards', [])
        if cards:
            text = "*Выберите номер открытки для отправки:*\n\n"
            for i, card in enumerate(cards, start=1):
                text += f"{i}. *{card.get('name_ru')}* {card.get('body')}\n"
            messages = long_message(text)
            for message in messages:
                update.message.reply_text(text=message, parse_mode=ParseMode.MARKDOWN)
            # хранение открыток
            context.user_data['available_cards'] = cards
            context.user_data['awaiting_card'] = True
        else:
            update.message.reply_text("Список открыток пуст.\nПовторите попытку позже.")


def handle_mentor_choice(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    if message_text.isdigit():
        index = int(message_text) - 1
        mentors = context.user_data.get('mentors', [])
        if 0 <= index < len(mentors):
            context.user_data['selected_mentor'] = mentors[index]
            handle_poscards(update, context)
        else:
            update.message.reply_text("Неверный номер ментора.")
        context.user_data['awaiting_mentor'] = False
    else:
        update.message.reply_text("Пожалуйста, введите номер ментора.")


def handle_card_choice(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    selected_card = None

    if message_text.isdigit():
        index = int(message_text) - 1
        cards = context.user_data.get('available_cards')
        if cards and 0 <= index < len(cards):
            selected_card = cards[index]

            selected_mentor = context.user_data.get('selected_mentor')
            if selected_mentor:
                try:
                    first_name = selected_mentor['name']['first']
                    text = insert_name(selected_card['body'], first_name)
                    context.bot.send_message(
                        chat_id=selected_mentor['tg_chat_id'],
                        text=text,
                        parse_mode=ParseMode.MARKDOWN
                    )
                    update.message.reply_text("Открытка отправлена!")
                except TelegramError as e:
                    handle_errors(update, context, e)
            else:
                update.message.reply_text("Ментор не выбран.")
        else:
            update.message.reply_text("Неверный номер открытки.")
    else:
        update.message.reply_text("Пожалуйста, введите номер открытки.")
    context.user_data['awaiting_card'] = False


def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text

    if text == 'Показать менторов':
        handle_mentors(update, context)
    elif text == 'Показать открытки':
        handle_poscards(update, context)
    elif text == 'Показать праздники':
        handle_holidays(update, context)
    elif context.user_data.get('awaiting_mentor'):
        handle_mentor_choice(update, context)
    elif context.user_data.get('awaiting_card'):
        handle_card_choice(update, context)
    else:
        handle_start(update, context)
