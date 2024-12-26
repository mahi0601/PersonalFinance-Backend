from app.core.security import hash_password, verify_password
from app.models.users import create_user

def signup_user(username: str, password: str):
    hashed_password = hash_password(password)
    return create_user(username, hashed_password)
