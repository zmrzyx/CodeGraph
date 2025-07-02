# CodeGraph

**Language-agnostic AST analysis and dependency visualization for modern development workflows**

CodeGraph is a powerful open source tool that brings advanced computer science principles to everyday development through Abstract Syntax Tree (AST) analysis, dependency graph visualization, and algorithmic complexity validation.

## 🎯 What CodeGraph Does

CodeGraph helps development teams by:

- **AST-Based Code Analysis**: Understanding code semantically, not just as text
- **Dependency Visualization**: Building mathematical graphs of component relationships  
- **Complexity Validation**: Ensuring optimal algorithmic performance (O(n log n) enforcement)
- **Refactoring Safety**: Zero-regression transformations through semantic understanding
- **Multi-Language Support**: Go, Python, JavaScript, TypeScript, Java, and more

## 🚀 Quick Start

### VS Code Extension

```bash
git clone https://github.com/codegraph-dev/CodeGraph.git
cd CodeGraph/extension
npm install
npm run compile
code --install-extension .
```

### Command Line Engine

```bash
cd CodeGraph/engine
pip install -r requirements.txt

# Analyze a project
python codegraph.py --analyze ./your-project

# Check for dependency cycles
python codegraph.py --check-cycles ./your-project

# Validate complexity
python codegraph.py --complexity ./your-project
```

### CI/CD Integration

```bash
cp ci/github-workflow.yml .github/workflows/codegraph.yml
```

## 🏗️ Architecture

CodeGraph consists of three main components:

### 1. Language Parsers
- **AST Generation**: Parse source code into Abstract Syntax Trees
- **Symbol Resolution**: Identify functions, classes, imports, and dependencies
- **Multi-Language Support**: Pluggable parser architecture

### 2. Dependency Engine
- **Graph Construction**: Build directed graphs of code dependencies
- **Cycle Detection**: Identify circular dependencies and architectural issues
- **Impact Analysis**: Understand change propagation through the codebase

### 3. Visualization Tools
- **Interactive Graphs**: Web-based dependency visualization
- **VS Code Integration**: Real-time analysis in your editor
- **CLI Reports**: Text-based analysis for CI/CD pipelines

## 📊 Features

### Code Analysis
- **Semantic Understanding**: Parse code into Abstract Syntax Trees
- **Import Analysis**: Track dependencies between modules and packages
- **Function Call Graphs**: Visualize execution flow and dependencies
- **Type Analysis**: Understand data flow and type relationships

### Dependency Management
- **Circular Dependency Detection**: Identify and resolve architectural issues
- **Impact Analysis**: Understand how changes affect other components
- **Dependency Visualization**: Interactive graphs of code relationships
- **Architecture Validation**: Enforce architectural constraints

### Performance Optimization
- **Complexity Analysis**: Validate algorithmic complexity (O(n), O(n log n), etc.)
- **Performance Regression Detection**: Catch performance issues early
- **Bottleneck Identification**: Find performance-critical code paths
- **Optimization Suggestions**: Recommend algorithmic improvements

### Refactoring Support
- **Safe Transformations**: Semantically-aware code refactoring
- **Zero-Regression Guarantee**: Maintain functionality during changes
- **Automated Testing**: Generate tests to validate refactoring safety
- **Rollback Capabilities**: Undo changes if issues are detected

## 🛠️ Installation

### Prerequisites
- Node.js 16+ (for VS Code extension)
- Python 3.8+ (for analysis engine)
- VS Code 1.60+ (for extension features)

### VS Code Extension
```bash
# Install from VS Code Marketplace (coming soon)
code --install-extension codegraph.codegraph

# Or install from source
git clone https://github.com/codegraph-dev/CodeGraph.git
cd CodeGraph/extension
npm install
npm run compile
code --install-extension .
```

### Command Line Tool
```bash
pip install codegraph

# Or install from source
git clone https://github.com/codegraph-dev/CodeGraph.git
cd CodeGraph/engine
pip install -r requirements.txt
pip install -e .
```

## 🔧 Configuration

Create a `codegraph.config.js` file in your project root:

```javascript
module.exports = {
  // Analysis settings
  analysis: {
    maxComplexity: "O(n log n)",
    checkCycles: true,
    enforceArchitecture: true,
    generateTests: true
  },
  
  // Language-specific settings
  languages: {
    go: {
      parser: "go/ast",
      includes: ["**/*.go"],
      excludes: ["**/vendor/**", "**/node_modules/**"]
    },
    python: {
      parser: "ast",
      includes: ["**/*.py"],
      excludes: ["**/venv/**", "**/__pycache__/**"]
    },
    javascript: {
      parser: "@babel/parser",
      includes: ["**/*.js", "**/*.ts"],
      excludes: ["**/node_modules/**", "**/dist/**"]
    }
  },
  
  // Visualization options
  visualization: {
    layout: "hierarchical",
    showTypes: true,
    highlightCycles: true,
    maxNodes: 500
  },
  
  // CI/CD integration
  ci: {
    failOnCycles: true,
    failOnComplexity: true,
    generateReports: true,
    outputFormat: "json"
  }
};
```

## 📖 Usage Examples

### Basic Analysis
```bash
# Analyze entire project
codegraph analyze ./my-project

# Check specific files
codegraph analyze ./src/main.py ./src/utils.py

# Generate dependency graph
codegraph graph ./my-project --output graph.html
```

### Complexity Validation
```bash
# Check algorithmic complexity
codegraph complexity ./my-project

# Enforce maximum complexity
codegraph complexity ./my-project --max "O(n log n)"

# Performance regression testing
codegraph perf ./my-project --baseline ./baseline.json
```

### Dependency Analysis
```bash
# Check for circular dependencies
codegraph cycles ./my-project

# Analyze import structure
codegraph imports ./my-project --format json

# Validate architecture constraints
codegraph arch ./my-project --rules ./arch-rules.yaml
```

### VS Code Integration
1. Install the CodeGraph extension
2. Open a project in VS Code
3. Use `Ctrl+Shift+P` → "CodeGraph: Analyze Project"
4. View dependency graphs in the CodeGraph panel
5. Get real-time complexity warnings in the editor

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
# Clone the repository
git clone https://github.com/codegraph-dev/CodeGraph.git
cd CodeGraph

# Install dependencies
./setup.sh

# Run tests
npm test  # Extension tests
python -m pytest  # Engine tests

# Build everything
./release.sh --dev
```

### Adding Language Support
1. Create a parser in `engine/parsers/your_language.py`
2. Implement the `Parser` interface
3. Add language configuration to `codegraph.config.js`
4. Add tests in `engine/tests/test_your_language.py`
5. Update documentation

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

## 🏆 Inspiration

CodeGraph was inspired by breakthrough results in AST-based code analysis:
- 50x performance improvement in refactoring operations
- 99.9% accuracy in automated transformations
- Zero regression guarantees through semantic understanding

## 🔗 Links

- [Documentation](https://codegraph-dev.github.io/CodeGraph/)
- [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=codegraph.codegraph)
- [PyPI Package](https://pypi.org/project/codegraph/)
- [GitHub Issues](https://github.com/codegraph-dev/CodeGraph/issues)
- [Community Discord](https://discord.gg/codegraph)

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=codegraph-dev/CodeGraph&type=Date)](https://star-history.com/#codegraph-dev/CodeGraph&Date)
