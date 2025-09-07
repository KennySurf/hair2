from db.db_funcs import get_user_messages, add_message
from db.price_question_db_funcs import get_price_question_state
from classifire_logic.question.service_cost.service_cost_scenario import get_hook, get_visual, idle


def get_service_cost_reply(user_id):
    state = get_price_question_state(user_id)
    user_messages = get_user_messages(user_id)
    print()
    print(f'state = {state}')

    if state == 'idle':
        reply = idle(user_id, user_messages)
    elif state == 'get_hook':
        reply = get_hook(user_id, user_messages)
    else:
        reply = get_visual(user_id, user_messages)

    add_message(user_id, 'assistant', reply)
    return reply