"""
Script generator service.
Orchestrates RAG retrieval, LLM generation, and validation.
"""
from typing import Tuple
import logging

from app.models.brand import BrandProfile
from app.models.script_request import ScriptRequest
from app.models.output import ReelScriptOutput, ValidationResult
from app.rag.retrieve import RetrievalService
from app.services.llm import LLMService
from app.validation.checks import ScriptValidator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScriptGenerator:
    """Main service for generating validated reel scripts."""
    
    def __init__(self):
        """Initialize generator with required services."""
        self.retrieval_service = RetrievalService()
        self.llm_service = LLMService()
        self.validator = ScriptValidator()
    
    def generate(
        self,
        brand_profile: BrandProfile,
        script_request: ScriptRequest
    ) -> Tuple[ReelScriptOutput, ValidationResult]:
        """
        Generate and validate a reel script.
        
        Args:
            brand_profile: Brand intelligence profile
            script_request: Script generation parameters
            
        Returns:
            Tuple of (generated script, validation result)
            
        Raises:
            ValueError: If generation or validation fails critically
        """
        logger.info(
            f"Generating script for brand: {brand_profile.brand_name}, "
            f"sector: {brand_profile.sector}"
        )
        
        # Step 1: Retrieve relevant examples using RAG
        logger.info("Retrieving reference examples...")
        reference_examples = self.retrieval_service.retrieve_for_generation(
            brand_profile=brand_profile.model_dump(),
            script_request=script_request.model_dump()
        )
        logger.info(f"Retrieved {len(reference_examples)} reference examples")
        
        # Step 2: Construct prompt
        logger.info("Constructing prompt...")
        prompt = self.llm_service.construct_prompt(
            brand_profile=brand_profile.model_dump(),
            script_request=script_request.model_dump(),
            reference_examples=reference_examples
        )
        
        # Step 3: Generate script using LLM
        logger.info("Generating script with LLM...")
        max_retries = 3
        script_output = None
        
        for attempt in range(max_retries):
            try:
                raw_response = self.llm_service.generate(prompt)
                parsed_response = self.llm_service.parse_json_response(raw_response)
                
                # Validate JSON structure and create output object
                script_output = ReelScriptOutput(**parsed_response)
                logger.info("Script generated successfully")
                break
                
            except (ValueError, KeyError) as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise ValueError(f"Failed to generate valid script after {max_retries} attempts")
        
        # Step 4: Validate generated script
        logger.info("Validating generated script...")
        validation_result = self.validator.validate(script_output, brand_profile)
        
        if validation_result.is_valid:
            logger.info("Script passed validation")
        else:
            logger.warning(f"Script validation errors: {validation_result.errors}")
        
        if validation_result.warnings:
            logger.info(f"Script validation warnings: {validation_result.warnings}")
        
        return script_output, validation_result
    
    def regenerate_if_invalid(
        self,
        brand_profile: BrandProfile,
        script_request: ScriptRequest,
        max_attempts: int = 2
    ) -> Tuple[ReelScriptOutput, ValidationResult]:
        """
        Generate script with automatic retry on validation failure.
        
        Args:
            brand_profile: Brand intelligence profile
            script_request: Script generation parameters
            max_attempts: Maximum number of generation attempts
            
        Returns:
            Tuple of (best generated script, validation result)
        """
        best_script = None
        best_validation = None
        
        for attempt in range(max_attempts):
            logger.info(f"Generation attempt {attempt + 1}/{max_attempts}")
            
            try:
                script, validation = self.generate(brand_profile, script_request)
                
                # Keep track of best attempt
                if best_script is None or validation.is_valid:
                    best_script = script
                    best_validation = validation
                
                # Return if valid
                if validation.is_valid:
                    return script, validation
                    
            except Exception as e:
                logger.error(f"Generation attempt {attempt + 1} failed: {e}")
                if attempt == max_attempts - 1:
                    raise
        
        # Return best attempt even if not valid
        logger.warning("Could not generate valid script, returning best attempt")
        return best_script, best_validation
