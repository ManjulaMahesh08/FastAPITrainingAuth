from pydantic import BaseModel

# define User model

class User(BaseModel):
    username: str
    password: str


