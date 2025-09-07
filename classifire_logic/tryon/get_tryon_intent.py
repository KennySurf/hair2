# classifire_logic/question/get_tryon_reply.py
from services.gpt.gpt_client import send_to_gpt
from db.db_funcs import get_user_messages

def return_tryon_intent(user_id, message):
    messages = get_user_messages(user_id)

    prompt = """
    Ты NLU-классификатор согласия на примерку прически.
    Классы:
    - TRYON_ACCEPT: пользователь соглашается/просит примерку, в процессе визуализации или даёт показания для визуализации и т п
    - TRYON_REJECT: клиент отказывается от примерки
    - TRYON_OTHER: вопросы про примерку

    Верни только один класс без пояснений.
        """

    reply = send_to_gpt(messages[1:-1] + [{'role': 'system', 'content': prompt}] + messages[-1:])
    return reply
