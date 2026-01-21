# Development Tasks - Quick Reference

## 🎯 Current Focus: Phase 2 Testing

### What You Need to Do Next

#### 1. Create RAG System Tests
**File**: `tests/test_rag/test_embed.py`
```python
# Test EmbeddingService:
- test_generate_embeddings()
- test_create_faiss_index()
- test_save_and_load_index()
- test_batch_embedding_generation()
```

**File**: `tests/test_rag/test_retrieve.py`
```python
# Test RetrievalService:
- test_retrieve_examples()
- test_filter_by_sector()
- test_filter_by_hook_type()
- test_top_k_results()
```

#### 2. Create Service Layer Tests
**File**: `tests/test_services/test_llm.py`
```python
# Test LLMService:
- test_prompt_construction()
- test_llm_api_call()
- test_retry_logic()
- test_error_handling()
```

**File**: `tests/test_services/test_generator.py`
```python
# Test ScriptGenerator:
- test_full_generation_flow()
- test_validation_retry()
- test_error_propagation()
```

#### 3. Create API Tests
**File**: `tests/test_api/test_routes.py`
```python
# Test API endpoints:
- test_generate_reel_success()
- test_generate_reel_invalid_input()
- test_health_endpoint()
- test_sectors_endpoint()
- test_hook_types_endpoint()
```

---

## 🚀 Quick Commands

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_models/test_models.py -v

# Run tests with specific marker
pytest -m unit
pytest -m integration

# Run tests and stop on first failure
pytest -x

# Run tests with output
pytest -s
```

### Code Quality
```bash
# Format code
black app/ tests/

# Sort imports
isort app/ tests/

# Lint code
flake8 app/ tests/ --max-line-length=120

# Type check
mypy app/ --ignore-missing-imports
```

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload

# Run tests in watch mode (requires pytest-watch)
ptw
```

---

## 📝 Task Checklist

### Phase 2: Testing (Current)
```
Testing Infrastructure:
[x] pytest configuration
[x] Test fixtures
[x] Test directory structure
[x] CI/CD pipeline
[x] Updated requirements.txt

Unit Tests:
[x] Model tests (16 test cases)
[x] Validation tests (14 test cases)
[ ] RAG system tests (8-10 test cases needed)
[ ] Service layer tests (10-12 test cases needed)
[ ] API endpoint tests (8-10 test cases needed)

Integration Tests:
[ ] End-to-end generation flow
[ ] Error handling scenarios
[ ] Validation retry flow

Quality Metrics:
[ ] 80%+ code coverage
[ ] All CI checks passing
[ ] No security issues
[ ] Documentation complete
```

### Phase 3: Production (Next)
```
Authentication:
[ ] JWT implementation
[ ] API key system
[ ] User management
[ ] RBAC

Infrastructure:
[ ] Rate limiting
[ ] Logging system
[ ] Monitoring setup
[ ] Database integration
[ ] Redis caching

Deployment:
[ ] Dockerfile
[ ] Docker Compose
[ ] Kubernetes manifests
[ ] Production configs
```

---

## 🎓 Test Writing Guide

### Pattern 1: Model Tests
```python
@pytest.mark.unit
@pytest.mark.models
def test_valid_model(self, sample_data):
    """Test creating a valid model."""
    model = ModelClass(**sample_data)
    assert model.field == expected_value
```

### Pattern 2: Service Tests
```python
@pytest.mark.unit
@pytest.mark.services
def test_service_function(self, mock_dependency):
    """Test service function with mocked dependency."""
    service = ServiceClass(mock_dependency)
    result = service.function()
    assert result == expected
```

### Pattern 3: API Tests
```python
@pytest.mark.integration
@pytest.mark.api
def test_api_endpoint(client):
    """Test API endpoint."""
    response = client.post("/api/endpoint", json=data)
    assert response.status_code == 200
    assert response.json() == expected
```

---

## 📚 Key Files to Review

### Core Implementation
- `app/main.py` - FastAPI application
- `app/api/routes.py` - API endpoints
- `app/models/*.py` - Pydantic models
- `app/rag/*.py` - RAG system
- `app/services/*.py` - Business logic
- `app/validation/*.py` - Validation logic

### Testing
- `tests/conftest.py` - Test fixtures
- `tests/test_models/test_models.py` - Model tests ✅
- `tests/test_validation/test_validation.py` - Validation tests ✅
- `pytest.ini` - Test configuration

### Documentation
- `README.md` - User documentation
- `ROADMAP.md` - Complete development plan ⭐
- `NEXT_STEPS.md` - Current status and next steps ⭐
- `IMPLEMENTATION_SUMMARY.md` - Technical details
- `QUICKSTART.md` - Quick setup
- `SECURITY.md` - Security patches

### CI/CD
- `.github/workflows/ci.yml` - GitHub Actions pipeline

---

## 🔍 Coverage Analysis

After running tests with coverage:

```bash
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

Look for:
- 🔴 Red lines (not covered) - Need tests
- 🟢 Green lines (covered) - Tested
- 🟡 Yellow lines (partial) - Need edge case tests

Priority: Test red/yellow lines in critical paths:
1. RAG retrieval logic
2. LLM service calls
3. Validation logic
4. API endpoints
5. Error handling

---

## ⚡ Pro Tips

### Testing
1. **Use fixtures** - Define once, use everywhere (conftest.py)
2. **Mock external APIs** - Don't call OpenAI in tests
3. **Test edge cases** - Empty inputs, max values, invalid data
4. **Use markers** - Organize tests (@pytest.mark.unit, @pytest.mark.integration)
5. **Test errors** - Use pytest.raises() for expected failures

### Code Quality
1. **Format before commit** - Run black and isort
2. **Fix flake8 warnings** - Clean code is maintainable code
3. **Add type hints** - Helps catch bugs early
4. **Write docstrings** - Explain what and why

### Development
1. **Small commits** - One logical change per commit
2. **Test frequently** - Run tests after each change
3. **Read the roadmap** - Understand the big picture (ROADMAP.md)
4. **Check CI** - Fix failures immediately

---

## 🚨 Common Issues

### Issue: Tests fail with OpenAI API errors
**Solution**: Tests should use mocks. Check conftest.py fixtures.

### Issue: Coverage is low
**Solution**: Add tests for uncovered code paths. Check htmlcov/index.html.

### Issue: CI pipeline fails
**Solution**: Run locally first. Check GitHub Actions logs.

### Issue: Import errors in tests
**Solution**: Make sure PYTHONPATH includes project root.

---

## 📞 Quick Links

- **ROADMAP**: Complete 6-phase development plan
- **NEXT_STEPS**: Current status and immediate tasks
- **README**: User-facing documentation
- **IMPLEMENTATION_SUMMARY**: Technical implementation details
- **GitHub Actions**: CI/CD pipeline results

---

## ✅ Definition of Done

A task is complete when:
- ✅ Code is written and works
- ✅ Tests are written and passing
- ✅ Coverage is maintained/improved
- ✅ Code is formatted (black, isort)
- ✅ Linting passes (flake8)
- ✅ Type checks pass (mypy)
- ✅ Documentation updated
- ✅ CI pipeline green
- ✅ Code reviewed
- ✅ Changes committed

---

**Remember**: Focus on completing Phase 2 testing before moving to Phase 3!

**Current Priority**: Write remaining unit tests for RAG, services, and API.

**Next Milestone**: 80% code coverage with all tests passing.

---

**Last Updated**: January 21, 2026  
**Status**: Phase 2 - 50% Complete
