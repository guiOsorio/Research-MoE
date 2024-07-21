# command to run app locally: poetry run uvicorn chatbot.main:app --reload
# commands to build updated docker image and run app on localhost with docker: docker-compose build THEN docker-compose up -d
# command to check containers: docker ps
# command for logs: docker logs moe-chatbot-1
# command to stop container: docker stop moe-chatbot-1
# command to remove container: docker rm moe-chatbot-1
# command to check what is running on port 8000: sudo lsof -i :8000
# command to kill what is running on a port: sudo kill -9 [PID]

# Public imports
import os
import logging
import markdown
from openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.responses import RedirectResponse

# Private imports
from chatbot.services.search import search_chunks
from chatbot.services.embedding import get_embedding
from chatbot.services.prompt import get_system_prompt, get_turn_prompt
from chatbot.services.conversation import add_session_id_to_request, get_conversation_context, update_conversation_context, session_storage

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define the root path of the project
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Load environment variables from .env file
load_dotenv(os.path.join(ROOT_PATH, ".env"))

# Initialize OpenAI API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Add middleware for session management
app.middleware("http")(add_session_id_to_request)

class QueryRequest(BaseModel):
    question: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    session_id = request.cookies.get("session_id")
    answer_html = None
    
    if session_id and session_id in session_storage:
        session_data = session_storage[session_id]
        answer_html = session_data.get("answer_html")

    return templates.TemplateResponse("index.html", {"request": request, "answer": answer_html})


@app.get("/reset-session")
async def reset_session(request: Request):
    session_id = request.cookies.get("session_id")
    
    response = RedirectResponse(url="/")
    response.delete_cookie("session_id")

    if session_id in session_storage:
        del session_storage[session_id]
    
    return response

@app.post("/submit", response_class=HTMLResponse)
async def handle_form(request: Request, question: str = Form(...)):
    
    # Conversation management
    session_id = request.state.session_id
    session_data = session_storage.get(session_id, {})
    context = get_conversation_context(session_id)

    # Get relevant info to feed to the chatbot
    resources = search_chunks(question)
    resources_str = ""
    for k in resources.keys():
        chunk_content = resources[k]['chunk_content']
        source_name = resources[k]['source_name']
        source_url = resources[k]['source_url']
        resource_str = f"""CHUNK CONTENT: {chunk_content}\nSOURCE NAME: {source_name}\nSOURCE URL: {source_url}\n\n\n"""
        resources_str += resource_str

    # Get the prompts
    system_prompt = get_system_prompt()
    turn_prompt_template = get_turn_prompt()
    turn_prompt = turn_prompt_template.format(question=question, resources=resources_str)

    logging.info(f"Context: {context}")
    # Add the system prompt to the context if it's the first interaction
    if not any(entry['role'] == 'system' for entry in context):
        context.insert(0, {"role": "system", "content": system_prompt})

    messages_to_llm = context[:]
    messages_to_llm.append({"role": "user", "content": turn_prompt})
    logging.info(f"Context passed to the LLM: {messages_to_llm}")

    # Generate the response
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.4,
            messages=messages_to_llm
        )
        answer = response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        return HTMLResponse(content="Error generating response. Please try again.", status_code=500)

    # Update the context with the new user question
    context.append({"role": "user", "content": question})
    # Update the context with the assistant's response
    context.append({"role": "assistant", "content": answer})

    # Convert Markdown to HTML
    answer_html = markdown.markdown(answer)

    # Update session
    session_data["context"] = context
    session_data["answer_html"] = answer_html
    session_storage[session_id] = session_data


    # Redirect to the root URL
    return RedirectResponse(url="/", status_code=303)
