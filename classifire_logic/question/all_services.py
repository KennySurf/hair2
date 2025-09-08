from services.gpt.gpt_client import send_to_gpt
from db.db_funcs import add_message, get_user_messages



def get_all_services_reply(user_id):
    history_user_messages = get_user_messages(user_id)

    all_services_intent_prompt = """
    Расскажи клиенту, какие у нас есть услуги, в тёплой и дружелюбной манере.
    ⚠️ Важно: никаких других услуг, брендов, деталей или консультаций упоминать нельзя.

    Список услуг:
    - Наращивание волос
    - Окрашивание волос
    - Стрижка волос
    
    ОБЯЗАТЕЛЬНО!!!
    После списка сделай новый абзац и мягко, дружелюбно спроси клиента,
    хочет ли он, чтобы мы подробнее рассказали про какую-то услугу.
    Не упоминай консультацию и не добавляй других вариантов.

    НИКАКИХ ДОПОЛНИТЕЛЬНЫХ УСЛУГ, ТОЛЬКО ТЕ, ЧТО Я ТЕБЕ РАЗРЕШИЛ ГОВОРИТЬ!!!!
    """

    reply = send_to_gpt(history_user_messages + [{'role': 'system', 'content': all_services_intent_prompt}])
    add_message(user_id, 'assistant', reply)
    return reply