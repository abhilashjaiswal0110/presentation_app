# Quick Reference Card

A condensed reference for common tasks and commands.

## 🚀 Getting Started (30 seconds)

```bash
# Backend
cd backend && python -m venv venv && source venv/bin/activate  # or venv\Scripts\activate (Windows)
pip install -r requirements.txt && cd pptx_converter && npm install && cd ..
cp .env.example .env  # Add your API keys
uvicorn main:app --reload

# Frontend (new terminal)
cd web && npm install
cp .env.example .env.local
npm run dev
```

## 🔑 Required API Keys

- **Anthropic**: https://console.anthropic.com/ → API Keys
- **LlamaCloud**: https://cloud.llamaindex.ai/ → API Keys (optional)

## 📡 Default Ports

- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

## 🔧 Common Commands

### Backend
```bash
# Run
uvicorn main:app --reload

# With debug logging
uvicorn main:app --reload --log-level debug

# Different port
uvicorn main:app --reload --port 8001

# Tests
pytest
pytest -v  # verbose
pytest --cov  # with coverage

# Code quality
black .  # format
flake8 .  # lint
mypy .  # type check
```

### Frontend
```bash
# Run
npm run dev

# Different port
npm run dev -- -p 3001

# Build
npm run build
npm start  # production server

# Tests
npm test
npm run lint
npm run typecheck
```

## 📂 Key Files

| File | Purpose |
|------|---------|
| `backend/main.py` | FastAPI app entry point |
| `backend/agent.py` | Claude Agent integration |
| `backend/models.py` | Data models |
| `web/src/app/page.tsx` | Main frontend page |
| `web/src/lib/api.ts` | API client |

## 🐛 Quick Troubleshooting

### "Module not found"
```bash
# Backend: reinstall dependencies
pip install -r requirements.txt

# Frontend: reinstall dependencies
rm -rf node_modules && npm install
```

### "Port already in use"
```bash
# Find and kill process
# Windows: netstat -ano | findstr :8000
# Linux/Mac: lsof -ti:8000 | xargs kill
```

### "API key invalid"
- Check `.env` file has no extra spaces
- Verify key is active in provider console
- Ensure no quotes around the key

### "CORS error"
```env
# backend/.env
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## 📖 Documentation

- **Setup**: [Setup Guide](setup-guide.md) - First-time setup
- **Technical**: [Technical Documentation](technical/README.md) - Deep dive
- **Contributing**: [Contributing Guide](../CONTRIBUTING.md) - How to contribute
- **Security**: [Security Policy](../SECURITY.md) - Security guidelines

## 🔐 Security Reminders

- ❌ NEVER commit `.env` files
- ✅ Use `.env.example` templates
- ✅ Rotate API keys regularly
- ✅ Use HTTPS in production

## 📝 Commit Convention

```
<type>(<scope>): <subject>

Types: feat, fix, docs, style, refactor, test, chore
Examples:
  feat(agent): add custom layouts
  fix(export): resolve Windows path issue
  docs(api): update endpoint descriptions
```

## 🧪 Testing Checklist

- [ ] All tests pass (`pytest` / `npm test`)
- [ ] Code formatted (`black` / `npm run lint`)
- [ ] Type checking passes (`mypy` / `npm run typecheck`)
- [ ] Manual testing completed
- [ ] Documentation updated

## 🔗 Quick Links

- Health Check: http://localhost:8000/health
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:3000

## 💡 Pro Tips

1. **Keep both terminals open** - One for backend, one for frontend
2. **Watch the logs** - They show real-time activity
3. **Use `--reload`** - Auto-restarts on code changes
4. **Check `/docs`** - Interactive API documentation
5. **Test locally first** - Before pushing changes

## 🆘 Need Help?

1. Check `SETUP.md` Troubleshooting section
2. Search GitHub Issues
3. Create new issue with template
4. Read `TECHNICAL_DOCUMENTATION.md`

---

**Print this card and keep it handy!** 📋
