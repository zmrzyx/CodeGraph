#!/usr/bin/env python3
"""
Test suite for CodeGraph analysis engine
"""

import unittest
import os
import tempfile
import json
from pathlib import Path
import sys

# Add the engine directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from codegraph import (
    CodeGraphAnalyzer, 
    PythonParser, 
    JavaScriptParser, 
    GoParser,
    DependencyGraphAnalyzer
)


class TestPythonParser(unittest.TestCase):
    """Test Python AST parser"""
    
    def setUp(self):
        self.parser = PythonParser()
    
    def test_can_parse_python_files(self):
        """Test that parser recognizes Python files"""
        self.assertTrue(self.parser.can_parse("test.py"))
        self.assertTrue(self.parser.can_parse("module.py"))
        self.assertFalse(self.parser.can_parse("test.js"))
        self.assertFalse(self.parser.can_parse("test.go"))
    
    def test_parse_simple_python(self):
        """Test parsing a simple Python file"""
        # Create temporary Python file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
import os
import json
from typing import List

def simple_function():
    return "hello"

def complex_function(items):
    result = []
    for item in items:
        for i in range(len(item)):
            result.append(item[i])
    return result

class TestClass:
    def method(self):
        pass
""")
            f.flush()
            
            # Parse the file
            result = self.parser.parse(f.name)
            
            # Check results
            self.assertIn('dependencies', result)
            self.assertIn('complexity', result)
            self.assertIn('functions', result)
            
            # Check dependencies
            deps = result['dependencies']
            self.assertTrue(any(dep['target'] == 'os' for dep in deps))
            self.assertTrue(any(dep['target'] == 'json' for dep in deps))
            
            # Check functions
            functions = result['functions']
            self.assertIn('simple_function', functions)
            self.assertIn('complex_function', functions)
            
            # Check complexity
            complexity = result['complexity']
            self.assertTrue(len(complexity) >= 2)
            
            # Clean up
            os.unlink(f.name)


class TestJavaScriptParser(unittest.TestCase):
    """Test JavaScript parser"""
    
    def setUp(self):
        self.parser = JavaScriptParser()
    
    def test_can_parse_js_files(self):
        """Test that parser recognizes JavaScript files"""
        self.assertTrue(self.parser.can_parse("test.js"))
        self.assertTrue(self.parser.can_parse("test.ts"))
        self.assertTrue(self.parser.can_parse("component.jsx"))
        self.assertFalse(self.parser.can_parse("test.py"))
        self.assertFalse(self.parser.can_parse("test.go"))
    
    def test_parse_simple_javascript(self):
        """Test parsing a simple JavaScript file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write("""
const fs = require('fs');
import { Component } from 'react';

function simpleFunction() {
    return "hello";
}

const complexFunction = (items) => {
    const result = [];
    for (const item of items) {
        for (let i = 0; i < item.length; i++) {
            result.push(item[i]);
        }
    }
    return result;
};

class TestClass {
    method() {
        return "test";
    }
}
""")
            f.flush()
            
            result = self.parser.parse(f.name)
            
            # Check results
            self.assertIn('dependencies', result)
            self.assertIn('complexity', result)
            self.assertIn('functions', result)
            
            # Check dependencies
            deps = result['dependencies']
            self.assertTrue(any(dep['target'] == 'fs' for dep in deps))
            self.assertTrue(any(dep['target'] == 'react' for dep in deps))
            
            # Check functions
            functions = result['functions']
            self.assertIn('simpleFunction', functions)
            self.assertIn('complexFunction', functions)
            
            os.unlink(f.name)


class TestGoParser(unittest.TestCase):
    """Test Go parser"""
    
    def setUp(self):
        self.parser = GoParser()
    
    def test_can_parse_go_files(self):
        """Test that parser recognizes Go files"""
        self.assertTrue(self.parser.can_parse("main.go"))
        self.assertTrue(self.parser.can_parse("utils.go"))
        self.assertFalse(self.parser.can_parse("test.py"))
        self.assertFalse(self.parser.can_parse("test.js"))
    
    def test_parse_simple_go(self):
        """Test parsing a simple Go file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.go', delete=False) as f:
            f.write("""
package main

import (
    "fmt"
    "os"
    "encoding/json"
)

func simpleFunction() string {
    return "hello"
}

func complexFunction(items [][]string) []string {
    result := make([]string, 0)
    for _, item := range items {
        for _, str := range item {
            result = append(result, str)
        }
    }
    return result
}

type TestStruct struct {
    Name string
}

