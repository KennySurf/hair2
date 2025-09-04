from classifire_logic.question.get_question_intent import return_question_intent
from docx import Document
from services.gpt.gpt_client import send_to_gpt
from db.db_funcs import add_message, get_user_messages

def get_question_reply(user_id, user_message):
    prompt = 'Опираясь на информацию из файла дай ответ по вопросу клиента. Но только сам не упоминай, что ты опираешься на информацию из файла'

    intent = return_question_intent(user_message)
    reply = ''

    if intent == 'все услуги':
        prompt = """
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
        reply = send_to_gpt([{'role': 'system', 'content': prompt}])
    else:
        file = f'classifire_logic/question/files/{intent.lower()}.docx'
        doc = Document(file)

        full_text = "\n".join([para.text for para in doc.paragraphs])

        input_prompt = [
            {
                'role': 'system',
                'content': f"""{prompt}
                информация из файла: {full_text}"""
            }
        ]
        messages = get_user_messages(user_id)

        reply = send_to_gpt(messages[:-1] + input_prompt + messages[-1:])

    add_message(user_id, 'assistant', reply)
    return reply
