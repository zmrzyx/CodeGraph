#!/usr/bin/env python3
"""
CodeGraph Analysis Engine
Language-agnostic AST analysis and dependency visualization tool
"""

import ast
import argparse
import json
import os
import sys
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import importlib.util


@dataclass
class DependencyInfo:
    """Represents a dependency relationship between code components"""
    source: str
    target: str
    type: str  # 'import', 'function_call', 'inheritance', 'composition'
    line: int
    column: int


@dataclass
class ComplexityInfo:
    """Represents algorithmic complexity information for a function"""
    function: str
    file: str
    complexity: str
    line: int
    warning: Optional[str] = None


@dataclass
class CircularDependency:
    """Represents a circular dependency cycle"""
    cycle: List[str]
    severity: str  # 'warning' or 'error'


@dataclass
class ProjectMetrics:
    """Overall project analysis metrics"""
    total_files: int
    total_functions: int
    average_complexity: str
    dependency_count: int
    circular_dependencies: int


@dataclass
class AnalysisResult:
    """Complete analysis result"""
    dependencies: List[DependencyInfo]
    complexity: List[ComplexityInfo]
    cycles: List[CircularDependency]
    metrics: ProjectMetrics


class BaseParser:
    """Base class for language-specific parsers"""
    
    def __init__(self, file_extensions: List[str]):
        self.file_extensions = file_extensions
    
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle the given file"""
        return any(file_path.endswith(ext) for ext in self.file_extensions)
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """Parse a file and extract analysis data"""
        raise NotImplementedError("Subclasses must implement parse method")


class PythonParser(BaseParser):
    """Python AST parser for dependency and complexity analysis"""
    
    def __init__(self):
        super().__init__(['.py'])
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """Parse Python file using AST"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content, filename=file_path)
            
            dependencies = self._extract_dependencies(tree, file_path)
            complexity = self._analyze_complexity(tree, file_path)
            functions = self._extract_functions(tree)
            
            return {
                'dependencies': dependencies,
                'complexity': complexity,
                'functions': functions,
                'imports': self._extract_imports(tree),
                'classes': self._extract_classes(tree)
            }
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return {
                'dependencies': [],
                'complexity': [],
                'functions': [],
                'imports': [],
                'classes': []
            }
    
    def _extract_dependencies(self, tree: ast.AST, file_path: str) -> List[Dict[str, Any]]:
        """Extract import dependencies from AST"""
        dependencies = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    dependencies.append({
                        'source': file_path,
                        'target': alias.name,
                        'type': 'import',
                        'line': node.lineno,
                        'column': node.col_offset
                    })
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    for alias in node.names:
                        dependencies.append({
                            'source': file_path,
                            'target': f"{node.module}.{alias.name}",
                            'type': 'import',
                            'line': node.lineno,
                            'column': node.col_offset
                        })
        
        return dependencies
    
    def _analyze_complexity(self, tree: ast.AST, file_path: str) -> List[Dict[str, Any]]:
        """Analyze algorithmic complexity of functions"""
        complexity_info = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                complexity = self._estimate_complexity(node)
                warning = None
                
                if self._is_high_complexity(complexity):
                    warning = f"Consider optimizing - complexity is {complexity}"
                
                complexity_info.append({
                    'function': node.name,
                    'file': file_path,
                    'complexity': complexity,
                    'line': node.lineno,
                    'warning': warning
                })
        
        return complexity_info
    
    def _estimate_complexity(self, func_node: ast.AST) -> str:
        """Estimate algorithmic complexity based on AST patterns"""
        # Simple heuristic-based complexity estimation
        loops = 0
        nested_loops = 0
        recursive_calls = 0
        
        for node in ast.walk(func_node):
            if isinstance(node, (ast.For, ast.While)):
                loops += 1
                # Check for nested loops
                for child in ast.walk(node):
                    if child != node and isinstance(child, (ast.For, ast.While)):
                        nested_loops += 1
            elif isinstance(node, ast.Call):
                if hasattr(node.func, 'id') and isinstance(func_node, ast.FunctionDef):
                    if node.func.id == func_node.name:
                        recursive_calls += 1
        
        # Complexity estimation logic
        if recursive_calls > 0:
            return "O(2^n)"  # Assume exponential for recursive without memoization
        elif nested_loops > 0:
            return "O(n²)"
        elif loops > 0:
            return "O(n)"
        else:
            return "O(1)"
    
    def _is_high_complexity(self, complexity: str) -> bool:
        """Check if complexity is considered high"""
        high_complexity = ["O(n²)", "O(2^n)", "O(n!)"]
        return complexity in high_complexity
    
    def _extract_functions(self, tree: ast.AST) -> List[str]:
        """Extract function names from AST"""
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(node.name)
        return functions
    
    def _extract_imports(self, tree: ast.AST) -> List[str]:
        """Extract import statements"""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        return imports
    
    def _extract_classes(self, tree: ast.AST) -> List[str]:
        """Extract class names from AST"""
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)
        return classes


