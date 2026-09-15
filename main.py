import os # py needs oss to read eviroment variables 
from dotenv import load_dotenv # to read .env
from fastapi import FastAPI  # for app = fastapi()
from supabase import create_client , Client # bn3mel fun conncetion betweeen client w supabase 


load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


supabase: Client = create_client(SUPABASE_URL , SUPABASE_KEY)


app = FastAPI()


@app.get("/")
def home ():
    return {"message": "Server running and connected to Supabase"}

