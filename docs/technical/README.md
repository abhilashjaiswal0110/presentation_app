# Technical Documentation

**Version:** 1.0  
**Last Updated:** February 5, 2026  
**Audience:** Developers, DevOps Engineers, Technical Architects

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Architecture](#2-architecture)
3. [Technology Stack](#3-technology-stack)
4. [Getting Started](#4-getting-started)
5. [Development Environment](#5-development-environment)
6. [API Documentation](#6-api-documentation)
7. [Data Models](#7-data-models)
8. [Agent System](#8-agent-system)
9. [Session Management](#9-session-management)
10. [File Processing](#10-file-processing)
11. [PPTX Export](#11-pptx-export)
12. [Security](#12-security)
13. [Performance & Scalability](#13-performance--scalability)
14. [Testing](#14-testing)
15. [Deployment](#15-deployment)
16. [Troubleshooting](#16-troubleshooting)
17. [Contributing](#17-contributing)
18. [Appendix](#18-appendix)

---

## 1. System Overview

### 1.1 Purpose

The Presentation App is an AI-powered presentation generation system that enables users to create, edit, and export presentations through natural language conversation. Built on Claude AI and modern web technologies, it provides an intuitive chat interface for presentation development.

### 1.2 Key Features

- **Natural Language Interface**: Create and edit presentations through conversational AI
- **Real-time Streaming**: Live updates as Claude generates content
- **Context-Aware**: Upload reference documents to inform slide content
- **Template Support**: Apply custom styling and branding
- **Multi-turn Conversations**: Iterative refinement and editing
- **PPTX Export**: Download presentations in PowerPoint format
- **Session Persistence**: Resume work across browser sessions

### 1.3 Use Cases

- **Rapid Prototyping**: Quickly generate presentation drafts
- **Content Repurposing**: Transform documents into slide decks
- **Iterative Design**: Refine presentations through natural conversation
- **Branded Content**: Apply organization templates automatically

---

## 2. Architecture

### 2.1 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Browser                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         Next.js Frontend (React + TypeScript)          │ │
│  │  • Chat Interface  • Slide Viewer  • File Upload      │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/REST + SSE
                     │
┌────────────────────▼────────────────────────────────────────┐
│                   FastAPI Backend (Python)                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Claude Agent SDK Integration             │  │
│  │  • Tool Definitions  • Streaming  • State Management  │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Session Management Layer                 │  │
│  │  • SQLite Persistence  • File Storage  • Cleanup      │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Document Processing                      │  │
│  │  • LlamaParse  • Context Extraction  • Caching        │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              PPTX Export (Node.js Subprocess)         │  │
│  │  • pptxgenjs  • HTML→PPTX  • Styling                  │  │
│  └───────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌──▼────────┐ ┌─▼────────────┐
│  Anthropic   │ │ LlamaCloud│ │  File System │
│  Claude API  │ │    API    │ │   Storage    │
└──────────────┘ └───────────┘ └──────────────┘
```

### 2.2 Component Overview

#### Frontend (Next.js)
- **Framework**: Next.js 15 with React 19
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4
- **State Management**: React hooks and context
- **HTTP Client**: Native Fetch API

#### Backend (FastAPI)
- **Framework**: FastAPI
- **Language**: Python 3.10+
- **AI Integration**: Claude Agent SDK, Anthropic SDK
- **Document Processing**: LlamaCloud Services
- **Persistence**: SQLite + File System

#### Export Layer (Node.js)
- **Runtime**: Node.js
- **Library**: pptxgenjs
- **IPC**: Python subprocess communication

### 2.3 Data Flow

1. **User Input** → Frontend captures message
2. **API Request** → POST to `/agent` endpoint with session context
3. **Agent Processing** → Claude processes request using defined tools
4. **Tool Execution** → Backend executes presentation manipulation tools
5. **State Updates** → Session state persisted to SQLite + filesystem
6. **Streaming Response** → Server-Sent Events stream results to client
7. **UI Update** → Frontend renders updated presentation

---

## 3. Technology Stack

### 3.1 Frontend Dependencies

```json
{
  "dependencies": {
    "next": "15.5.9",              // React framework
    "react": "^19.0.0",            // UI library
    "react-dom": "^19.0.0",        // DOM bindings
    "tailwindcss": "^4"            // Utility-first CSS
  },
  "devDependencies": {
    "typescript": "^5",            // Type safety
    "eslint": "^9",                // Linting
    "@types/node": "^22",          // Node type definitions
    "@types/react": "^19"          // React type definitions
  }
}
```

### 3.2 Backend Dependencies

```
fastapi>=0.109.0              # Web framework
uvicorn>=0.27.0               # ASGI server
anthropic>=0.52.0             # Anthropic API client
claude-agent-sdk>=0.1.0       # Claude Agent SDK
pydantic>=2.0.0               # Data validation
python-multipart>=0.0.6       # File upload support
llama-cloud-services>=0.6.0   # Document parsing
mcp>=1.0.0                    # Model Context Protocol
httpx>=0.27.0                 # Async HTTP client
```

### 3.3 Export Dependencies

```json
{
  "dependencies": {
    "pptxgenjs": "^3.12.0"     // PowerPoint generation
  }
}
```

### 3.4 Required External Services

- **Anthropic Claude API**: AI model access
- **LlamaCloud API**: Document parsing (optional, for context files)

---

## 4. Getting Started

### 4.1 Prerequisites

- **Python**: 3.10 or higher
- **Node.js**: 18.x or higher
- **npm**: 9.x or higher
- **Git**: Latest version

### 4.2 API Keys

You'll need the following API keys:

1. **Anthropic API Key** (Required)
   - Sign up at: https://console.anthropic.com/
   - Create an API key
   - Pricing: Pay-as-you-go (Claude models)

2. **LlamaCloud API Key** (Optional - for context files)
   - Sign up at: https://cloud.llamaindex.ai/
   - Create an API key
   - Free tier available

### 4.3 Quick Start

```bash
# 1. Clone the repository
git clone <repository-url>
cd presentation_app

# 2. Set up backend
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies for PPTX export
cd pptx_converter
npm install
cd ..

# Copy and configure environment file
cp .env.example .env
# Edit .env and add your API keys

# 3. Set up frontend
cd ../web
npm install

# Copy and configure environment file
cp .env.example .env.local
# Edit .env.local if needed

# 4. Start the application
# Terminal 1 - Backend:
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend:
cd web
npm run dev
```

### 4.4 Verify Installation

1. Backend: http://localhost:8000/docs (FastAPI Swagger UI)
2. Frontend: http://localhost:3000 (Next.js app)

---

## 5. Development Environment

### 5.1 Backend Development

#### Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-asyncio black flake8 mypy
```

#### Environment Variables

Create `backend/.env`:

```env
# Required
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LLAMA_CLOUD_API_KEY=llx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional
CLAUDE_MODEL=claude-sonnet-4-20250514
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development
DEBUG=true
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
LOG_LEVEL=INFO
```

#### Running the Backend

```bash
# Development mode with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# With custom log level
uvicorn main:app --reload --log-level debug
```

### 5.2 Frontend Development

#### Environment Variables

Create `web/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENABLE_CONTEXT_FILES=true
NEXT_PUBLIC_ENABLE_TEMPLATES=true
NEXT_PUBLIC_ENABLE_EXPORT=true
NEXT_PUBLIC_APP_TITLE=Presentation App
NEXT_PUBLIC_DEV_MODE=true
```

#### Running the Frontend

```bash
# Development mode
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint

# Type checking
npm run typecheck
```

### 5.3 Project Structure

```
presentation_app/
├── backend/                    # Python FastAPI backend
│   ├── agent.py               # Claude Agent SDK integration
│   ├── main.py                # FastAPI application
│   ├── models.py              # Data models (Pydantic)
│   ├── session.py             # Session management
│   ├── parser.py              # Document parsing (LlamaParse)
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Backend container
│   ├── .env.example           # Environment template
│   └── pptx_converter/        # Node.js PPTX export
│       ├── convert.js         # Main converter
│       ├── convert-pdf.js     # PDF conversion
│       └── package.json       # Node dependencies
│
├── web/                        # Next.js frontend
│   ├── src/
│   │   ├── app/               # Next.js 15 app directory
│   │   │   ├── layout.tsx     # Root layout
│   │   │   ├── page.tsx       # Home page
│   │   │   └── globals.css    # Global styles
│   │   ├── components/        # React components
│   │   │   ├── ChatPanel.tsx  # Chat interface
│   │   │   ├── SlideViewer.tsx# Slide display
│   │   │   ├── SlideGrid.tsx  # Grid view
│   │   │   └── ...
│   │   ├── lib/               # Utilities
│   │   │   ├── api.ts         # API client
│   │   │   └── session.ts     # Session utilities
│   │   └── types/             # TypeScript types
│   │       └── index.ts       # Type definitions
│   ├── public/                # Static assets
│   ├── next.config.ts         # Next.js configuration
│   ├── tsconfig.json          # TypeScript config
│   ├── tailwind.config.ts     # Tailwind config
│   ├── package.json           # Node dependencies
│   └── .env.example           # Environment template
│
├── .gitignore                 # Git ignore rules
├── .env.example               # Root environment template
├── README.md                  # User documentation
├── CHANGELOG.md               # Version history
├── CONTRIBUTING.md            # Contribution guidelines
├── SECURITY.md                # Security policy
├── CODE_OF_CONDUCT.md         # Community guidelines
├── LICENSE                    # MIT License
├── docs/                      # Documentation folder
│   ├── README.md             # Documentation index
│   ├── setup-guide.md        # Setup instructions
│   ├── quick-reference.md    # Developer cheat sheet
│   └── technical/
│       └── README.md         # Technical documentation (this document)
└── render.yaml               # Render.com deployment config
```

---

## 6. API Documentation

### 6.1 Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/agent` | Stream agent interaction |
| POST | `/validate-api-key` | Validate LlamaCloud API key |
| POST | `/validate-anthropic-key` | Validate Anthropic API key |
| POST | `/parse-context-file` | Parse uploaded document |
| POST | `/export-pptx` | Export presentation to PPTX |
| POST | `/reset-session` | Reset session state |
| GET | `/session/{session_id}` | Get session state |
| GET | `/health` | Health check |
| GET | `/docs` | Swagger UI documentation |

### 6.2 POST /agent

**Purpose**: Stream agent interaction for creating/editing presentations.

**Request**:
```
Content-Type: multipart/form-data

Fields:
- message: string (required) - User message
- session_id: string (optional) - Resume existing session
- anthropic_api_key: string (required) - API key
- context_files: array (optional) - Parsed context file data
- style_template: object (optional) - Template styling
```

**Response**:
```
Content-Type: text/event-stream

Events:
- data: {"type": "activity", "content": "...", "status": "..."}
- data: {"type": "message", "content": "..."}
- data: {"type": "presentation_update", "presentation": {...}}
- data: {"type": "pending_edits", "edits": [...]}
- data: {"type": "session_id", "session_id": "..."}
- data: {"type": "done"}
```

**Example**:

```bash
curl -X POST http://localhost:8000/agent \
  -F "message=Create a 3-slide deck about AI" \
  -F "anthropic_api_key=sk-ant-xxx"
```

### 6.3 POST /validate-api-key

**Purpose**: Validate LlamaCloud API key.

**Request**:
```
Content-Type: multipart/form-data

Fields:
- api_key: string (required)
```

**Response**:
```json
{
  "valid": true,
  "message": "API key is valid"
}
```

### 6.4 POST /parse-context-file

**Purpose**: Parse uploaded document for context extraction.

**Request**:
```
Content-Type: multipart/form-data

Fields:
- file: binary (required) - Document file
- api_key: string (required) - LlamaCloud API key
```

**Response** (Server-Sent Events):
```
data: {"type": "progress", "stage": "uploading", "message": "Uploading file..."}
data: {"type": "progress", "stage": "parsing", "message": "Parsing document..."}
data: {"type": "result", "text": "...", "metadata": {...}}
```

### 6.5 POST /export-pptx

**Purpose**: Export presentation to PowerPoint format.

**Request**:
```json
{
  "presentation": {
    "title": "My Presentation",
    "slides": [
      {
        "index": 0,
        "html": "<div>...</div>",
        "layout": "title",
        "notes": "Speaker notes"
      }
    ],
    "theme": {
      "primaryColor": "#4A90E2",
      "fontFamily": "Arial"
    }
  }
}
```

**Response**:
```
Content-Type: application/vnd.openxmlformats-officedocument.presentationml.presentation
Content-Disposition: attachment; filename="presentation.pptx"

[Binary PPTX data]
```

### 6.6 POST /reset-session

**Purpose**: Reset session state (hard or soft reset).

**Request**:
```json
{
  "session_id": "uuid",
  "hard_reset": false
}
```

**Response**:
```json
{
  "success": true,
  "session_id": "uuid",
  "reset_type": "soft"
}
```

### 6.7 GET /session/{session_id}

**Purpose**: Retrieve session state.

**Response**:
```json
{
  "session_id": "uuid",
  "presentation": {
    "title": "...",
    "slides": [...]
  },
  "pending_edits": [],
  "context_files": [],
  "created_at": "2026-02-05T10:00:00",
  "updated_at": "2026-02-05T11:30:00"
}
```

---

## 7. Data Models

### 7.1 Slide

Represents a single slide in a presentation.

```python
@dataclass
class Slide:
    index: int              # 0-based position
    html: str               # Raw HTML content
    layout: SlideLayout     # Enum: title, title_content, two_column, blank
    notes: str = ""         # Speaker notes
```

**HTML Structure**:
```html
<div class="slide-content">
  <h1>Slide Title</h1>
  <p>Content goes here</p>
  <ul>
    <li>Bullet point</li>
  </ul>
</div>
```

### 7.2 Presentation

Complete presentation with metadata.

```python
@dataclass
class Presentation:
    title: str
    slides: list[Slide] = []
    theme: dict = {}        # Colors, fonts, etc.
```

**Theme Structure**:
```json
{
  "primaryColor": "#4A90E2",
  "secondaryColor": "#E94E77",
  "fontFamily": "Arial, sans-serif",
  "fontSize": "18px",
  "backgroundColor": "#FFFFFF"
}
```

### 7.3 PendingEdit

Staged edit awaiting approval.

```python
@dataclass
class PendingEdit:
    edit_id: str           # UUID
    slide_index: int       # Target slide
    operation: str         # ADD, UPDATE, DELETE, REORDER
    params: dict           # Operation parameters
    preview: str           # Human-readable description
```

**Operations**:
- `ADD`: Add new slide
- `UPDATE`: Modify existing slide
- `DELETE`: Remove slide
- `REORDER`: Change slide position

### 7.4 PresentationSession

Session state container.

```python
class PresentationSession:
    session_id: str
    presentation: Optional[Presentation]
    pending_edits: list[PendingEdit]
    applied_edits: list[dict]
    context_files: list[dict]
    style_template: Optional[dict]
    is_continuation: bool
    claude_session_id: Optional[str]
    created_at: datetime
    updated_at: datetime
```

---

## 8. Agent System

### 8.1 Claude Agent SDK Integration

The application uses Claude Agent SDK to provide structured tool-based interactions.

**Key Components**:

```python
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    tool,
    create_sdk_mcp_server
)

# Initialize client
client = ClaudeSDKClient(api_key=api_key)

# Define tools using decorator
@tool(
    name="create_presentation",
    description="Create a new presentation",
    params={"title": "string", "num_slides": "int"}
)
async def create_presentation(title: str, num_slides: int):
    # Implementation
    pass
```

### 8.2 Available Tools

#### 8.2.1 create_presentation

Creates a new presentation with title and initial slides.

```python
@tool(
    name="create_presentation",
    description="Create a new presentation with a title and specified number of slides",
    params={
        "title": {"type": "string", "description": "Presentation title"},
        "num_slides": {"type": "integer", "description": "Number of slides"}
    }
)
```

#### 8.2.2 add_slide

Adds a new slide to the presentation.

```python
@tool(
    name="add_slide",
    description="Add a new slide with content",
    params={
        "index": {"type": "integer", "description": "Position (0-based)"},
        "html": {"type": "string", "description": "HTML content"},
        "layout": {"type": "string", "description": "Layout type"},
        "notes": {"type": "string", "description": "Speaker notes"}
    }
)
```

#### 8.2.3 update_slide

Updates content of an existing slide.

```python
@tool(
    name="update_slide",
    description="Update an existing slide's content",
    params={
        "index": {"type": "integer", "description": "Slide index"},
        "html": {"type": "string", "description": "New HTML content"},
        "notes": {"type": "string", "description": "Updated notes"}
    }
)
```

#### 8.2.4 delete_slide

Removes a slide from the presentation.

```python
@tool(
    name="delete_slide",
    description="Delete a slide",
    params={
        "index": {"type": "integer", "description": "Slide index to delete"}
    }
)
```

#### 8.2.5 reorder_slides

Changes the order of slides.

```python
@tool(
    name="reorder_slides",
    description="Reorder slides in the presentation",
    params={
        "from_index": {"type": "integer"},
        "to_index": {"type": "integer"}
    }
)
```

#### 8.2.6 get_presentation_state

Returns current presentation state for agent reference.

```python
@tool(
    name="get_presentation_state",
    description="Get current presentation state",
    params={}
)
```

### 8.3 System Prompt

The agent operates with a comprehensive system prompt that defines its role and capabilities:

```
You are an expert presentation designer and content creator.
Your task is to create and edit presentations based on user requests.

Available Tools:
- create_presentation: Start a new deck
- add_slide: Add new content
- update_slide: Modify existing content
- delete_slide: Remove unwanted slides
- reorder_slides: Reorganize structure
- get_presentation_state: Check current state

Guidelines:
1. Always create well-structured, visually appealing HTML
2. Use semantic HTML tags (h1, h2, p, ul, etc.)
3. Keep content concise and focused
4. Use appropriate layouts for different content types
5. Add speaker notes for important context

When user uploads context files, use that information to inform your content.
When user provides a template, match the styling and structure.
```

### 8.4 Streaming Response

Agent responses are streamed to the client in real-time using Server-Sent Events (SSE):

```python
async def stream_agent_response(
    message: str,
    session: PresentationSession,
    api_key: str
) -> AsyncGenerator[str, None]:
    """Stream agent responses."""
    
    async for event in agent.stream_interaction(message, session):
        # Format as SSE
        yield f"data: {json.dumps(event)}\n\n"
```

**Event Types**:
- `activity`: Tool execution updates
- `message`: Assistant responses
- `presentation_update`: State changes
- `pending_edits`: Staged modifications
- `error`: Error messages
- `done`: Completion signal

---

## 9. Session Management

### 9.1 Session Lifecycle

1. **Creation**: New session created on first message
2. **Persistence**: State saved to SQLite + filesystem after each update
3. **Retrieval**: Session restored from storage on subsequent requests
4. **Cleanup**: Automatic deletion of sessions older than 24 hours

### 9.2 Storage Architecture

**SQLite Database** (`sessions.db`):
```sql
CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    metadata TEXT  -- JSON blob
);
```

**File System** (`sessions_data/`):
```
sessions_data/
├── {session_id}.json       # Full session state
└── {session_id}_backup.json # Backup copy
```

### 9.3 SessionManager API

```python
class SessionManager:
    def get_session(self, session_id: str) -> Optional[PresentationSession]:
        """Retrieve session by ID."""
    
    def save_session(self, session: PresentationSession) -> None:
        """Persist session to storage."""
    
    def delete_session(self, session_id: str) -> None:
        """Remove session from storage."""
    
    def cleanup_old_sessions(self, cutoff: datetime) -> int:
        """Delete sessions older than cutoff."""
    
    def list_sessions(self) -> list[str]:
        """List all session IDs."""
```

### 9.4 Session Cleanup

Automatic cleanup runs hourly in the background:

```python
async def cleanup_old_sessions():
    """Background task to clean up old sessions."""
    while True:
        cutoff = datetime.now() - timedelta(hours=24)
        cleaned = session_manager.cleanup_old_sessions(cutoff)
        if cleaned > 0:
            logger.info(f"Cleaned up {cleaned} old sessions")
        await asyncio.sleep(3600)  # Run every hour
```

**Configuration**:
- `SESSION_TIMEOUT_HOURS`: Session expiration time (default: 24)
- `SESSION_CLEANUP_INTERVAL`: Cleanup frequency in seconds (default: 3600)

---

## 10. File Processing

### 10.1 Context File Upload

Users can upload documents to provide context for presentation generation.

**Supported Formats**:
- PDF (`.pdf`)
- Word Documents (`.docx`)
- Text Files (`.txt`)
- Markdown (`.md`)
- PowerPoint (`.pptx`)

**Processing Flow**:

1. **Upload**: File received via multipart/form-data
2. **Validation**: Check file type and size
3. **LlamaParse**: Send to LlamaCloud for parsing
4. **Extraction**: Extract text, tables, images
5. **Storage**: Cache parsed content in session
6. **Context**: Make available to agent

### 10.2 LlamaParse Integration

```python
from llama_cloud_services import LlamaParse

async def parse_context_file(
    file: UploadFile,
    api_key: str
) -> dict:
    """Parse uploaded file using LlamaParse."""
    
    parser = LlamaParse(api_key=api_key)
    
    # Upload file
    result = await parser.parse_file(
        file=file.file,
        filename=file.filename
    )
    
    return {
        "text": result.text,
        "metadata": result.metadata,
        "filename": file.filename
    }
```

**Progress Tracking**:
```python
async def stream_parse_progress():
    yield {"type": "progress", "stage": "uploading"}
    yield {"type": "progress", "stage": "parsing"}
    yield {"type": "result", "text": "..."}
```

### 10.3 Template Upload

Custom styling templates can be uploaded to maintain brand consistency.

**Template Structure**:
```json
{
  "filename": "corporate_template.pptx",
  "text": "Extracted style guide text",
  "screenshots": [
    {
      "slide_number": 1,
      "image_data": "base64...",
      "description": "Title slide layout"
    }
  ],
  "colors": {
    "primary": "#003366",
    "secondary": "#FF6600"
  },
  "fonts": {
    "heading": "Arial Bold",
    "body": "Arial"
  }
}
```

---

## 11. PPTX Export

### 11.1 Export Architecture

The PPTX export system uses Node.js with pptxgenjs to convert HTML slides to PowerPoint format.

**Communication Flow**:
```
Python (FastAPI)
    ↓ JSON via subprocess
Node.js (convert.js)
    ↓ pptxgenjs API
PowerPoint File (.pptx)
```

### 11.2 Conversion Process

1. **Serialize**: Convert Presentation object to JSON
2. **Subprocess**: Spawn Node.js process with JSON input
3. **Parse**: Extract content from HTML
4. **Generate**: Create PPTX using pptxgenjs
5. **Return**: Stream binary PPTX back to client

### 11.3 HTML to PPTX Mapping

```javascript
// convert.js
const pptx = new PptxGenJS();

presentation.slides.forEach((slide, index) => {
  const pptxSlide = pptx.addSlide();
  
  // Parse HTML and extract elements
  const parsed = parseHTML(slide.html);
  
  // Add elements to slide
  parsed.forEach(element => {
    if (element.type === 'text') {
      pptxSlide.addText(element.content, {
        x: element.x,
        y: element.y,
        w: element.w,
        h: element.h,
        fontSize: element.fontSize,
        color: element.color
      });
    }
    // Handle images, shapes, etc.
  });
  
  // Add speaker notes
  if (slide.notes) {
    pptxSlide.addNotes(slide.notes);
  }
});

// Save file
pptx.writeFile({ fileName: 'presentation.pptx' });
```

### 11.4 Styling and Themes

```javascript
// Apply presentation theme
pptx.defineLayout({
  name: 'CUSTOM',
  width: 10,
  height: 5.625
});

pptx.theme = {
  headFontFace: presentation.theme.fontFamily || 'Arial',
  bodyFontFace: presentation.theme.fontFamily || 'Arial'
};

// Define master slides
pptx.defineSlideMaster({
  title: 'TITLE_SLIDE',
  background: { color: presentation.theme.backgroundColor || 'FFFFFF' }
});
```

---

## 12. Security

### 12.1 API Key Management

**Storage**:
- API keys are NEVER stored in backend
- Keys passed with each request from frontend
- Frontend stores keys in browser sessionStorage (not localStorage)

**Validation**:
```python
async def validate_anthropic_key(api_key: str) -> bool:
    """Verify API key with Anthropic."""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=10,
            messages=[{"role": "user", "content": "test"}]
        )
        return True
    except anthropic.AuthenticationError:
        return False
```

### 12.2 File Upload Security

**Validation**:
```python
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt', '.md', '.pptx'}

def validate_upload(file: UploadFile) -> None:
    # Check file extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Invalid file type")
    
    # Check file size
    file.file.seek(0, 2)  # Seek to end
    size = file.file.tell()
    file.file.seek(0)  # Reset
    
    if size > MAX_UPLOAD_SIZE:
        raise HTTPException(400, "File too large")
```

**Sanitization**:
- Filenames sanitized to prevent path traversal
- Files stored in isolated temporary directory
- Automatic cleanup of temporary files

### 12.3 CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get(
        "CORS_ORIGINS",
        "http://localhost:3000"
    ).split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production Recommendations**:
- Restrict origins to specific domains
- Use HTTPS only
- Implement rate limiting
- Add authentication layer

### 12.4 Input Sanitization

**HTML Content**:
- User-generated HTML is NOT executed server-side
- Frontend displays HTML in sandboxed iframes
- CSP headers prevent XSS attacks

**SQL Injection**:
- Parameterized queries used exclusively
- No raw SQL string concatenation

### 12.5 Environment Variables

**Never commit**:
- `.env` files
- API keys
- Secrets

**Use**:
- `.env.example` templates
- Environment-specific configurations
- Secret management services (AWS Secrets Manager, Azure Key Vault)

---

## 13. Performance & Scalability

### 13.1 Backend Performance

**Async/Await**:
- All I/O operations are asynchronous
- Non-blocking API calls
- Concurrent request handling

**Streaming**:
- Server-Sent Events for real-time updates
- Chunked transfer encoding
- Reduced Time to First Byte (TTFB)

**Caching**:
- Parsed context files cached in session
- Template data cached
- Session state in memory + disk

### 13.2 Database Optimization

**SQLite Performance**:
```python
# Connection pooling
conn = sqlite3.connect(
    DB_PATH,
    check_same_thread=False,
    isolation_level=None  # Autocommit mode
)

# Indexes
CREATE INDEX idx_updated_at ON sessions(updated_at);
CREATE INDEX idx_created_at ON sessions(created_at);

# Pragmas
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
```

### 13.3 Scalability Considerations

**Horizontal Scaling**:
- Stateless backend design (session data external)
- Load balancer compatible
- Shared file system (NFS, S3) for session data

**Vertical Scaling**:
- Uvicorn workers: `--workers 4`
- CPU-bound tasks offloaded to subprocess (PPTX)
- Memory management via session cleanup

**Rate Limiting**:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/agent")
@limiter.limit("60/minute")
async def agent_endpoint(...):
    pass
```

### 13.4 Monitoring

**Metrics to Track**:
- Request latency (p50, p95, p99)
- Error rates
- Active sessions
- API call volume (Anthropic, LlamaCloud)
- Memory usage
- Disk usage (session data)

**Logging**:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

**APM Integration**:
- Sentry for error tracking
- Datadog/New Relic for performance monitoring
- Prometheus for metrics

---

## 14. Testing

### 14.1 Backend Testing

**Unit Tests**:
```python
# tests/test_models.py
import pytest
from models import Slide, Presentation

def test_slide_serialization():
    slide = Slide(index=0, html="<h1>Test</h1>")
    data = slide.to_dict()
    restored = Slide.from_dict(data)
    assert restored.index == slide.index
    assert restored.html == slide.html

def test_presentation_creation():
    pres = Presentation(title="Test")
    pres.slides.append(Slide(index=0, html="<h1>Test</h1>"))
    assert len(pres.slides) == 1
```

**Integration Tests**:
```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200

def test_agent_endpoint_requires_auth():
    response = client.post("/agent", data={"message": "test"})
    assert response.status_code == 422  # Missing API key
```

**Run Tests**:
```bash
# Install pytest
pip install pytest pytest-asyncio pytest-cov

# Run all tests
pytest

# With coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_models.py -v
```

### 14.2 Frontend Testing

**Component Tests**:
```typescript
// __tests__/ChatPanel.test.tsx
import { render, screen } from '@testing-library/react';
import ChatPanel from '@/components/ChatPanel';

test('renders chat input', () => {
  render(<ChatPanel onSend={() => {}} />);
  const input = screen.getByPlaceholderText(/type a message/i);
  expect(input).toBeInTheDocument();
});
```

**API Mocking**:
```typescript
// __tests__/api.test.ts
import { validateApiKey } from '@/lib/api';

global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({ valid: true })
  })
);

test('validates API key', async () => {
  const result = await validateApiKey('test-key');
  expect(result.valid).toBe(true);
});
```

**Run Tests**:
```bash
# Install testing libraries
npm install --save-dev @testing-library/react @testing-library/jest-dom jest

# Run tests
npm test

# Watch mode
npm test -- --watch
```

### 14.3 End-to-End Testing

**Playwright Setup**:
```typescript
// e2e/presentation.spec.ts
import { test, expect } from '@playwright/test';

test('create presentation flow', async ({ page }) => {
  await page.goto('http://localhost:3000');
  
  // Enter API key
  await page.fill('[name="apiKey"]', process.env.TEST_API_KEY);
  await page.click('button:has-text("Continue")');
  
  // Send message
  await page.fill('[name="message"]', 'Create a 2-slide deck');
  await page.click('button:has-text("Send")');
  
  // Wait for response
  await page.waitForSelector('.slide-viewer');
  
  // Verify slides
  const slides = await page.$$('.slide');
  expect(slides.length).toBeGreaterThan(0);
});
```

---

## 15. Deployment

### 15.1 Docker Deployment

**Backend Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install Node.js for PPTX converter
RUN apt-get update && apt-get install -y nodejs npm

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Install Node dependencies for PPTX converter
WORKDIR /app/pptx_converter
RUN npm install
WORKDIR /app

# Expose port
EXPOSE 8000

# Run server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile**:
```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:18-alpine

WORKDIR /app

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/public ./public

EXPOSE 3000

CMD ["npm", "start"]
```

**Docker Compose**:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - LLAMA_CLOUD_API_KEY=${LLAMA_CLOUD_API_KEY}
    volumes:
      - session-data:/app/sessions_data
    restart: unless-stopped

  frontend:
    build: ./web
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  session-data:
```

### 15.2 Cloud Deployment

**Render.com** (see `render.yaml`):
```yaml
services:
  - type: web
    name: presentation-app-backend
    env: python
    buildCommand: "pip install -r requirements.txt && cd pptx_converter && npm install"
    startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: ANTHROPIC_API_KEY
        sync: false
      - key: LLAMA_CLOUD_API_KEY
        sync: false

  - type: web
    name: presentation-app-frontend
    env: node
    buildCommand: "npm install && npm run build"
    startCommand: "npm start"
    envVars:
      - key: NEXT_PUBLIC_API_URL
        value: https://presentation-app-backend.onrender.com
```

**AWS Deployment**:
- **Backend**: ECS Fargate or Lambda (with API Gateway)
- **Frontend**: Amplify or CloudFront + S3
- **Database**: RDS (PostgreSQL) or DynamoDB
- **File Storage**: S3
- **Secrets**: AWS Secrets Manager

**Azure Deployment**:
- **Backend**: App Service or Container Instances
- **Frontend**: Static Web Apps
- **Database**: Azure SQL or Cosmos DB
- **File Storage**: Blob Storage
- **Secrets**: Azure Key Vault

### 15.3 Environment Configuration

**Production Checklist**:
- [ ] Set `ENVIRONMENT=production`
- [ ] Disable `DEBUG` mode
- [ ] Configure proper `CORS_ORIGINS`
- [ ] Set up SSL/TLS certificates
- [ ] Enable rate limiting
- [ ] Configure monitoring and logging
- [ ] Set up automated backups
- [ ] Implement health checks
- [ ] Configure auto-scaling
- [ ] Set up CDN (frontend)

---

## 16. Troubleshooting

### 16.1 Common Issues

#### Backend won't start

**Symptom**: `ModuleNotFoundError: No module named 'claude_agent_sdk'`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

#### PPTX export fails

**Symptom**: `Node.js subprocess error`

**Solution**:
```bash
# Install Node.js dependencies
cd backend/pptx_converter
npm install

# Verify Node.js installation
node --version  # Should be 18.x or higher
```

#### CORS errors

**Symptom**: `Access-Control-Allow-Origin` errors in browser console

**Solution**:
```python
# backend/main.py
# Update CORS_ORIGINS environment variable
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,https://yourdomain.com
```

#### Session not persisting

**Symptom**: Session resets between requests

**Solution**:
```bash
# Check sessions directory exists and is writable
mkdir -p backend/sessions_data
chmod 755 backend/sessions_data

# Check SQLite database
sqlite3 backend/sessions.db ".tables"
```

### 16.2 Logging and Debugging

**Enable Debug Logging**:
```bash
# backend/.env
DEBUG=true
LOG_LEVEL=DEBUG

# Run backend with verbose output
uvicorn main:app --reload --log-level debug
```

**Check Logs**:
```bash
# Backend logs
tail -f backend/app.log

# Frontend logs (browser console)
# Open Developer Tools (F12) → Console tab
```

### 16.3 Performance Issues

**Symptom**: Slow response times

**Diagnostics**:
```python
# Add timing logs
import time

@app.post("/agent")
async def agent_endpoint(...):
    start = time.time()
    # ... process request
    logger.info(f"Request took {time.time() - start:.2f}s")
```

**Solutions**:
- Increase Uvicorn workers: `--workers 4`
- Enable caching for parsed files
- Optimize database queries
- Use connection pooling
- Monitor API rate limits

---

## 17. Contributing

### 17.1 Development Workflow

1. **Fork Repository**: Create personal fork
2. **Create Branch**: `git checkout -b feature/my-feature`
3. **Make Changes**: Implement feature or fix
4. **Test**: Run all tests
5. **Commit**: Use conventional commits
6. **Push**: Push to your fork
7. **Pull Request**: Submit PR with description

### 17.2 Code Style

**Python (PEP 8)**:
```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

**TypeScript (ESLint)**:
```bash
# Lint code
npm run lint

# Type checking
npm run typecheck

# Format code (if using Prettier)
npx prettier --write "src/**/*.{ts,tsx}"
```

### 17.3 Commit Guidelines

**Conventional Commits**:
```
feat: add template import functionality
fix: resolve session cleanup race condition
docs: update API documentation
style: format code with black
refactor: simplify agent tool definitions
test: add unit tests for models
chore: update dependencies
```

### 17.4 Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests added/updated
```

---

## 18. Appendix

### 18.1 Environment Variables Reference

#### Backend Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `ANTHROPIC_API_KEY` | string | **Required** | Anthropic API key |
| `LLAMA_CLOUD_API_KEY` | string | Optional | LlamaCloud API key |
| `CLAUDE_MODEL` | string | `claude-sonnet-4-20250514` | Claude model to use |
| `HOST` | string | `0.0.0.0` | Server host |
| `PORT` | int | `8000` | Server port |
| `ENVIRONMENT` | string | `development` | Environment mode |
| `DEBUG` | bool | `false` | Debug mode |
| `CORS_ORIGINS` | string | `http://localhost:3000` | Allowed origins (comma-separated) |
| `SESSION_TIMEOUT_HOURS` | int | `24` | Session expiration time |
| `MAX_UPLOAD_SIZE` | int | `10485760` | Max file size (bytes) |
| `LOG_LEVEL` | string | `INFO` | Logging level |

#### Frontend Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | string | `http://localhost:8000` | Backend API URL |
| `NEXT_PUBLIC_ENABLE_CONTEXT_FILES` | bool | `true` | Enable file uploads |
| `NEXT_PUBLIC_ENABLE_TEMPLATES` | bool | `true` | Enable templates |
| `NEXT_PUBLIC_ENABLE_EXPORT` | bool | `true` | Enable PPTX export |
| `NEXT_PUBLIC_APP_TITLE` | string | `Presentation App` | App title |
| `NEXT_PUBLIC_DEV_MODE` | bool | `false` | Development mode |

### 18.2 API Error Codes

| Code | Status | Description |
|------|--------|-------------|
| `E001` | 400 | Invalid request format |
| `E002` | 401 | Invalid API key |
| `E003` | 403 | Insufficient permissions |
| `E004` | 404 | Session not found |
| `E005` | 413 | File too large |
| `E006` | 415 | Unsupported file type |
| `E007` | 429 | Rate limit exceeded |
| `E008` | 500 | Internal server error |
| `E009` | 503 | Service unavailable |

### 18.3 Glossary

- **Agent**: AI system using Claude to manipulate presentations
- **Context Files**: User-uploaded documents providing information
- **LlamaParse**: Document parsing service from LlamaIndex
- **Pending Edits**: Staged modifications awaiting user approval
- **Session**: Stateful conversation with presentation state
- **SSE**: Server-Sent Events for real-time streaming
- **Tool**: Structured function callable by Claude Agent

### 18.4 Resources

**Documentation**:
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)
- [Claude API Docs](https://docs.anthropic.com/)
- [LlamaIndex Docs](https://docs.llamaindex.ai/)
- [pptxgenjs Docs](https://gitbrent.github.io/PptxGenJS/)

**Community**:
- GitHub Issues: Report bugs and feature requests
- Discussions: Ask questions and share ideas
- Contributing Guide: See CONTRIBUTING.md

**Support**:
- Technical Issues: [Create GitHub Issue]
- Security Issues: See SECURITY.md
- General Questions: [GitHub Discussions]

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-05 | Initial documentation |

---

**Document Maintainers**: Development Team  
**Review Cycle**: Quarterly  
**Last Reviewed**: February 5, 2026
