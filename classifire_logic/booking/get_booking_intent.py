from services.gpt.gpt_client import send_to_gpt

def return_booking_intent(message: str) -> str:
    """
    Классификатор сообщений внутри booking
    :param message:
    :return: str
    """

    prompt = """
    Ты — NLU классификатор для сценария записи в салон красоты. Определи, относится ли сообщение пользователя к записи на услугу. Верни один из вариантов:
    
    answer: Сообщение содержит информацию о записи (например, услуга, мастер, имя мастера, дата, время, или клиент оставляет свои данные и т п).
    
    other: Сообщение не связано с записью (например, запрос о выборе мастера или услуг).

    Верни только один из вариантов: answer или other.
    """
    classifier_message = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": message}
    ]
    return send_to_gpt(classifier_message)
