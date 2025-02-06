import os
import gdown
import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException
from faiss_voronoid import FaissIndex
from sentence_transformers import SentenceTransformer

router = APIRouter()

# Google Drive File ID for embeddings file
GDRIVE_FILE_ID = "13DMY2d_ApmoGJpPl5vv8gAsCQjmldsqd"  # Replace with your actual Google Drive file ID
EMBEDDINGS_FILE = "data/sbert_embeddings.npz"
MOVIES_CSV = "data/movies_with_keywords.csv"

# Function to download the embeddings file if missing
def download_embeddings():
    os.makedirs("data", exist_ok=True)  # Ensure the "data" folder exists
    url = f"https://drive.google.com/uc?id={GDRIVE_FILE_ID}"
    print(f"Downloading embeddings from {url}...")
    gdown.download(url, EMBEDDINGS_FILE, quiet=False)

# Check if embeddings file exists, otherwise download it
if not os.path.exists(EMBEDDINGS_FILE):
    download_embeddings()

# Load dataset
df = pd.read_csv(MOVIES_CSV)

# Load SBERT model and FAISS index
sbert_model = SentenceTransformer("all-mpnet-base-v2")
faiss_index = FaissIndex(EMBEDDINGS_FILE)

@router.get("/search")
def search_movies(query: str, top_k: int = 5):
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    query_embedding = sbert_model.encode(query).reshape(1, -1)
    indices = faiss_index.search(query_embedding, top_k)[0]

    results = []
    for idx in indices:
        results.append({
            "title": df.iloc[idx]["title"],
            "overview": df.iloc[idx]["overview"],
            "release_date": df.iloc[idx]["release_date"],
            "runtime": int(df.iloc[idx]["runtime"]),
        })
    
    return results
