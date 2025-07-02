# Installation Guide

This guide will help you install and set up CodeGraph for your development environment.

## Prerequisites

Before installing CodeGraph, ensure you have:

- **Node.js 16+** - [Download from nodejs.org](https://nodejs.org/)
- **Python 3.8+** - [Download from python.org](https://python.org/)
- **VS Code 1.60+** (optional) - [Download from code.visualstudio.com](https://code.visualstudio.com/)

## Quick Installation

### Option 1: Automated Setup (Recommended)

```bash
git clone https://github.com/codegraph-dev/CodeGraph.git
cd CodeGraph
./setup.sh
```

The setup script will:
- Check prerequisites
- Install all dependencies
- Build the VS Code extension
- Set up the Python engine
- Create example projects
- Run basic tests

### Option 2: Manual Installation

#### Install VS Code Extension

```bash
# From VS Code Marketplace (coming soon)
code --install-extension codegraph.codegraph

# Or from source
git clone https://github.com/codegraph-dev/CodeGraph.git
cd CodeGraph/extension
npm install
npm run compile
vsce package
code --install-extension codegraph-*.vsix
```

#### Install Python Engine

```bash
# Using pip (coming soon)
pip install codegraph

# Or from source
cd CodeGraph/engine
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Verification

### Test VS Code Extension

1. Open VS Code
2. Press `Ctrl+Shift+P` (Cmd+Shift+P on Mac)
3. Type "CodeGraph: Analyze Project"
4. Select a project folder
5. View results in the CodeGraph panel

### Test Python Engine

```bash
cd CodeGraph/engine
source venv/bin/activate
python codegraph.py --analyze ../examples/ --format json
```

You should see JSON output with analysis results.

### Test CLI Integration

```bash
# Analyze a project
codegraph analyze ./my-project

# Check for circular dependencies
codegraph cycles ./my-project

# Generate HTML report
codegraph analyze ./my-project --output report.html --format html
```

## Configuration

Create a `codegraph.config.js` file in your project root:

```javascript
module.exports = {
  analysis: {
    maxComplexity: "O(n log n)",
    checkCycles: true,
    generateTests: false
  },
  languages: {
    python: {
      includes: ["**/*.py"],
      excludes: ["**/venv/**", "**/__pycache__/**"]
    },
    javascript: {
      includes: ["**/*.js", "**/*.ts"],
      excludes: ["**/node_modules/**", "**/dist/**"]
    }
  },
  output: {
    format: "html",
    includeMetrics: true
  }
};
```

## Troubleshooting

### Common Issues

#### "Command not found: codegraph"
The Python engine is not in your PATH. Either:
- Use the full path: `python /path/to/codegraph.py`
- Activate the virtual environment: `source venv/bin/activate`
- Install globally: `pip install -e .` (from engine directory)

#### "Cannot find module 'vscode'"
VS Code extension dependencies not installed:
```bash
cd extension
npm install
```

#### "Python module not found"
Engine dependencies not installed:
```bash
cd engine
pip install -r requirements.txt
```

#### Extension not working in VS Code
1. Check extension is installed: `code --list-extensions | grep codegraph`
2. Reload VS Code: `Ctrl+Shift+P` → "Developer: Reload Window"
3. Check VS Code version: Must be 1.60+

### Getting Help

If you encounter issues:

1. Check the [FAQ](faq.md)
2. Search [GitHub Issues](https://github.com/codegraph-dev/CodeGraph/issues)
3. Join our [Discord](https://discord.gg/codegraph)
4. Create a new issue with:
   - Your operating system
   - Node.js and Python versions
   - Complete error messages
   - Steps to reproduce

## Next Steps

- [Quick Start Guide](quickstart.md) - Learn basic usage
- [Configuration Guide](configuration.md) - Customize for your project
- [VS Code Extension Guide](vscode-extension.md) - Master the extension
- [Examples](../examples/) - See CodeGraph in action

## Development Installation

If you want to contribute to CodeGraph:

```bash
# Clone and set up development environment
git clone https://github.com/codegraph-dev/CodeGraph.git
cd CodeGraph

# Install dependencies
npm install  # Extension dependencies
cd engine && pip install -r requirements-dev.txt  # Engine dependencies

# Build everything
npm run build

# Run tests
npm test
python -m pytest

# Package for distribution
./release.sh
```

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for detailed development guidelines.
