import os # py needs oss to read eviroment variables 
from dotenv import load_dotenv # to read .env
from fastapi import FastAPI ,Body # for app = fastapi()
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from supabase import create_client , Client # bn3mel fun conncetion betweeen client w supabase 

#load varibles from .env
load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("Supabase URL:", SUPABASE_URL)

#connect to supabase
supabase: Client = create_client(SUPABASE_URL , SUPABASE_KEY)

#create fastapi app
app = FastAPI()

#home route
@app.get("/")
def home ():
    return {"message": "Server running and connected to Supabase"}


#SIGNUP
@app.post("/auth/signup")
async def signup(data:dict = Body(...)):

    email = data.get("email")
    password = data.get("password")

    #validate input 
    if not email or not password :
        return JSONResponse( status_code=400, content={"error":"email and password are required"})
    try:
        response = supabase.auth.sign_up({"email":email , "password":password})
        return JSONResponse(status_code=201, content={ "user": jsonable_encoder(response.user)})
    except Exception as e :
        return JSONResponse(status_code=400,content={"error":str(e)})


#LOGIN
@app.post("/auth/login")
async def login(data: dict=Body(...)):

    email = data.get("email")
    password = data.get("password")

    #validation
    if not email or not password:
        return JSONResponse(status_code=400, content={"error":"email and password are required"})

    try:
        response = supabase.auth.sign_in_with_password({"email":email, "password":password})
        return JSONResponse(status_code=200,content={"access token": response.session.access_token , "refresh_token": response.session.refresh_token})

    except Exception:
        return JSONResponse(status_code=401 , content={"error":"Invalid login credentials"})



