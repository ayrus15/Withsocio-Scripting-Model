"""
Embedding generation and FAISS index management.
Handles document embedding and index creation/loading.
"""
import json
import os
from typing import List, Dict, Any
import numpy as np
import faiss
from openai import OpenAI

from app.utils.config import settings


class EmbeddingService:
    """Service for generating embeddings and managing FAISS index."""
    
    def __init__(self):
        """Initialize the embedding service with OpenAI client."""
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.embedding_model = settings.openai_embedding_model
        self.index = None
        self.metadata = []
        
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding
    
    def generate_embeddings_batch(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            Numpy array of embeddings
        """
        embeddings = []
        for text in texts:
            embedding = self.generate_embedding(text)
            embeddings.append(embedding)
        return np.array(embeddings, dtype=np.float32)
    
    def create_index(self, documents: List[Dict[str, Any]]) -> None:
        """
        Create FAISS index from documents.
        
        Args:
            documents: List of documents with 'text' and metadata fields
        """
        # Extract texts
        texts = [doc['text'] for doc in documents]
        
        # Generate embeddings
        embeddings = self.generate_embeddings_batch(texts)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        
        # Store metadata
        self.metadata = [
            {k: v for k, v in doc.items() if k != 'text'}
            for doc in documents
        ]
        
    def save_index(self, index_path: str = None, metadata_path: str = None) -> None:
        """
        Save FAISS index and metadata to disk.
        
        Args:
            index_path: Path to save index file
            metadata_path: Path to save metadata file
        """
        if index_path is None:
            index_path = settings.faiss_index_path
        if metadata_path is None:
            metadata_path = settings.faiss_metadata_path
            
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        
        # Save index
        faiss.write_index(self.index, index_path)
        
        # Save metadata
        with open(metadata_path, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def load_index(self, index_path: str = None, metadata_path: str = None) -> None:
        """
        Load FAISS index and metadata from disk.
        
        Args:
            index_path: Path to index file
            metadata_path: Path to metadata file
        """
        if index_path is None:
            index_path = settings.faiss_index_path
        if metadata_path is None:
            metadata_path = settings.faiss_metadata_path
            
        # Load index
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
        else:
            raise FileNotFoundError(f"Index file not found: {index_path}")
        
        # Load metadata
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
        else:
            raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