func (t *TestStruct) Method() string {
    return t.Name
}
""")
            f.flush()
            
            result = self.parser.parse(f.name)
            
            # Check results
            self.assertIn('dependencies', result)
            self.assertIn('complexity', result)
            self.assertIn('functions', result)
            
            # Check dependencies
            deps = result['dependencies']
            self.assertTrue(any(dep['target'] == 'fmt' for dep in deps))
            self.assertTrue(any(dep['target'] == 'os' for dep in deps))
            
            # Check functions
            functions = result['functions']
            self.assertIn('simpleFunction', functions)
            self.assertIn('complexFunction', functions)
            
            os.unlink(f.name)


class TestDependencyGraphAnalyzer(unittest.TestCase):
    """Test dependency graph analysis"""
    
    def setUp(self):
        self.analyzer = DependencyGraphAnalyzer()
    
    def test_add_dependency(self):
        """Test adding dependencies"""
        self.analyzer.add_dependency("A", "B")
        self.analyzer.add_dependency("B", "C")
        
        deps_a = self.analyzer.get_dependencies("A")
        self.assertIn("B", deps_a)
        
        dependents_b = self.analyzer.get_dependents("B")
        self.assertIn("A", dependents_b)
    
    def test_cycle_detection(self):
        """Test circular dependency detection"""
        # Create a cycle: A -> B -> C -> A
        self.analyzer.add_dependency("A", "B")
        self.analyzer.add_dependency("B", "C")
        self.analyzer.add_dependency("C", "A")
        
        cycles = self.analyzer.detect_cycles()
        self.assertTrue(len(cycles) > 0)
        
        # Check that the cycle contains our nodes
        found_cycle = False
        for cycle in cycles:
            if "A" in cycle and "B" in cycle and "C" in cycle:
                found_cycle = True
                break
        self.assertTrue(found_cycle)
    
    def test_no_cycles(self):
        """Test detection when no cycles exist"""
        # Create a DAG: A -> B -> C
        self.analyzer.add_dependency("A", "B")
        self.analyzer.add_dependency("B", "C")
        
        cycles = self.analyzer.detect_cycles()
        self.assertEqual(len(cycles), 0)


class TestCodeGraphAnalyzer(unittest.TestCase):
    """Test main analyzer"""
    
    def setUp(self):
        self.analyzer = CodeGraphAnalyzer()
    
    def test_analyze_empty_project(self):
        """Test analyzing an empty directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = self.analyzer.analyze_project(tmpdir)
            
            self.assertEqual(result.metrics.total_files, 0)
            self.assertEqual(len(result.dependencies), 0)
            self.assertEqual(len(result.complexity), 0)
            self.assertEqual(len(result.cycles), 0)
    
    def test_analyze_simple_project(self):
        """Test analyzing a simple project"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a simple Python file
            py_file = os.path.join(tmpdir, "test.py")
            with open(py_file, 'w') as f:
                f.write("""
import os
import json

def simple_function():
    return "hello"

def complex_function(items):
    result = []
    for item in items:
        for i in range(len(item)):
            result.append(item[i])
    return result
""")
            
            result = self.analyzer.analyze_project(tmpdir)
            
            # Check basic metrics
            self.assertEqual(result.metrics.total_files, 1)
            self.assertTrue(len(result.dependencies) > 0)
            self.assertTrue(len(result.complexity) > 0)
            
            # Check that we found the functions
            complexity_funcs = [c.function for c in result.complexity]
            self.assertIn('simple_function', complexity_funcs)
            self.assertIn('complex_function', complexity_funcs)
            
            # Check that we found the imports
            import_targets = [d.target for d in result.dependencies]
            self.assertIn('os', import_targets)
            self.assertIn('json', import_targets)


class TestComplexityAnalysis(unittest.TestCase):
    """Test complexity analysis functionality"""
    
    def test_complexity_estimation(self):
        """Test complexity estimation for different patterns"""
        parser = PythonParser()
        
        # Test O(1) function
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
def constant_function():
    return 42
""")
            f.flush()
            result = parser.parse(f.name)
            complexity = result['complexity'][0]
            self.assertEqual(complexity['complexity'], 'O(1)')
            os.unlink(f.name)
        
        # Test O(n) function
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
def linear_function(items):
    for item in items:
        print(item)
""")
            f.flush()
            result = parser.parse(f.name)
            complexity = result['complexity'][0]
            self.assertEqual(complexity['complexity'], 'O(n)')
            os.unlink(f.name)
        
        # Test O(n²) function
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
def quadratic_function(items):
    for i in items:
        for j in items:
            print(i, j)
""")
            f.flush()
            result = parser.parse(f.name)
            complexity = result['complexity'][0]
            self.assertEqual(complexity['complexity'], 'O(n²)')
            os.unlink(f.name)


def run_tests():
    """Run all tests"""
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestPythonParser,
        TestJavaScriptParser,
        TestGoParser,
        TestDependencyGraphAnalyzer,
        TestCodeGraphAnalyzer,
        TestComplexityAnalysis
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
