"""Brand intelligence data model."""
from pydantic import BaseModel, Field
from typing import List, Optional


class TargetAudience(BaseModel):
    """Target audience demographics and characteristics."""
    age_range: str = Field(..., description="Age range (e.g., '18-35')")
    gender: str = Field(..., description="Gender focus (e.g., 'All', 'Male', 'Female')")
    location: str = Field(..., description="Geographic location")
    pain_points: List[str] = Field(..., description="Audience pain points")


class BrandProfile(BaseModel):
    """Complete brand intelligence profile."""
    brand_name: str = Field(..., description="Name of the brand")
    sector: str = Field(..., description="Business sector (e.g., 'fitness', 'finance', 'fashion')")
    target_audience: TargetAudience = Field(..., description="Target audience details")
    brand_voice: List[str] = Field(..., description="Brand voice characteristics (e.g., ['professional', 'friendly'])")
    offer: str = Field(..., description="Main offer or value proposition")
    platform: str = Field(default="instagram", description="Social media platform")
    cta_style: str = Field(..., description="Call-to-action style (e.g., 'direct', 'soft', 'question')")
    do_not_use: List[str] = Field(default_factory=list, description="Banned words or phrases")
    
    class Config:
        json_schema_extra = {
            "example": {
                "brand_name": "FitLife Pro",
                "sector": "fitness",
                "target_audience": {
                    "age_range": "25-40",
                    "gender": "All",
                    "location": "USA",
                    "pain_points": ["lack of motivation", "time constraints", "expensive gym memberships"]
                },
                "brand_voice": ["energetic", "motivational", "authentic"],
                "offer": "AI-powered home workout plans",
                "platform": "instagram",
                "cta_style": "direct",
                "do_not_use": ["lazy", "fat", "impossible"]
            }
        }
