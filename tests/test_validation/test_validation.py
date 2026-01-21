"""
Unit tests for validation logic.

Tests validation rules and script validator.
"""

import pytest
from app.validation.rules import ValidationRules
from app.validation.checks import ScriptValidator
from app.models.output import ReelScriptOutput


class TestValidationRules:
    """Tests for ValidationRules class."""
    
    @pytest.mark.unit
    @pytest.mark.validation
    def test_word_count_limits(self):
        """Test word count limit constants."""
        assert ValidationRules.MIN_HOOK_WORDS == 3
        assert ValidationRules.MAX_HOOK_WORDS == 15
        assert ValidationRules.MIN_BODY_WORDS == 20
        assert ValidationRules.MAX_BODY_WORDS == 150
        assert ValidationRules.MIN_CTA_WORDS == 3
        assert ValidationRules.MAX_CTA_WORDS == 15
    
    @pytest.mark.unit
    @pytest.mark.validation
    def test_caption_limits(self):
        """Test caption length limits."""
        assert ValidationRules.MIN_CAPTION_LENGTH == 50
        assert ValidationRules.MAX_CAPTION_LENGTH == 200
    
    @pytest.mark.unit
    @pytest.mark.validation
    def test_hashtag_limits(self):
        """Test hashtag count limits."""
        assert ValidationRules.MIN_HASHTAGS == 3
        assert ValidationRules.MAX_HASHTAGS == 10
    
    @pytest.mark.unit
    @pytest.mark.validation
    def test_brand_voice_keywords(self):
        """Test brand voice keyword mappings exist."""
        assert "professional" in ValidationRules.BRAND_VOICE_KEYWORDS
        assert "friendly" in ValidationRules.BRAND_VOICE_KEYWORDS
        assert len(ValidationRules.BRAND_VOICE_KEYWORDS["professional"]) > 0


class TestScriptValidator:
    """Tests for ScriptValidator class."""
    
    @pytest.fixture
    def validator(self):
        """Create a validator instance."""
        return ScriptValidator()
    
    @pytest.fixture
    def valid_script(self, sample_script_output):
        """Create a valid script for testing."""
        return ReelScriptOutput(**sample_script_output)
    
    @pytest.mark.unit
    @pytest.mark.validation
    def test_validate_valid_script(self, validator, valid_script):
        """Test validation of a completely valid script."""
        result = validator.validate(
            valid_script,
            brand_voice=["energetic", "motivational"],
            banned_words=[]
        )
        assert result.is_valid is True
        assert len(result.errors) == 0
    
    @pytest.mark.unit
    @pytest.mark.validation
    def test_validate_hook_too_short(self, validator):
        """Test validation fails when hook is too short."""
        script = ReelScriptOutput(
            hook="Go!",  # Only 1 word
            body="This is a valid body with enough words to pass validation requirements.",
            cta="Download the app now!",
            caption="A valid caption that meets the minimum length requirement for testing",
            hashtags=["#Test", "#Valid", "#Hashtags"]
        )
        result = validator.validate(script, brand_voice=[], banned_words=[])
        assert result.is_valid is False
        assert any("Hook" in error for error in result.errors)
    
    @pytest.mark.unit
    @pytest.mark.validation
    def test_validate_hook_too_long(self, validator):
        """Test validation fails when hook is too long."""
        script = ReelScriptOutput(
            hook="This is an extremely long hook that has way too many words and should fail validation",
            body="This is a valid body with enough words to pass validation requirements.",
            cta="Download the app now!",
            caption="A valid caption that meets the minimum length requirement for testing",
            hashtags=["#Test", "#Valid", "#Hashtags"]
        )
        result = validator.validate(script, brand_voice=[], banned_words=[])
        assert result.is_valid is False
        assert any("Hook" in error for error in result.errors)
    
    @pytest.mark.unit
    @pytest.mark.validation
    def test_validate_body_too_short(self, validator):
        """Test validation fails when body is too short."""
        script = ReelScriptOutput(
            hook="Ready to start?",
            body="Too short.",  # Only 2 words
            cta="Download the app now!",
            caption="A valid caption that meets the minimum length requirement for testing",
            hashtags=["#Test", "#Valid", "#Hashtags"]
        )
        result = validator.validate(script, brand_voice=[], banned_words=[])
        assert result.is_valid is False
        assert any("Body" in error for error in result.errors)
    
    @pytest.mark.unit
    @pytest.mark.validation
    def test_validate_caption_too_short(self, validator):
        """Test validation fails when caption is too short."""
        script = ReelScriptOutput(
            hook="Ready to start?",
            body="This is a valid body with enough words to pass validation requirements.",
            cta="Download the app now!",
            caption="Short",  # Too short
            hashtags=["#Test", "#Valid", "#Hashtags"]
        )
        result = validator.validate(script, brand_voice=[], banned_words=[])
        assert result.is_valid is False
        assert any("Caption" in error for error in result.errors)
    
    @pytest.mark.unit
    @pytest.mark.validation
    def test_validate_hashtags_count(self, validator):
        """Test validation of hashtag count."""
        # Too few hashtags
        script = ReelScriptOutput(
            hook="Ready to start?",
            body="This is a valid body with enough words to pass validation requirements.",
            cta="Download the app now!",
            caption="A valid caption that meets the minimum length requirement for testing",
            hashtags=["#Test"]  # Only 1 hashtag
        )
        result = validator.validate(script, brand_voice=[], banned_words=[])
        assert result.is_valid is False
        assert any("hashtag" in error.lower() for error in result.errors)
    
    @pytest.mark.unit
    @pytest.mark.validation
    def test_banned_words_detection(self, validator):
        """Test detection of banned words."""
        script = ReelScriptOutput(
            hook="Are you lazy?",  # Contains banned word
            body="This is a valid body with enough words to pass validation requirements.",
            cta="Download the app now!",
            caption="A valid caption that meets the minimum length requirement for testing",
            hashtags=["#Test", "#Valid", "#Hashtags"]
        )
        result = validator.validate(
            script,
            brand_voice=[],
            banned_words=["lazy"]
        )
        assert result.is_valid is False
        assert any("banned" in error.lower() for error in result.errors)
    
    @pytest.mark.unit
    @pytest.mark.validation
    def test_cta_effectiveness(self, validator, valid_script):
        """Test CTA effectiveness validation."""
        # Valid CTA with action words
        result = validator.validate(valid_script, brand_voice=[], banned_words=[])
        # Should not have CTA errors
        cta_errors = [e for e in result.errors if "CTA" in e]
        assert len(cta_errors) == 0
    
    @pytest.mark.unit
    @pytest.mark.validation
    def test_warnings_non_blocking(self, validator, valid_script):
        """Test that warnings don't make script invalid."""
        result = validator.validate(
            valid_script,
            brand_voice=["professional"],  # May generate warnings
            banned_words=[]
        )
        # Script can still be valid even with warnings
        if len(result.warnings) > 0:
            # Warnings should not affect validity if no errors
            if len(result.errors) == 0:
                assert result.is_valid is True
