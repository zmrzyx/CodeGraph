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
