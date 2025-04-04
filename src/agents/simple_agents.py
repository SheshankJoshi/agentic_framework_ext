from langchain import Agent, Tool, LLMChain
from experiments.tools import some_existing_tool
from lmstudio import Model
# Initialize the model
model = Model(api_key="your_api_key_here")
# Create a tool from some_existing_tool
my_tool = Tool(name="some_existing_tool", func=some_existing_tool)
# Define a list of tools
tools = [my_tool]
# Create an LLMChain for the agent to use
llm_chain = LLMChain(llm=model, prompt="You are a helpful assistant.")
# Initialize the agent with the tools and LLMChain
agent = Agent(tools=tools, llm_chain=llm_chain)
# Use the agent to answer a question
response = agent.run("What is the answer to life, the universe, and everything?")
print(response)
