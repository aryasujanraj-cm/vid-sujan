def get_users():
    return {"demo": "demo123", "admin": "admin123", "user1": "pass123"}


def verify_login(username, password):
    users = get_users()
    return users.get(username) == password
