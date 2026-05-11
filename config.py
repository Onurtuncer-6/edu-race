# config.py
import os;
from dotenv import load_dotenv;

load_dotenv();

class Config:
    # General Configurations
    PORT = 3000;
    DEBUG = True;

    # Json Arrangement Configurations
    JSON_AS_ASCII = False;
    JSON_SORT_KEYS = False;


    SECRET_KEY = "onur_macbook_secret";
    SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
    SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY")