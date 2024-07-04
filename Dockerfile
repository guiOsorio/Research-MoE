# Use an official Python runtime as a parent image
FROM python:3.12.2-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the FastAPI application code into the container at /usr/src/app
COPY ./chatbot ./chatbot

# Copy the Poetry configuration files into the container at /usr/src/app
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN pip install poetry

# Configure Poetry: Do not create a virtual environment, install dependencies globally
RUN poetry config virtualenvs.create false

# Install project dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED 1

# Run the application:
CMD ["uvicorn", "chatbot.main:app", "--host", "0.0.0.0", "--port", "8000"]
