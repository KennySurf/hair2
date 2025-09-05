# classifire_logic/question/make_question_reply.py
from classifire_logic.question.get_question_intent import return_question_intent
from docx import Document
from services.gpt.gpt_client import send_to_gpt
from db.db_funcs import add_message, get_user_messages
from db.tryon_db_funcs import get_end_cooldown_time, update_end_cooldown_time
from datetime import datetime

def get_question_reply(user_id, user_message):

    intent = return_question_intent(user_message)
    reply = ''

    if intent == 'все услуги':
        reply = send_to_gpt([{'role': 'system', 'content': all_services_intent_prompt}])
    else:
        try_on_closer = ''

        if (intent in ("Наращивание волос", "Окрашивание волос", "Стрижка волос")
            and datetime.strptime(get_end_cooldown_time(user_id), "%Y-%m-%d %H:%M:%S") < datetime.now()):
            print()
            print('QUESTION_TRY_ON_FUNC')

            try_on_closer = """
            Если клиент говорит о какой то услуге, спроси его - не хочет ли он её примерить на себе
            """

            update_end_cooldown_time(user_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        file = f'classifire_logic/question/files/{intent.lower()}.docx'
        doc = Document(file)

        full_text = "\n".join([para.text for para in doc.paragraphs])

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

get_question_start_prompt = """
Опираясь на информацию из файла дай ответ по вопросу клиента. 
Но только сам не упоминай, что ты опираешься на информацию из файла.
"""
all_services_intent_prompt = """
    Расскажи клиенту, какие у нас есть услуги - вот перечень.
    Соблюдай правила доброжелательности, которые я устанавливал в самом первом сообщении.
        [
        "Наращивание волос",
        "Окрашивание волос",
        "Стрижка волос",
        "Укладки и мейк",
        "Уход за волосами",
        "Окрашивание и ламинирование бровей",
        "Продажа волос"
         ]
    Спроси клиента, рассказать ли ему о какой то конкретной услуги?
    """

