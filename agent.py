import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from supabase_client import get_overdue_accounts

load_dotenv()

# --- Define Tools ---
@tool
def fetch_overdue_accounts(query: str) -> str:
    """
    Fetches all receivables data from the database including retailer names,
    invoice numbers, outstanding balances, and aging days.
    Use this for ANY question about retailers, outstanding payments, overdue invoices,
    defaulters, total amounts, lists of parties, or any accounts receivable question.
    """
    data = get_overdue_accounts()

    if isinstance(data, dict) and "error" in data:
        return data["error"]

    if not data:
        return "No overdue accounts found in the database."

    total = sum(r.get("closing_balance", 0) for r in data)
    top3 = data[:3]

    summary = f"📊 **Total Outstanding: ₹{total:,.2f}**\n"
    summary += f"📋 **Total Overdue Accounts: {len(data)}**\n\n"
    summary += "**Top 3 Defaulters:**\n"
    for i, r in enumerate(top3, 1):
        summary += (
            f"{i}. {r['retailer_name']} — "
            f"₹{r['closing_balance']:,.2f} "
            f"({r['aging_days']} days overdue, "
            f"Invoice: {r['invoice_number']})\n"
        )

    summary += "\n**All Overdue Accounts:**\n"
    for r in data:
        summary += (
            f"• {r['retailer_name']} | "
            f"₹{r['closing_balance']:,.2f} | "
            f"{r['aging_days']} days | "
            f"Invoice #{r['invoice_number']}\n"
        )

    return summary


# --- Build Agent ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)

tools = [fetch_overdue_accounts]
agent = create_react_agent(llm, tools)


# --- Run Agent ---
def run_agent(user_message: str) -> str:
    try:
        result = agent.invoke({
            "messages": [HumanMessage(content=user_message)]
        })
        last_message = result["messages"][-1]
        
        # Handle both string and list content formats
        if isinstance(last_message.content, str):
            return last_message.content
        elif isinstance(last_message.content, list):
            return " ".join(
                part["text"] for part in last_message.content
                if isinstance(part, dict) and "text" in part
            )
        else:
            return str(last_message.content)
    except Exception as e:
        return f"❌ Agent error: {str(e)}"