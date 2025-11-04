
from fastapi import FastAPI, HTTPException, Depends,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from authentication import create_access_token, get_current_user, oauth2_scheme
from users import users_db
from user import User


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Authentication Example"}


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or user.password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}. You are authenticated!"}