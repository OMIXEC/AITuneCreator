# AITuneCreator Developer Guide

Quick reference guide for developers working with AITuneCreator across test, dev, and prod environments.

## Quick Start (5 minutes)

```bash
# 1. Clone and navigate
git clone <repo-url>
cd AITuneCreator

# 2. Setup
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .

# 3. Configure
cp .env.example .env.dev
# Edit .env.dev: Add your GROQ_API_KEY from https://console.groq.com

# 4. Run
export ENV=dev
streamlit run app.py
```

Visit: `http://localhost:8501`

---

## Environment Setup Checklist

### For Development (Your Machine)

- [ ] Python 3.11+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed: `pip install -e .`
- [ ] `.env.dev` created from `.env.example`
- [ ] `GROQ_API_KEY` added to `.env.dev`
- [ ] App runs: `export ENV=dev && streamlit run app.py`
- [ ] Verify at `http://localhost:8501`

### For Testing (CI/CD or Local Tests)

- [ ] Virtual environment set up (same as dev)
- [ ] `.env.test` created with test API key
- [ ] App starts: `export ENV=test && streamlit run app.py --logger.level=debug`
- [ ] Verify at `http://localhost:8502`

### For Production (Deployment Server)

- [ ] Production API keys configured securely
- [ ] Docker image built: `docker build -t aituner-creator:latest .`
- [ ] Environment variables set via secrets management
- [ ] Deployment verified: `curl http://<prod-endpoint>:8501`

---

## The Three Environments

| Aspect | Development | Testing | Production |
|--------|-------------|---------|-----------|
| **Purpose** | Local development | Automated testing | Live users |
| **API Calls** | Full, unlimited | Minimal/cached | Full, optimized |
| **Config File** | `.env.dev` | `.env.test` | Container secrets |
| **Port** | 8501 | 8502 | 8501 |
| **Logging** | DEBUG | INFO | WARNING |
| **Caching** | Disabled | Enabled | Enabled |

---

## File Structure

```
AITuneCreator/
├── app.py                    # Main Streamlit app
├── app/
│   ├── main.py              # MusicLLM class
│   └── utils.py             # Audio utilities
├── requirements.txt         # Python dependencies
├── setup.py                 # Package setup
├── Dockerfile               # Container definition
├── kubernetes-deployment.yaml # K8s manifest
├── .gitlab-ci.yml           # CI/CD pipeline
├── .env.example             # Config template
├── CLAUDE.md                # Claude Code guidance
└── DEVELOPER_GUIDE.md       # This file
```

---

## Common Tasks

### 1. Adding New Features

```bash
# 1. Activate environment
source venv/bin/activate
export ENV=dev

# 2. Make changes to code

# 3. Test changes
streamlit run app.py

# 4. Commit when ready
git add <files>
git commit -m "feature: description"
```

### 2. Running in Different Environments

**Development:**
```bash
export ENV=dev
streamlit run app.py
```

**Testing:**
```bash
export ENV=test
streamlit run app.py --logger.level=debug
```

**Production (Docker):**
```bash
docker build -t aituner-creator:latest .
docker run -p 8501:8501 \
  -e ENV=prod \
  -e GROQ_API_KEY=$PROD_KEY \
  aituner-creator:latest
```

### 3. Debugging Issues

**Check environment setup:**
```bash
python -c "
import os
from dotenv import load_dotenv
env = os.getenv('ENV', 'dev')
load_dotenv(f'.env.{env}')
print(f'Loaded: .env.{env}')
print(f'API Key: {\"SET\" if os.getenv(\"GROQ_API_KEY\") else \"NOT SET\"}')"
```

**Test API connectivity:**
```bash
python -c "
from app.main import MusicLLM
llm = MusicLLM()
print('✓ LLM initialized successfully')
"
```

**Check Python dependencies:**
```bash
pip list | grep -E 'streamlit|langchain|groq'
```

---

## Environment Variables Explained

### Required

| Variable | Purpose | Example |
|----------|---------|---------|
| `GROQ_API_KEY` | Groq API authentication | `gsk_...` |
| `ENVIRONMENT` | Environment name | `dev` / `test` / `prod` |

### Optional

| Variable | Purpose | Default | Dev | Test | Prod |
|----------|---------|---------|-----|------|------|
| `STREAMLIT_SERVER_PORT` | Server port | 8501 | 8501 | 8502 | 8501 |
| `LOG_LEVEL` | Logging verbosity | DEBUG | DEBUG | INFO | WARNING |
| `ENABLE_CACHING` | Cache responses | false | false | true | true |

---

## Deployment Checklist

### Before Deploying to Production

- [ ] Code reviewed and tested locally
- [ ] All dependencies in `requirements.txt`
- [ ] No hardcoded secrets or API keys in code
- [ ] `.env` files not committed to git
- [ ] Dockerfile builds successfully
- [ ] Environment variables configured in secrets manager
- [ ] CI/CD pipeline passes
- [ ] Production GROQ_API_KEY configured securely

### Deployment Steps

1. **Push to main branch:**
   ```bash
   git push origin main
   ```

2. **Monitor CI/CD:**
   - Go to GitLab → Pipelines
   - Watch build and deploy stages

3. **Verify deployment:**
   ```bash
   curl http://<prod-endpoint>:8501
   ```

4. **Check logs:**
   ```bash
   kubectl logs -f deployment/aituner-creator
   ```

---

## Troubleshooting

### "ModuleNotFoundError" or Import Errors
```bash
# Reinstall dependencies
pip install --force-reinstall -e .
```

### "GROQ_API_KEY not found"
```bash
# Verify .env file exists and has the key
cat .env.dev
# Make sure it's loaded before running
export ENV=dev
streamlit run app.py
```

### Port 8501 Already in Use
```bash
# Use a different port
streamlit run app.py --server.port 8080
```

### Virtual Environment Corrupted
```bash
# Recreate it
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install -e .
```

### Docker Build Fails
```bash
# Clear cache and rebuild
docker build --no-cache -t aituner-creator:latest .
```

---

## Development Workflow Example

```bash
# Morning: Start development
source venv/bin/activate
export ENV=dev

# Work: Make changes
# (Edit code in your editor)
streamlit run app.py  # Auto-reloads on changes

# Lunchtime: Check different environment
export ENV=test
streamlit run app.py --logger.level=debug

# Afternoon: Commit changes
deactivate  # Exit venv
git add .
git commit -m "fix: melody generation for short inputs"
git push origin feature-branch

# Evening: Create pull request and monitor CI/CD
# (Go to GitLab/GitHub and create PR)
```

---

## Tips & Best Practices

- **Use virtual environments**: Always activate `venv` before working
- **Set ENV variable**: Always `export ENV=<dev|test|prod>` before running
- **Never commit secrets**: Keep `.env` files local only
- **Test before pushing**: Run locally in dev environment first
- **Check logs**: Use `--logger.level=debug` to see detailed output
- **Use `.env.test` for CI/CD**: Configure test API key in CI/CD secrets
- **Monitor API costs**: Use caching in test/prod to reduce API calls

---

## Getting Help

1. **Check CLAUDE.md** - Comprehensive technical guide
2. **Review error messages** - Usually tell you exactly what's wrong
3. **Check environment variables** - Most issues are config-related
4. **Test imports** - Verify dependencies are installed
5. **Read code comments** - Documentation in main.py and utils.py

For more detailed information, see **CLAUDE.md**.
