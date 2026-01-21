"""
Pytest configuration and fixtures for the test suite.

This module provides shared fixtures and configuration for all tests.
"""

import pytest
from typing import Dict, Any
from unittest.mock import Mock, MagicMock
import numpy as np

# Sample test data
SAMPLE_BRAND_PROFILE = {
    "brand_name": "TestBrand",
    "sector": "fitness",
    "target_audience": {
        "age_range": "25-40",
        "gender": "All",
        "location": "USA",
        "pain_points": ["lack of motivation", "time constraints"]
    },
    "brand_voice": ["energetic", "motivational"],
    "offer": "AI-powered home workout plans",
    "platform": "instagram",
    "cta_style": "direct",
    "do_not_use": ["lazy", "fat"]
}

SAMPLE_SCRIPT_REQUEST = {
    "goal": "conversion",
    "hook_type": "question",
    "emotion": "curiosity",
    "script_length": 30,
    "language": "english",
    "cta": "Download the app now!"
}

SAMPLE_SCRIPT_OUTPUT = {
    "hook": "Ready to transform your fitness journey?",
    "body": "With TestBrand's AI-powered workout plans, you can achieve your goals at home. No expensive gym memberships needed. Our smart algorithms create personalized routines just for you.",
    "cta": "Download the app now and start your transformation!",
    "caption": "Your fitness journey starts at home 💪 #TestBrand",
    "hashtags": ["#FitnessGoals", "#HomeWorkout", "#TestBrand"]
}


@pytest.fixture
def sample_brand_profile() -> Dict[str, Any]:
    """Fixture providing a sample brand profile for testing."""
    return SAMPLE_BRAND_PROFILE.copy()


@pytest.fixture
def sample_script_request() -> Dict[str, Any]:
    """Fixture providing a sample script request for testing."""
    return SAMPLE_SCRIPT_REQUEST.copy()


@pytest.fixture
def sample_script_output() -> Dict[str, Any]:
    """Fixture providing a sample script output for testing."""
    return SAMPLE_SCRIPT_OUTPUT.copy()


@pytest.fixture
def sample_full_request(sample_brand_profile, sample_script_request) -> Dict[str, Any]:
    """Fixture providing a complete API request."""
    return {
        "brand_profile": sample_brand_profile,
        "script_request": sample_script_request
    }


@pytest.fixture
def mock_openai_response() -> Dict[str, Any]:
    """Fixture providing a mock OpenAI API response."""
    return {
        "id": "chatcmpl-test123",
        "object": "chat.completion",
        "created": 1234567890,
        "model": "gpt-4-turbo-preview",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": str(SAMPLE_SCRIPT_OUTPUT)
                },
                "finish_reason": "stop"
            }
        ]
    }


@pytest.fixture
def mock_embedding() -> np.ndarray:
    """Fixture providing a mock embedding vector."""
    return np.random.rand(1536).astype('float32')


@pytest.fixture
def mock_openai_client():
    """Fixture providing a mock OpenAI client."""
    mock_client = MagicMock()
    
    # Mock embeddings
    mock_embedding_response = MagicMock()
    mock_embedding_response.data = [MagicMock(embedding=np.random.rand(1536).tolist())]
    mock_client.embeddings.create.return_value = mock_embedding_response
    
    # Mock chat completions
    mock_completion = MagicMock()
    mock_completion.choices = [
        MagicMock(
            message=MagicMock(
                content=str(SAMPLE_SCRIPT_OUTPUT)
            )
        )
    ]
    mock_client.chat.completions.create.return_value = mock_completion
    
    return mock_client


@pytest.fixture
def mock_faiss_index():
    """Fixture providing a mock FAISS index."""
    mock_index = MagicMock()
    mock_index.ntotal = 8
    
    # Mock search results
    distances = np.array([[0.1, 0.2, 0.3]], dtype='float32')
    indices = np.array([[0, 1, 2]], dtype='int64')
    mock_index.search.return_value = (distances, indices)
    
    return mock_index


@pytest.fixture(autouse=True)
def reset_env_vars(monkeypatch):
    """Automatically reset environment variables for each test."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key-123")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    monkeypatch.setenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
