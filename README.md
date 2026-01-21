# Withsocio Reel Script Generator

Production-ready RAG-based Instagram Reel script generation API built with FastAPI, OpenAI, and FAISS.

## Overview

This system generates brand-safe, high-performing Instagram Reel scripts using:
- **RAG (Retrieval-Augmented Generation)**: Finds relevant high-performing examples
- **OpenAI GPT-4**: Generates contextually appropriate scripts
- **FAISS Vector Search**: Efficient semantic similarity search
- **Pydantic Validation**: Strict input/output schemas
- **Brand Safety**: Automated validation and guardrails

## Features

✅ Structured brand intelligence input
✅ Retrieval-augmented generation with FAISS
✅ Filtered semantic search by sector, hook type, and emotion
✅ Brand voice and safety validation
✅ JSON-only structured outputs
✅ Modular, production-ready architecture
✅ Comprehensive error handling and retry logic
✅ FastAPI with OpenAPI documentation

## Architecture

```
app/
├── main.py                 # FastAPI application entry point
├── api/
│   └── routes.py          # API endpoint definitions
├── models/
│   ├── brand.py           # Brand profile schema
│   ├── script_request.py  # Script request schema
│   └── output.py          # Output schemas
├── rag/
│   ├── embed.py           # Embedding generation & FAISS
│   └── retrieve.py        # Semantic retrieval
├── prompts/
│   ├── system.txt         # System prompt
│   └── instruction.txt    # Instruction template
├── validation/
│   ├── rules.py           # Validation rules
│   └── checks.py          # Validation logic
├── services/
│   ├── llm.py            # LLM service
│   └── generator.py      # Main generator orchestrator
└── utils/
    └── config.py         # Configuration management
```

## Installation

### Prerequisites

- Python 3.10+
- OpenAI API key

### Setup

1. Clone the repository:
```bash
git clone https://github.com/ayrus15/Withsocio-Scripting-Model.git
cd Withsocio-Scripting-Model
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Configuration

Edit `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
MAX_TOKENS=1500
TEMPERATURE=0.7
TOP_K_RESULTS=5
```

## Running the API

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Usage

### Generate Reel Script

**Endpoint**: `POST /api/generate-reel`

**Request Body**:
```json
{
  "brand_profile": {
    "brand_name": "FitLife Pro",
    "sector": "fitness",
    "target_audience": {
      "age_range": "25-40",
      "gender": "All",
      "location": "USA",
      "pain_points": ["lack of motivation", "time constraints"]
    },
    "brand_voice": ["energetic", "motivational", "authentic"],
    "offer": "AI-powered home workout plans",
    "platform": "instagram",
    "cta_style": "direct",
    "do_not_use": ["lazy", "fat"]
  },
  "script_request": {
    "goal": "conversion",
    "hook_type": "question",
    "emotion": "curiosity",
    "script_length": 30,
    "language": "english",
    "cta": "Download the app now!"
  }
}
```

**Response**:
```json
{
  "script": {
    "hook": "Tired of expensive gym memberships?",
    "body": "What if I told you that you can get fit at home...",
    "cta": "Download FitLife Pro now and start your transformation!",
    "caption": "Your fitness journey starts at home 💪",
    "hashtags": ["#FitnessGoals", "#HomeWorkout", "#FitLife"]
  },
  "validation": {
    "is_valid": true,
    "errors": [],
    "warnings": []
  },
  "metadata": {
    "brand": "FitLife Pro",
    "sector": "fitness",
    "goal": "conversion"
  }
}
```

### Other Endpoints

- **GET /api/health** - Health check
- **GET /api/sectors** - List available sectors
- **GET /api/hook-types** - List available hook types

## Available Options

### Sectors
- fitness, finance, fashion, beauty, productivity, pets, education, wellness, technology, food, travel, real_estate

### Hook Types
- question, bold_claim, relatable, shocking, curiosity, statistic, story

### Emotions
- excitement, curiosity, urgency, inspiration, fear, joy, surprise

### CTA Styles
- direct, soft, question, command

### Brand Voice
- professional, friendly, energetic, motivational, authentic, casual, humorous, authoritative

## Validation Rules

The system automatically validates:
- ✅ Word count limits (hook: 3-15, body: 20-150, CTA: 3-15)
- ✅ Caption length (50-200 characters)
- ✅ Hashtag count (3-10)
- ✅ Banned words detection
- ✅ CTA effectiveness
- ✅ Brand voice alignment

## Development

### Project Structure Philosophy

- **Separation of Concerns**: Each module has a single responsibility
- **No Business Logic in Routes**: API layer only handles HTTP
- **Type Safety**: Pydantic models for all data
- **Testability**: Services are independently testable
- **Configuration**: Centralized in config.py

### Adding New Examples

To add high-performing examples to the FAISS index:

1. Edit `app/rag/retrieve.py`
2. Add to `sample_documents` in `_initialize_sample_index()`
3. Delete existing `data/` directory
4. Restart the server (index will be recreated)

### Extending the System

**Add New Validation Rule**:
1. Add rule to `app/validation/rules.py`
2. Implement check in `app/validation/checks.py`

**Add New Prompt Template**:
1. Create file in `app/prompts/`
2. Load in `app/services/llm.py`

**Change LLM Provider**:
1. Modify `app/services/llm.py`
2. Update `app/utils/config.py`

## Production Considerations

### Before Deployment

1. **Security**:
   - Set proper CORS origins
   - Use secrets management (not .env)
   - Add rate limiting
   - Implement authentication

2. **Performance**:
   - Use production ASGI server (Gunicorn + Uvicorn)
   - Enable response caching
   - Optimize FAISS index size
   - Add request queuing

3. **Monitoring**:
   - Add application logging
   - Set up error tracking (Sentry)
   - Monitor API metrics
   - Track generation costs

4. **Data**:
   - Populate FAISS with real high-performing examples
   - Regularly update reference examples
   - Version control prompts

### Deployment Example

```bash
# Production server
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Testing

The system includes sample data for testing. Test the endpoint:

```bash
curl -X POST http://localhost:8000/api/generate-reel \
  -H "Content-Type: application/json" \
  -d @example_request.json
```

## Troubleshooting

**Issue**: `FileNotFoundError: Index file not found`
- **Solution**: Index will be created automatically on first run with sample data

**Issue**: `OpenAI API authentication error`
- **Solution**: Check `.env` file has valid `OPENAI_API_KEY`

**Issue**: Validation errors in response
- **Solution**: Check validation.errors in response and adjust inputs

**Issue**: Slow response times
- **Solution**: Reduce `TOP_K_RESULTS` or use smaller embedding model

## License

[Add license information]

## Contributing

[Add contribution guidelines]

## Support

For issues and questions:
- GitHub Issues: [Repository Issues](https://github.com/ayrus15/Withsocio-Scripting-Model/issues)
- Documentation: [API Docs](http://localhost:8000/docs)

