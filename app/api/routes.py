"""
API routes for script generation endpoints.
Handles HTTP requests and responses.
"""
from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
import logging

from app.models.brand import BrandProfile
from app.models.script_request import ScriptRequest
from app.models.output import ReelScriptOutput

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api", tags=["script-generation"])

# Generator will be initialized lazily on first request
generator = None


def get_generator():
    """Lazy initialization of generator."""
    global generator
    if generator is None:
        from app.services.generator import ScriptGenerator
        generator = ScriptGenerator()
    return generator


@router.post(
    "/generate-reel",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Generate Instagram Reel Script",
    description="Generate a brand-safe Instagram Reel script using RAG and LLM"
)
async def generate_reel(
    brand_profile: BrandProfile,
    script_request: ScriptRequest
) -> Dict[str, Any]:
    """
    Generate Instagram Reel script with RAG-enhanced LLM.
    
    Args:
        brand_profile: Brand intelligence profile
        script_request: Script generation parameters
        
    Returns:
        Dictionary containing:
        - script: Generated reel script with hook, body, cta, caption, hashtags
        - validation: Validation results with errors and warnings
        - metadata: Generation metadata
        
    Raises:
        HTTPException: If generation fails
    """
    try:
        logger.info(f"Received generation request for brand: {brand_profile.brand_name}")
        
        # Generate script with validation
        gen = get_generator()
        script, validation = gen.regenerate_if_invalid(
            brand_profile=brand_profile,
            script_request=script_request,
            max_attempts=2
        )
        
        # Prepare response
        response = {
            "script": {
                "hook": script.hook,
                "body": script.body,
                "cta": script.cta,
                "caption": script.caption,
                "hashtags": script.hashtags
            },
            "validation": {
                "is_valid": validation.is_valid,
                "errors": validation.errors,
                "warnings": validation.warnings
            },
            "metadata": {
                "brand": brand_profile.brand_name,
                "sector": brand_profile.sector,
                "goal": script_request.goal,
                "hook_type": script_request.hook_type,
                "script_length": script_request.script_length
            }
        }
        
        logger.info("Script generated successfully")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to generate valid script: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during script generation"
        )


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check if the API is running"
)
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    
    Returns:
        Status message
    """
    return {"status": "healthy", "service": "reel-script-generator"}


@router.get(
    "/sectors",
    status_code=status.HTTP_200_OK,
    summary="Get Available Sectors",
    description="List available business sectors in the system"
)
async def get_sectors() -> Dict[str, list]:
    """
    Get list of available sectors.
    
    Returns:
        List of supported sectors
    """
    sectors = [
        "fitness",
        "finance",
        "fashion",
        "beauty",
        "productivity",
        "pets",
        "education",
        "wellness",
        "technology",
        "food",
        "travel",
        "real_estate"
    ]
    return {"sectors": sectors}


@router.get(
    "/hook-types",
    status_code=status.HTTP_200_OK,
    summary="Get Available Hook Types",
    description="List available hook types for scripts"
)
async def get_hook_types() -> Dict[str, list]:
    """
    Get list of available hook types.
    
    Returns:
        List of supported hook types
    """
    hook_types = [
        "question",
        "bold_claim",
        "relatable",
        "shocking",
        "curiosity",
        "statistic",
        "story"
    ]
    return {"hook_types": hook_types}
