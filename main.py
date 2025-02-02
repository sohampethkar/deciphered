#loginregister/main.py
from fastapi import FastAPI, Request, APIRouter,Depends,Form,HTTPException,Response
import aiomysql
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine
from connection import get_mysql_connection
from Crypto.Hash import HMAC, SHA256, SHA384, SHA512
from sqlalchemy.orm import Session
from scurity import get_password_hash,verify_password, create_access_token, verify_token, COOKIE_NAME
from starlette.responses  import RedirectResponse
# Repository
from repositoryuser import UserRepository, SendEmailVerify
 
# Model
from models import UserModel
 
templates = Jinja2Templates(directory="templates")
 
app = FastAPI()
app.mount("/static",StaticFiles(directory="static",html=True),name="static")
 
#db engin
SQLALCHEMY_DATABASE_URL = 'mysql+pymsql://root:#IITbombay71@127.0.0.1:3306/mini_project'
Base.metadata.create_all(bind=create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}))
 
@app.get("/")
def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about")
def about_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/user/signup")
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})
 
@app.post("/signupuser")
async def signup_user(username: str = Form(), email: str = Form(), password: str = Form(), db=Depends(get_mysql_connection)):
    print(username)
    print(email)
    print(password)
    userRepository = UserRepository(db)
    db_user = userRepository.get_user_by_username(username)
    
    if db_user:
        return "username is not valid"

    signup = UserModel(email=email, username=username, password=get_password_hash(password))
    success = userRepository.create_user(signup)
    token = create_access_token(signup)
    SendEmailVerify.sendVerify(token)
    
    if success:
        return "create  user successfully"
    else:
        raise HTTPException(status_code=401, detail="Credentials not correct")
        
 
@app.get("/user/signin")
def login(req: Request):
    return templates.TemplateResponse("signin.html", {"request": req})

 
@app.post("/signinuser")
async def signin_user(response: Response, db=Depends(get_mysql_connection), username: str = Form(), password: str = Form()):
    userRepository = UserRepository(db)
    db_user = userRepository.get_user_by_username(username)
    
    if not db_user:
        return "username or password is not valid"

    if verify_password(password, db_user.password):
        token = create_access_token(db_user)
        response.set_cookie(
            key=COOKIE_NAME,
            value=token,
            httponly=True,
            expires=1800
        )
        return {COOKIE_NAME: token, "token_type": "cairocoders"}
 
@app.get('/user/verify/{token}')
async def verify_user(token, db=Depends(get_mysql_connection)):
    userRepository = UserRepository(db)
    payload = verify_token(token)
    username = payload.get("username")
    db_user = userRepository.get_user_by_username(username)
    
    if not username:
        raise HTTPException(status_code=401, detail="Credentials not correct")
    
    if db_user.is_active == True:
        return "Your account has already been activated"

    db_user.is_active = True
    await db.commit()  # Await commit operation as we are using an asynchronous database connection

    response = RedirectResponse(url="/user/signin")
    return response
    #http://127.0.0.1:8000/user/verify/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNseWRleTAxMzEiLCJlbWFpbCI6ImNseWRleUBnbWFpbC5jb20iLCJyb2xlIjoidXNlciIsImFjdGl2ZSI6ZmFsc2V9.BKektCLzr47qn-fRtnGVulSdYlcMdemJQO_p32jWDk0