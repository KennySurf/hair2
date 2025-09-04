from telegram import Update
from telegram.ext import ContextTypes
from core.dialogue_manager import dialogue_manager


async def text_catcher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message = update.message.text

    await update.message.reply_text(dialogue_manager(user_id, message))
