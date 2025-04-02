from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return JSONResponse(content={"message": "Hello, World! This is Agentic Framework simple server using FastAPI."})

def main():
    # Run the server on all interfaces on port 8000 with auto-reload enabled.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
