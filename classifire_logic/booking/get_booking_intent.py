from services.gpt.gpt_client import send_to_gpt

def return_booking_intent(message: str) -> str:
    """
    Классификатор сообщений внутри booking
    :param message:
    :return: str
    """

    prompt = """
    Ты - NLU классификатор для сценария записи в салон красоты.
    Определи, что делает пользователь:
    - answer: конкретно отвечает на вопрос по записи (например: называет услугу, мастера, дату или время)
    - other: сообщение не относится к записи (например: давайте выберем мастера, давайте посмотрим услуги)

    Верни только один из вариантов: answer или other.
    """
    classifier_message = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": message}
    ]
    return send_to_gpt(classifier_message)