class JavaScriptParser(BaseParser):
    """JavaScript/TypeScript parser using regex patterns"""
    
    def __init__(self):
        super().__init__(['.js', '.ts', '.jsx', '.tsx'])
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """Parse JavaScript/TypeScript file using regex patterns"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            dependencies = self._extract_dependencies(content, file_path)
            complexity = self._analyze_complexity(content, file_path)
            functions = self._extract_functions(content)
            
            return {
                'dependencies': dependencies,
                'complexity': complexity,
                'functions': functions,
                'imports': self._extract_imports(content),
                'classes': self._extract_classes(content)
            }
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return {
                'dependencies': [],
                'complexity': [],
                'functions': [],
                'imports': [],
                'classes': []
            }
    
    def _extract_dependencies(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract import/require dependencies using regex"""
        dependencies = []
        lines = content.split('\n')
        
        # Match import statements
        import_patterns = [
            r'import\s+.*\s+from\s+[\'"]([^\'"]+)[\'"]',
            r'import\s+[\'"]([^\'"]+)[\'"]',
            r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)',
            r'import\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)'
        ]
        
        for line_num, line in enumerate(lines, 1):
            for pattern in import_patterns:
                matches = re.finditer(pattern, line)
                for match in matches:
                    dependencies.append({
                        'source': file_path,
                        'target': match.group(1),
                        'type': 'import',
                        'line': line_num,
                        'column': match.start()
                    })
        
        return dependencies
    
    def _analyze_complexity(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Analyze function complexity using regex patterns"""
        complexity_info = []
        functions = self._extract_functions_with_lines(content)
        
        for func_name, line_num, func_content in functions:
            complexity = self._estimate_js_complexity(func_content)
            warning = None
            
            if self._is_high_complexity(complexity):
                warning = f"Consider optimizing - complexity is {complexity}"
            
            complexity_info.append({
                'function': func_name,
                'file': file_path,
                'complexity': complexity,
                'line': line_num,
                'warning': warning
            })
        
        return complexity_info
    
    def _extract_functions_with_lines(self, content: str) -> List[Tuple[str, int, str]]:
        """Extract functions with their line numbers and content"""
        functions = []
        lines = content.split('\n')
        
        # Function patterns
        patterns = [
            r'function\s+(\w+)\s*\(',
            r'(\w+)\s*:\s*function\s*\(',
            r'(\w+)\s*=\s*function\s*\(',
            r'(\w+)\s*=\s*\([^)]*\)\s*=>\s*{',
            r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>'
        ]
        
        for line_num, line in enumerate(lines, 1):
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    func_name = match.group(1)
                    # Extract function content (simplified)
                    func_content = self._extract_function_body(lines, line_num - 1)
                    functions.append((func_name, line_num, func_content))
        
        return functions
    
    def _extract_function_body(self, lines: List[str], start_line: int) -> str:
        """Extract function body content (simplified)"""
        if start_line >= len(lines):
            return ""
        
        # Simple brace counting to find function end
        brace_count = 0
        function_lines = []
        
        for i in range(start_line, min(len(lines), start_line + 50)):  # Limit search
            line = lines[i]
            function_lines.append(line)
            
            brace_count += line.count('{') - line.count('}')
            if i > start_line and brace_count <= 0:
                break
        
        return '\n'.join(function_lines)
    
    def _estimate_js_complexity(self, func_content: str) -> str:
        """Estimate JavaScript function complexity"""
        loops = len(re.findall(r'\b(for|while|forEach)\b', func_content))
        nested_loops = 0
        
        # Simple nested loop detection
        lines = func_content.split('\n')
        in_loop = False
        for line in lines:
            if re.search(r'\b(for|while|forEach)\b', line):
                if in_loop:
                    nested_loops += 1
                in_loop = True
            elif '}' in line:
                in_loop = False
        
        if nested_loops > 0:
            return "O(n²)"
        elif loops > 0:
            return "O(n)"
        else:
            return "O(1)"
    
    def _is_high_complexity(self, complexity: str) -> bool:
        """Check if complexity is considered high"""
        return complexity in ["O(n²)", "O(2^n)", "O(n!)"]
    
    def _extract_functions(self, content: str) -> List[str]:
        """Extract function names"""
        functions = []
        patterns = [
            r'function\s+(\w+)\s*\(',
            r'(\w+)\s*:\s*function\s*\(',
            r'(\w+)\s*=\s*function\s*\(',
            r'(\w+)\s*=\s*\([^)]*\)\s*=>\s*{',
            r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                functions.append(match.group(1))
        
        return functions
    
    def _extract_imports(self, content: str) -> List[str]:
        """Extract import statements"""
        imports = []
        patterns = [
            r'import\s+.*\s+from\s+[\'"]([^\'"]+)[\'"]',
            r'import\s+[\'"]([^\'"]+)[\'"]',
            r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                imports.append(match.group(1))
        
        return imports
    
    def _extract_classes(self, content: str) -> List[str]:
        """Extract class names"""
        classes = []
        pattern = r'class\s+(\w+)(?:\s+extends\s+\w+)?'
        matches = re.finditer(pattern, content)
        for match in matches:
            classes.append(match.group(1))
        return classes


class GoParser(BaseParser):
    """Go parser using regex patterns"""
    
    def __init__(self):
        super().__init__(['.go'])
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """Parse Go file using regex patterns"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            dependencies = self._extract_dependencies(content, file_path)
            complexity = self._analyze_complexity(content, file_path)
            functions = self._extract_functions(content)
            
            return {
                'dependencies': dependencies,
                'complexity': complexity,
                'functions': functions,
                'imports': self._extract_imports(content),
                'structs': self._extract_structs(content)
            }
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return {
                'dependencies': [],
                'complexity': [],
                'functions': [],
                'imports': [],
                'structs': []
            }
    
    def _extract_dependencies(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract import dependencies"""
        dependencies = []
        lines = content.split('\n')
        
        # Match import statements
        import_patterns = [
            r'import\s+"([^"]+)"',
            r'import\s+\(\s*"([^"]+)"\s*\)',
            r'^\s*"([^"]+)"\s*$'  # Inside import block
        ]
        
        in_import_block = False
        for line_num, line in enumerate(lines, 1):
            if 'import (' in line:
                in_import_block = True
                continue
            elif ')' in line and in_import_block:
                in_import_block = False
                continue
            
            if in_import_block:
                match = re.search(r'"([^"]+)"', line)
                if match:
                    dependencies.append({
                        'source': file_path,
                        'target': match.group(1),
                        'type': 'import',
                        'line': line_num,
                        'column': match.start()
                    })
            else:
                for pattern in import_patterns:
                    matches = re.finditer(pattern, line)
                    for match in matches:
                        dependencies.append({
                            'source': file_path,
                            'target': match.group(1),
                            'type': 'import',
                            'line': line_num,
                            'column': match.start()
                        })
        
        return dependencies
    
    def _analyze_complexity(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Analyze function complexity"""
        complexity_info = []
        functions = self._extract_functions_with_lines(content)
        
        for func_name, line_num, func_content in functions:
            complexity = self._estimate_go_complexity(func_content)
            warning = None
            
            if self._is_high_complexity(complexity):
                warning = f"Consider optimizing - complexity is {complexity}"
            
            complexity_info.append({
                'function': func_name,
                'file': file_path,
                'complexity': complexity,
                'line': line_num,
                'warning': warning
            })
        
        return complexity_info
    
    def _extract_functions_with_lines(self, content: str) -> List[Tuple[str, int, str]]:
        """Extract functions with their line numbers and content"""
        functions = []
        lines = content.split('\n')
        
        func_pattern = r'func\s+(?:\([^)]*\)\s+)?(\w+)\s*\([^)]*\)'
        
        for line_num, line in enumerate(lines, 1):
            match = re.search(func_pattern, line)
            if match:
                func_name = match.group(1)
                func_content = self._extract_go_function_body(lines, line_num - 1)
                functions.append((func_name, line_num, func_content))
        
        return functions
    
    def _extract_go_function_body(self, lines: List[str], start_line: int) -> str:
        """Extract Go function body"""
        if start_line >= len(lines):
            return ""
        
        brace_count = 0
        function_lines = []
        
        for i in range(start_line, min(len(lines), start_line + 100)):  # Limit search
            line = lines[i]
            function_lines.append(line)
            
            brace_count += line.count('{') - line.count('}')
            if i > start_line and brace_count <= 0:
                break
        
        return '\n'.join(function_lines)
    
    def _estimate_go_complexity(self, func_content: str) -> str:
        """Estimate Go function complexity"""
        loops = len(re.findall(r'\b(for|range)\b', func_content))
        nested_loops = 0
        
        # Simple nested loop detection
        lines = func_content.split('\n')
        in_loop = False
        for line in lines:
            if re.search(r'\bfor\b', line):
                if in_loop:
                    nested_loops += 1
                in_loop = True
            elif '}' in line and in_loop:
                in_loop = False
        
        if nested_loops > 0:
            return "O(n²)"
        elif loops > 0:
            return "O(n)"
        else:
            return "O(1)"
    
    def _is_high_complexity(self, complexity: str) -> bool:
        """Check if complexity is considered high"""
        return complexity in ["O(n²)", "O(2^n)", "O(n!)"]
    
    def _extract_functions(self, content: str) -> List[str]:
        """Extract function names"""
        functions = []
        pattern = r'func\s+(?:\([^)]*\)\s+)?(\w+)\s*\([^)]*\)'
        matches = re.finditer(pattern, content)
        for match in matches:
            functions.append(match.group(1))
        return functions
    
    def _extract_imports(self, content: str) -> List[str]:
        """Extract import statements"""
        imports = []
        lines = content.split('\n')
        
        in_import_block = False
        for line in lines:
            if 'import (' in line:
                in_import_block = True
                continue
            elif ')' in line and in_import_block:
                in_import_block = False
                continue
            
            if in_import_block:
                match = re.search(r'"([^"]+)"', line)
                if match:
                    imports.append(match.group(1))
            else:
                match = re.search(r'import\s+"([^"]+)"', line)
                if match:
                    imports.append(match.group(1))
        
        return imports
    
    def _extract_structs(self, content: str) -> List[str]:
        """Extract struct names"""
        structs = []
        pattern = r'type\s+(\w+)\s+struct'
        matches = re.finditer(pattern, content)
        for match in matches:
            structs.append(match.group(1))
        return structs


class DependencyGraphAnalyzer:
    """Analyzes dependency relationships and detects cycles"""
    
    def __init__(self):
        self.graph = defaultdict(set)
        self.reverse_graph = defaultdict(set)
    
    def add_dependency(self, source: str, target: str):
        """Add a dependency relationship"""
        self.graph[source].add(target)
        self.reverse_graph[target].add(source)
    
    def detect_cycles(self) -> List[List[str]]:
        """Detect circular dependencies using DFS"""
        visited = set()
        rec_stack = set()
        cycles = []
        
        def dfs(node: str, path: List[str]) -> bool:
            if node in rec_stack:
                # Find the cycle in the path
                cycle_start = path.index(node)
                cycle = path[cycle_start:] + [node]
                cycles.append(cycle)
                return True
            
            if node in visited:
                return False
            
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in self.graph[node]:
                if dfs(neighbor, path):
                    # Don't return immediately to find all cycles
                    pass
            
            rec_stack.remove(node)
            path.pop()
            return False
        
        for node in list(self.graph.keys()):
            if node not in visited:
                dfs(node, [])
        
        return cycles
    
    def get_dependencies(self, node: str) -> Set[str]:
        """Get all dependencies of a node"""
        return self.graph[node].copy()
    
    def get_dependents(self, node: str) -> Set[str]:
        """Get all nodes that depend on this node"""
        return self.reverse_graph[node].copy()


class CodeGraphAnalyzer:
    """Main analyzer class that coordinates parsing and analysis"""
    
    def __init__(self):
        self.parsers = [
            PythonParser(),
            JavaScriptParser(),
            GoParser()
        ]
        self.dependency_analyzer = DependencyGraphAnalyzer()
    
    def analyze_project(self, project_path: str, exclude_patterns: List[str] = None) -> AnalysisResult:
        """Analyze entire project"""
        if exclude_patterns is None:
            exclude_patterns = [
                '**/node_modules/**',
                '**/vendor/**',
                '**/.git/**',
                '**/venv/**',
                '**/__pycache__/**',
                '**/dist/**',
                '**/build/**'
            ]
        
        all_files = self._find_source_files(project_path, exclude_patterns)
        
        all_dependencies = []
        all_complexity = []
        all_functions = []
        
        # Parse all files
        for file_path in all_files:
            parser = self._get_parser(file_path)
            if parser:
                result = parser.parse(file_path)
                
                all_dependencies.extend([
                    DependencyInfo(**dep) for dep in result['dependencies']
                ])
                all_complexity.extend([
                    ComplexityInfo(**comp) for comp in result['complexity']
                ])
                all_functions.extend(result['functions'])
        
        # Build dependency graph
        for dep in all_dependencies:
            self.dependency_analyzer.add_dependency(dep.source, dep.target)
        
        # Detect cycles
        cycles = self.dependency_analyzer.detect_cycles()
        circular_deps = [
            CircularDependency(cycle=cycle, severity='error' if len(cycle) > 5 else 'warning')
            for cycle in cycles
        ]
        
        # Calculate metrics
        metrics = ProjectMetrics(
            total_files=len(all_files),
            total_functions=len(all_functions),
            average_complexity=self._calculate_average_complexity(all_complexity),
            dependency_count=len(all_dependencies),
            circular_dependencies=len(circular_deps)
        )
        
        return AnalysisResult(
            dependencies=all_dependencies,
            complexity=all_complexity,
            cycles=circular_deps,
            metrics=metrics
        )
    
    def _find_source_files(self, project_path: str, exclude_patterns: List[str]) -> List[str]:
        """Find all source files in project"""
        source_files = []
        project_path = Path(project_path)
        
        for file_path in project_path.rglob('*'):
            if file_path.is_file():
                file_str = str(file_path)
                
                # Check if file should be excluded
                should_exclude = False
                for pattern in exclude_patterns:
                    # Simple pattern matching (could be improved with fnmatch)
                    if pattern.replace('**/', '').replace('/**', '') in file_str:
                        should_exclude = True
                        break
                
                if not should_exclude and self._get_parser(file_str):
                    source_files.append(file_str)
        
        return source_files
    
    def _get_parser(self, file_path: str) -> Optional[BaseParser]:
        """Get appropriate parser for file"""
        for parser in self.parsers:
            if parser.can_parse(file_path):
                return parser
        return None
    
    def _calculate_average_complexity(self, complexity_info: List[ComplexityInfo]) -> str:
        """Calculate average complexity across all functions"""
        if not complexity_info:
            return "O(1)"
        
        # Simple complexity scoring for averaging
        complexity_scores = {
            "O(1)": 1,
            "O(log n)": 2,
            "O(n)": 3,
            "O(n log n)": 4,
            "O(n²)": 5,
            "O(2^n)": 6,
            "O(n!)": 7
        }
        
        total_score = sum(complexity_scores.get(comp.complexity, 3) for comp in complexity_info)
        avg_score = total_score / len(complexity_info)
        
        # Map back to complexity
        score_to_complexity = {
            1: "O(1)", 2: "O(log n)", 3: "O(n)", 4: "O(n log n)",
            5: "O(n²)", 6: "O(2^n)", 7: "O(n!)"
        }
        
        return score_to_complexity.get(round(avg_score), "O(n)")


def generate_html_report(analysis: AnalysisResult, output_path: str):
    """Generate HTML report from analysis results"""
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CodeGraph Analysis Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .metric {{ background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 5px; }}
            .warning {{ background: #fff3cd; border: 1px solid #ffeaa7; }}
            .error {{ background: #f8d7da; border: 1px solid #f5c6cb; }}
            .dependency {{ margin: 5px 0; padding: 5px; background: #e9ecef; }}
            .complexity-high {{ color: #dc3545; font-weight: bold; }}
            .complexity-medium {{ color: #ffc107; }}
            .complexity-low {{ color: #28a745; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>CodeGraph Analysis Report</h1>
        
        <div class="metric">
            <h2>Project Metrics</h2>
            <p><strong>Total Files:</strong> {total_files}</p>
            <p><strong>Total Functions:</strong> {total_functions}</p>
            <p><strong>Average Complexity:</strong> {avg_complexity}</p>
            <p><strong>Dependencies:</strong> {dependency_count}</p>
            <p><strong>Circular Dependencies:</strong> {circular_deps}</p>
        </div>
        
        <h2>Complexity Analysis</h2>
        <table>
            <tr><th>Function</th><th>File</th><th>Complexity</th><th>Warning</th></tr>
            {complexity_rows}
        </table>
        
        <h2>Circular Dependencies</h2>
        {cycles_html}
        
        <h2>Dependencies</h2>
        <div>
            {dependencies_html}
        </div>
    </body>
    </html>
    """
    
    # Generate complexity rows
    complexity_rows = ""
    for comp in analysis.complexity:
        css_class = "complexity-low"
        if comp.complexity in ["O(n²)", "O(2^n)", "O(n!)"]:
            css_class = "complexity-high"
        elif comp.complexity in ["O(n)", "O(n log n)"]:
            css_class = "complexity-medium"
        
        complexity_rows += f"""
        <tr class="{css_class}">
            <td>{comp.function}</td>
            <td>{comp.file}</td>
            <td>{comp.complexity}</td>
            <td>{comp.warning or ''}</td>
        </tr>
        """
    
    # Generate cycles HTML
    cycles_html = ""
    for cycle in analysis.cycles:
        css_class = "error" if cycle.severity == "error" else "warning"
        cycles_html += f'<div class="{css_class}">{"→".join(cycle.cycle)}</div>'
    
    if not cycles_html:
        cycles_html = '<div class="metric">No circular dependencies found!</div>'
    
    # Generate dependencies HTML
    dependencies_html = ""
    for dep in analysis.dependencies[:50]:  # Limit to first 50
        dependencies_html += f'<div class="dependency">{dep.source} → {dep.target} ({dep.type})</div>'
    
    # Fill template
    html_content = html_template.format(
        total_files=analysis.metrics.total_files,
        total_functions=analysis.metrics.total_functions,
        avg_complexity=analysis.metrics.average_complexity,
        dependency_count=analysis.metrics.dependency_count,
        circular_deps=analysis.metrics.circular_dependencies,
        complexity_rows=complexity_rows,
        cycles_html=cycles_html,
        dependencies_html=dependencies_html
    )
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='CodeGraph - AST-based code analysis tool')
    parser.add_argument('--analyze', metavar='PATH', help='Analyze project at given path')
    parser.add_argument('--complexity', metavar='PATH', help='Check complexity of specific file')
    parser.add_argument('--check-cycles', metavar='PATH', help='Check for circular dependencies')
    parser.add_argument('--output', metavar='FILE', help='Output file for reports')
    parser.add_argument('--format', choices=['json', 'text', 'html'], default='text', help='Output format')
    parser.add_argument('--exclude', nargs='*', help='Patterns to exclude from analysis')
    
    args = parser.parse_args()
    
    analyzer = CodeGraphAnalyzer()
    
    if args.analyze:
        result = analyzer.analyze_project(args.analyze, args.exclude)
        
        if args.format == 'json':
            output = asdict(result)
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(output, f, indent=2)
            else:
                print(json.dumps(output, indent=2))
        elif args.format == 'html':
            output_file = args.output or 'codegraph-report.html'
            generate_html_report(result, output_file)
            print(f"HTML report generated: {output_file}")
        else:  # text format
            print(f"📊 CodeGraph Analysis Results")
            print(f"Files analyzed: {result.metrics.total_files}")
            print(f"Functions found: {result.metrics.total_functions}")
            print(f"Dependencies: {result.metrics.dependency_count}")
            print(f"Circular dependencies: {result.metrics.circular_dependencies}")
            
            if result.complexity:
                print(f"\n🔍 Complexity Analysis:")
                for comp in result.complexity:
                    status = "⚠️" if comp.warning else "✅"
                    print(f"  {status} {comp.function} ({comp.complexity}) - {comp.file}:{comp.line}")
            
            if result.cycles:
                print(f"\n🔄 Circular Dependencies:")
                for cycle in result.cycles:
                    print(f"  ⚠️ {' → '.join(cycle.cycle)}")
    
    elif args.complexity:
        # Single file complexity check
        parser = analyzer._get_parser(args.complexity)
        if parser:
            result = parser.parse(args.complexity)
            complexity = result['complexity']
            
            if args.format == 'json':
                print(json.dumps({'complexity': complexity}, indent=2))
            else:
                for comp in complexity:
                    print(f"{comp['function']}: {comp['complexity']}")
                    if comp.get('warning'):
                        print(f"  Warning: {comp['warning']}")
        else:
            print(f"No parser available for {args.complexity}")
    
    elif args.check_cycles:
        result = analyzer.analyze_project(args.check_cycles, args.exclude)
        
        if args.format == 'json':
            output = {'cycles': [asdict(cycle) for cycle in result.cycles]}
            print(json.dumps(output, indent=2))
        else:
            if result.cycles:
                print("Circular dependencies found:")
                for cycle in result.cycles:
                    print(f"  {' → '.join(cycle.cycle)} ({cycle.severity})")
            else:
                print("No circular dependencies found!")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
