# classifire_logic/question/get_tryon_reply.py
from services.gpt.gpt_client import send_to_gpt

def return_tryon_intent(message):
    prompt = """
    Ты NLU-классификатор согласия на примерку прически.
    Классы:
    - TRYON_ACCEPT: пользователь соглашается/просит примерку
    - TRYON_REJECT: явно отказывается
    - TRYON_OTHER: не про примерку

    Верни только один класс без пояснений.
        """.strip()

    reply = send_to_gpt([{'role': 'system', 'content': prompt},
                         {'role': 'user', 'content': message}])
    return reply
