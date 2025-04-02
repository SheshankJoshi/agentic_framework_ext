from langchain_deepseek.api import RestAPI

handler = RestAPI(base_url="http://localhost:1234/v1", ,
                  api_key="not_needed",
                  )

headers = {
    "Content-Type": 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer token'
}

result = handler.