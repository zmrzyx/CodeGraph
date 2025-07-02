/**
 * CodeGraph Configuration
 * Language-agnostic project configuration for code analysis
 */
module.exports = {
    // Analysis settings
    analysis: {
        maxComplexity: "O(n log n)",
        checkCycles: true,
        enforceArchitecture: true,
        generateTests: false,
        realTimeAnalysis: true
    },

    // Language-specific settings
    languages: {
        go: {
            parser: "go_parser",
            includes: ["**/*.go"],
            excludes: ["**/vendor/**", "**/node_modules/**"],
            complexity: {
                maxLoops: 2,
                maxNesting: 3,
                warnOnRecursion: true
            }
        },
        python: {
            parser: "python_parser",
            includes: ["**/*.py"],
            excludes: ["**/venv/**", "**/__pycache__/**", "**/site-packages/**"],
            complexity: {
                maxLoops: 2,
                maxNesting: 3,
                warnOnRecursion: true
            }
        },
        javascript: {
            parser: "javascript_parser",
            includes: ["**/*.js", "**/*.ts", "**/*.jsx", "**/*.tsx"],
            excludes: ["**/node_modules/**", "**/dist/**", "**/build/**"],
            complexity: {
                maxLoops: 2,
                maxNesting: 3,
                warnOnRecursion: true
            }
        },
        typescript: {
            parser: "javascript_parser", // Reuse JS parser for now
            includes: ["**/*.ts", "**/*.tsx"],
            excludes: ["**/node_modules/**", "**/dist/**", "**/build/**"],
            complexity: {
                maxLoops: 2,
                maxNesting: 3,
                warnOnRecursion: true
            }
        }
    },

    // Visualization options  
    visualization: {
        layout: "hierarchical", // "hierarchical", "force", "circular"
        showTypes: true,
        highlightCycles: true,
        maxNodes: 500,
        groupByModule: true,
        colorScheme: "default" // "default", "dark", "colorblind"
    },

    // Output settings
    output: {
        format: "html", // "html", "json", "svg", "png"
        includeSourceCode: false,
        includeMetrics: true,
        generateSummary: true,
        verbose: false
    },

    // CI/CD integration
    ci: {
        failOnCycles: true,
        failOnComplexity: true,
        failOnArchitectureViolation: false,
        generateReports: true,
        outputFormat: "json",
        reportPath: "./codegraph-report.json"
    },

    // Architecture rules (optional)
    architecture: {
        layers: [
            {
                name: "presentation",
                patterns: ["**/ui/**", "**/components/**", "**/pages/**"],
                canDependOn: ["business", "data"]
            },
            {
                name: "business",
                patterns: ["**/services/**", "**/domain/**", "**/logic/**"],
                canDependOn: ["data"]
            },
            {
                name: "data",
                patterns: ["**/repositories/**", "**/models/**", "**/db/**"],
                canDependOn: []
            }
        ],
        rules: [
            {
                name: "no-cross-layer-dependencies",
                description: "Layers should only depend on lower layers",
                enforce: true
            },
            {
                name: "no-circular-dependencies",
                description: "No circular dependencies allowed",
                enforce: true
            }
        ]
    },

    // Performance settings
    performance: {
        maxFileSize: "10MB",
        maxAnalysisTime: 300, // seconds
        parallelProcessing: true,
        cacheResults: true,
        cacheLocation: "./.codegraph-cache"
    },

    // Custom parsers (for extending language support)
    customParsers: {
        // Example custom parser configuration
        // rust: {
        //   command: "rust-analyzer",
        //   args: ["--analyze", "{file}"],
        //   outputFormat: "json"
        // }
    },

    // Plugin system (for future extensibility)
    plugins: [
        // "codegraph-security-plugin",
        // "codegraph-performance-plugin",
        // "codegraph-documentation-plugin"
    ]
};
