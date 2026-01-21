# Quick Start Guide

Get the Withsocio Reel Script Generator running in 5 minutes.

## Prerequisites

- Python 3.10 or higher
- OpenAI API key

## Installation Steps

### 1. Clone and Setup

```bash
git clone https://github.com/ayrus15/Withsocio-Scripting-Model.git
cd Withsocio-Scripting-Model
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### 3. Start Server

```bash
uvicorn app.main:app --reload
```

You should see:
```
INFO: Uvicorn running on http://127.0.0.1:8000
```

### 4. Test the API

Open your browser and go to:
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

### 5. Generate Your First Script

Using curl:
```bash
curl -X POST http://localhost:8000/api/generate-reel \
  -H "Content-Type: application/json" \
  -d @example_request.json
```

Or use the interactive docs at http://localhost:8000/docs

## What's Next?

- Read the [full README](README.md) for detailed documentation
- Check [IMPLEMENTATION_SUMMARY](IMPLEMENTATION_SUMMARY.md) for technical details
- Explore available sectors: http://localhost:8000/api/sectors
- Try different hook types: http://localhost:8000/api/hook-types

## Common Issues

**Issue**: `OpenAI API authentication error`
- **Fix**: Check your API key in `.env` file

**Issue**: `ModuleNotFoundError`
- **Fix**: Run `pip install -r requirements.txt` again

**Issue**: `Port 8000 already in use`
- **Fix**: Use a different port: `uvicorn app.main:app --port 8001`

## Support

- GitHub Issues: https://github.com/ayrus15/Withsocio-Scripting-Model/issues
- Documentation: http://localhost:8000/docs
