from langchain.agents import initialize_agent, AgentType
from tools import *
from llms import get_llm




if __name__ == "__main__":
    # Initialize the LLM
    # This is a wrapper for the lmstudio LLM model.
    # The model is loaded from the server and passed to the agent.
    # The server is running on localhost:1234
    # The model is loaded from the server and passed to the agent.
    # The server is running on localhost:1234
    llm = get_llm()

    web_search_tools = [web_search, analyze_text, summarize_text]

    # # Initialize the agent with the tools and a specific agent type
    # This is a normal agent with tools. The agent can be having a checkpointer or memory too for continued conversations.
    web_search_agent = initialize_agent(
        web_search_tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
