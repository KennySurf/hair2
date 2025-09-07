from services.gpt.gpt_client import send_to_gpt
from db.db_funcs import add_message, get_user_messages



def get_all_services_reply(user_id):
    history_user_messages = get_user_messages(user_id)

    all_services_intent_prompt = """
    Расскажи клиенту, какие у нас есть услуги, в тёплой и дружелюбной манере.
    Перечень:
    [
    "Наращивание волос",
    "Окрашивание волос",
    "Стрижка волос",
    "Укладки и мейк",
    "Уход за волосами",
    "Окрашивание и ламинирование бровей",
    "Продажа волос"
    ]
    После списка — мягко и по-человечески спроси клиента: 
    хочет ли он, чтобы мы подробнее рассказали про что-то одно.
    Не повторяй один и тот же шаблон, используй естественные варианты вроде:
    - "Могу подсказать подробнее про любую из них 😊"
    - "Хотите, расскажу подробнее о какой-то услуге?"
    """

    reply = send_to_gpt(history_user_messages + [{'role': 'system', 'content': all_services_intent_prompt}])
    add_message(user_id, 'assistant', reply)
    return reply