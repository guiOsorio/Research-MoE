# command to run app locally: poetry run uvicorn main:app --reload
# commands to build updated docker image and run app on localhost with docker: docker-compose build THEN docker-compose up -d
# command to check containers: docker ps
# command for logs: docker logs moe-chatbot-1
# command to stop container: docker stop moe-chatbot-1
# command to remove container: docker rm moe-chatbot-1
# command to check what is running on port 8000: sudo lsof -i :8000
# command to kill what is running on a port: sudo kill -9 [PID]

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    text = "Chatbot_test"
    return text