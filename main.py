from environs import Env
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from handlers.handlers import handle_errors, handle_message, handle_start


def main():
    env = Env()
    env.read_env()
    token = env.str('TG_TOKEN')

    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", handle_start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command,
                       handle_message)
    )

    dispatcher.add_error_handler(handle_errors)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
