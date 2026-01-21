"""
Retrieval service for finding relevant examples using FAISS.
Implements filtered semantic search based on metadata.
"""
from typing import List, Dict, Any, Optional
import numpy as np

from app.rag.embed import EmbeddingService
from app.utils.config import settings


class RetrievalService:
    """Service for retrieving relevant examples from FAISS index."""
    
    def __init__(self):
        """Initialize retrieval service with embedding service."""
        self.embedding_service = EmbeddingService()
        self._load_or_initialize_index()
    
    def _load_or_initialize_index(self) -> None:
        """Load existing index or initialize with sample data."""
        try:
            self.embedding_service.load_index()
        except FileNotFoundError:
            # Initialize with sample data if index doesn't exist
            self._initialize_sample_index()
    
    def _initialize_sample_index(self) -> None:
        """Initialize index with sample high-performing examples."""
        sample_documents = [
            {
                "text": "Hook: Are you tired of wasting money on gym memberships you never use? Body: Discover how our AI creates personalized home workouts that fit YOUR schedule. No equipment needed. Results in 30 days or money back. CTA: Download FitLife Pro now!",
                "sector": "fitness",
                "hook_type": "question",
                "emotion": "frustration",
                "performance_level": "high",
                "engagement_rate": 8.5
            },
            {
                "text": "Hook: This one trick changed my entire financial future. Body: I automated my savings without thinking about it. Set up smart rules, watch your money grow. No complex spreadsheets. CTA: Start your free trial today!",
                "sector": "finance",
                "hook_type": "bold_claim",
                "emotion": "curiosity",
                "performance_level": "high",
                "engagement_rate": 9.2
            },
            {
                "text": "Hook: POV: You finally found jeans that actually fit. Body: Custom measurements. Premium denim. Delivered to your door. We analyzed 10,000 body types to create the perfect fit algorithm. CTA: Get measured now!",
                "sector": "fashion",
                "hook_type": "relatable",
                "emotion": "excitement",
                "performance_level": "high",
                "engagement_rate": 7.8
            },
            {
                "text": "Hook: Your skin is crying for help and you don't even know it. Body: 97% of people use the wrong products for their skin type. Our AI analyzes your skin in 60 seconds and recommends the perfect routine. Dermatologist approved. CTA: Take the skin quiz now!",
                "sector": "beauty",
                "hook_type": "shocking",
                "emotion": "urgency",
                "performance_level": "high",
                "engagement_rate": 8.9
            },
            {
                "text": "Hook: Stop scrolling - this will save you 10 hours this week. Body: Productivity isn't about doing more. It's about doing what matters. Our AI prioritizes your tasks based on impact. Join 50,000+ professionals. CTA: Try it free for 14 days!",
                "sector": "productivity",
                "hook_type": "bold_claim",
                "emotion": "curiosity",
                "performance_level": "high",
                "engagement_rate": 9.5
            },
            {
                "text": "Hook: What if your pet could tell you exactly what they need? Body: Our smart collar monitors health, activity, and mood. Get alerts before problems start. Vet-designed technology. 30-day guarantee. CTA: Shop now and save 20%!",
                "sector": "pets",
                "hook_type": "question",
                "emotion": "curiosity",
                "performance_level": "high",
                "engagement_rate": 8.1
            },
            {
                "text": "Hook: I spent $10,000 on courses so you don't have to. Body: Everything you need to launch your online business in one place. Step-by-step system. Real results. No fluff. 1000+ success stories. CTA: Join the waitlist now!",
                "sector": "education",
                "hook_type": "relatable",
                "emotion": "excitement",
                "performance_level": "high",
                "engagement_rate": 9.0
            },
            {
                "text": "Hook: Your morning routine is sabotaging your entire day. Body: Science-backed morning rituals that actually work. Personalized to your chronotype. Track your energy levels. Feel the difference in 7 days. CTA: Download the app free!",
                "sector": "wellness",
                "hook_type": "shocking",
                "emotion": "urgency",
                "performance_level": "high",
                "engagement_rate": 8.7
            }
        ]
        
        self.embedding_service.create_index(sample_documents)
        self.embedding_service.save_index()
    
    def retrieve(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant examples based on query and optional filters.
        
        Args:
            query: Search query text
            filters: Optional metadata filters (e.g., {'sector': 'fitness', 'hook_type': 'question'})
            top_k: Number of results to return (defaults to settings.top_k_results)
            
        Returns:
            List of relevant documents with metadata and similarity scores
        """
        if top_k is None:
            top_k = settings.top_k_results
        
        # Generate query embedding
        query_embedding = np.array([self.embedding_service.generate_embedding(query)], dtype=np.float32)
        
        # Search in FAISS index (get more results for filtering)
        search_k = top_k * 3 if filters else top_k
        distances, indices = self.embedding_service.index.search(query_embedding, search_k)
        
        # Collect results with metadata
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.embedding_service.metadata):
                result = {
                    **self.embedding_service.metadata[idx],
                    "similarity_score": float(1 / (1 + distance))  # Convert distance to similarity
                }
                
                # Apply filters if provided
                if filters:
                    match = all(
                        result.get(key) == value
                        for key, value in filters.items()
                    )
                    if match:
                        results.append(result)
                else:
                    results.append(result)
                
                # Stop if we have enough results
                if len(results) >= top_k:
                    break
        
        return results[:top_k]
    
    def retrieve_for_generation(
        self,
        brand_profile: Dict[str, Any],
        script_request: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Retrieve examples specifically for script generation.
        
        Args:
            brand_profile: Brand profile dictionary
            script_request: Script request dictionary
            
        Returns:
            List of relevant high-performing examples
        """
        # Create query from brand and request
        query = f"Generate {script_request['hook_type']} hook for {brand_profile['sector']} sector targeting {script_request['emotion']} emotion"
        
        # Create filters
        filters = {
            "sector": brand_profile['sector'],
            "performance_level": "high"
        }
        
        # Retrieve relevant examples
        return self.retrieve(query, filters=filters)
