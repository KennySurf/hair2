from openai.resources.containers.files import content
from classifire_logic.booking.other_intent_logic import other_intent

from db.db_funcs import get_state, update_state, update_services_id, get_services_id, update_master_id, update_date, \
    get_master_id, get_date, update_time, get_time
from services.gpt.gpt_client import send_to_gpt
from services.yclients.booking import get_services, get_masters, make_booking, get_time_api


def answer_intent(user_id, user_message):
    user_message_prompt = [{'role': 'user', 'content': user_message}]
    state = get_state(user_id)
    reply = ''
    print(f'state - {state}')
    print(user_message_prompt)

    if state == 'idle':
        services = get_services().values()
        prompt = f"""
           Вежливо спроси какая из списка услуга клиента интересует.
           Список услуг: {services}
           """
        update_state(user_id, 'get_services')
        reply = send_to_gpt([{'role': 'system', 'content': prompt}])

    if state == 'get_services':
        services = list(get_services().values())
        print(f'services - {services}')

        prompt = f"""
                    Проверь, есть ли выбранная клиентом услуга в нашем перечне.
                    Выбранная клиентом услуга - {user_message}
                    Наш перечень - {services}

                    Если да, верни название услуги
                    Если нет, верни False"""
        reply = send_to_gpt([{'role': 'system', 'content': prompt}] + user_message_prompt)
        if reply:
            print()
            print(f'reply - {reply}')
            service_id = list(get_services().keys())[services.index(reply)]

            update_state(user_id, 'get_masters')
            update_services_id(user_id, service_id)
            reply = send_to_gpt([{'role': 'system',
                                  'content': f'вежливо озвучь клиенту что он выбрал услугу {reply} и спроси хочет ли он к какому то конкрентому мастеру, или мне дать список мастеров. Не спрашивай критерии для списка - просто тут логика или клиент знает уже к какому мастеру он хочет, или мы предоставим ему список всех мастеров по услуге'}])

    elif state == 'get_masters':
        service_id = get_services_id(user_id)
        masters = list(get_masters(service_id).values())

        prompt = f"""
                    Проверь, есть ли выбранный клиентом мастер в нашем перечне.
                    Выбранный мастер - {user_message}
                    Наш перечень - {masters}

                    Если имя выбранного мастера, встречется в нашем перечне - верни выбранного мастера так, как он записан в нашем перечне
                    Если нет, верни False"""

        reply = send_to_gpt([{'role': 'system', 'content': prompt}] + user_message_prompt)
        if reply != 'False':
            master_id = list(get_masters(service_id).keys())[masters.index(reply)]

            update_master_id(user_id, master_id)
            update_state(user_id, 'get_date')
            reply = send_to_gpt([{'role': 'system',
                                  'content': f'вежливо озвучь клиенту что он выбрал мастера {reply} и спроси на какое число его записать'}])

        else: return other_intent(user_id)

    elif state == 'get_date':
        prompt = f"""
           Если сообщение клиента дата - в том числе завтра, послезавтра и т д.
           Верни выбранную клиентом дату в формате Y-M-D
           Если он не указал дату, верни False
           """
        reply = send_to_gpt([{'role': 'system', 'content': prompt}] + user_message_prompt)
        if reply:
            update_date(user_id, reply)
            reply = send_to_gpt([{'role': 'system', 'content': f'Вежливо спроси клиента на какое время его записать. Без вариантов, только просьба указать желаемое время'}])
            update_state(user_id, 'get_time')

    elif state == 'get_time':
        service_id = get_services_id(user_id)
        master_id = get_master_id(user_id)
        date = get_date(user_id)
        print()
        print(f'выбранное время - {user_message}')

        times = get_time_api(service_id, master_id, date)
        print(f'перечень времён {times}')
        prompt = f"""
                    Проверь, доступно ли выбранное клиентом время.
                    Выбранное время - {user_message}
                    Наш перечень - {times}

                    Если да, верни выбранное время в формате H:m:s
                    Если нет, верни False"""

        reply = send_to_gpt([{'role': 'system', 'content': prompt}] + user_message_prompt)
        if reply != 'False':
            update_time(user_id, reply)
            update_state(user_id, 'get_date')
            reply = send_to_gpt([{'role': 'system',
                                  'content': f'Вежливо спроси клиента на какое имя записать, номер телефона и почту'}])
            update_state(user_id, 'finish')
        else: return 'На данное время нету записей, выберите другое'

    elif state == 'finish':
        prompt = f"""
        обработай ввод пользователя в строго такой формат -
        ('номер телефона пользователя', 'имя пользователя', 'почта пользователя')

        Если каких то данных не хватает верни - None
        """
        reply = send_to_gpt([{'role': 'system', 'content': prompt}] + user_message_prompt)

        if reply:
            service_id = get_services_id(user_id)
            master_id = get_master_id(user_id)
            date = get_date(user_id)
            time = get_time(user_id)

            reply = eval(reply)
            time = send_to_gpt(
                [{'role': 'system', 'content': f'верни верный формат datetime {date} {time} - Y-M-D H:m:s'}])
            if make_booking(reply[0], reply[1], reply[2], service_id, master_id, time):
                reply = 'запись успешно создана'
            else:
                reply = 'Произошла ошибка при добавлении записи, попробуйте ещё раз'

    return reply if reply else 'я не совсем вас поняла, напишите ещё раз'
