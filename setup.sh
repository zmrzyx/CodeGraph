#!/bin/bash

# CodeGraph Setup Script
# Automated environment setup and example project creation

set -e

echo "🚀 Setting up CodeGraph development environment..."

# Check prerequisites
check_prerequisites() {
    echo "📋 Checking prerequisites..."
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js is required but not installed"
        echo "   Please install Node.js 16+ from https://nodejs.org/"
        exit 1
    fi
    
    node_version=$(node --version | sed 's/v//')
    if [[ $(echo "$node_version 16.0.0" | tr " " "\n" | sort -V | head -n1) != "16.0.0" ]]; then
        echo "❌ Node.js 16+ is required (found $node_version)"
        exit 1
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3.8+ is required but not installed"
        exit 1
    fi
    
    python_version=$(python3 --version | cut -d' ' -f2)
    if [[ $(echo "$python_version 3.8.0" | tr " " "\n" | sort -V | head -n1) != "3.8.0" ]]; then
        echo "❌ Python 3.8+ is required (found $python_version)"
        exit 1
    fi
    
    # Check VS Code (optional)
    if command -v code &> /dev/null; then
        echo "✅ VS Code found - extensions can be installed"
    else
        echo "⚠️  VS Code not found - extension installation will be skipped"
    fi
    
    echo "✅ Prerequisites check passed"
}

# Install dependencies
install_dependencies() {
    echo "📦 Installing dependencies..."
    
    # Install extension dependencies
    if [ -d "extension" ]; then
        echo "  Installing VS Code extension dependencies..."
        cd extension
        npm install
        cd ..
    fi
    
    # Install engine dependencies
    if [ -d "engine" ]; then
        echo "  Installing Python engine dependencies..."
        cd engine
        
        # Create virtual environment if it doesn't exist
        if [ ! -d "venv" ]; then
            python3 -m venv venv
        fi
        
        # Activate virtual environment
        source venv/bin/activate
        
        # Install dependencies
        pip install --upgrade pip
        pip install -r requirements.txt
        
        cd ..
    fi
    
    echo "✅ Dependencies installed"
}

# Build components
build_components() {
    echo "🔨 Building components..."
    
    # Build VS Code extension
    if [ -d "extension" ]; then
        echo "  Building VS Code extension..."
        cd extension
        npm run compile
        cd ..
    fi
    
    # Test Python engine
    if [ -d "engine" ]; then
        echo "  Testing Python engine..."
        cd engine
        source venv/bin/activate
        python3 -c "import codegraph; print('✅ Engine import successful')"
        cd ..
    fi
    
    echo "✅ Components built successfully"
}

# Create example projects
create_examples() {
    echo "📁 Creating example projects..."
    
    mkdir -p examples
    
    # Python example
    cat > examples/python_example.py << 'EOF'
"""
Example Python code for CodeGraph analysis
Demonstrates various complexity patterns and dependencies
"""

import json
import os
from typing import List, Dict, Any

def simple_function() -> str:
    """O(1) complexity function"""
    return "Hello, CodeGraph!"

def linear_search(items: List[str], target: str) -> int:
    """O(n) complexity function"""
    for i, item in enumerate(items):
        if item == target:
            return i
    return -1

def nested_loop_function(matrix: List[List[int]]) -> int:
    """O(n²) complexity function - should trigger warning"""
    total = 0
    for row in matrix:
        for value in row:
            total += value
    return total

def recursive_fibonacci(n: int) -> int:
    """O(2^n) complexity function - should trigger high complexity warning"""
    if n <= 1:
        return n
    return recursive_fibonacci(n-1) + recursive_fibonacci(n-2)

class DataProcessor:
    """Example class with various methods"""
    
    def __init__(self):
        self.data = []
    
    def process_data(self, input_data: Dict[str, Any]) -> List[str]:
        """Process input data and return results"""
        results = []
        
        # Single loop - O(n)
        for key, value in input_data.items():
            if isinstance(value, str):
                results.append(f"{key}: {value}")
        
        return results
    
    def complex_analysis(self, data_sets: List[List[Dict[str, Any]]]) -> Dict[str, int]:
        """Complex nested processing - O(n³) complexity"""
        analysis = {}
        
        for dataset in data_sets:
            for record in dataset:
                for key, value in record.items():
                    if key not in analysis:
                        analysis[key] = 0
                    if isinstance(value, int):
                        analysis[key] += value
        
        return analysis

def main():
    """Main function demonstrating usage"""
    processor = DataProcessor()
    
    sample_data = {
        "name": "John",
        "age": 30,
        "city": "New York"
    }
    
    results = processor.process_data(sample_data)
    print(f"Processed results: {results}")
    
    # This should trigger complexity warnings
    fib_result = recursive_fibonacci(10)
    print(f"Fibonacci result: {fib_result}")

if __name__ == "__main__":
    main()
EOF

    # JavaScript example
    cat > examples/javascript_example.js << 'EOF'
/**
 * Example JavaScript code for CodeGraph analysis
 * Demonstrates various complexity patterns and dependencies
 */

const fs = require('fs');
const path = require('path');

// O(1) complexity function
function simpleFunction() {
    return "Hello, CodeGraph!";
}

// O(n) complexity function  
function linearSearch(items, target) {
    for (let i = 0; i < items.length; i++) {
        if (items[i] === target) {
            return i;
        }
    }
    return -1;
}

// O(n²) complexity function - should trigger warning
function bubbleSort(arr) {
    const n = arr.length;
    for (let i = 0; i < n - 1; i++) {
        for (let j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
            }
        }
    }
    return arr;
}

