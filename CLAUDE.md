# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AITuneCreator is a Streamlit-based web application that generates AI-composed music by combining LLM-generated melodies, harmonies, and rhythms into audio output. The application uses:

- **Streamlit**: Web UI framework
- **LangChain**: LLM orchestration
- **Groq API** (llama-3.1-8b-instant model): LLM backend for generating musical components
- **music21**: Note parsing and music theory
- **synthesizer**: Audio synthesis from frequencies
- **scipy**: WAV file generation

## Architecture

### Core Components

1. **app.py** - Entry point
   - Streamlit UI setup and orchestration
   - Handles user input (music description, style selection)
   - Coordinates the music generation pipeline
   - Renders audio output and composition summary

2. **app/main.py** - `MusicLLM` class
   - Wraps Groq API calls with LangChain
   - Four main methods for music generation:
     - `generate_melody()`: Converts user description to space-separated notes
     - `generate_harmony()`: Creates chord progressions (format: C4-E4-G4 F4-A4-C5)
     - `generate_rythm()`: Generates beat durations (format: 1.0 0.5 0.5 2.0)
     - `adapt_style()`: Applies style modifiers (Sad, Happy, Jazz, Romantic, Extreme)

3. **app/utils.py** - Utility functions
   - `note_to_frequencies()`: Converts music21 note strings to Hz frequencies
   - `generate_wav_bytes_from_notes_freq()`: Synthesizes WAV audio from frequency arrays using sine wave synthesis

### Data Flow

```
User Input (description + style)
  ↓
MusicLLM.generate_melody() → melody notes (space-separated)
  ↓
MusicLLM.generate_harmony() → harmony chords
MusicLLM.generate_rythm() → rhythm durations
  ↓
MusicLLM.adapt_style() → composition summary
  ↓
Parse melody/harmony → frequencies (music21)
  ↓
Generate WAV bytes → Streamlit audio widget
```

---

## Developer Setup Guide (Step-by-Step)

### Prerequisites

