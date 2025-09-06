# classifire_logic/question/make_tryon_reply.py
from db.tryon_db_funcs import get_tryon_state, update_tryon_state, update_tryon_prompt
from services.gpt.gpt_client import send_to_gpt
from db.db_funcs import get_user_messages

def get_tryon_accept_reply(user_id, user_message):
    tryon_state = get_tryon_state(user_id)
    history_user_messages = get_user_messages(user_id)

    if tryon_state == 'idle':
        prompt = """
        вежливо спроси у пользователя какие изменения он хочет на себе увидеть.
        опирайся на услугу, о которой был диалог до этого.
        Не предлагай вариации под пожелания клиента и не спрашивай какая техника интересна ему.
        Просто собери информацию по тому, какие изменения он хотел бы видеть
        """
        reply = send_to_gpt(history_user_messages + [{'role': 'system', 'content': prompt}])
        update_tryon_state(user_id, 'getting_a_prompt')
        return reply

    if tryon_state == 'getting_a_prompt':
        start_prompt = """
        Сгенерируй промпт для изменения фотографии пользователя, опираясь на его желания по изменению.
        Промпт должен быть на английском.
        Если пользователь говорит не о изменении прически, верни - не прическа
        Больше ничего не выводи - или только промпт на английском, или не прическа.
        """
        user_prompt = send_to_gpt(history_user_messages[:-1] +
                                  [{'role': 'system', 'content': start_prompt},
                                   {'role': 'user', 'content': user_message}])

        if user_prompt == 'не прическа':
            reply_prompt = """
            Вежливо сообщи пользователю, что мы можем визуализировать только прическу, пусть скорректирует свой запрос
            """
        else:
            reply_prompt = """
            Вежливо попроси у пользователя фотографию
            """
            update_tryon_prompt(user_id, user_prompt)
            update_tryon_state(user_id, 'getting_image')

        return send_to_gpt([{'role': 'system', 'content': reply_prompt}])

    if tryon_state == 'getting_image':
        prompt = """
        Вежливо скажи клиенту, что визуализация ещё генерируется 
        """
        reply = send_to_gpt([{'role': 'system', 'content': prompt}])
        return reply

    return None