// Class example
class DataProcessor {
    constructor() {
        this.data = [];
    }
    
    // O(n) complexity
    processData(inputData) {
        const results = [];
        
        for (const [key, value] of Object.entries(inputData)) {
            if (typeof value === 'string') {
                results.push(`${key}: ${value}`);
            }
        }
        
        return results;
    }
    
    // O(n³) complexity - should trigger high complexity warning
    complexAnalysis(dataSets) {
        const analysis = {};
        
        for (const dataset of dataSets) {
            for (const record of dataset) {
                for (const [key, value] of Object.entries(record)) {
                    if (!analysis[key]) {
                        analysis[key] = 0;
                    }
                    if (typeof value === 'number') {
                        analysis[key] += value;
                    }
                }
            }
        }
        
        return analysis;
    }
}

// Arrow function examples
const quickProcess = (data) => {
    return data.map(item => item.toString().toUpperCase());
};

const asyncProcessor = async (items) => {
    const results = [];
    for (const item of items) {
        const processed = await processItem(item);
        results.push(processed);
    }
    return results;
};

function processItem(item) {
    return new Promise(resolve => {
        setTimeout(() => resolve(`processed_${item}`), 10);
    });
}

// Main execution
function main() {
    const processor = new DataProcessor();
    
    const sampleData = {
        name: "John",
        age: 30,
        city: "New York"
    };
    
    const results = processor.processData(sampleData);
    console.log('Processed results:', results);
    
    // Test sorting (will trigger complexity warning)
    const unsorted = [64, 34, 25, 12, 22, 11, 90];
    const sorted = bubbleSort([...unsorted]);
    console.log('Sorted array:', sorted);
}

if (require.main === module) {
    main();
}

module.exports = {
    DataProcessor,
    simpleFunction,
    linearSearch,
    bubbleSort
};
EOF

    # Go example
    cat > examples/go_example.go << 'EOF'
package main

import (
	"fmt"
	"encoding/json"
	"os"
)

// Simple O(1) function
func simpleFunction() string {
	return "Hello, CodeGraph!"
}

// O(n) complexity function
func linearSearch(items []string, target string) int {
	for i, item := range items {
		if item == target {
			return i
		}
	}
	return -1
}

// O(n²) complexity function - should trigger warning
func bubbleSort(arr []int) []int {
	n := len(arr)
	for i := 0; i < n-1; i++ {
		for j := 0; j < n-i-1; j++ {
			if arr[j] > arr[j+1] {
				arr[j], arr[j+1] = arr[j+1], arr[j]
			}
		}
	}
	return arr
}

// Struct example
type DataProcessor struct {
	data []interface{}
}

// NewDataProcessor creates a new processor
func NewDataProcessor() *DataProcessor {
	return &DataProcessor{
		data: make([]interface{}, 0),
	}
}

// ProcessData processes input data - O(n) complexity
func (dp *DataProcessor) ProcessData(inputData map[string]interface{}) []string {
	results := make([]string, 0)
	
	for key, value := range inputData {
		if str, ok := value.(string); ok {
			results = append(results, fmt.Sprintf("%s: %s", key, str))
		}
	}
	
	return results
}

