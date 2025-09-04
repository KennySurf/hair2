# classifire_logic/booking_classifier.py
from db.db_funcs import get_state, get_services_id, get_user_messages, add_message, get_date, update_state, get_master_id, update_date, update_time, get_time, update_services_id, update_master_id
from services.yclients.booking import get_services, get_masters, get_time, make_booking
from services.gpt.gpt_client import send_to_gpt
#    - request: сам инициирует запись ("хочу записаться", "мне нужна стрижка завтра")

def get_booking_intent(message):
    prompt = """
    Ты - NLU классификатор для сценария записи в салон красоты.
    Определи, что делает пользователь:
    - answer: отвечает на вопрос (например: называет услугу, мастера, дату или время)
    - other: сообщение не относится к записи

    Верни только один из вариантов: answer или other.
    """
    classifier_message = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": message}
    ]
    return send_to_gpt(classifier_message)

def get_booking_reply(user_id, user_message):
    prompt = ''
    state = get_state(user_id)
    user_messages = get_user_messages(user_id)

    intent = get_booking_intent(user_message)
    if intent == 'answer':
        reply = answer_intent(state, user_message)
    else:
        reply = other_intent(state, user_message)

    add_message(user_id, 'assistant', reply)
    return reply

def answer_intent(user_id, user_message):
    user_message_prompt = [{'role': 'user', 'content': user_message}]
    state = get_state(user_id)
    reply = ''

    if state == 'get_services':
        services = get_services().values()

        prompt = f"""
                    Проверь, есть ли выбранная клиентом услуга в нашем перечне.
                    Выбранная клиентом услуга - {user_message}
                    Наш перечень - {services}

                    Если да, верни название услуги
                    Если нет, верни False"""

        reply = send_to_gpt([{'role': 'system', 'content': prompt}] + user_message_prompt)
        if reply:
            service_id = get_services().keys()[services.index(reply)]

            update_state(user_id, 'get_masters')
            update_services_id(user_id, service_id)
            reply = send_to_gpt([{'role': 'system', 'content': f'вежливо озвучь клиенту что он выбрал услугу {reply} и спроси переходим ли к выбору мастера'}])

    elif state == 'get_masters':
        service_id = get_services_id(user_id)
        masters = get_masters(service_id).values()

        prompt = f"""
                    Проверь, есть ли выбранный клиентом мастер в нашем перечне.
                    Выбранный мастер - {user_message}
                    Наш перечень - {masters}

                    Если да, верни выбранного мастера
                    Если нет, верни False"""

        reply = send_to_gpt([{'role': 'system', 'content': prompt}] + user_message_prompt)
        if reply:
            master_id = get_masters(service_id).keys()[masters.index(reply)]

            update_master_id(user_id, master_id)
            update_state(user_id, 'get_date')
            reply = send_to_gpt([{'role': 'system', 'content': f'вежливо озвучь клиенту что он выбрал мастера {reply} и спроси на какую дату его записать'}])

    elif state == 'get_time':
        service_id = get_services_id(user_id)
        master_id = get_master_id(service_id)
        date = get_date(user_id)

        times = get_time(service_id, master_id, date)
        prompt = f"""
                    Проверь, доступно ли выбранное клиентом время.
                    Выбранное время - {user_message}
                    Наш перечень - {times}

                    Если да, верни выбранное время в формате H:m:s
                    Если нет, верни False"""

        reply = send_to_gpt([{'role': 'system', 'content': prompt}] + user_message_prompt)
        if reply:
            update_time(user_id, reply)
            update_state(user_id, 'get_date')
            reply = send_to_gpt([{'role': 'system', 'content': f'Вежливо спроси клиента на какое имя записать, номер телефона и почту'}])
            update_state(user_id, 'finish')

    elif state == 'finish':
        prompt = f"""
        обработай ввод пользователя в строго такой формат -
        ('номер телефона пользователя', 'имя пользователя', 'почта пользователя')
        
        Если каких то данных не хватает верни - None
        """
        reply = send_to_gpt([{'role': 'system', 'content': prompt}] + user_message_prompt)

        if reply:
            service_id = get_services_id(user_id)
            master_id = get_master_id(service_id)
            date = get_date(user_id)
            time = get_time(user_id)

            reply = eval(reply)
            time = send_to_gpt([{'role': 'system', 'content': f'верни верный формат datetime {date} {time} - Y-M-D H:m:s'}])
            make_booking(reply[0], reply[1], reply[2], service_id, master_id, time)
            reply = 'запись успешно создана'

    return reply

def other_intent(user_id, user_message):
    state = get_state(user_id)
    prompt = ''

    if state == 'get_services':
        services = get_services().values()
        prompt = f"""
           Вежливо спроси какая услуга клиента интересует.
           Список услуг: {services}
           """


    elif state == 'get_masters':
        service_id = get_services_id(user_id)
        masters = get_masters(service_id)

        prompt = f"""
           Вежливо спроси к какому мастеру клиент хочет записаться.
           Список мастеров: {get_masters(service_id).values()}
           """

    elif state == 'get_date':
        prompt = f"""
           Вежливо спроси на какую дату клиент хочет записаться.
           """

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
