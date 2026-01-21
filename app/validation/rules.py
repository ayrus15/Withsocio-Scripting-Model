"""
Validation rules and configuration.
Defines constraints and checks for script validation.
"""
from typing import Dict, Any


class ValidationRules:
    """Centralized validation rules for script generation."""
    
    # Word count limits
    MIN_HOOK_WORDS = 3
    MAX_HOOK_WORDS = 15
    MIN_BODY_WORDS = 20
    MAX_BODY_WORDS = 150
    MIN_CTA_WORDS = 3
    MAX_CTA_WORDS = 15
    MIN_CAPTION_LENGTH = 50
    MAX_CAPTION_LENGTH = 200
    MIN_HASHTAGS = 3
    MAX_HASHTAGS = 10
    
    # Content checks
    REQUIRED_FIELDS = ['hook', 'body', 'cta', 'caption', 'hashtags']
    
    # Brand voice keywords (expandable)
    BRAND_VOICE_KEYWORDS = {
        'professional': ['expert', 'professional', 'proven', 'certified', 'trusted'],
        'friendly': ['hey', 'you', 'your', 'friend', 'together'],
        'energetic': ['amazing', 'incredible', 'wow', 'awesome', 'exciting'],
        'motivational': ['achieve', 'succeed', 'transform', 'believe', 'can'],
        'authentic': ['real', 'honest', 'genuine', 'true', 'actual'],
        'casual': ['yeah', 'gonna', 'wanna', 'cool', 'fun'],
    }
    
    @staticmethod
    def get_word_count_limits() -> Dict[str, Dict[str, int]]:
        """Return word count limits for each field."""
        return {
            'hook': {'min': ValidationRules.MIN_HOOK_WORDS, 'max': ValidationRules.MAX_HOOK_WORDS},
            'body': {'min': ValidationRules.MIN_BODY_WORDS, 'max': ValidationRules.MAX_BODY_WORDS},
            'cta': {'min': ValidationRules.MIN_CTA_WORDS, 'max': ValidationRules.MAX_CTA_WORDS},
        }
    
    @staticmethod
    def get_length_limits() -> Dict[str, Dict[str, int]]:
        """Return character length limits."""
        return {
            'caption': {'min': ValidationRules.MIN_CAPTION_LENGTH, 'max': ValidationRules.MAX_CAPTION_LENGTH},
        }
