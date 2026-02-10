# Presentation App

AI-powered PowerPoint generation agent. Chat interface to create and edit presentations.

## Stack

- **Backend**: FastAPI + Claude Agent SDK + Node.js (pptxgenjs)
- **Frontend**: Next.js 15 + React 19 + TypeScript + Tailwind CSS
- **Runtime**: Python 3.12, Node.js 18+
- **Architecture**: Forked from [form-filling-exp](https://github.com/jerryjliu/form_filling_app)

## Key Files

```
backend/
  agent.py              # Claude Agent SDK, MCP tool definitions, system prompts
  main.py               # FastAPI server, SSE streaming endpoints — run with: python main.py
  parser.py             # LlamaParse integration for context file / template parsing
  session.py            # Session persistence (SQLite-backed)
  models.py             # Pydantic data models (Presentation, Slide, PendingEdit)
  pptx_converter/       # Node.js service: HTML → PPTX/PDF via pptxgenjs + Puppeteer
  test_ppt_creation.py  # End-to-end integration test (requires running backend)

web/src/
  app/page.tsx          # Main app component
  lib/api.ts            # API client with SSE streaming
  lib/session.ts        # Session persistence
```

## Commands

```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux
pip install -r requirements.txt
cd pptx_converter && npm install && cd ..
python main.py                 # Starts on :8000 (loads .env automatically)

# Frontend
cd web && npm install
cd web && npm run dev          # Starts on :3000
```

## Environment Variables

```env
# backend/.env  (required)
ANTHROPIC_API_KEY=sk-ant-...
LLAMA_CLOUD_API_KEY=llx-...    # optional — enables LlamaParse document parsing

# web/.env.local  (optional — defaults shown)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

The backend loads `backend/.env` automatically via `python-dotenv` at startup.

## API Endpoints (key)

| Endpoint                              | Method | Description                              |
|---------------------------------------|--------|------------------------------------------|
| `/health`                             | GET    | Health check                             |
| `/agent-stream`                       | POST   | Stream agent interaction (SSE)           |
| `/session/{id}`                       | GET    | Get session state + presentation         |
| `/session/{id}/slides`                | GET    | List all slides                          |
| `/session/{id}/slides/{idx}`          | PATCH  | Update a slide's HTML                    |
| `/session/{id}/export`                | GET    | Download as PPTX                         |
| `/session/{id}/export/pdf`            | GET    | Download as PDF                          |
| `/parse-files`                        | POST   | Parse uploaded documents (SSE)           |
| `/parse-template`                     | POST   | Parse PPTX template + extract screenshots|
| `/validate-api-key`                   | POST   | Validate LlamaCloud key                  |
| `/validate-anthropic-key`             | POST   | Validate Anthropic key                   |
| `/docs`                               | GET    | Interactive Swagger UI                   |

## Agent Tools (MCP)

Tools exposed via in-process MCP server (`create_sdk_mcp_server`):

| Tool                  | Description                                      |
|-----------------------|--------------------------------------------------|
| `create_presentation` | Start a new presentation with a title            |
| `add_slide`           | Add slide HTML at a given position               |
| `update_slide`        | Replace a slide's HTML content                   |
| `delete_slide`        | Remove a slide by index                          |
| `reorder_slides`      | Move a slide from one index to another           |
| `list_slides`         | List all slides with index + text preview        |
| `get_slide`           | Get full HTML and metadata for one slide         |
| `set_theme`           | Set presentation theme (colors, fonts)           |
| `get_pending_edits`   | Inspect uncommitted edits                        |
| `commit_edits`        | Apply all pending edits and persist the session  |

## Integration Test

```bash
# With backend running on :8000
cd backend
python test_ppt_creation.py
```

Verifies: agent stream → session creation → PPTX export end-to-end.

## Context Files

- `research.md` - Comprehensive architecture research, patterns from form-filler, competitive analysis
- `plans/*.md` - Implementation plans with phases and success criteria
- `research/*.md` - Research documents from `/research` command
- `.claude/history/*.md` - Compacted conversation summaries

## Custom Commands

- `/create_plan <task>` - Create detailed implementation plan
- `/implement_plan <path>` - Execute plan phase-by-phase
- `/research <topic>` - Research codebase, output to research/
