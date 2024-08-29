from supabase import create_client, Client
import os
from dotenv import load_dotenv
load_dotenv()
url= os.environ.get("SUPABASE_URL")
key= os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
print(f"SUPABASE_URL: {url}")
print(f"SUPABASE_KEY: {key}")
def init_db(app=None):
    global supabase
    supabase = create_client(url, key)
