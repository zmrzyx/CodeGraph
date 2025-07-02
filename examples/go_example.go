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
