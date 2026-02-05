# Presentation App

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node.js-18+-green.svg)](https://nodejs.org/)

AI-powered presentation generation application that creates professional slide decks through natural language conversation. Built with Claude AI, FastAPI, and Next.js.

## ✨ Features

- 🤖 **AI-Powered Creation**: Describe your presentation needs in natural language
- 💬 **Conversational Interface**: Refine and edit through multi-turn dialogue
- 📄 **Context-Aware**: Upload reference documents to inform content
- 🎨 **Flexible HTML Slides**: Full control over slide content and styling
- 📊 **PPTX Export**: Download presentations in PowerPoint format
- 🔄 **Session Persistence**: Resume work across browser sessions
- ⚡ **Real-time Streaming**: Live updates as Claude generates content

## 📚 Documentation

- **[Documentation Index](docs/README.md)** - Complete documentation navigation
- **[Setup Guide](docs/setup-guide.md)** - Detailed installation and configuration
- **[Technical Documentation](docs/technical/README.md)** - Architecture, API reference, and technical details
- **[Quick Reference](docs/quick-reference.md)** - Developer cheat sheet
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project
- **[Security Policy](SECURITY.md)** - Security guidelines and vulnerability reporting

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Node.js 18.x or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))
- LlamaCloud API key (optional, for document parsing - [Get one here](https://cloud.llamaindex.ai/))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd presentation_app
   ```

2. **Set up the backend**
   ```bash
   cd backend
   
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Install Node.js dependencies for PPTX export
   cd pptx_converter
   npm install
   cd ..
   
   # Configure environment variables
   cp .env.example .env
   # Edit .env and add your API keys
   ```

3. **Set up the frontend**
   ```bash
   cd ../web
   
   # Install dependencies
   npm install
   
   # Configure environment variables
   cp .env.example .env.local
   # Edit .env.local if needed (API URL defaults to http://localhost:8000)
   ```

4. **Start the application**
   
   In one terminal (backend):
   ```bash
   cd backend
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   In another terminal (frontend):
   ```bash
   cd web
   npm run dev
   ```

5. **Open your browser**
   
   Navigate to [http://localhost:3000](http://localhost:3000)

## 🏗️ Architecture

```
┌─────────────────┐
│   Next.js UI    │  React + TypeScript + Tailwind
└────────┬────────┘
         │ HTTP/SSE
┌────────▼────────┐
│  FastAPI Server │  Python + Claude Agent SDK
└────────┬────────┘
         ├─────────► Anthropic Claude API
         ├─────────► LlamaCloud (Document Parsing)
         └─────────► Node.js (PPTX Export)
```

**Technology Stack:**
- **Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.10+, Claude Agent SDK
- **AI**: Anthropic Claude (Sonnet 4)
- **Document Processing**: LlamaCloud Services
- **Export**: Node.js + pptxgenjs

## 📖 Usage

1. **Enter API Keys**: On first launch, enter your Anthropic API key
2. **Start Chatting**: Describe your presentation needs in natural language
   - "Create a 5-slide deck about machine learning"
   - "Add a slide about neural networks with bullet points"
   - "Make the title slide more engaging"
3. **Upload Context** (Optional): Add reference documents to inform content
4. **Apply Templates** (Optional): Upload a PowerPoint template for consistent styling
5. **Export**: Download your presentation as a PPTX file

## 🔧 Configuration

### Required Environment Variables

**Backend** (`backend/.env`):
```env
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LLAMA_CLOUD_API_KEY=llx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Frontend** (`web/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

See [`.env.example`](.env.example) files for complete configuration options.

## 📡 API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agent` | POST | Stream agent interaction for presentation creation |
| `/validate-api-key` | POST | Validate LlamaCloud API key |
| `/validate-anthropic-key` | POST | Validate Anthropic API key |
| `/parse-context-file` | POST | Parse uploaded document |
| `/export-pptx` | POST | Export presentation to PPTX |
| `/reset-session` | POST | Reset session state |
| `/session/{session_id}` | GET | Get session state |
| `/health` | GET | Health check |
| `/docs` | GET | Interactive API documentation |

For detailed API documentation, visit `/docs` when the backend is running or see [Technical Documentation](docs/technical/README.md).

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Setting up the development environment
- Code style and standards
- Submitting pull requests
- Reporting bugs and requesting features

## 🔒 Security

Security is a top priority. Please review our [Security Policy](SECURITY.md) for:

- Reporting vulnerabilities
- Security best practices
- Supported versions

**Never commit sensitive data like API keys to version control.**

## 📋 Project Structure

```
presentation_app/
├── backend/                    # Python FastAPI backend
│   ├── agent.py               # Claude Agent SDK integration
│   ├── main.py                # FastAPI application
│   ├── models.py              # Data models
│   ├── session.py             # Session management
│   ├── parser.py              # Document parsing
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Environment template
│   └── pptx_converter/        # Node.js PPTX export
├── web/                        # Next.js frontend
│   ├── src/
│   │   ├── app/               # Next.js pages
│   │   ├── components/        # React components
│   │   ├── lib/               # API client
│   │   └── types/             # TypeScript types
│   ├── package.json           # Node dependencies
│   └── .env.example           # Environment template
├── .env.example               # Root environment template
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
├── CONTRIBUTING.md            # Contribution guidelines
├── SECURITY.md                # Security policy
├── CODE_OF_CONDUCT.md         # Community guidelines
├── LICENSE                    # MIT License
├── CHANGELOG.md               # Version history
└── docs/                      # Documentation
    ├── README.md              # Documentation index
    ├── setup-guide.md         # Setup instructions
    ├── quick-reference.md     # Developer cheat sheet
    └── technical/             # Technical documentation
        └── README.md          # Complete technical guide
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Anthropic](https://www.anthropic.com/) for Claude AI
- [LlamaIndex](https://www.llamaindex.ai/) for document parsing
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [Next.js](https://nextjs.org/) for the frontend framework
- [pptxgenjs](https://gitbrent.github.io/PptxGenJS/) for PowerPoint generation

## 📞 Support

- **Documentation**: [Documentation Index](docs/README.md)
- **Issues**: [GitHub Issues](https://github.com/abhilashjaiswal0110/presentation_app/issues)
- **Discussions**: [GitHub Discussions](https://github.com/abhilashjaiswal0110/presentation_app/discussions)

---

Made with ❤️ by the Presentation App Team
