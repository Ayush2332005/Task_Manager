from passlib.context import CryptContext

from jose import jwt

from datetime import (
    datetime,
    timedelta
)

import os

from dotenv import load_dotenv


load_dotenv()


SECRET_KEY=os.getenv(
    "SECRET_KEY"
)

ALGORITHM=os.getenv(
    "ALGORITHM"
)


pwd_context=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password):

    return pwd_context.hash(
        password
    )


def verify_password(
        plain,
        hashed
):

    return pwd_context.verify(
        plain,
        hashed
    )



def create_access_token(
        data:dict
):

    to_encode=data.copy()

    expire=datetime.utcnow()+timedelta(
        minutes=15
    )

    to_encode.update(
        {"exp":expire}
    )


    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )