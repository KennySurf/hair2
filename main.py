from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
from os import getenv
from bot.handlers import register_message_handler, register_image_handler
from bot.bot_funcs import text_catcher, image_cather
from db.models import run_table


load_dotenv()

if __name__ == "__main__":
    run_table()

    app = ApplicationBuilder().token(getenv('TELEGRAM_BOT_TOKEN')).build()
    register_message_handler(app, text_catcher)
    register_image_handler(app, image_cather)

    app.run_polling()
