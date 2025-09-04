# classifire_logic/get_classifier.py
from services.gpt.gpt_client import send_to_gpt
from db.db_funcs import get_user_messages

def get_message_classification(user_id, message):
    prompt ="""
    Ты - NLU классификатор салона красоты. Твоя цель определять, к какой роли относится сообщение пользователя.
    Правила:
    booking: хочет записаться (называет услугу/время/мастера или явно просит запись)
    question: задаёт вопрос (цены, график, адрес, услуги и т.д.)
    smalltalk: приветствие/прощание/вежливости без деловой сути
    other: иное
    
    Строго следую правилам и возвращай единственный ответ - роль сообщения. Никаких пояснений или других данных.
    Если ты думаешь, что сообщение может принадлежать к нескольким ролям - выводи старшую роль по правилам.
    """
    messages = get_user_messages(user_id)

    # classifier_message = [{'role': 'system', 'content': prompt},
    #                       {'role': 'user', 'content': message}]

    classifier_message = messages[1:-1] + [{'role': 'system', 'content': prompt}] + [messages[-1]]

    return send_to_gpt(classifier_message)