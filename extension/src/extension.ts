import { exec } from 'child_process';
import * as path from 'path';
import * as vscode from 'vscode';

/**
 * CodeGraph VS Code Extension
 * Provides AST-based code analysis and dependency visualization
 */

interface AnalysisResult {
    dependencies: DependencyInfo[];
    complexity: ComplexityInfo[];
    cycles: CircularDependency[];
    metrics: ProjectMetrics;
}

interface DependencyInfo {
    source: string;
    target: string;
    type: 'import' | 'function_call' | 'inheritance' | 'composition';
    line: number;
    column: number;
}

interface ComplexityInfo {
    function: string;
    file: string;
    complexity: string;
    line: number;
    warning?: string;
}

interface CircularDependency {
    cycle: string[];
    severity: 'warning' | 'error';
}

interface ProjectMetrics {
    totalFiles: number;
    totalFunctions: number;
    averageComplexity: string;
    dependencyCount: number;
    circularDependencies: number;
}

class CodeGraphProvider implements vscode.TreeDataProvider<CodeGraphItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<CodeGraphItem | undefined | null | void> = new vscode.EventEmitter<CodeGraphItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<CodeGraphItem | undefined | null | void> = this._onDidChangeTreeData.event;

    private analysisResult: AnalysisResult | null = null;

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    updateAnalysis(result: AnalysisResult): void {
        this.analysisResult = result;
        this.refresh();
    }

    getTreeItem(element: CodeGraphItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: CodeGraphItem): Thenable<CodeGraphItem[]> {
        if (!this.analysisResult) {
            return Promise.resolve([]);
        }

        if (!element) {
            // Root level items
            return Promise.resolve([
                new CodeGraphItem('Dependencies', vscode.TreeItemCollapsibleState.Collapsed, 'dependencies'),
                new CodeGraphItem('Complexity', vscode.TreeItemCollapsibleState.Collapsed, 'complexity'),
                new CodeGraphItem('Circular Dependencies', vscode.TreeItemCollapsibleState.Collapsed, 'cycles'),
                new CodeGraphItem('Metrics', vscode.TreeItemCollapsibleState.Collapsed, 'metrics')
            ]);
        }

        switch (element.contextValue) {
            case 'dependencies':
                return Promise.resolve(
                    this.analysisResult.dependencies.map(dep =>
                        new CodeGraphItem(
                            `${dep.source} → ${dep.target}`,
                            vscode.TreeItemCollapsibleState.None,
                            'dependency',
                            {
                                command: 'vscode.open',
                                title: 'Open File',
                                arguments: [vscode.Uri.file(dep.source), { selection: new vscode.Range(dep.line, dep.column, dep.line, dep.column) }]
                            }
                        )
                    )
                );

            case 'complexity':
                return Promise.resolve(
                    this.analysisResult.complexity.map(complex =>
                        new CodeGraphItem(
                            `${complex.function} (${complex.complexity})`,
                            vscode.TreeItemCollapsibleState.None,
                            'complexity-item',
                            {
                                command: 'vscode.open',
                                title: 'Open Function',
                                arguments: [vscode.Uri.file(complex.file), { selection: new vscode.Range(complex.line, 0, complex.line, 0) }]
                            }
                        )
                    )
                );

            case 'cycles':
                return Promise.resolve(
                    this.analysisResult.cycles.map(cycle =>
                        new CodeGraphItem(
                            cycle.cycle.join(' → '),
                            vscode.TreeItemCollapsibleState.None,
                            'cycle'
                        )
                    )
                );

            case 'metrics':
                const metrics = this.analysisResult.metrics;
                return Promise.resolve([
                    new CodeGraphItem(`Total Files: ${metrics.totalFiles}`, vscode.TreeItemCollapsibleState.None, 'metric'),
                    new CodeGraphItem(`Total Functions: ${metrics.totalFunctions}`, vscode.TreeItemCollapsibleState.None, 'metric'),
                    new CodeGraphItem(`Average Complexity: ${metrics.averageComplexity}`, vscode.TreeItemCollapsibleState.None, 'metric'),
                    new CodeGraphItem(`Dependencies: ${metrics.dependencyCount}`, vscode.TreeItemCollapsibleState.None, 'metric'),
                    new CodeGraphItem(`Circular Dependencies: ${metrics.circularDependencies}`, vscode.TreeItemCollapsibleState.None, 'metric')
                ]);

            default:
                return Promise.resolve([]);
        }
    }
}

class CodeGraphItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly contextValue: string,
        public readonly command?: vscode.Command
    ) {
        super(label, collapsibleState);
        this.tooltip = this.label;
    }
}

class CodeGraphEngine {
    private pythonPath: string;
    private enginePath: string;

    constructor(context: vscode.ExtensionContext) {
        const config = vscode.workspace.getConfiguration('codegraph');
        this.pythonPath = config.get('pythonPath', 'python');
        this.enginePath = config.get('enginePath', '');

        if (!this.enginePath) {
            // Default to engine directory relative to extension
            this.enginePath = path.join(context.extensionPath, '..', 'engine', 'codegraph.py');
        }
    }

    async analyzeProject(projectPath: string): Promise<AnalysisResult> {
        return new Promise((resolve, reject) => {
            const command = `${this.pythonPath} "${this.enginePath}" --analyze "${projectPath}" --format json`;

            exec(command, { cwd: projectPath }, (error, stdout, stderr) => {
                if (error) {
                    reject(new Error(`Analysis failed: ${error.message}`));
                    return;
                }

                if (stderr) {
                    console.log(`Analysis warnings: ${stderr}`);
                }

                try {
                    const result = JSON.parse(stdout);
                    resolve(result);
                } catch (parseError) {
                    reject(new Error(`Failed to parse analysis result: ${parseError}`));
                }
            });
        });
    }

    async checkComplexity(filePath: string): Promise<ComplexityInfo[]> {
        return new Promise((resolve, reject) => {
            const command = `${this.pythonPath} "${this.enginePath}" --complexity "${filePath}" --format json`;

            exec(command, (error, stdout, stderr) => {
                if (error) {
                    reject(new Error(`Complexity check failed: ${error.message}`));
                    return;
                }

                try {
                    const result = JSON.parse(stdout);
                    resolve(result.complexity || []);
                } catch (parseError) {
                    reject(new Error(`Failed to parse complexity result: ${parseError}`));
                }
            });
        });
    }

    async detectCycles(projectPath: string): Promise<CircularDependency[]> {
        return new Promise((resolve, reject) => {
            const command = `${this.pythonPath} "${this.enginePath}" --check-cycles "${projectPath}" --format json`;

            exec(command, { cwd: projectPath }, (error, stdout, stderr) => {
                if (error) {
                    reject(new Error(`Cycle detection failed: ${error.message}`));
                    return;
                }

                try {
                    const result = JSON.parse(stdout);
                    resolve(result.cycles || []);
                } catch (parseError) {
                    reject(new Error(`Failed to parse cycle detection result: ${parseError}`));
                }
            });
        });
    }

    async generateReport(projectPath: string, outputPath: string): Promise<void> {
        return new Promise((resolve, reject) => {
            const command = `${this.pythonPath} "${this.enginePath}" --analyze "${projectPath}" --output "${outputPath}" --format html`;

            exec(command, { cwd: projectPath }, (error, stdout, stderr) => {
                if (error) {
                    reject(new Error(`Report generation failed: ${error.message}`));
                    return;
                }

                resolve();
            });
        });
    }
}

// Global variables
let codeGraphProvider: CodeGraphProvider;
let codeGraphEngine: CodeGraphEngine;

