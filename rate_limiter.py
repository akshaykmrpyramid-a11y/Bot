import time

user_requests = {}

LIMIT_SECONDS = 10

def is_allowed(user_id):
    now = time.time()

    if user_id not in user_requests:
        user_requests[user_id] = now
        return True

    if now - user_requests[user_id] > LIMIT_SECONDS:
        user_requests[user_id] = now
        return True

    return False
