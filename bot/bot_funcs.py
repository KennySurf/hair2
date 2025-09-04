from telegram import Update
from telegram.ext import ContextTypes
from core.dialogue_manager import dialogue_manager
from db.db_funcs import add_message


async def text_catcher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message = update.message.text


    add_message(user_id, 'user', message)
    await update.message.reply_text(dialogue_manager(user_id, message))
