from langchain_openai import OpenAI

llm = OpenAI(
    base_url="http://localhost:1234/v1",
    temperature=0,
    api_key="not-needed",
    model="deepseek-r1-distill-llama-8b"
)
