# Public imports
from openai import OpenAI
import os
from dotenv import load_dotenv

# Define the root path of the project
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

# Load environment variables from .env file
load_dotenv(os.path.join(ROOT_PATH, ".env"))

# Initialize OpenAI API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI()

def get_embedding(text: str, model="text-embedding-3-small") -> list:
    """
    Generate an embedding for the given text using OpenAI's text-embedding-3-small model.
    """
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding