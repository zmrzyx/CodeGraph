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
