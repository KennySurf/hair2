from services.gpt.gpt_client import send_to_gpt
from db.db_funcs import get_user_messages, add_message


def get_other_reply(user_id, user_message):
    prompt = f"""Поддержи диалог с пользователем в рамках обговорённых правил.
                Если он задаёт вопрос, отвечай в рамках нашей ниши - салона красоты.
                Если он чем то делится, в рамках нашей ниши, поддерживай его.
                Главная цель - поддерживая плавно вывести на запись услуг
                """

    messages = get_user_messages(user_id)
    reply = send_to_gpt(messages[:-1] + [{'role': 'system', 'content': prompt}] + messages[-1:])

    add_message(user_id, 'assistant', reply)
    return reply
