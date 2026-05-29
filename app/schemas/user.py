from pydantic import BaseModel


class UserCreate(BaseModel):

    email:str
    password:str
    role:str="user"



class UserLogin(BaseModel):

    email:str
    password:str    