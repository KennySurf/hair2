# classifire_logic/question/make_tryon_reply.py
from db.tryon_db_funcs import get_tryon_state, reset_tryon_state, update_tryon_state
from services.gpt.gpt_client import send_to_gpt

def get_tryon_accept_reply(user_id, user_message):
    tryon_state = get_tryon_state(user_id)

    if tryon_state == 'idle':
        prompt = """
        вежливо спроси у пользователя какие изменения он хочет на себе увидеть
        """
        reply = send_to_gpt([{'role': 'system', 'content': prompt}])
        update_tryon_state(user_id, 'getting_a_prompt')
        return reply

    if tryon_state == 'getting_a_prompt':
        start_prompt = """
        Сгенерируй промпт для изменения фотографии пользователя, опираясь на его желания по изменению.
        """
        user_prompt = send_to_gpt([{'role': 'system', 'content': start_prompt},
                                   {'role': 'user', 'content': user_message}])

        reply_prompt = """
        Вежливо попроси у пользователя фотографию
        """
        update_tryon_state(user_id, 'getting_image')
        return send_to_gpt([{'role': 'system', 'content': reply_prompt}])

    if tryon_state == 'getting_image':
        prompt = """
        Сгенерируй промпт для изменения фотографии пользователя, опираясь на его желания по изменению.
        """

