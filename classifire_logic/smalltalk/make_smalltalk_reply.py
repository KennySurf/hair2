from services.gpt.gpt_client import send_to_gpt
from db.db_funcs import get_user_messages, add_message


def get_smalltalk_reply(user_id, user_message):
    prompt = f"""Если пользователь здоровается - вежливо поздоровайся, представься и спроси а как его зовут.
                Если пользователь даёт нам своё имя - скажи, что приятно познакомиться и спроси хочет он записаться на услуги или рассказать ему о наших услугахбольше.
                Если пользователь прощается - вежливо прощайся тоже и говори что будешь его ждать.
                Если пользователь обменивается любезностями - хвалит и т д, будь благодарным, поддерживай его.
                Придерживайся правил самого первого системного сообщения.
                """

    messages = get_user_messages(user_id)
    reply = send_to_gpt(messages[:-1] + [{'role': 'system', 'content': prompt}] + messages[-1:])

    add_message(user_id, 'assistant', reply)
    return reply
