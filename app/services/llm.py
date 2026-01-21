"""
LLM service for interacting with OpenAI API.
Handles prompt construction and API calls with retry logic.
"""
import json
import os
from typing import Dict, Any, Optional
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from app.utils.config import settings


class LLMService:
    """Service for LLM interactions via OpenAI API."""
    
    def __init__(self):
        """Initialize LLM service with OpenAI client."""
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.max_tokens = settings.max_tokens
        self.temperature = settings.temperature
        
        # Load prompt templates
        self.system_prompt = self._load_prompt_template('system.txt')
        self.instruction_template = self._load_prompt_template('instruction.txt')
    
    def _load_prompt_template(self, filename: str) -> str:
        """
        Load prompt template from file.
        
        Args:
            filename: Name of the prompt template file
            
        Returns:
            Content of the prompt template
        """
        prompts_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'prompts'
        )
        filepath = os.path.join(prompts_dir, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def construct_prompt(
        self,
        brand_profile: Dict[str, Any],
        script_request: Dict[str, Any],
        reference_examples: list[Dict[str, Any]]
    ) -> str:
        """
        Construct the full prompt with injected data.
        
        Args:
            brand_profile: Brand profile data
            script_request: Script request parameters
            reference_examples: Retrieved reference examples
            
        Returns:
            Formatted prompt string
        """
        # Format brand profile
        brand_profile_str = json.dumps(brand_profile, indent=2)
        
        # Format script request
        script_request_str = json.dumps(script_request, indent=2)
        
        # Format reference examples
        examples_str = ""
        for i, example in enumerate(reference_examples, 1):
            examples_str += f"\nExample {i} (Similarity: {example.get('similarity_score', 0):.2f}):\n"
            examples_str += f"Sector: {example.get('sector', 'N/A')}\n"
            examples_str += f"Hook Type: {example.get('hook_type', 'N/A')}\n"
            examples_str += f"Engagement Rate: {example.get('engagement_rate', 'N/A')}%\n"
            examples_str += "---\n"
        
        if not examples_str:
            examples_str = "No reference examples available."
        
        # Inject data into instruction template
        prompt = self.instruction_template.format(
            brand_profile=brand_profile_str,
            script_request=script_request_str,
            reference_examples=examples_str
        )
        
        return prompt
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def generate(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate text using OpenAI API with retry logic.
        
        Args:
            prompt: User prompt
            temperature: Override default temperature
            max_tokens: Override default max tokens
            
        Returns:
            Generated text response
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature or self.temperature,
            max_tokens=max_tokens or self.max_tokens,
            response_format={"type": "json_object"}
        )
        
        return response.choices[0].message.content
    
    def parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        Parse JSON response from LLM.
        
        Args:
            response: Raw response string
            
        Returns:
            Parsed JSON dictionary
            
        Raises:
            ValueError: If response is not valid JSON
        """
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response: {e}")