export function activate(context: vscode.ExtensionContext) {
    console.log('CodeGraph extension is now active');

    // Initialize providers and engine
    codeGraphProvider = new CodeGraphProvider();
    codeGraphEngine = new CodeGraphEngine(context);

    // Register tree data providers
    vscode.window.createTreeView('codegraphDependencies', {
        treeDataProvider: codeGraphProvider
    });

    // Register commands
    const analyzeProjectCommand = vscode.commands.registerCommand('codegraph.analyzeProject', async () => {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showErrorMessage('No workspace folder open');
            return;
        }

        const projectPath = workspaceFolders[0].uri.fsPath;

        try {
            vscode.window.showInformationMessage('Analyzing project with CodeGraph...');
            const result = await codeGraphEngine.analyzeProject(projectPath);
            codeGraphProvider.updateAnalysis(result);

            vscode.window.showInformationMessage(
                `Analysis complete: ${result.metrics.totalFiles} files, ${result.metrics.dependencyCount} dependencies, ${result.metrics.circularDependencies} cycles`
            );
        } catch (error) {
            vscode.window.showErrorMessage(`Analysis failed: ${error}`);
        }
    });

    const showDependencyGraphCommand = vscode.commands.registerCommand('codegraph.showDependencyGraph', async () => {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showErrorMessage('No workspace folder open');
            return;
        }

        const projectPath = workspaceFolders[0].uri.fsPath;
        const outputPath = path.join(projectPath, 'codegraph-report.html');

        try {
            await codeGraphEngine.generateReport(projectPath, outputPath);

            // Open the generated HTML report
            const uri = vscode.Uri.file(outputPath);
            await vscode.env.openExternal(uri);
        } catch (error) {
            vscode.window.showErrorMessage(`Failed to generate dependency graph: ${error}`);
        }
    });

    const checkComplexityCommand = vscode.commands.registerCommand('codegraph.checkComplexity', async () => {
        const activeEditor = vscode.window.activeTextEditor;
        if (!activeEditor) {
            vscode.window.showErrorMessage('No active file');
            return;
        }

        const filePath = activeEditor.document.fileName;

        try {
            const complexity = await codeGraphEngine.checkComplexity(filePath);

            if (complexity.length === 0) {
                vscode.window.showInformationMessage('No complexity issues found');
                return;
            }

            // Show complexity results
            const items = complexity.map(c => `${c.function}: ${c.complexity}${c.warning ? ` (${c.warning})` : ''}`);
            const selected = await vscode.window.showQuickPick(items, {
                placeHolder: 'Select function to navigate to'
            });

            if (selected) {
                const selectedIndex = items.indexOf(selected);
                const complexityInfo = complexity[selectedIndex];

                const position = new vscode.Position(complexityInfo.line, 0);
                activeEditor.selection = new vscode.Selection(position, position);
                activeEditor.revealRange(new vscode.Range(position, position));
            }
        } catch (error) {
            vscode.window.showErrorMessage(`Complexity check failed: ${error}`);
        }
    });

    const detectCyclesCommand = vscode.commands.registerCommand('codegraph.detectCycles', async () => {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showErrorMessage('No workspace folder open');
            return;
        }

        const projectPath = workspaceFolders[0].uri.fsPath;

        try {
            const cycles = await codeGraphEngine.detectCycles(projectPath);

            if (cycles.length === 0) {
                vscode.window.showInformationMessage('No circular dependencies found');
                return;
            }

            // Show cycles
            const cycleStrings = cycles.map(c => c.cycle.join(' → '));
            await vscode.window.showQuickPick(cycleStrings, {
                placeHolder: `Found ${cycles.length} circular dependencies`
            });
        } catch (error) {
            vscode.window.showErrorMessage(`Cycle detection failed: ${error}`);
        }
    });

    const validateArchitectureCommand = vscode.commands.registerCommand('codegraph.validateArchitecture', async () => {
        vscode.window.showInformationMessage('Architecture validation coming soon!');
    });

    const generateReportCommand = vscode.commands.registerCommand('codegraph.generateReport', async () => {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showErrorMessage('No workspace folder open');
            return;
        }

        const projectPath = workspaceFolders[0].uri.fsPath;
        const outputPath = await vscode.window.showSaveDialog({
            defaultUri: vscode.Uri.file(path.join(projectPath, 'codegraph-report.html')),
            filters: {
                'HTML Files': ['html'],
                'JSON Files': ['json']
            }
        });

        if (!outputPath) {
            return;
        }

        try {
            await codeGraphEngine.generateReport(projectPath, outputPath.fsPath);
            vscode.window.showInformationMessage(`Report generated: ${outputPath.fsPath}`);

            // Ask if user wants to open the report
            const openReport = await vscode.window.showInformationMessage(
                'Report generated successfully!',
                'Open Report'
            );

            if (openReport === 'Open Report') {
                await vscode.env.openExternal(outputPath);
            }
        } catch (error) {
            vscode.window.showErrorMessage(`Report generation failed: ${error}`);
        }
    });

    // Register all commands
    context.subscriptions.push(
        analyzeProjectCommand,
        showDependencyGraphCommand,
        checkComplexityCommand,
        detectCyclesCommand,
        validateArchitectureCommand,
        generateReportCommand
    );

    // Auto-analyze on startup if enabled
    const config = vscode.workspace.getConfiguration('codegraph');
    if (config.get('enableRealTimeAnalysis', true)) {
        vscode.commands.executeCommand('codegraph.analyzeProject');
    }

    // Set up file watchers for real-time analysis
    const fileWatcher = vscode.workspace.createFileSystemWatcher('**/*.{go,py,js,ts}');

    fileWatcher.onDidChange(() => {
        if (config.get('enableRealTimeAnalysis', true)) {
            // Debounce the analysis
            setTimeout(() => {
                vscode.commands.executeCommand('codegraph.analyzeProject');
            }, 1000);
        }
    });

    context.subscriptions.push(fileWatcher);

    // Show welcome message
    vscode.window.showInformationMessage('CodeGraph is ready! Use Ctrl+Shift+P and search for "CodeGraph" to get started.');
}

export function deactivate() {
    console.log('CodeGraph extension is now deactivated');
}
