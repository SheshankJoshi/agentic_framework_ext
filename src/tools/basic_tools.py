import requests
import os
from functools import partial
from langchain.agents import initialize_agent, tool
# from langchain_deepseek.tools import load_deepseek_age
# from langchain_deepseek.chat_models import ChatDeepSeek
from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper
from tools.implementation import *
# from dotenv import load_dotenv
# load_dotenv()


# Set up environment variables with necessary credentials and keys.
# os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"
# os.environ["CUSTOM_SEARCH_ENGINE_ID"] = "YOUR_CSE_ID"
print("Google Search ID : ", os.getenv("GOOGLE_API_KEY"))


web_search_google = Tool(
    name="google_search",
    description="Search Google for recent results.",
    func=google_search_web() # NOTE : The difference here is very clearly formatted the way partial implementation is given, for pre-configuration
)

ppt_tool = Tool(
    name="create_ppt",
    func=generate_presentation,
    description="Generates a PowerPoint presentation with provided title, content and references."
)
ref_tool = Tool(
    name="add_references",
    func=process_references,
    description="Processes and formats a list of references."
)

@tool
def analyze_url_text(url: str) -> dict:
    """Analyze the text content of a given URL and returns the first 1500 words of it."""
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
    # -- This is a just a temporary work around. Nothing here is actually the way.
    from llms.lmstudio_llm import get_llm
    llm = get_llm()
    if llm:
        summary = llm.invoke(f"Summarize this: {text}")
        return {"summary": summary}
    else:
        raise ValueError("LLM not initialized.")


# @tool
# def recommend_tools(summary: str) -> list:
#     """Recommend tools based on the provided summary."""
#     # This function is a placeholder. In practice, you would have a database or API for recommendations.
#     recommendations = ["Tool A", "Tool B", "Tool C"]
#     return recommendations
if __name__ == "__main__":
    print(web_search_google.func("best places to visit in UAE"))
