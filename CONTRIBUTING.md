# Contributing to CodeGraph

We love your input! We want to make contributing to CodeGraph as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issues](https://github.com/codegraph-dev/CodeGraph/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/codegraph-dev/CodeGraph/issues/new); it's that easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Development Setup

### Prerequisites

- Node.js 16+
- Python 3.8+
- VS Code 1.60+
- Git

### Local Development

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/CodeGraph.git
cd CodeGraph

# Run setup script
./setup.sh

# Install extension dependencies
cd extension
npm install

# Install engine dependencies  
cd ../engine
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
npm test                    # Extension tests
python -m pytest          # Engine tests
```

### Extension Development

```bash
cd extension

# Compile TypeScript
npm run compile

# Watch for changes
npm run watch

# Package extension
npm run package

# Install locally for testing
code --install-extension codegraph-*.vsix
```

### Engine Development

```bash
cd engine

# Run tests with coverage
python -m pytest --cov=codegraph

# Type checking
mypy codegraph.py

# Lint code
flake8 codegraph.py
black codegraph.py

# Run specific language parser tests
python -m pytest tests/test_go_parser.py
```

## Code Style

### TypeScript (Extension)

- Use TypeScript strict mode
- Follow VS Code extension guidelines
- Use ESLint with provided configuration
- Format with Prettier

### Python (Engine)

- Follow PEP 8
- Use type hints
- Format with Black
- Lint with flake8
- Type check with mypy

## Adding Language Support

To add support for a new programming language:

1. **Create Parser**
   ```python
   # engine/parsers/your_language.py
   from .base import Parser
   
   class YourLanguageParser(Parser):
       def parse(self, code: str) -> Dict[str, Any]:
           # Implementation
           pass
   ```

2. **Add Tests**
   ```python
   # engine/tests/test_your_language.py
   import pytest
   from parsers.your_language import YourLanguageParser
   
   def test_parse_basic():
       # Test implementation
       pass
   ```

3. **Update Configuration**
   ```javascript
   // codegraph.config.js
   languages: {
     your_language: {
       parser: "your_language",
       includes: ["**/*.ext"],
       excludes: ["**/build/**"]
     }
   }
   ```

4. **Add Documentation**
   - Update README.md
   - Add language-specific examples
   - Document parser capabilities

## Testing

### Unit Tests

```bash
# Run all tests
npm test && python -m pytest

# Run specific test files
npm test -- --testNamePattern="dependency"
python -m pytest tests/test_dependency_graph.py

# Run with coverage
npm test -- --coverage
python -m pytest --cov=codegraph --cov-report=html
```

### Integration Tests

```bash
# Test against real projects
python -m pytest tests/integration/

# Test VS Code extension
npm run test:integration
```

### Manual Testing

1. Install development version
2. Test with various project types
3. Verify VS Code integration works
4. Check CLI functionality
5. Validate output formats

## Documentation

### Code Documentation

- Document all public APIs
- Use JSDoc for TypeScript
- Use docstrings for Python
- Include examples in documentation

### User Documentation

- Update README.md for new features
- Add examples to `/examples` directory
- Update installation instructions
- Create tutorial content

## Release Process

1. Update version numbers
2. Update CHANGELOG.md
3. Run full test suite
4. Create release branch
5. Submit PR for review
6. Tag release after merge
7. Publish to marketplaces

## Getting Help

- Join our [Discord](https://discord.gg/codegraph)
- Check existing [Issues](https://github.com/codegraph-dev/CodeGraph/issues)
- Read the [Documentation](https://codegraph-dev.github.io/CodeGraph/)

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation
- Annual contributor highlights

Thank you for your contributions! 🚀
