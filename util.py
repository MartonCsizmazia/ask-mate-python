from datetime import datetime
import bcrypt
import data_manager


def date_now():
    dt = datetime.now()
    return dt.replace(microsecond=0)


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, username):
    try:
        hashed_password = data_manager.get_hashed_password_for_user(username)
        hashed_bytes_password = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)
    except TypeError:
        return False
