## Preprocesses contents of notes and papers into chunks, then inserts these chunks into a Pinecone Index

# Public imports
import os
import docx
import fitz  # PyMuPDF
from openai import OpenAI
from pinecone import Pinecone
import sqlite3
from dotenv import load_dotenv

# Private imports
from paper_names import paper_names

load_dotenv(dotenv_path="../.env")
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI()

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_INDEX_HOST = os.getenv('PINECONE_INDEX_HOST')
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(host=PINECONE_INDEX_HOST)

# Function to read .docx files
def read_docx(file_path):
    try:
        doc = docx.Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""
    

# Function to read .pdf files
def read_pdf(file_path):
    try:
        pdf_document = fitz.open(file_path)
        text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""
    
# Function to chunk text into chunks of specified size
def chunk_text(text, chunk_size=1000, overlap=250):
    start = 0
    chunks = []
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

# Function to insert chunk data into the database
def insert_chunk(chunk_id, content, source_name, source_url):
    conn = sqlite3.connect('../chunks.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO chunks (chunk_id, content, source_name, source_url) VALUES (?, ?, ?, ?)
    ''', (chunk_id, content, source_name, source_url))
    conn.commit()
    conn.close()

# Directory containing the files
directory = "../research"

# Dictionary to store file content
file_contents = {}

# Traverse the directory and read files
for root, dirs, files in os.walk(directory):
    for file in files:
        file_path = os.path.join(root, file)
        if file in ('MoE Notes FINAL.docx', 'MoE Notes.docx'):
            content = read_docx(file_path)
            file_contents[file] = {}
            file_contents[file]["content"] = content
        elif file.endswith('.pdf'):
            content = read_pdf(file_path)
            file_contents[file] = {}
            file_contents[file]["content"] = content

# Add metadata to file's info
for (file, content) in paper_names.items():
    if (file in ('MoE Notes FINAL.docx', 'MoE Notes.docx')) or (file.endswith('.pdf')):
        file_contents[file]['source_name'] = content[0]
        file_contents[file]['source_url'] = content[1]

# Chunk file contents
chunked_contents = {
    key: {
        'chunks': [],
        'source_name': '',
        'source_url': ''
    }
    for key in file_contents.keys()
}
for file, content in file_contents.items():
    chunks = chunk_text(content['content'])
    chunked_contents[file]['chunks'] = chunks
    chunked_contents[file]['source_name'] = file_contents[file]['source_name']
    chunked_contents[file]['source_url'] = file_contents[file]['source_url']

# Connect to SQLite database (it will create the database file if it doesn't exist)
conn = sqlite3.connect('../chunks.db')
cursor = conn.cursor()

# Drop the table if it exists
cursor.execute('''
DROP TABLE IF EXISTS chunks
''')

# Create a table to store chunks
cursor.execute('''
CREATE TABLE chunks (
    chunk_id TEXT PRIMARY KEY,
    content TEXT,
    source_name TEXT,
    source_url TEXT
)
''')

# Commit and close the connection
conn.commit()
conn.close()


for file, contents in chunked_contents.items():
    source_name = contents['source_name']
    source_url = contents['source_url']
    for i, chunk in enumerate(contents['chunks']):
        chunk_id = f"{file}_chunk_{i}"
        # SQLite3 insert
        insert_chunk(chunk_id, chunk, source_name, source_url)
        # Pinecone insert
        metadata = {"file_name": file, "source_name": source_name, "source_url": source_url}
        embed = get_embedding(chunk)
        upsert_response = index.upsert(
            vectors=[
                (chunk_id, embed, metadata),
            ]
        )