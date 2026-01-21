"""Output data models."""
from pydantic import BaseModel, Field
from typing import List, Optional


class ReelScriptOutput(BaseModel):
    """Structured output for generated reel script."""
    hook: str = Field(..., description="Opening hook (first 3 seconds)")
    body: str = Field(..., description="Main script content")
    cta: str = Field(..., description="Call-to-action")
    caption: str = Field(..., description="Instagram caption")
    hashtags: List[str] = Field(..., description="Recommended hashtags")
    
    class Config:
        json_schema_extra = {
            "example": {
                "hook": "Tired of expensive gym memberships?",
                "body": "What if I told you that you can get fit at home with just 15 minutes a day? Our AI-powered workout plans adapt to your schedule and fitness level.",
                "cta": "Download FitLife Pro now and start your transformation!",
                "caption": "Your fitness journey starts at home 💪 No more excuses!",
                "hashtags": ["#FitnessGoals", "#HomeWorkout", "#FitLife", "#HealthyLifestyle", "#TransformationTuesday"]
            }
        }


class ValidationResult(BaseModel):
    """Validation result for generated scripts."""
    is_valid: bool = Field(..., description="Whether the script passes validation")
    errors: List[str] = Field(default_factory=list, description="List of validation errors")
    warnings: List[str] = Field(default_factory=list, description="List of validation warnings")
