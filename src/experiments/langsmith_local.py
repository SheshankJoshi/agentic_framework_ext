import os
def setup_langsmith_local():
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = "http://localhost:8080"
    os.environ["LANGCHAIN_API_KEY"] = "your_local_api_key"
