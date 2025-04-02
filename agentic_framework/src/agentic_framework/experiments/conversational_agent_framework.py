#%%
from tabnanny import check
import uuid
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain.agents import AgentType, create_tool_calling_agent, AgentExecutor, create_openai_functions_agent
from llm_init import llm
import gradio as gr
from agents import web_search_tools
from prompts_templates import simple_prompt
from langgraph.prebuilt import create_react_agent

#%% Step 1 -  Define a new graph as a workflow
workflow = StateGraph(state_schema=MessagesState) # This stategraph contains the scope for bigger and better conversational flows

#%% Step 2 - Define a chat model
model = llm

#%% Step 3 - Create a new graph to capture that workflow and make it directional
# Define the function that calls the model


def call_model(state: MessagesState):
    response = model.invoke(state["messages"])
    # We return a list, because this will get added to the existing list
    return {"messages": response}

# Define the two nodes we will cycle between
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

#%% Step 4 - Introduce memory element into this 
# Adding memory is straight forward in langgraph!
memory = MemorySaver()

app = workflow.compile(
    checkpointer=memory
)
# ------ USE BELOW for SIMPLE MEMORY EXEUCTION --------
# input_message = HumanMessage(content="hi! I'm bob")
# for event in app.stream({"messages": [input_message]}, config, stream_mode="values"):
#     event["messages"][-1].pretty_print()

# # Here, let's confirm that the AI remembers our name!
# input_message = HumanMessage(content="what was my name?")
# for event in app.stream({"messages": [input_message]}, config, stream_mode="values"):
#     event["messages"][-1].pretty_print()
# -----------------------------------------------------


#%% Step 5 - Creating a framework for thread storage
# The thread id is a unique key that identifies this particular conversation.
# We'll just generate a random uuid here.
# This enables a single application to manage conversations among multiple users.
thread_id = uuid.uuid4()
config = {"configurable": {"thread_id": str(thread_id)}}


#%% Step 7 - Create a prompt for the agent to give to llm
prompt_template = simple_prompt  # Place all the prompts into one single place


#%% Step 6 - Creating an agent and attaching a memory element to it
# Modify the agent to include memory
agent = create_react_agent( # This is not compatible with DeepSeek now
    tools=web_search_tools,
    model=llm,
    prompt = prompt_template, 
    checkpointer=memory
    # Ensures follow-up questions are understood
)

# agent = create_openai_functions_agent(
#     tools=web_search_tools,
#     llm=llm,
#     prompt=prompt_template,
#     # checkpointer=memory
#     # Ensures follow-up questions are understood
# )

#%% Step 7 - Create an agent executor and attach our agent to it
executor = AgentExecutor(agent=agent, 
                         tools=web_search_tools, 
                         checkpointer=memory,
                         verbose=True, 
                         return_intermediate_steps=True, 
                         early_stopping_method="generate")
#%%
def chat(query):
    RECURSION_LIMIT = 2 * 3 + 1
    for chunk in executor.stream({"input": query},
                                {"recursion_limit": RECURSION_LIMIT}):
        chunk["messages"][-1].pretty_print()
    # chunk = executor.invoke({"input": query})
    return chunk["messages"][-1].content
# Launch Gradio interface
# gr.Interface(
#     fn=chat,
#     inputs=gr.Textbox(label="Ask a question"),
#     outputs=gr.Textbox(label="Response"),
#     title="Conversational AI Agent",
#     description="Ask questions and follow up based on previous responses.",
#     live=True
# ).launch()

#%%
# if __name__ == "__main__":
#     from pprint import pprint
while True:
    inp = input("You: ")
    if inp == "exit":
        break
    else:
        resp = chat(inp)
        pprint("System : " , resp)

#%%




# def run_agent(query: str):
#     result = agent.invoke({"input": query})
#     return result


# # Function to handle conversation
# def chat(user_query, history):
#     response = agent.invoke({"input": user_query})
#     memory.save_context({"input": user_query}, {"output": response})
#     return response



