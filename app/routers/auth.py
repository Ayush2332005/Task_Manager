from app.schemas import UserCreate
from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)

from jose import jwt, JWTError


from app.database import SessionLocal
from app.models import User

from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# database session

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



# signup

@router.post("/signup")
def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email exists"
        )

    new_user = User(
        email=user.email,
        password=hash_password(
            user.password
        ),
        role=user.role
    )

    db.add(new_user)
    db.commit()

    return {
        "message":"created"
    }

    existing = db.query(User).filter(
        User.email == user.email
    ).first()


    if existing:

        raise HTTPException(
            status_code=400,
            detail="Email exists"
        )


    new_user = User(

        email=user.email,

        password=hash_password(
            user.password
        ),

        role=user.role
    )


    db.add(new_user)

    db.commit()


    return {
        "message":"created"
    }



# login

@router.post("/login")
def login(

    form_data:
    OAuth2PasswordRequestForm
    =Depends(),

    db:Session=Depends(get_db)
):


    user = db.query(User).filter(

        User.email ==
        form_data.username

    ).first()



    if not user:

        raise HTTPException(
            401,
            "Invalid user"
        )



    if not verify_password(

        form_data.password,

        user.password

    ):

        raise HTTPException(
            401,
            "Wrong password"
        )



    token=create_access_token(
        {
        "sub":user.email,
        "role":user.role
        }
    )


    return {

        "access_token":token,

        "token_type":"bearer"
    }




# current user

def get_current_user(

    token:str=Depends(
        oauth2_scheme
    )
):


    try:

        payload=jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[ALGORITHM]

        )


        return {

        "email":
        payload.get("sub"),

        "role":
        payload.get("role")

        }


    except JWTError:


        raise HTTPException(

            401,

            "Invalid token"

        )




# profile

@router.get("/profile")
def profile(

    user=Depends(
        get_current_user
    )

):

    return user