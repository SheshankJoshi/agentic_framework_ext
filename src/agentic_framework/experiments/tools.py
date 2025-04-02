from langchain.agents import initialize_agent, tool
# from langchain_deepseek.tools import load_deepseek_age
# from langchain_deepseek.chat_models import ChatDeepSeek
from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper
from dotenv import load_dotenv
load_dotenv()
from functools import partial

import os
import requests

# Set up environment variables with necessary credentials and keys.
# os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"
# os.environ["CUSTOM_SEARCH_ENGINE_ID"] = "YOUR_CSE_ID"
# print("Google Search ID", os.getenv("GOOGLE_API_KEY"))


def get_search_tool(num_results=5):
    search = GoogleSearchAPIWrapper()
    tool = Tool(
        name="google_search",
        description="Search Google for recent results.",
        func=partial(search.results, num_results=num_results)
    )
    return tool


search_tool = get_search_tool()


@tool
def web_search(query: str) -> list:
    """Search the web for information on a given query."""
    results = search_tool.run(query)
    # print("Got reponse from google as ", results)
    return [result['link'] for result in results]


@tool
def analyze_text(url: str) -> dict:
    """Analyze the text content of a given URL."""
    response = requests.get(url)  # WE can use much better scraper here
    if response.status_code == 200:
        # Limit to first 1500 characters for analysis
        text_content = response.text[:1500]
        return {"content": text_content, "status": "success"}
    else:
        return {"content": "", "status": "failed"}


@tool
def summarize_text(text: str) -> dict:
    """Summarize the given text."""
    summary = llm.invoke(f"Summarize this: {text}")
    return {"summary": summary}


@tool
def recommend_tools(summary: str) -> list:
    """Recommend tools based on the provided summary."""
    # This function is a placeholder. In practice, you would have a database or API for recommendations.
    recommendations = ["Tool A", "Tool B", "Tool C"]
    return recommendations
