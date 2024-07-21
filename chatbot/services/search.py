## Deals with embedding search through Pinecone

# Public imports
from pinecone import Pinecone
import sqlite3
import os
from typing import List
from dotenv import load_dotenv

# Private imports
from chatbot.services.embedding import get_embedding

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

def search_chunks(query: str, top_k: int = 16) -> List[str]:
    """
    Search for the most relevant chunks based on the query.
    """
    # Get embedding for the query
    query_embedding = get_embedding(query)
    
    # Perform the search in Pinecone
    search_results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    # Retrieve content from SQLite based on search results
    resources = {}
    for match in search_results['matches']:
        chunk_id = match['id']
        resources[chunk_id] = {}
        content = get_chunk_content(chunk_id)
        chunk_content = content[0]
        source_name = content[1]
        source_url = content[2]
        if content:
            resources[chunk_id]['chunk_content'] = chunk_content
            resources[chunk_id]['source_name'] = source_name
            resources[chunk_id]['source_url'] = source_url
    return resources

def get_chunk_content(chunk_id: str) -> str:
    """
    Retrieve the content of a chunk from SQLite based on the chunk_id.
    """
    cursor = conn.cursor()
    cursor.execute('SELECT content, source_name, source_url FROM chunks WHERE chunk_id = ?', (chunk_id,))
    result = cursor.fetchone()
    return result if result else None