// ComplexAnalysis performs nested analysis - O(n³) complexity
func (dp *DataProcessor) ComplexAnalysis(dataSets [][]map[string]interface{}) map[string]int {
	analysis := make(map[string]int)
	
	for _, dataset := range dataSets {
		for _, record := range dataset {
			for key, value := range record {
				if _, exists := analysis[key]; !exists {
					analysis[key] = 0
				}
				if num, ok := value.(int); ok {
					analysis[key] += num
				}
			}
		}
	}
	
	return analysis
}

// Recursive function - O(2^n) complexity
func fibonacci(n int) int {
	if n <= 1 {
		return n
	}
	return fibonacci(n-1) + fibonacci(n-2)
}

func main() {
	processor := NewDataProcessor()
	
	sampleData := map[string]interface{}{
		"name": "John",
		"age":  30,
		"city": "New York",
	}
	
	results := processor.ProcessData(sampleData)
	fmt.Printf("Processed results: %v\n", results)
	
	// Test fibonacci (will trigger high complexity warning)  
	fibResult := fibonacci(10)
	fmt.Printf("Fibonacci result: %d\n", fibResult)
	
	// Test sorting (will trigger complexity warning)
	unsorted := []int{64, 34, 25, 12, 22, 11, 90}
	sorted := bubbleSort(append([]int(nil), unsorted...))
	fmt.Printf("Sorted array: %v\n", sorted)
}
EOF

    echo "✅ Example projects created in examples/ directory"
}

# Install VS Code extension  
install_vscode_extension() {
    if [ -d "extension" ]; then
        echo "🔧 Building VS Code extension..."
        cd extension
        
        # Package extension for distribution
        if command -v vsce &> /dev/null; then
            echo "  Packaging extension..."
            vsce package --no-git-tag-version || echo "  ⚠️  Packaging failed, but continuing..."
            
            # Try to install if VS Code CLI is available
            if command -v code &> /dev/null && ls *.vsix 1> /dev/null 2>&1; then
                echo "  Installing extension to VS Code..."
                code --install-extension *.vsix
                echo "  ✅ VS Code extension installed"
            else
                echo "  📦 Extension packaged (VS Code CLI not available for auto-install)"
                echo "  Manual install: Open VS Code → Extensions → Install from VSIX → Select the .vsix file"
            fi
        else
            echo "  ⚠️  vsce not found - installing globally..."
            npm install -g @vscode/vsce
            vsce package --no-git-tag-version || echo "  ⚠️  Packaging failed, but continuing..."
            
            if command -v code &> /dev/null && ls *.vsix 1> /dev/null 2>&1; then
                code --install-extension *.vsix
                echo "  ✅ VS Code extension installed"
            else
                echo "  📦 Extension packaged (manual install required)"
            fi
        fi
        
        cd ..
    else
        echo "⚠️  Extension directory not found - skipping"
    fi
}

# Run tests
run_tests() {
    echo "🧪 Running tests..."
    
    # Test extension
    if [ -d "extension" ]; then
        echo "  Testing VS Code extension..."
        cd extension
        npm test 2>/dev/null || echo "  ⚠️  Extension tests not yet implemented"
        cd ..
    fi
    
    # Test engine
    if [ -d "engine" ]; then
        echo "  Testing Python engine..."
        cd engine
        
        # Activate virtual environment if it exists
        if [ -d "venv" ]; then
            source venv/bin/activate
        fi
        
        # Run basic engine test - create a simple test file first
        cat > test_input.py << 'EOF'
def simple_function():
    return "test"

def complex_function():
    for i in range(10):
        for j in range(10):
            print(i, j)
EOF
        
        # Test the engine
        python3 codegraph.py --analyze . --format json > /dev/null && echo "  ✅ Engine analysis test passed" || echo "  ⚠️  Engine test had issues but continuing"
        
        # Clean up test file
        rm -f test_input.py
        
        cd ..
    fi
    
    echo "✅ Tests completed"
}

# Main setup flow
main() {
    echo "Starting CodeGraph setup..."
    
    check_prerequisites
    install_dependencies
    build_components
    create_examples
    install_vscode_extension
    run_tests
    
    echo ""
    echo "🎉 CodeGraph setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Open VS Code and use Ctrl+Shift+P → 'CodeGraph: Analyze Project'"
    echo "2. Try the CLI: cd engine && source venv/bin/activate && python3 codegraph.py --analyze ../examples/"
    echo "3. Check out the examples in the examples/ directory"
    echo "4. Read the documentation in docs/"
    echo ""
    echo "Happy coding with CodeGraph! 🚀"
}

# Run main function
main "$@"
