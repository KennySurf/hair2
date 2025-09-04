# classifire_logic/booking_classifier.py
from db.db_funcs import get_state, get_services_id, get_date, update_state, get_time
from services.gpt.gpt_client import send_to_gpt
from services.yclients.booking import get_services, get_masters, get_time


def other_intent(user_id):
    state = get_state(user_id)
    print()
    print(f'state: {state}')
    prompt = ''

    if state == 'idle':
        services = get_services().values()
        prompt = f"""
              Вежливо спроси какая из списка услуга клиента интересует.
              Список услуг: {services}
              """
        update_state(user_id, 'get_services')

    elif state == 'get_services':
        services = get_services().values()
        prompt = f"""
           Вежливо спроси какая услуга клиента интересует.
           Список услуг: {services}
           """


    elif state == 'get_masters':
        service_id = get_services_id(user_id)
        masters = get_masters(service_id)

        prompt = f"""
           Вежливо спроси имя мастера, к которому клиент хочет записаться.
           Список мастеров: {masters.values()}
           """

    elif state == 'get_date':
        prompt = f"""
           Вежливо спроси на какую дату клиент хочет записаться.
           """
        update_state(user_id, 'get_time')

    elif state == 'get_time':
        service_id = get_services_id(user_id)
        master_id = get_masters(service_id)
        date = get_date(user_id)

        times = get_time(service_id, master_id, date)

        prompt = f"""Вежливо спроси на какое время клиент хочет записаться
           список доступного времени - {times}
           Если список пуст - скажи что сегодня нет свободного времени у мастера"""

    elif state == 'finish':
        prompt = f"""
        Вежливо спроси клиента на какое имя записать, номер телефона и почту"""

    reply = send_to_gpt([{'role': 'system', 'content': prompt}])
    return reply
