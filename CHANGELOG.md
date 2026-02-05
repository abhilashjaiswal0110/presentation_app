# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- **Documentation Structure**: Reorganized documentation following best practices
  - Created `/docs` folder for detailed documentation
  - Moved technical documentation to `docs/technical/README.md`
  - Moved setup guide to `docs/setup-guide.md`
  - Moved quick reference to `docs/quick-reference.md`
  - Created `docs/README.md` as documentation index
  - Removed redundant `SETUP_SUMMARY.md` (consolidated into docs index)
  - Updated all cross-references to new locations
- **Repository Structure**: Follows standard open-source best practices
  - Root contains standard files: README, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, LICENSE
  - Detailed documentation organized under `/docs`
  - Clear navigation with documentation index

### Added
- Documentation index (`docs/README.md`) with role-based navigation
- Better organization for finding information quickly

## [0.1.0] - 2026-02-05

### Added
- AI-powered presentation generation using Claude
- Natural language chat interface
- Real-time streaming responses
- HTML-based slide rendering
- PPTX export functionality
- Context file upload and parsing (LlamaParse)
- Template support for branded presentations
- Session persistence with SQLite
- FastAPI backend with Claude Agent SDK
- Next.js 15 frontend with React 19
- Multi-turn conversation support
- Slide editing and refinement capabilities
- Speaker notes support
- Automatic session cleanup

### Architecture
- FastAPI backend with Python 3.10+
- Next.js 15 frontend with TypeScript
- Claude Agent SDK for AI integration
- LlamaCloud for document parsing
- Node.js subprocess for PPTX generation
- SQLite for session storage
- Server-Sent Events for real-time streaming

### Documentation
- Comprehensive technical documentation
- API reference
- Setup and installation guides
- Contributing guidelines
- Security policy
- Code of conduct

[Unreleased]: https://github.com/yourorg/presentation_app/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourorg/presentation_app/releases/tag/v0.1.0
