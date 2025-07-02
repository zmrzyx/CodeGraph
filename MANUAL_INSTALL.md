# CodeGraph Manual Installation Guide

Since VS Code CLI (`code` command) is not available in your environment, here's how to manually install the CodeGraph extension:

## VS Code Extension Installation

1. **Locate the Extension Package**
   - Find the file: `/Users/jmc/Scheduling_test/RefaactoringW_Go/codegraph/extension/codegraph-0.1.0.vsix`

2. **Install in VS Code**
   - Open VS Code
   - Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
   - Type "Extensions: Install from VSIX..."
   - Select the command from the dropdown
   - Navigate to and select the `codegraph-0.1.0.vsix` file
   - Click "Install"

3. **Verify Installation**
   - Go to Extensions panel (`Cmd+Shift+X`)
   - Search for "CodeGraph" 
   - You should see "CodeGraph" extension installed
   - Check that it shows "AST-based code analysis and dependency visualization"

## Using CodeGraph

### In VS Code
1. Open a project folder in VS Code
2. Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
3. Type "CodeGraph" to see available commands:
   - **CodeGraph: Analyze Project** - Full project analysis
   - **CodeGraph: Show Dependency Graph** - Generate HTML visualization
   - **CodeGraph: Check Algorithmic Complexity** - Check current file complexity
   - **CodeGraph: Detect Circular Dependencies** - Find circular dependencies

### Command Line
```bash
# Navigate to engine directory
cd /Users/jmc/Scheduling_test/RefaactoringW_Go/codegraph/engine

# Activate virtual environment
source venv/bin/activate

# Analyze a project
python3 codegraph.py --analyze ../examples

# Check complexity of specific file
python3 codegraph.py --complexity ../examples/python_example.py

# Check for circular dependencies
python3 codegraph.py --check-cycles ../examples

# Generate JSON output
python3 codegraph.py --analyze ../examples --format json

# Generate HTML report
python3 codegraph.py --analyze ../examples --format html --output report.html
```

## Test with Example Files

The setup created example files in the `examples/` directory:

- `python_example.py` - Python code with various complexity patterns
- `javascript_example.js` - JavaScript code with complexity examples  
- `go_example.go` - Go code with complexity examples

These files demonstrate:
- ✅ O(1) functions (constant time)
- ✅ O(n) functions (linear time)
- ⚠️ O(n²) functions (quadratic time - triggers warnings)
- ⚠️ O(2^n) functions (exponential time - triggers warnings)

## Configuration

You can create a `codegraph.config.js` file in your project root to customize behavior:

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
    },
    go: {
      includes: ["**/*.go"],
      excludes: ["**/vendor/**"]
    }
  }
};
```

## Troubleshooting

### Extension Not Working
1. Check VS Code version (requires 1.60+)
2. Reload VS Code window (`Cmd+R` or `Ctrl+R`)
3. Check the Output panel (View → Output → CodeGraph)

### Engine Issues
1. Ensure Python 3.8+ is installed
2. Check virtual environment is activated: `source venv/bin/activate`
3. Verify dependencies: `pip list | grep networkx`

### No Analysis Results
1. Check file patterns in configuration
2. Ensure files aren't excluded by default patterns
3. Check file permissions

## Example Analysis Output

```
📊 CodeGraph Analysis Results
Files analyzed: 3
Functions found: 23
Dependencies: 10
Circular dependencies: 0

🔍 Complexity Analysis:
  ✅ simple_function (O(1)) - ../examples/python_example.py:10
  ✅ linear_search (O(n)) - ../examples/python_example.py:14
  ⚠️ nested_loop_function (O(n²)) - ../examples/python_example.py:21
  ⚠️ recursive_fibonacci (O(2^n)) - ../examples/python_example.py:29
```

## Next Steps

1. Try analyzing your own projects
2. Experiment with the VS Code extension commands
3. Use the complexity warnings to optimize your code
4. Generate HTML reports for sharing with your team

Happy coding with CodeGraph! 🚀
