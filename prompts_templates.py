from langchain_core.prompts import ChatPromptTemplate
simple_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI assistant"),
        ("human", "{input}"),
        # Placeholders fill up a **list** of messages
        ("placeholder", "{agent_scratchpad}"),
    ]
)