- Python 3.11+
- pip package manager
- Git
- Access to Groq API keys (https://console.groq.com)

### Step 1: Clone and Initial Setup

```bash
# Clone the repository
git clone <repository-url>
cd AITuneCreator

# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### Step 2: Environment Configuration

#### 2a. Understand Environment Variables

The application supports three environments: **test**, **dev**, and **prod**. Each has different configurations:

- **test**: Minimal API calls, cached responses for testing
- **dev**: Full functionality with development API keys
- **prod**: Optimized for production with monitoring

#### 2b. Create Environment Files

Create the following `.env` files from `.env.example`:

```bash
# For development (local machine)
cp .env.example .env.dev
# Edit .env.dev with your dev credentials

# For testing (CI/CD or local testing)
cp .env.example .env.test
# Edit .env.test with test API keys (can use mock values)

# For production (production server)
cp .env.example .env.prod
# Edit .env.prod with prod credentials (configure only in production)
```

#### 2c. Configure Each Environment

**`.env.dev` (Development)**
```
ENVIRONMENT=dev
GROQ_API_KEY=<your-dev-groq-api-key>
STREAMLIT_SERVER_PORT=8501
LOG_LEVEL=DEBUG
ENABLE_CACHING=false
```

**`.env.test` (Testing)**
```
ENVIRONMENT=test
GROQ_API_KEY=sk-test-dummy-key-for-testing
STREAMLIT_SERVER_PORT=8502
LOG_LEVEL=INFO
ENABLE_CACHING=true
```

**`.env.prod` (Production)**
```
ENVIRONMENT=prod
GROQ_API_KEY=<your-prod-groq-api-key>
STREAMLIT_SERVER_PORT=8501
LOG_LEVEL=WARNING
ENABLE_CACHING=true
```

### Step 3: Install Dependencies

```bash
# Install in development mode (includes all dependencies)
pip install -e .

# Verify installation
pip list | grep -E "streamlit|langchain|groq|music21"
```

### Step 4: Load Environment Based on Context

#### For Development
```bash
# Load .env.dev automatically
export ENV=dev
streamlit run app.py
# App will be available at http://localhost:8501
```

#### For Testing
```bash
# Load .env.test for local testing
export ENV=test
streamlit run app.py --logger.level=debug
# App will be available at http://localhost:8502
```

#### For Production
```bash
# Load .env.prod (typically on production server)
export ENV=prod
streamlit run app.py --server.headless=true --server.port=8501
```

### Step 5: Verify Setup

```bash
# Test imports and API connectivity
python -c "
import os
from dotenv import load_dotenv
from app.main import MusicLLM

env = os.getenv('ENV', 'dev')
load_dotenv(f'.env.{env}')

print(f'Environment: {env}')
print(f'GROQ_API_KEY set: {bool(os.getenv(\"GROQ_API_KEY\"))}')

try:
    llm = MusicLLM()
    print('MusicLLM initialized successfully')
except Exception as e:
    print(f'Error initializing MusicLLM: {e}')
"
```

---

## Environment-Specific Workflows

### Development Workflow

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Set development environment
export ENV=dev

# 3. Run the app
streamlit run app.py

# 4. Access at http://localhost:8501
# 5. Make code changes - Streamlit auto-reloads

# 6. When done, deactivate
deactivate
```

### Testing Workflow

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Set test environment
export ENV=test

# 3. Run tests (add test suite as project grows)
# pytest tests/

# 4. Run app in test mode
streamlit run app.py --logger.level=debug

# 5. Verify with test API key
```

### Production Deployment Workflow

```bash
# 1. Ensure production environment variables are set on the server
# This should be done via:
# - Docker secrets
# - Kubernetes secrets
# - Environment management service (e.g., GitLab CI/CD variables)

# 2. Build Docker image
docker build -t aituner-creator:latest .

# 3. Run container with production environment
docker run -d \
  --name aituner-prod \
  -p 8501:8501 \
  -e ENV=prod \
  -e GROQ_API_KEY=$PROD_GROQ_API_KEY \
  aituner-creator:latest

# 4. Verify deployment
curl http://localhost:8501
```

---

## Common Development Commands

### Local Development

```bash
# Install in development mode with all dependencies
pip install -e .

# Run the Streamlit app (dev environment)
export ENV=dev && streamlit run app.py

# Run with custom port
export ENV=dev && streamlit run app.py --server.port 8080

# Run with debug logging
export ENV=dev && streamlit run app.py --logger.level=debug

# Check code structure
python -c "from app.main import MusicLLM; print(MusicLLM.__doc__)"
```

### Testing and Validation

```bash
# Verify all dependencies are installed
pip list

# Test Python syntax
python -m py_compile app.py app/main.py app/utils.py

# Verify imports work
python -c "import streamlit; import langchain; import music21; print('All imports OK')"

# Test environment setup
python -c "import os; from dotenv import load_dotenv; load_dotenv('.env.dev'); print(f'API Key set: {bool(os.getenv(\"GROQ_API_KEY\"))}')"
```

### Docker Operations

```bash
# Build Docker image
docker build -t aituner-creator:latest .

# Run locally in Docker (dev)
docker run -p 8501:8501 \
  -e ENV=dev \
  -e GROQ_API_KEY=$DEV_GROQ_API_KEY \
  aituner-creator:latest

# Build and push to registry
docker build -t us-central1-docker.pkg.dev/project/repo/aituner-creator:latest .
docker push us-central1-docker.pkg.dev/project/repo/aituner-creator:latest
```

---

## Environment Variables Reference

| Variable | Required | Dev Value | Test Value | Prod Value |
|----------|----------|-----------|-----------|-----------|
| `ENVIRONMENT` | Yes | `dev` | `test` | `prod` |
| `GROQ_API_KEY` | Yes | Valid Groq API key | Mock test key | Valid Groq API key |
| `STREAMLIT_SERVER_PORT` | No | `8501` | `8502` | `8501` |
| `LOG_LEVEL` | No | `DEBUG` | `INFO` | `WARNING` |
| `ENABLE_CACHING` | No | `false` | `true` | `true` |

---

## Deployment Guide

### Docker

The project includes a Dockerfile for containerization:
- Base image: python:3.11-slim
- Installs dependencies via `pip install -e .`
- Exposes port 8501
- Runs: `streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true`

### Kubernetes/GCP

Deployment is orchestrated via:
- `.gitlab-ci.yml`: GitLab CI/CD pipeline that builds Docker image and deploys to GKE
- `kubernetes-deployment.yaml`: Kubernetes deployment manifest
- GCP service account with Artifact Registry and Container permissions

The CI/CD pipeline requires:
- `GCP_SA_KEY`: Base64-encoded GCP service account key as GitLab CI/CD secret
- GKE cluster credentials configured with `GROQ_API_KEY` as a Kubernetes secret

**Deploy via CI/CD:**
1. Push to main branch
2. GitLab CI/CD automatically triggers
3. Pipeline builds Docker image
4. Pipeline deploys to GKE cluster
5. App is available at configured service endpoint

---

## Key Design Patterns

### LLM Integration

- Uses LangChain's `ChatPromptTemplate` and pipe operator syntax (`|`) for prompt chaining
- Temperature set to 0.7 (moderate creativity)
- Simple string parsing of LLM outputs (space/dash-separated values)

### Audio Generation

- Converts musical notes to frequencies using music21's pitch calculations
- Uses sine wave synthesis via the `synthesizer` library
- Concatenates individual note waves with 0.5-second duration each
- Outputs as 44100 Hz WAV format

### Error Handling

- Note parsing uses try-except to skip invalid notes (app/utils.py:10-14)
- UI validation checks for non-empty music input before generating

---

## Troubleshooting

### Virtual Environment Issues
```bash
# If venv is corrupted, recreate it
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -e .
```

### Missing Dependencies
```bash
# Reinstall all dependencies
pip install --force-reinstall -r requirements.txt
```

### API Key Issues
```bash
# Verify API key is loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv('.env.dev'); print('Key:', os.getenv('GROQ_API_KEY')[:10]+'...')"
```

### Streamlit Port Already in Use
```bash
# Use different port
export ENV=dev && streamlit run app.py --server.port 8080
```

---

## Important Notes

- The app is stateless and generates music on-demand per request
- No persistent storage of generated music or user data
- LLM responses are parsed with string split/join operations—format consistency is important
- The Groq API key must be available in the environment for the app to function
- Always use `.env.dev` locally and never commit `.env` files to version control
- Keep API keys in CI/CD secrets, not in code or config files
- Test environment should use mock or test API keys for cost efficiency
