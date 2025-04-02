from langchain_deepseek import ChatDeepSeek
import os
os.environ["DEEPSEEK_API_KEY"]=""
client = ChatDeepSeek(model="deepseek-r1-distill-llama-8b",
                      base_url="http:/127.0.0.1:1234/v1")

result = client.invoke("Can you tell me story about a rabbit in a forest")
print(result)

