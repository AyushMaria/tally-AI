import requests
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_overdue_accounts(min_aging_days=0):
    url = f"{SUPABASE_URL}/rest/v1/receivables"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    params = {
        "select": "retailer_name,invoice_number,closing_balance,aging_days",
        "aging_days": f"gte.{min_aging_days}",   # ← filter in DB, not in Python
        "order": "aging_days.desc",
        "limit": "100"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Supabase error: {response.status_code} — {response.text}"}


def get_retailer_outstanding(retailer_name: str):
    url = f"{SUPABASE_URL}/rest/v1/receivables"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    params = {
        "select": "*",
        "retailer_name": f"ilike.*{retailer_name}*",  # case-insensitive partial match
        "order": "aging_days.desc"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Supabase error: {response.status_code} — {response.text}"}