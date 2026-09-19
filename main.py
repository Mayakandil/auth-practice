import os # py needs oss to read eviroment variables 
from dotenv import load_dotenv # to read .env
from fastapi import FastAPI ,Body , Header , Query , Depends , HTTPException , Response , Security# for app = fastapi()
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder # as supabase return non json objects so we encode it to be able to jsonfy it 
from supabase import create_client , Client # Create_client-> fun conncetion/client betweeen python w supabase  , Client --> type used to indecate that the var supabase is a Supabase Client 
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
#load varibles from .env
load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("Supabase URL:", SUPABASE_URL)

#connect to supabase
supabase: Client = create_client(SUPABASE_URL , SUPABASE_KEY) #create a supabase client to connect 
#fastapi app -> supabase client -> supabase -> authentication , database , etc.

#create fastapi app
app = FastAPI()

security = HTTPBearer()

#dependecies
async def verify_user(credentials : HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
         response= supabase.auth.get_user(token)
    except Exception:
         raise HTTPException(status_code=401, detail="Invalid or expired token" )
    
    return response.user


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
        response = supabase.auth.sign_up({"email":email , "password":password}) # route -> fastapi -> email +password -> supabase.auth.sign_up() -> Supabase Auth -> new user saved in response  
        return JSONResponse(status_code=201, content={ "user": jsonable_encoder(response.user)}) # access the new user through response.user , used jsonable_encoder to trun it into an object that can be converted to json format 
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
        return JSONResponse(status_code=200,content={"access token": response.session.access_token , "refresh_token": response.session.refresh_token}) # email+pass -> Supabase Auth -> credentials correct ? -> yes -> session -> acces token (indecated success loggin , used with protected endpoints ) + refresh token (as access token doesn't live for ever the refresh token is used to get new access token )

    except Exception:
        return JSONResponse(status_code=401 , content={"error":"Invalid login credentials"})


@app.get("/public/info")
async def public_info():
    return {"message":"welcom starnger! this info is public "}

@app.get("/protected/profile")
async def protected_profile( user = Depends(verify_user)):
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }

@app.get("/protected/dashboard")
async def protected_dashboard(user = Depends(verify_user)):
    
    return {
        "message": "Welcome to your dashboard",
        "user_id": user.id,
        "email": user.email
    }

@app.post("/auth/logout",status_code=204)
async def logout(auth = Depends(verify_user)):
     supabase.auth.sign_out()
     return Response(status_code=204)
