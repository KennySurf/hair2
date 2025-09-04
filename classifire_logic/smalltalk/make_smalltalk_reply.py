from services.gpt.gpt_client import send_to_gpt
from db.db_funcs import get_user_messages, add_message


def get_smalltalk_reply(user_id, user_message):
    prompt = f"""Если пользователь здоровается - вежливо поздоровайся с ним и хочет ли он записаться на услуги, или чтобы ты подробней рассказала об наших услугах.
                Если пользователь прощается - вежливо прощайся тоже и говори что будешь его ждать.
                Если пользователь обменивается любезностями - хвалит и т д, говори, поддерживай его.
                Главное в этом пункте всегда поддерживать пользователя.
                """

    messages = get_user_messages(user_id)
    reply = send_to_gpt(messages[:-1] + [{'role': 'system', 'content': prompt}] + messages[-1:])

    add_message(user_id, 'assistant', reply)
    return reply
