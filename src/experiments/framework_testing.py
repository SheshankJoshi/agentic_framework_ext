
from langchain.agents import initialize_agent

from langchain.agents import initialize_agent, AgentType
# from langchain_deepseek.tools import load_deepseek_age
# from langchain_deepseek.chat_models import ChatDeepSeek
from langchain_core.tools import Tool
from functools import partial
from tools import *
from llm_init import llm

import os
import requests
from pydantic import BaseModel, Field

# Set up environment variables with necessary credentials and keys.
# os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"
# os.environ["CUSTOM_SEARCH_ENGINE_ID"] = "YOUR_CSE_ID"
# print("Google Search ID", os.getenv("GOOGLE_API_KEY"))

class response_format(BaseModel):
    text: str = Field("Consists of the response in plain simple text")

# Initialize the language model

# llm = llm.with_structured_output(response_format.model_json_schema())
# Define tools available to the agent


if __name__ == "__main__":
    from agents import agent
    def run_agent(query: str):
        result = agent.invoke(query)
        return result
    result = agent.invoke("which stock is currently the best projected performing stock. Can you get some stock details with numbers ?")
    # response_format = {"type":"json_schema", "json_schema":"{'text':'response in text format'}"}
    # import gradio as gr
    # gr.Interface(fn=run_agent, inputs="text", outputs="text").launch()
    
    # Streamlit Input Box
    # import streamlit as st
    # user_query = st.text_input("🔍 Enter your query:")

    # if user_query:
    #     with st.spinner("🤖 Thinking..."):
    #         result = agent.invoke(user_query, return_only_outputs=True)
    #         st.subheader("💡 Agent Response")
    #         st.write(result)
