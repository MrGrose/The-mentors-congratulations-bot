import logging

from telegram import (
    KeyboardButton,
    ParseMode,
    ReplyKeyboardMarkup,
    Update
)
from telegram.error import (
    BadRequest,
    TelegramError,
    Unauthorized
)
from telegram.ext import CallbackContext

from libs.api_client.api_requests import (
    ResponseFormatError,
    ServerError,
    get_mentors,
    get_postcards
)
from libs.utils import (
    format_long_name,
    insert_name,
    message_splitter,
    start_role
)


logger = logging.getLogger(__name__)


def handle_errors(update: Update, context: CallbackContext, error: Exception) -> None:
    """Обрабатывает ошибки, возникающие во время выполнения запросов."""
    logger.error("Произошла ошибка: %s", error, exc_info=True)
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


def handle_start(update: Update, context: CallbackContext, mentors_url: str, postcards_url: str) -> None:
    """
    Обрабатывает команду `/start` и отправляет приветственное сообщение.

    Восстанавливает состояние после остановки.

    """
    try:
        if context.user_data is None:
            context.user_data = {}

        user = update.effective_user

        if user is None:
            raise BadRequest("Ошибка: пользователь не найден.")

        user_id = user.id
        context.user_data.setdefault(user_id, {})

        keyboard = [
            [KeyboardButton("Показать менторов"),
             KeyboardButton("Показать открытки")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        if context.user_data[user_id].get("awaiting_card") and context.user_data[user_id].get("selected_mentor"):
            logger.info("Бот успешно восстановил состояние и начал работу.")
            update.message.reply_text(
                "🔄 Продолжаем с остановки...",
                reply_markup=reply_markup
            )
            handle_show_postcards(update, context, postcards_url)

        elif context.user_data[user_id].get("awaiting_mentor"):
            logger.info("Бот успешно восстановил состояние и начал работу.")
            update.message.reply_text(
                "🔄 Продолжаем с остановки...",
                reply_markup=reply_markup
            )
            handle_show_mentors(update, context, mentors_url)

        else:
            role = start_role(user.username, mentors_url)
            welcome_message = (
                f"{role}\n\nПриветствует тебя dvmn бот.\n\n"
                "Это бот, который поздравляет менторов dvmn с праздниками."
            )
            update.message.reply_text(
                welcome_message,
                reply_markup=reply_markup
            )
            context.user_data[user_id] = {"last_action": "начало работы"}

    except Exception as error:
        handle_errors(update, context, error)


def handle_mentors(update: Update, context: CallbackContext, mentors_data: dict) -> None:
    """Отображает список менторов и запрашивает выбор ментора для отправки открытки."""
    if context.user_data is None:
        context.user_data = {}

    if update.effective_user is None:
        raise BadRequest("Ошибка: пользователь не найден.")

    user_id = update.effective_user.id
    mentors = mentors_data.get("mentors")

    if mentors:
        text = "\n".join(
            ["🌟 *Наши менторы:*", *[
                f"✨ *{num}.* {(
                    format_long_name(mentor.get("name")))} ([{mentor.get("tg_username")}](https://t.me/{mentor.get("tg_username")[1:]}))"
                for num, mentor in enumerate(mentors, start=1)]]
            )

        context.user_data[user_id].update({
            "mentors": [{
                "first_name": mentor.get("name").get("first"),
                "tg_chat_id": mentor.get("tg_chat_id"),
                "tg_username": mentor.get("tg_username")
            } for mentor in mentors],
            "awaiting_mentor": True,
            "last_action": "выбор ментора"
        })
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


def handle_postcards(update: Update, context: CallbackContext, cards_data: dict) -> None:
    """Отображает список открыток и запрашивает выбор открытки для отправки."""
    if context.user_data is None:
        context.user_data = {}

    if update.effective_user is None:
        raise BadRequest("Ошибка: пользователь не найден.")

    user_id = update.effective_user.id
    cards = cards_data.get("postcards")

    if cards:
        text = "*Выберите номер открытки для отправки:*\n\n"
        for num, card in enumerate(cards, start=1):
            text += f"{num}. *{card.get("name_ru")}* {card.get("body")}\n"

        context.user_data[user_id].update({
            "available_cards": [card.get("body") for card in cards],
            "awaiting_card": True,
            "last_action": "выбор открытки"
        })
        for message in message_splitter(text):
            update.message.reply_text(
                text=message,
                parse_mode=ParseMode.MARKDOWN
            )

    else:
        update.message.reply_text("Список открыток пуст.\nПовторите попытку позже.")


def handle_mentor_choice(update: Update, context: CallbackContext, postcards_url: str) -> None:
    """Обрабатывает выбор ментора и запрашивает открытку для отправки."""
    if context.user_data is None:
        context.user_data = {}

    if update.effective_user is None:
        raise BadRequest("Ошибка: пользователь не найден.")

    user_id = update.effective_user.id
    message_text = update.message.text

    if message_text.isdigit():
        index = int(message_text) - 1
        mentors = context.user_data[user_id].get("mentors", [])

        if 0 <= index < len(mentors):
            context.user_data[user_id].update({
                "selected_mentor": mentors[index],
                "awaiting_mentor": False,
                "awaiting_card": True
            })
            update.message.reply_text(f"✅ Выбрали: {mentors[index]["first_name"]}")
            handle_show_postcards(update, context, postcards_url)
        else:
            update.message.reply_text("❌ Неверный номер ментора.")
    else:
        update.message.reply_text("🔢 Пожалуйста, введите номер ментора.")


def handle_card_choice(update: Update, context: CallbackContext) -> None:
    """Обрабатывает выбор открытки и отправляет ее выбранному ментору."""
    if context.user_data is None:
        context.user_data = {}

    if update.effective_user is None:
        raise BadRequest("Ошибка: пользователь не найден.")

    user_id = update.effective_user.id
    user_data = context.user_data.get(user_id, {})

    try:
        index = int(update.message.text) - 1
        cards = user_data.get("available_cards", [])
        mentor = user_data.get("selected_mentor")

        if not mentor:
            update.message.reply_text("❌ Ментор не выбран!")
            return

        if 0 <= index < len(cards):
            context.bot.send_message(
                chat_id=mentor["tg_chat_id"],
                text=insert_name(cards[index], mentor["first_name"]),
                parse_mode=ParseMode.MARKDOWN
            )
            update.message.reply_text("🎉 Открытка отправлена!")
            context.user_data[user_id].clear()
        else:
            update.message.reply_text("❌ Неверный номер открытки.")
    except TelegramError as e:
        handle_errors(update, context, e)


def handle_show_mentors(update: Update, context: CallbackContext, mentors_url: str) -> None:
    """Обрабатывает запрос на отображение списка менторов."""
    mentors_data = get_mentors(mentors_url)
    handle_mentors(update, context, mentors_data)


def handle_show_postcards(update: Update, context: CallbackContext, postcards_url: str) -> None:
    """Обрабатывает запрос на отображение списка открыток."""
    cards_data = get_postcards(postcards_url)
    handle_postcards(update, context, cards_data)


def handle_message(update: Update, context: CallbackContext, mentors_url: str, postcards_url: str) -> None:
    """Обрабатывает текстовые сообщения."""
    try:
        if context.user_data is None:
            context.user_data = {}

        if update.effective_user is None:
            raise BadRequest("Ошибка: пользователь не найден.")

        user_id = update.effective_user.id
        user_data = context.user_data.get(user_id, {})

        text = update.message.text

        if text == "Показать менторов":
            handle_show_mentors(update, context, mentors_url)
        elif text == "Показать открытки":
            handle_show_postcards(update, context, postcards_url)
        elif user_data.get("awaiting_mentor"):
            handle_mentor_choice(update, context, postcards_url)
        elif user_data.get("awaiting_card"):
            handle_card_choice(update, context)
        else:
            handle_start(update, context, mentors_url, postcards_url)

    except Exception as error:
        handle_errors(update, context, error)
