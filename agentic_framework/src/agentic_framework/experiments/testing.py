from typing import Optional, Type
from pydantic import Field, BaseModel
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import tool
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI


llm: ChatOpenAI = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    temperature=0,
    api_key="not-needed"
)


@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    print("Using tool")
    return len(word)


tools = [get_word_length]
llm_with_tools = llm.bind_tools(tools=tools)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are very powerful assistant, but don't know current events",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
res = list(agent_executor.stream(
    {"input": "what is the length of characters in the word eudca"}))
print(res)
