import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from tools import fetch_overdue_accounts, fetch_retailer_outstanding

load_dotenv()


# --- Build Agent ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY
)

tools = [fetch_overdue_accounts, fetch_retailer_outstanding]

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