import requests
import os
from langchain_core.tools import tool
from supabase_client import get_overdue_accounts, get_retailer_outstanding

@tool
def fetch_overdue_accounts(min_aging_days: int = 0) -> str:
    """
    Fetches all overdue receivables from the database.
    Use min_aging_days to filter (e.g., 30 means only accounts overdue by 30+ days).
    Returns retailer names, invoice numbers, balances, and aging days.
    """
    data = get_overdue_accounts(min_aging_days=min_aging_days)

    if isinstance(data, dict) and "error" in data:
        return data["error"]

    if not data:
        return "No overdue accounts found."

    total = sum(r.get("closing_balance", 0) for r in data)
    result = f"📋 **Overdue Accounts (>{min_aging_days} days)** — {len(data)} records\n"
    result += f"💰 **Total Outstanding: ₹{total:,.2f}**\n\n"
    for r in data:
        result += (
            f"• {r['retailer_name']} | "
            f"Invoice #{r['invoice_number']} | "
            f"₹{r['closing_balance']:,.2f} | "
            f"{r['aging_days']} days\n"
        )
    return result


@tool
def fetch_retailer_outstanding(retailer_name: str) -> str:
    """
    Fetches outstanding balance for a specific retailer by their name.
    Use this when the user asks about a specific retailer, party, or shop by name.
    Supports partial name matching (e.g., 'Sharma' will match 'Sharma Traders').
    """
    data = get_retailer_outstanding(retailer_name)

    if isinstance(data, dict) and "error" in data:
        return data["error"]

    if not data:
        return f"❌ No retailer found matching '{retailer_name}'."

    total = sum(r.get("closing_balance", 0) for r in data)
    result = f"🏪 **Retailer: {retailer_name.title()}**\n"
    result += f"💰 **Total Outstanding: ₹{total:,.2f}**\n\n"
    result += "**Invoice Breakdown:**\n"
    for r in data:
        result += (
            f"• Invoice #{r['invoice_number']} | "
            f"₹{r['closing_balance']:,.2f} | "
            f"{r['aging_days']} days overdue\n"
        )
    return result