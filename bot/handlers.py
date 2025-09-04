from telegram.ext import MessageHandler, filters

def register_message_handler(app, func_name):
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, func_name))
