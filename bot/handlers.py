from telegram.ext import MessageHandler, filters, CommandHandler

def register_command_handler(app, command_name, func_name):
    app.add_handler(CommandHandler(command_name, func_name))

def register_message_handler(app, func_name):
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, func_name))

def register_image_handler(app, func_name):
    app.add_handler(MessageHandler(filters.PHOTO, func_name))
