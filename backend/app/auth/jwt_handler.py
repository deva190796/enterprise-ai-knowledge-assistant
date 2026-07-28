from datetime import datetime, timedelta
from jose import jwt

from app.core.config import SECRET_KEY, ALGORITHM


def create_access_token(data: dict, expires_minutes: int = 30):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt