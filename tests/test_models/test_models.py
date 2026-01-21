"""
Unit tests for Pydantic models.

Tests brand profile, script request, and output models.
"""

import pytest
from pydantic import ValidationError
from app.models.brand import BrandProfile, TargetAudience
from app.models.script_request import ScriptRequest
from app.models.output import ReelScriptOutput, ValidationResult


class TestTargetAudience:
    """Tests for TargetAudience model."""
    
    @pytest.mark.unit
    @pytest.mark.models
    def test_valid_target_audience(self):
        """Test creating a valid target audience."""
        data = {
            "age_range": "25-40",
            "gender": "All",
            "location": "USA",
            "pain_points": ["lack of motivation"]
        }
        audience = TargetAudience(**data)
        assert audience.age_range == "25-40"
        assert audience.gender == "All"
        assert audience.location == "USA"
        assert len(audience.pain_points) == 1
    
    @pytest.mark.unit
    @pytest.mark.models
    def test_target_audience_optional_fields(self):
        """Test that optional fields can be omitted."""
        data = {
            "age_range": "18-65",
            "gender": "All",
            "location": "Global"
        }
        audience = TargetAudience(**data)
        assert audience.pain_points == []


class TestBrandProfile:
    """Tests for BrandProfile model."""
    
    @pytest.mark.unit
    @pytest.mark.models
    def test_valid_brand_profile(self, sample_brand_profile):
        """Test creating a valid brand profile."""
        profile = BrandProfile(**sample_brand_profile)
        assert profile.brand_name == "TestBrand"
        assert profile.sector == "fitness"
        assert profile.platform == "instagram"
        assert "energetic" in profile.brand_voice
    
    @pytest.mark.unit
    @pytest.mark.models
    def test_brand_profile_with_nested_audience(self, sample_brand_profile):
        """Test brand profile with nested target audience."""
        profile = BrandProfile(**sample_brand_profile)
        assert isinstance(profile.target_audience, TargetAudience)
        assert profile.target_audience.age_range == "25-40"
    
    @pytest.mark.unit
    @pytest.mark.models
    def test_brand_profile_optional_fields(self):
        """Test brand profile with minimal required fields."""
        data = {
            "brand_name": "MinimalBrand",
            "sector": "technology",
            "target_audience": {
                "age_range": "18-65",
                "gender": "All",
                "location": "Global"
            },
            "brand_voice": ["professional"],
            "offer": "Tech solutions",
            "platform": "instagram",
            "cta_style": "direct"
        }
        profile = BrandProfile(**data)
        assert profile.brand_name == "MinimalBrand"
        assert profile.do_not_use == []
    
    @pytest.mark.unit
    @pytest.mark.models
    def test_brand_profile_validation_error(self):
        """Test that validation error is raised for invalid data."""
        with pytest.raises(ValidationError):
            BrandProfile(brand_name="Test")  # Missing required fields


class TestScriptRequest:
    """Tests for ScriptRequest model."""
    
    @pytest.mark.unit
    @pytest.mark.models
    def test_valid_script_request(self, sample_script_request):
        """Test creating a valid script request."""
        request = ScriptRequest(**sample_script_request)
        assert request.goal == "conversion"
        assert request.hook_type == "question"
        assert request.emotion == "curiosity"
        assert request.script_length == 30
    
    @pytest.mark.unit
    @pytest.mark.models
    def test_script_length_validation(self):
        """Test script length must be between 15 and 60."""
        valid_request = {
            "goal": "awareness",
            "hook_type": "bold_claim",
            "emotion": "excitement",
            "script_length": 30,
            "language": "english",
            "cta": "Learn more!"
        }
        request = ScriptRequest(**valid_request)
        assert request.script_length == 30
        
        # Test too short
        with pytest.raises(ValidationError):
            invalid_request = valid_request.copy()
            invalid_request["script_length"] = 10
            ScriptRequest(**invalid_request)
        
        # Test too long
        with pytest.raises(ValidationError):
            invalid_request = valid_request.copy()
            invalid_request["script_length"] = 70
            ScriptRequest(**invalid_request)
    
    @pytest.mark.unit
    @pytest.mark.models
    def test_script_request_optional_language(self):
        """Test that language defaults to english."""
        data = {
            "goal": "engagement",
            "hook_type": "story",
            "emotion": "joy",
            "script_length": 45,
            "cta": "Join us!"
        }
        request = ScriptRequest(**data)
        assert request.language == "english"


class TestReelScriptOutput:
    """Tests for ReelScriptOutput model."""
    
    @pytest.mark.unit
    @pytest.mark.models
    def test_valid_script_output(self, sample_script_output):
        """Test creating a valid script output."""
        output = ReelScriptOutput(**sample_script_output)
        assert output.hook == sample_script_output["hook"]
        assert output.body == sample_script_output["body"]
        assert output.cta == sample_script_output["cta"]
        assert len(output.hashtags) == 3
    
    @pytest.mark.unit
    @pytest.mark.models
    def test_script_output_validation(self):
        """Test that all required fields must be present."""
        with pytest.raises(ValidationError):
            ReelScriptOutput(hook="Test", body="Test")  # Missing required fields


class TestValidationResult:
    """Tests for ValidationResult model."""
    
    @pytest.mark.unit
    @pytest.mark.models
    def test_valid_validation_result(self):
        """Test creating a valid validation result."""
        result = ValidationResult(
            is_valid=True,
            errors=[],
            warnings=["Minor warning"]
        )
        assert result.is_valid is True
        assert len(result.errors) == 0
        assert len(result.warnings) == 1
    
    @pytest.mark.unit
    @pytest.mark.models
    def test_invalid_validation_result(self):
        """Test validation result with errors."""
        result = ValidationResult(
            is_valid=False,
            errors=["Hook too long", "Body too short"],
            warnings=[]
        )
        assert result.is_valid is False
        assert len(result.errors) == 2
