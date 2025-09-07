from classifire_logic.booking.other_intent_logic import other_intent
from db.db_funcs import get_state, update_state, update_services_id, get_services_id, update_master_id, update_date, \
    get_master_id, get_date, update_time, get_time, reset_all_states, get_user_messages, add_message
from services.gpt.gpt_client import send_to_gpt
from services.yclients.booking import get_services, get_masters, make_booking, get_time_api


def answer_intent(user_id, user_message):
    user_message_prompt = [{'role': 'user', 'content': user_message}]
    history_user_messages = get_user_messages(user_id)
    state = get_state(user_id)
    reply = ''
    print(f'state - {state}')
    print(user_message_prompt)

    if state == 'idle':
        services = get_services().values()
        prompt = f"""
           Перечисли список услуг и вежливо спроси, какая из них интересует клиента?
           Список услуг:     [
    "Наращивание волос",
    "Окрашивание волос",
    "Стрижка волос"
    ]
           """
        # Список услуг: {services}
        update_state(user_id, 'get_services')
        reply = send_to_gpt(history_user_messages + [{'role': 'system', 'content': prompt}])
        #reply = send_to_gpt([{'role': 'system', 'content': prompt}])


    if state == 'get_services':
        services = list(get_services().values())
        print(f'services - {services}')

        prompt = f"""
                    Проверь, есть ли выбранная клиентом услуга в нашем перечне.
                    Проверять надо не написание, а смысл.
                    Выбранная клиентом услуга - {user_message}
                    Наш перечень - наращивание волос, окрашивание волос, стрижка волос.

                    Если смысл соответствует, верни название подходящей услуги из нашего перечня.
                    Если нет, верни False"""
        reply = send_to_gpt([{'role': 'system', 'content': prompt}] + user_message_prompt)

        if reply in ('наращивание волос', 'окрашивание волос'):
            reply = send_to_gpt(history_user_messages + [{'role': 'system', 'content': 'сообщи клиенту, что ему нужно сначала записаться на бесплатную консультацию. На ней мы подберём лучшее решение для волос клиента. Спроси, записать ли его? Не говори "понимаю"'}])
            update_state(user_id, 'get_advice')
        elif reply == 'стрижка волос':
            reply = send_to_gpt(history_user_messages + [{'role': 'system',
                             'content': f'вежливо озвучь клиенту что он выбрал стрижку и спроси хочет ли он к какому то конкрентому мастеру, или мне дать список мастеров. Не спрашивай критерии для списка - просто тут логика или клиент знает уже к какому мастеру он хочет, или мы предоставим ему список всех мастеров по услуге'}])
            update_state(user_id, 'get_masters')
            update_services_id(user_id, '10268227')
            add_message(user_id, 'assistant', reply)
        else:
            reply = send_to_gpt(history_user_messages + [{'role': 'system', 'content': 'Если клиент выбрал услугу из списка, который мы давали - скажи что данная услуга сейчас недоступна, предложи выбрать другую. А если он услугу не из списка - скажи, что у нас такой нету, предложи выбрать из нашего списка'}])
            add_message(user_id, 'assistant', reply)

    elif state == 'get_advice':
        print()
        print('get_advice')
        prompt = f"""
        идентифицируй ответ пользователя как да или нет и выведи его.
        Выводи только да или нет
        """
        reply = send_to_gpt(history_user_messages[:-1] + [{'role': 'system', 'content': prompt}] + user_message_prompt)
        print(reply)
        if reply == 'да':
            prompt = """В зависимости от предыдущего диалога верни услугу, которую клиент выбрал.
            Если это наращивание - наращивание
            Если это окрашивание - окрашивание
            Не выводи ничего лишнего, только название услуги, что я указал"""

            service = send_to_gpt(history_user_messages + [{'role': 'system', 'content': prompt}])
            if service == 'наращивание':
                update_services_id(user_id, '10928000')
            update_services_id(user_id, '17637553')

            prompt = 'вежливо спроси клиента, есть у него уже мастер, к которому он хочет записаться, или ему помочь подобрать'
            reply = send_to_gpt(history_user_messages + [{'role': 'system', 'content': prompt}])
            print(reply)
            update_state(user_id, 'get_masters')
            add_message(user_id, 'assistant', reply)
        else:
            prompt = """обработай возражение опираясь на положение:
            Общие правила работы:
            Никогда не спорь с клиентом.
            Подтверждай эмоцию клиента (понимание, уважение к его позиции).
            Показывай ценность консультации или услуги (опыт мастеров, индивидуальный подход, репутация студии).
            Не закрывай возражение снижением цены.
            Не обещай невозможных результатов.
            Завершай ответ приглашением к следующему шагу: «Давайте подберу время…», «Когда вам удобно встретиться…».
            
            Пример сценария — клиент говорит: «Не хочу консультацию, просто скажите цену».
            Шаблон ответа:
            Подтверди эмоцию: «Очень понимаю желание сразу определиться с бюджетом ❤️».
            Дай ценность: «Наращивание или окрашивание всегда рассчитывается индивидуально. На консультации мастер подберёт длину, объём и метод так, чтобы результат выглядел максимально естественно. Дополнительно мы проводим диагностику кожи головы (обычно 3.000₽), для вас она будет бесплатной».
            Заверши приглашением: «Давайте подберём удобное время для встречи»."""
            reply = send_to_gpt(history_user_messages + [{'role': 'system', 'content': prompt}])
            add_message(user_id, 'assistant', reply)

    elif state == 'get_masters':
        service_id = get_services_id(user_id)
        masters = get_masters(service_id)

        prompt = f"""
           Вежливо спроси имя мастера, к которому клиент хочет записаться.
           Список мастеров: {masters.values()}
           """

        reply = send_to_gpt(history_user_messages + [{'role': 'system', 'content': prompt}])
        print(reply)
        update_state(user_id, 'checkout_master')
        add_message(user_id, 'assistant', reply)

    elif state == 'checkout_master':
        print()
        print('checkout_master')
        service_id = get_services_id(user_id)
        masters = list(get_masters(service_id).values())

        prompt = f"""
                    Проверь, есть ли выбранный клиентом мастер в нашем перечне.
                    Выбранный мастер - {user_message}
                    Наш перечень - {masters}
                    
                    Сравнивай не столько по идентичному написанию, сколько по смыслу.
                    Если имя выбранного мастера, встречется в нашем перечне - верни выбранного мастера так, как он записан в нашем перечне
                    Если нет, верни False"""

        reply = send_to_gpt([{'role': 'system', 'content': prompt}] + user_message_prompt)
        if reply != 'False':
            master_id = list(get_masters(service_id).keys())[masters.index(reply)]

            update_master_id(user_id, master_id)
            update_state(user_id, 'get_date')
            reply = send_to_gpt(history_user_messages + [{'role': 'system',
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
            reply = send_to_gpt(history_user_messages + [{'role': 'system', 'content': f'Вежливо спроси клиента на какое время его записать. Без вариантов, только просьба указать желаемое время'}])
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
            reply = send_to_gpt(history_user_messages + [{'role': 'system',
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
                reset_all_states(user_id)
            else:
                reply = 'Произошла ошибка при добавлении записи, попробуйте ещё раз'

    return reply if reply else 'я не совсем вас поняла, напишите ещё раз'
