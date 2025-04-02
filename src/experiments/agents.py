from langchain.agents import initialize_agent, AgentType
from tools import *
from llm_init import llm

web_search_tools = [web_search, analyze_text, summarize_text]

# # Initialize the agent with the tools and a specific agent type
# This is a normal agent with tools. The agent can be having a checkpointer or memory too for continued conversations.
web_search_agent = initialize_agent(
    web_search_tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
