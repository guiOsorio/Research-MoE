# command to run app locally: poetry run uvicorn chatbot.main:app --reload
# commands to build updated docker image and run app on localhost with docker: docker-compose build THEN docker-compose up -d
# command to check containers: docker ps
# command for logs: docker logs moe-chatbot-1
# command to stop container: docker stop moe-chatbot-1
# command to remove container: docker rm moe-chatbot-1
# command to check what is running on port 8000: sudo lsof -i :8000
# command to kill what is running on a port: sudo kill -9 [PID]

import sys
import os
# print(f"HERE {sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))}")


from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from chatbot.services.search import search_chunks
from chatbot.services.embedding import get_embedding
from chatbot.services.prompt import get_system_prompt, get_turn_prompt
from openai import OpenAI

from dotenv import load_dotenv

# Define the root path of the project
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Load environment variables from .env file
load_dotenv(os.path.join(ROOT_PATH, ".env"))

# Initialize OpenAI API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class QueryRequest(BaseModel):
    question: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def handle_form(request: Request, question: str = Form(...)):
    # Get relevant info to feed to the chatbot
    resources = search_chunks(question)
    resources_str = "\n".join(resources)

    # Get the prompts
    system_prompt = get_system_prompt()
    turn_prompt_template = get_turn_prompt()
    turn_prompt = turn_prompt_template.format(question=question, resources=resources_str)
    
    # Generate the response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.4,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": turn_prompt},
        ]
    )

    answer = response.choices[0].message.content

    return templates.TemplateResponse("index.html", {"request": request, "answer": answer})
