from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import pinecone
from sentence_transformers import SentenceTransformer
import numpy as np
import os

app = FastAPI()

# Initialize Pinecone
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV")
)

# Load sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

class VectorQuery(BaseModel):
    texts: List[str]
    namespace: Optional[str] = None
    metadata: Optional[Dict] = None

class SearchQuery(BaseModel):
    query: str
    namespace: Optional[str] = None
    top_k: int = 5

class VectorResponse(BaseModel):
    success: bool
    ids: List[str]
    error: Optional[str] = None

class SearchResponse(BaseModel):
    matches: List[Dict]
    error: Optional[str] = None

@app.post('/upsert', response_model=VectorResponse)
async def upsert_vectors(request: VectorQuery):
    try:
        # Generate embeddings
        embeddings = model.encode(request.texts)
        
        # Create vector records
        vectors = [
            (str(i), embedding.tolist(), request.metadata)
            for i, embedding in enumerate(embeddings)
        ]
        
        # Upsert to Pinecone
        index = pinecone.Index(os.getenv("PINECONE_INDEX"))
        index.upsert(vectors=vectors, namespace=request.namespace)
        
        return VectorResponse(
            success=True,
            ids=[v[0] for v in vectors]
        )
    except Exception as e:
        return VectorResponse(success=False, ids=[], error=str(e))

@app.post('/search', response_model=SearchResponse)
async def search_vectors(request: SearchQuery):
    try:
        # Generate query embedding
        query_embedding = model.encode(request.query)
        
        # Search in Pinecone
        index = pinecone.Index(os.getenv("PINECONE_INDEX"))
        results = index.query(
            vector=query_embedding.tolist(),
            namespace=request.namespace,
            top_k=request.top_k,
            include_metadata=True
        )
        
        return SearchResponse(matches=results.matches)
    except Exception as e:
        return SearchResponse(matches=[], error=str(e))

@app.get('/health')
async def health_check():
    try:
        # Check Pinecone connection
        pinecone.list_indexes()
        return {'status': 'healthy'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))