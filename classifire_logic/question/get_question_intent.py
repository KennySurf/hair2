# classifire_logic/question/get_question_intent.py
from db.db_funcs import get_user_messages
from services.gpt.gpt_client import send_to_gpt

def return_question_intent(user_id, message):
    prompt = f"""
    Ты nlu классификатор для сценария вопроса. Определи к какой теме из нашего перечня относится вопрос клиента.
    наш перечень тем:
    [
    "Наращивание волос",
    "Окрашивание волос",
    "Стрижка волос",
    "Укладки и мейк",
    "Уход за волосами",
    "Окрашивание и ламинирование бровей",
    "Продажа волос"
    "Вопрос цены" - если клиент запрашивает цену, выбирай это
    ]
    
    Верни только один из вариантов: название услуги.
    Если это вопрос - какие у нас услуги есть, верни сообщение: все услуги
    """

    messages = get_user_messages(user_id)
    reply = send_to_gpt(messages[:-1] + [{'role': 'system', 'content': prompt}] + messages[-1:])
    return reply
