"""Script request data model."""
from pydantic import BaseModel, Field
from typing import Optional


class ScriptRequest(BaseModel):
    """Request parameters for script generation."""
    goal: str = Field(..., description="Script goal (e.g., 'awareness', 'conversion', 'engagement')")
    hook_type: str = Field(..., description="Hook type (e.g., 'question', 'bold_claim', 'relatable', 'shocking')")
    emotion: str = Field(..., description="Target emotion (e.g., 'excitement', 'curiosity', 'urgency')")
    script_length: int = Field(..., description="Script length in seconds (15-60)", ge=15, le=60)
    language: str = Field(default="english", description="Script language")
    cta: str = Field(..., description="Call-to-action text")
    
    class Config:
        json_schema_extra = {
            "example": {
                "goal": "conversion",
                "hook_type": "question",
                "emotion": "curiosity",
                "script_length": 30,
                "language": "english",
                "cta": "Download the app now!"
            }
        }
