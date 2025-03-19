import logging

from environs import Env
from telegram.ext import (
    CommandHandler,
    Filters,
    MessageHandler,
    PicklePersistence,
    Updater
)

from libs.arg_parser import create_parser
from handlers.handlers import (
    handle_errors,
    handle_message,
    handle_start
)


logging.basicConfig(
    format="[%(asctime)s] - %(levelname)s - %(funcName)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    env = Env()
    env.read_env()
    mentors_url, postcards_url, tg_token_input = create_parser()
    tg_token = tg_token_input if tg_token_input else env.str("TG_TOKEN")
    persistence = PicklePersistence(filename="id", single_file=False)

    updater = Updater(tg_token, persistence=persistence)
    dispatcher = updater.dispatcher

    logger.info("Бот запускается...")

    dispatcher.add_handler(CommandHandler(
        "start",
        lambda update, context: handle_start(
            update, context, mentors_url, postcards_url)
        )
    )
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command,
        lambda update, context: handle_message(
            update, context, mentors_url, postcards_url)
        )
    )
    dispatcher.add_error_handler(handle_errors)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
