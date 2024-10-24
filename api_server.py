from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define the data model
class Greeting(BaseModel):
    message: str

# Create a FastAPI app instance
app = FastAPI()

# GET endpoint
@app.get("/hello", response_model=Greeting)
async def get_hello():
    logging.info("Handling GET /hello request")
    response = Greeting(message="Hello, world!")
    logging.info(f"GET /hello response: {response}")
    return response

# POST endpoint
@app.post("/greet", response_model=Greeting)
async def post_greeting(payload: Greeting):
    logging.info(f"Handling POST /greet request with payload: {payload}")
    response = Greeting(message=f"Hello, {payload.message}!")
    logging.info(f"POST /greet response: {response}")
    return response

# Entry point for running the server
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3000)
