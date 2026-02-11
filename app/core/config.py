import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
FRONTEND_URL = os.getenv("FRONTEND_URL")
