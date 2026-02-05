# Contributing to Presentation App

Thank you for your interest in contributing to the Presentation App! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Community](#community)

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Node.js 18.x or higher
- Git
- Basic knowledge of FastAPI and Next.js

### First-Time Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/presentation_app.git
   cd presentation_app
   ```

2. **Set up development environment**
   
   Follow the detailed setup instructions in [Setup Guide](docs/setup-guide.md).

3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-asyncio black flake8 mypy

# Install PPTX converter dependencies
cd pptx_converter && npm install && cd ..

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run backend
uvicorn main:app --reload
```

### Frontend Development

```bash
cd web

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local

# Run development server
npm run dev
```

## How to Contribute

### Reporting Bugs

Before creating a bug report:
- Check the [existing issues](https://github.com/abhilashjaiswal0110/presentation_app/issues) to avoid duplicates
- Collect information about the bug (error messages, logs, screenshots)
- Determine the steps to reproduce the issue

**Bug Report Template**:
```markdown
**Description**
A clear and concise description of the bug.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment**
- OS: [e.g., Windows 11, macOS 13, Ubuntu 22.04]
- Python version: [e.g., 3.11]
- Node.js version: [e.g., 18.17]
- Browser: [e.g., Chrome 120]

**Additional Context**
Any other relevant information.
```

### Suggesting Enhancements

**Feature Request Template**:
```markdown
**Problem Statement**
Describe the problem this feature would solve.

**Proposed Solution**
Describe your proposed solution.

**Alternatives Considered**
Other solutions you've considered.

**Additional Context**
Mockups, examples, or additional information.
```

### Code Contributions

We welcome contributions in the following areas:

- **Bug fixes**: Fix existing issues
- **New features**: Add new functionality
- **Performance improvements**: Optimize existing code
- **Documentation**: Improve or add documentation
- **Tests**: Add or improve test coverage
- **Refactoring**: Improve code quality

## Pull Request Process

### Before Submitting

1. **Update your branch**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests**
   ```bash
   # Backend
   cd backend
   pytest
   
   # Frontend
   cd web
   npm test
   ```

3. **Check code style**
   ```bash
   # Backend
   black . --check
   flake8 .
   mypy .
   
   # Frontend
   npm run lint
   npm run typecheck
   ```

4. **Update documentation** if you've changed APIs or added features

### Submitting a Pull Request

1. **Push your branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a pull request** on GitHub with the following information:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Related Issues
Fixes #(issue number)

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
Describe the tests you ran and how to reproduce them:
- [ ] Test A
- [ ] Test B
- [ ] Manual testing steps:
  1. Step 1
  2. Step 2

## Screenshots (if applicable)
Add screenshots to demonstrate changes

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published
```

### Review Process

1. **Automated checks**: CI/CD pipeline runs tests and linters
2. **Code review**: Maintainers review your code
3. **Feedback**: Address review comments
4. **Approval**: Once approved, maintainers will merge your PR

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with the following specifications:

- **Line length**: 88 characters (Black default)
- **Indentation**: 4 spaces
- **Imports**: Organized using isort
- **Type hints**: Required for all function signatures
- **Docstrings**: Google style docstrings

**Example**:
```python
from typing import Optional

def process_slide(
    index: int,
    content: str,
    layout: Optional[str] = None
) -> dict:
    """Process slide content and return formatted data.
    
    Args:
        index: The slide index (0-based).
        content: The HTML content of the slide.
        layout: Optional layout type (default: "blank").
    
    Returns:
        A dictionary containing processed slide data.
    
    Raises:
        ValueError: If index is negative or content is empty.
    """
    if index < 0:
        raise ValueError("Index must be non-negative")
    
    return {
        "index": index,
        "content": content,
        "layout": layout or "blank"
    }
```

### TypeScript Style Guide

- **Indentation**: 2 spaces
- **Semicolons**: Optional (but be consistent)
- **Quotes**: Single quotes for strings
- **Type annotations**: Required for function parameters and return types
- **React**: Functional components with hooks

**Example**:
```typescript
interface SlideProps {
  index: number;
  content: string;
  onEdit?: (index: number) => void;
}

export function SlideComponent({ 
  index, 
  content, 
  onEdit 
}: SlideProps): JSX.Element {
  const handleEdit = () => {
    if (onEdit) {
      onEdit(index);
    }
  };
  
  return (
    <div className="slide">
      <div dangerouslySetInnerHTML={{ __html: content }} />
      <button onClick={handleEdit}>Edit</button>
    </div>
  );
}
```

### Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

**Examples**:
```
feat(agent): add support for custom slide layouts

Add ability to define and use custom slide layouts through
the agent tool interface. Includes validation and error handling.

Closes #123
```

```
fix(export): resolve PPTX generation error on Windows

The subprocess call was failing on Windows due to path issues.
Updated to use pathlib for cross-platform compatibility.

Fixes #456
```

## Testing Guidelines

### Backend Testing

1. **Unit Tests**: Test individual functions and classes
   ```python
   def test_slide_creation():
       slide = Slide(index=0, html="<h1>Test</h1>")
       assert slide.index == 0
       assert slide.html == "<h1>Test</h1>"
   ```

2. **Integration Tests**: Test API endpoints
   ```python
   def test_agent_endpoint(client, mock_api_key):
       response = client.post(
           "/agent",
           data={
               "message": "Create a slide",
               "anthropic_api_key": mock_api_key
           }
       )
       assert response.status_code == 200
   ```

3. **Async Tests**: Use pytest-asyncio
   ```python
   @pytest.mark.asyncio
   async def test_async_function():
       result = await async_operation()
       assert result is not None
   ```

### Frontend Testing

1. **Component Tests**: Test React components
   ```typescript
   test('renders slide content', () => {
     render(<SlideComponent index={0} content="<h1>Test</h1>" />);
     expect(screen.getByText('Test')).toBeInTheDocument();
   });
   ```

2. **Integration Tests**: Test component interactions
   ```typescript
   test('handles slide edit', async () => {
     const onEdit = jest.fn();
     render(<SlideComponent index={0} content="Test" onEdit={onEdit} />);
     
     fireEvent.click(screen.getByText('Edit'));
     expect(onEdit).toHaveBeenCalledWith(0);
   });
   ```

### Test Coverage

- Aim for **>80%** code coverage
- All new features must include tests
- Bug fixes should include regression tests

## Documentation

### Code Documentation

- **Python**: Use Google-style docstrings
- **TypeScript**: Use JSDoc comments
- **Complex logic**: Add inline comments explaining "why", not "what"

### User Documentation

- Update README.md for user-facing changes
- Update docs/technical/README.md for technical changes
- Include examples and use cases

### API Documentation

- FastAPI automatically generates OpenAPI docs
- Add detailed descriptions to endpoint docstrings
- Include example requests and responses

## Community

### Getting Help

- **Questions**: Open a [GitHub Discussion](https://github.com/abhilashjaiswal0110/presentation_app/discussions)
- **Bugs**: Create an [Issue](https://github.com/abhilashjaiswal0110/presentation_app/issues)
- **Security**: See [SECURITY.md](SECURITY.md)

### Communication Channels

- **GitHub Discussions**: General questions and ideas
- **GitHub Issues**: Bug reports and feature requests
- **Pull Requests**: Code contributions

### Recognition

Contributors will be acknowledged in:
- GitHub contributors page
- Release notes
- CONTRIBUTORS.md file (if applicable)

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see [LICENSE](LICENSE)).

---

Thank you for contributing to the Presentation App! 🎉
