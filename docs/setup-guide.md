# Local Setup Guide

This guide will help you set up the Presentation App for local development.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Initial Setup](#initial-setup)
- [Running the Application](#running-the-application)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

## Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

1. **Python 3.10 or higher**
   - Check version: `python --version` or `python3 --version`
   - Download: https://www.python.org/downloads/
   - **Windows Users**: Make sure to check "Add Python to PATH" during installation

2. **Node.js 18.x or higher**
   - Check version: `node --version`
   - Download: https://nodejs.org/
   - npm comes bundled with Node.js

3. **Git**
   - Check version: `git --version`
   - Download: https://git-scm.com/downloads

### Required API Keys

1. **Anthropic API Key** (Required)
   - Sign up at: https://console.anthropic.com/
   - Navigate to API Keys section
   - Create a new API key
   - **Pricing**: Pay-as-you-go (Claude Sonnet 4 costs ~$3-$15 per million tokens)

2. **LlamaCloud API Key** (Optional - for document parsing)
   - Sign up at: https://cloud.llamaindex.ai/
   - Navigate to API Keys section
   - Create a new API key
   - **Free tier**: 1,000 pages per month

## Initial Setup

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd presentation_app
```

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell):
venv\Scripts\Activate.ps1
# On Windows (CMD):
venv\Scripts\activate.bat
# On macOS/Linux:
source venv/bin/activate

# You should see (venv) in your terminal prompt

# Upgrade pip
python -m pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies for PPTX converter
cd pptx_converter
npm install
cd ..

# Copy environment template
# On Windows (PowerShell):
Copy-Item .env.example .env
# On Windows (CMD):
copy .env.example .env
# On macOS/Linux:
cp .env.example .env

# Edit .env file with your API keys
# Use your preferred text editor:
# - Windows: notepad .env
# - macOS: nano .env or open .env
# - Linux: nano .env or vim .env
```

**Edit the `.env` file and add your API keys:**
```env
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
LLAMA_CLOUD_API_KEY=llx-your-actual-key-here
```

### Step 3: Frontend Setup

Open a new terminal (keep the backend terminal open):

```bash
# Navigate to frontend directory
cd web

# Install dependencies
npm install

# Copy environment template
# On Windows (PowerShell):
Copy-Item .env.example .env.local
# On Windows (CMD):
copy .env.example .env.local
# On macOS/Linux:
cp .env.example .env.local

# The default configuration should work, but you can edit if needed
# Use your preferred text editor to edit .env.local
```

## Running the Application

### Terminal 1: Start Backend

```bash
cd backend

# Activate virtual environment (if not already activated)
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Start the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# You should see:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete
```

**Verify Backend:**
- Open http://localhost:8000/health in your browser
- You should see: `{"status": "healthy"}`
- Open http://localhost:8000/docs for API documentation

### Terminal 2: Start Frontend

```bash
cd web

# Start the Next.js development server
npm run dev

# You should see:
# ▲ Next.js 15.x.x
# - Local:   http://localhost:3000
# - Ready in X.Xs
```

**Verify Frontend:**
- Open http://localhost:3000 in your browser
- You should see the Presentation App interface

### Using the Application

1. **Enter API Key**: On first load, you'll be prompted to enter your Anthropic API key
2. **Start Creating**: Type a message like "Create a 3-slide deck about artificial intelligence"
3. **Watch It Generate**: Claude will create slides in real-time
4. **Iterate**: Make changes by describing what you want
5. **Export**: Download your presentation as a PPTX file

## Troubleshooting

### Backend Issues

#### Issue: `ModuleNotFoundError: No module named 'fastapi'`
**Solution**: Make sure virtual environment is activated and dependencies are installed
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

#### Issue: `Error: Cannot find module 'pptxgenjs'`
**Solution**: Install Node.js dependencies for PPTX converter
```bash
cd backend/pptx_converter
npm install
```

#### Issue: `Invalid API key`
**Solution**: 
- Double-check your API key in `backend/.env`
- Ensure there are no extra spaces or quotes
- Verify the key is active in Anthropic console

#### Issue: Port 8000 already in use
**Solution**: Either stop the other process or use a different port
```bash
# Find process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <pid> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill

# Or use different port:
uvicorn main:app --reload --port 8001
# Update NEXT_PUBLIC_API_URL in web/.env.local to http://localhost:8001
```

### Frontend Issues

#### Issue: `Error: Cannot find module`
**Solution**: Delete `node_modules` and reinstall
```bash
cd web
rm -rf node_modules  # or rmdir /s node_modules on Windows
npm install
```

#### Issue: Port 3000 already in use
**Solution**: 
```bash
# Next.js will automatically try port 3001, 3002, etc.
# Or manually specify:
npm run dev -- -p 3001
```

#### Issue: Cannot connect to backend
**Solution**: 
- Verify backend is running on http://localhost:8000
- Check `NEXT_PUBLIC_API_URL` in `web/.env.local`
- Check browser console for CORS errors
- Ensure `CORS_ORIGINS` in `backend/.env` includes frontend URL

### CORS Issues

#### Issue: `Access-Control-Allow-Origin` error
**Solution**: Update CORS origins in `backend/.env`
```env
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:3001
```

### Database Issues

#### Issue: Session not persisting
**Solution**: 
```bash
# Check if sessions directory exists
cd backend
mkdir -p sessions_data  # or mkdir sessions_data on Windows

# Verify database file is created
ls sessions.db  # or dir sessions.db on Windows

# If corrupt, delete and restart
rm sessions.db
# Backend will recreate on next startup
```

### Python Virtual Environment Issues

#### Issue: Cannot activate virtual environment on Windows
**Solution**: PowerShell execution policy issue
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again
venv\Scripts\Activate.ps1
```

#### Issue: `python: command not found` (macOS/Linux)
**Solution**: Try `python3` instead
```bash
python3 -m venv venv
python3 -m pip install -r requirements.txt
```

## Next Steps

### Development

- Read [Technical Documentation](technical/README.md) for architecture details
- Check [Quick Reference](quick-reference.md) for common commands
- Review [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines
- Review [SECURITY.md](../SECURITY.md) for security best practices

### Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd web
npm test
```

### Production Deployment

See [Technical Documentation - Deployment](technical/README.md#15-deployment) for:
- Docker deployment
- Cloud platform deployment (AWS, Azure, Render)
- Production configuration
- Security hardening

## Common Commands Reference

### Backend

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install new package
pip install package-name
pip freeze > requirements.txt  # Update requirements

# Run with different settings
uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level debug

# Run tests
pytest
pytest -v  # verbose
pytest --cov  # with coverage
```

### Frontend

```bash
# Install new package
npm install package-name

# Run development server
npm run dev

# Build for production
npm run build
npm start  # Start production server

# Lint and type check
npm run lint
npm run typecheck
```

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Check status
git status

# Stage changes
git add .

# Commit with conventional commit message
git commit -m "feat: add new feature"

# Push to remote
git push origin feature/your-feature-name
```

## Getting Help

If you're still having issues:

1. **Check the logs**:
   - Backend logs in terminal where uvicorn is running
   - Frontend logs in browser console (F12)

2. **Search existing issues**: [GitHub Issues](https://github.com/abhilashjaiswal0110/presentation_app/issues)

3. **Ask for help**: [GitHub Discussions](https://github.com/abhilashjaiswal0110/presentation_app/discussions)

4. **Report a bug**: Create a new issue with:
   - Clear description
   - Steps to reproduce
   - Error messages and logs
   - Environment details (OS, Python version, Node version)

## Environment Checklist

Before starting development, verify:

- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] Git installed
- [ ] Anthropic API key obtained
- [ ] LlamaCloud API key obtained (optional)
- [ ] Backend virtual environment created and activated
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] PPTX converter dependencies installed (`npm install` in `pptx_converter/`)
- [ ] Backend `.env` file configured with API keys
- [ ] Frontend dependencies installed (`npm install` in `web/`)
- [ ] Frontend `.env.local` file created
- [ ] Backend starts successfully on port 8000
- [ ] Frontend starts successfully on port 3000
- [ ] Can access http://localhost:3000 in browser
- [ ] Can create a simple presentation

---

**Happy Coding! 🚀**
