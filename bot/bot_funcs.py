from telegram import Update
from telegram.ext import ContextTypes
from core.dialogue_manager import dialogue_manager
from db.db_funcs import add_message, get_user_messages
from db.tryon_db_funcs import get_tryon_prompt, reset_tryon_prompt, reset_tryon_state, get_tryon_state
from services.gemini.generate_photo import generate_img
import os
from services.gpt.gpt_client import send_to_gpt



async def text_catcher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message = update.message.text


    add_message(user_id, 'user', message)
    await update.message.reply_text(dialogue_manager(user_id, message, update))

async def image_cather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if get_tryon_state(user_id) != 'getting_image':
        message = 'Вы хотите примерить на себе услугу?'
        add_message(user_id, 'assistant', message)
        await update.message.reply_text(message)
        return

    photo_file = update.message.photo[-1]
    user_folder = f'static/{user_id}'

    if not os.path.exists(user_folder):
        os.mkdir(user_folder)
        os.mkdir(f'{user_folder}/input_img')
        os.mkdir(f'{user_folder}/output_img')

    print('сюда')
    file = await photo_file.get_file()
    print('сюда2')
    await file.download_to_drive(f'static/{user_id}/input_img/input.jpg')
    await update.message.reply_text('Фотография принята, ожидайте генерации')

    prompt = get_tryon_prompt(user_id)
    await generate_img(user_id, prompt)

    with open(f'static/{user_id}/output_img/output.jpg', 'rb') as f:
        await update.message.reply_photo(photo=f)

    reset_tryon_prompt(user_id)
    reset_tryon_state(user_id)

    after_photo_prompt = """
    Мы уже визуализировали образ клиента и только что отправили фотографию.
    Сообщи клиенту, что его фотография готова, скажи что он хорошо выглядит и спроси хочет ли он записаться на раннее обсуждаемую услугу.
    Не спрашивай детали записи, только вопрос - хочет ли он записаться
    """
    user_history_messages = get_user_messages(user_id)
    after_photo_reply = send_to_gpt(user_history_messages + [{'role': 'system', 'content': after_photo_prompt}])
    add_message(user_id, 'assistant', after_photo_reply)
    await update.message.reply_text(after_photo_reply)
