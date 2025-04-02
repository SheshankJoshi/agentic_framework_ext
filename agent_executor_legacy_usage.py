from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate

from llm_init import llm
model = llm


@tool
def get_user_age(name: str) -> str:
    """Use this tool to find the user's age."""
    # This is a placeholder for the actual implementation
    if "bob" in name.lower():
        return "42 years old"
    return "41 years old"


tools = [get_user_age]

prompt = ChatPromptTemplate.from_messages(
    [
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# Construct the Tools agent
agent = create_tool_calling_agent(model, tools, prompt)
# Instantiate memory
memory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=True)

# Create an agent
agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,  # Pass the memory to the executor
)

# Verify that the agent can use tools
print(agent_executor.invoke({"input": "hi! my name is bob what is my age?"}))
print()
# Verify that the agent has access to conversation history.
# The agent should be able to answer that the user's name is bob.
print(agent_executor.invoke({"input": "do you remember my name?"}))
