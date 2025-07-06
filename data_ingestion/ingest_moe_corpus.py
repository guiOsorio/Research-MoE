"""
Ingest MoE research corpus:

1. Crawl ../research for .docx and .pdf files.
2. Split documents into overlapping text chunks.
3. Store chunks in both:
   • SQLite table `../chunks.db`
   • Pinecone vector index (text-embedding-3-small)
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Dict, List

import docx
import fitz  # PyMuPDF
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

import logging

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

ROOT: Path = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY: str | None = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_HOST: str | None = os.getenv("PINECONE_INDEX_HOST")

client = OpenAI(api_key=OPENAI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(host=PINECONE_INDEX_HOST)


def read_docx(path: Path) -> str:
    """Return full text of a .docx file."""
    try:
        doc = docx.Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return ""



def read_pdf(path: Path) -> str:
    """Return full text of a .pdf file."""
    try:
        pdf = fitz.open(path)
        return "".join(pdf[page].get_text() for page in range(len(pdf)))
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return ""


def chunk_text(text: str, size: int = 1000, overlap: int = 250) -> List[str]:
    """Slide a window over text and yield overlapping chunks."""
    chunks: List[str] = []
    step = size - overlap
    for start in range(0, len(text), step):
        end = start + size
        chunks.append(text[start:end])
    return chunks


def embed(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """Return embedding vector for text."""
    clean = text.replace("\n", " ")
    embedding = client.embeddings.create(
        input=[clean],
        model=model
    ).data[0].embedding
    return embedding


def insert_sqlite(chunk_id: str, content: str, db_path: Path) -> None:
    """Insert a single chunk into SQLite."""
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "INSERT INTO chunks(chunk_id, content) VALUES (?, ?)",
            (chunk_id, content),
        )
        conn.commit()


def ingest(
    corpus_dir: Path = ROOT / "research",
    db_path: Path = ROOT / "chunks.db"
) -> None:
    """Process all files under corpus_dir and sync to SQLite + Pinecone."""
    logger.info("Started processing %s → %s", corpus_dir, db_path)

    texts = {}
    for path in corpus_dir.rglob("*"):
        logger.info("Reading path %s", path)
        if path.suffix.lower() == ".docx":
            texts[path.name] = read_docx(path)
        elif path.suffix.lower() == ".pdf":
            texts[path.name] = read_pdf(path)
        logger.info("Done reading path %s", path)

    with sqlite3.connect(db_path) as conn:
        conn.execute("DROP TABLE IF EXISTS chunks") 
        conn.execute(
            "CREATE TABLE chunks(chunk_id TEXT PRIMARY KEY, content TEXT)"
        )
        conn.commit()

    for fname, text in texts.items():
        logger.info("Inserting file %s", fname)
        for i, chunk in enumerate(chunk_text(text)):
            chunk_id = f"{fname}_chunk_{i}"
            insert_sqlite(chunk_id, chunk, db_path)
            index.upsert(
                vectors=[(chunk_id, embed(chunk), {"file_name": fname})],
            )
            logger.info("Chunk %s inserted", i)
        logger.info("Done inserting file %s", fname)


if __name__ == "__main__":
    ingest()