"""
Validation checks for generated scripts.
Implements comprehensive validation logic.
"""
from typing import List, Dict, Any
from app.models.output import ReelScriptOutput, ValidationResult
from app.models.brand import BrandProfile
from app.validation.rules import ValidationRules


class ScriptValidator:
    """Validator for generated reel scripts."""
    
    def __init__(self):
        """Initialize validator with rules."""
        self.rules = ValidationRules()
    
    def validate(
        self,
        script: ReelScriptOutput,
        brand_profile: BrandProfile
    ) -> ValidationResult:
        """
        Validate generated script against all rules.
        
        Args:
            script: Generated script output
            brand_profile: Brand profile with restrictions
            
        Returns:
            ValidationResult with errors and warnings
        """
        errors = []
        warnings = []
        
        # Check word counts
        word_count_errors = self._check_word_counts(script)
        errors.extend(word_count_errors)
        
        # Check character lengths
        length_errors = self._check_lengths(script)
        errors.extend(length_errors)
        
        # Check banned words
        banned_word_errors = self._check_banned_words(script, brand_profile.do_not_use)
        errors.extend(banned_word_errors)
        
        # Check CTA presence
        cta_warnings = self._check_cta(script)
        warnings.extend(cta_warnings)
        
        # Check brand voice alignment
        voice_warnings = self._check_brand_voice(script, brand_profile.brand_voice)
        warnings.extend(voice_warnings)
        
        # Check hashtags
        hashtag_errors = self._check_hashtags(script)
        errors.extend(hashtag_errors)
        
        is_valid = len(errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings
        )
    
    def _check_word_counts(self, script: ReelScriptOutput) -> List[str]:
        """Check word counts for hook, body, and CTA."""
        errors = []
        limits = self.rules.get_word_count_limits()
        
        for field_name, limits_dict in limits.items():
            field_value = getattr(script, field_name, "")
            word_count = len(field_value.split())
            
            if word_count < limits_dict['min']:
                errors.append(
                    f"{field_name.capitalize()} too short: {word_count} words "
                    f"(minimum: {limits_dict['min']})"
                )
            elif word_count > limits_dict['max']:
                errors.append(
                    f"{field_name.capitalize()} too long: {word_count} words "
                    f"(maximum: {limits_dict['max']})"
                )
        
        return errors
    
    def _check_lengths(self, script: ReelScriptOutput) -> List[str]:
        """Check character lengths for caption."""
        errors = []
        limits = self.rules.get_length_limits()
        
        for field_name, limits_dict in limits.items():
            field_value = getattr(script, field_name, "")
            char_count = len(field_value)
            
            if char_count < limits_dict['min']:
                errors.append(
                    f"{field_name.capitalize()} too short: {char_count} characters "
                    f"(minimum: {limits_dict['min']})"
                )
            elif char_count > limits_dict['max']:
                errors.append(
                    f"{field_name.capitalize()} too long: {char_count} characters "
                    f"(maximum: {limits_dict['max']})"
                )
        
        return errors
    
    def _check_banned_words(
        self,
        script: ReelScriptOutput,
        banned_words: List[str]
    ) -> List[str]:
        """Check for banned words in script."""
        if not banned_words:
            return []
        
        errors = []
        full_text = f"{script.hook} {script.body} {script.cta} {script.caption}".lower()
        
        found_banned = []
        for word in banned_words:
            if word.lower() in full_text:
                found_banned.append(word)
        
        if found_banned:
            errors.append(
                f"Script contains banned words: {', '.join(found_banned)}"
            )
        
        return errors
    
    def _check_cta(self, script: ReelScriptOutput) -> List[str]:
        """Check CTA effectiveness."""
        warnings = []
        
        cta_lower = script.cta.lower()
        
        # Check for action words
        action_words = ['download', 'try', 'start', 'join', 'get', 'shop', 'learn', 'discover', 'click']
        has_action = any(word in cta_lower for word in action_words)
        
        if not has_action:
            warnings.append("CTA might be more effective with an action verb")
        
        # Check for urgency words
        urgency_words = ['now', 'today', 'limited', 'free', 'save']
        has_urgency = any(word in cta_lower for word in urgency_words)
        
        if not has_urgency:
            warnings.append("CTA could benefit from urgency language")
        
        return warnings
    
    def _check_brand_voice(
        self,
        script: ReelScriptOutput,
        brand_voice: List[str]
    ) -> List[str]:
        """Check brand voice alignment."""
        warnings = []
        
        full_text = f"{script.hook} {script.body} {script.cta}".lower()
        
        # Count brand voice keyword matches
        matches = 0
        for voice in brand_voice:
            if voice.lower() in self.rules.BRAND_VOICE_KEYWORDS:
                keywords = self.rules.BRAND_VOICE_KEYWORDS[voice.lower()]
                voice_matches = sum(1 for kw in keywords if kw in full_text)
                matches += voice_matches
        
        if matches == 0 and brand_voice:
            warnings.append(
                f"Script may not align with brand voice: {', '.join(brand_voice)}"
            )
        
        return warnings
    
    def _check_hashtags(self, script: ReelScriptOutput) -> List[str]:
        """Check hashtags validity."""
        errors = []
        
        num_hashtags = len(script.hashtags)
        
        if num_hashtags < self.rules.MIN_HASHTAGS:
            errors.append(
                f"Too few hashtags: {num_hashtags} (minimum: {self.rules.MIN_HASHTAGS})"
            )
        elif num_hashtags > self.rules.MAX_HASHTAGS:
            errors.append(
                f"Too many hashtags: {num_hashtags} (maximum: {self.rules.MAX_HASHTAGS})"
            )
        
        # Check hashtag format
        for tag in script.hashtags:
            if not tag.startswith('#'):
                errors.append(f"Invalid hashtag format: {tag} (must start with #)")
            elif ' ' in tag:
                errors.append(f"Invalid hashtag: {tag} (cannot contain spaces)")
        
        return errors
