import bcrypt

def hash_password(password: str, cost_factor: int = 12) -> str:
    password_byte = password.encode("utf-8")
    salf = bcrypt.gensalt(rounds=cost_factor)
    hashed_password = bcrypt.hashpw(password_byte, salf)

    return hashed_password.decode("utf-8")