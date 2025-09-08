from db.db_funcs import add_message, get_user_messages
from db.tryon_db_funcs import get_end_cooldown_time, update_end_cooldown_time
from datetime import datetime, timedelta
from docx import Document

from services.gpt.gpt_client import send_to_gpt


def get_service_reply(user_id, intent):
    try_on_closer = ''

    if (intent in ("Наращивание волос", "Окрашивание волос", "Стрижка волос")
            and (get_end_cooldown_time(user_id) is None or
                 datetime.strptime(get_end_cooldown_time(user_id), "%Y-%m-%d %H:%M:%S") < datetime.now())):
        print()
        print('QUESTION_TRY_ON_FUNC')

        try_on_closer = """
    Если клиент спрашивает про конкретную услугу — в первую очередь предложи ему примерить её на себе, 
    сказав, что мы можем визуализировать, как это будет выглядеть. 
    Говори дружелюбно, коротко и по-человечески ❤️.
    Не нужно уточнять технические детали или спрашивать, какой именно метод интересует, говорить что то про консультации и т д — 
    главное только мягко предложить примерку.
    Не нужно спрашивать про запись на консультацию!
    Не нужно спрашивать детали, чего бы пользователь хотел и т д- нужно только спросить - хочет ли он визуализацию, это единственный вопрос, который должен тут звучать
    Разделяй на абзацы рассказ об услуге и предложение визуализации"""

        updated_cooldown_time = datetime.now() + timedelta(hours=6)
        print()
        print(f'updated_cooldown_time: {updated_cooldown_time}')
        update_end_cooldown_time(user_id, updated_cooldown_time.strftime('%Y-%m-%d %H:%M:%S'))

    # file = f'classifire_logic/question/files/{intent.lower()}.docx'
    file = f'classifire_logic/question/files/общее положение.docx'

    doc = Document(file)

    full_text = "\n".join([para.text for para in doc.paragraphs])

    get_question_start_prompt = """
    Отвечай клиенту на его вопрос, используя информацию из файла, но не говори, что берёшь её из файла. Если информации недостаточно, добавляй только то, что соответствует теме услуги. 
    Когда клиент спрашивает про услугу, давай краткое описание, не более одного абзаца. 
    Не забывай про дружественный тон, но избегай излишних деталей. 
    Формулировки должны быть естественными и варьироваться, чтобы не повторяться.
    """

    input_prompt = [
        {
            'role': 'system',
            'content': f"""{get_question_start_prompt + try_on_closer}
                    информация из файла: {full_text}"""
        }
    ]
    messages = get_user_messages(user_id)

    reply = send_to_gpt(messages[:-1] + input_prompt + messages[-1:])


    add_message(user_id, 'assistant', reply)
    return reply