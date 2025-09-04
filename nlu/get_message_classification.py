# nlu/get_message_classification
from services.gpt.gpt_client import send_to_gpt
from db.db_funcs import get_user_messages

def return_message_classification(user_id: str, message: str) -> str:
    prompt ="""
    Ты - NLU классификатор салона красоты. Твоя цель определять, к какой роли относится сообщение пользователя.
    Обязательно смотри контекст всего диалога, чтобы точнее понять к чему пренадлежит последнее сообщение.
    Правила:
    booking: всё что касается записи - (называет услугу/время/мастера или явно просит запись и т п)
    question: задаёт вопрос вне записи - (интересуется ценами, графиком, адресом, какие вообще услуги у нас есть, описанием услуг и т.д.)
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
