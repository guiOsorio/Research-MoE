from pinecone import Pinecone
import sqlite3
import os
from typing import List
from chatbot.services.embedding import get_embedding
from dotenv import load_dotenv

# Define the root path of the project
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

# Load environment variables from .env file
load_dotenv(os.path.join(ROOT_PATH, ".env"))

# Initialize Pinecone
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_INDEX_HOST = os.getenv('PINECONE_INDEX_HOST')
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(host=PINECONE_INDEX_HOST)

# Connect to SQLite database
conn = sqlite3.connect(os.path.join(ROOT_PATH, 'chunks.db'))

def search_chunks(query: str, top_k: int = 10) -> List[str]:
    """
    Search for the most relevant chunks based on the query.
    """
    # Get embedding for the query
    query_embedding = get_embedding(query)
    
    # Perform the search in Pinecone
    search_results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=False
    )

    # Retrieve content from SQLite based on search results
    resources = []
    for match in search_results['matches']:
        chunk_id = match['id']
        content = get_chunk_content(chunk_id)
        if content:
            resources.append(content)

    return resources

def get_chunk_content(chunk_id: str) -> str:
    """
    Retrieve the content of a chunk from SQLite based on the chunk_id.
    """
    cursor = conn.cursor()
    cursor.execute('SELECT content FROM chunks WHERE chunk_id = ?', (chunk_id,))
    result = cursor.fetchone()
    return result[0] if result else None
