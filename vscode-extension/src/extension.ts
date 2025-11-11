import * as vscode from 'vscode';
import { spawn } from 'child_process';
import * as path from 'path';

export function activate(context: vscode.ExtensionContext) {
    console.log('Coding Assist with Gemini extension is now active!');

    // Command to list files
    let listFilesDisposable = vscode.commands.registerCommand('coding-assist-gemini.listFiles', () => {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showErrorMessage('No workspace folder open');
            return;
        }

        const pythonPath = getPythonPath();
        const scriptPath = path.join(context.extensionPath, '..', 'api_wrapper.py');

        const process = spawn(pythonPath, [scriptPath, 'list_files'], {
            cwd: workspaceFolders[0].uri.fsPath
        });

        let output = '';
        process.stdout.on('data', (data) => {
            output += data.toString();
        });

        process.on('close', (code) => {
            if (code === 0) {
                vscode.window.showInformationMessage(output);
            } else {
                vscode.window.showErrorMessage(`Error listing files: ${output}`);
            }
        });
    });

    // Command to read file
    let readFileDisposable = vscode.commands.registerCommand('coding-assist-gemini.readFile', (uri: vscode.Uri) => {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showErrorMessage('No workspace folder open');
            return;
        }

        const filePath = path.relative(workspaceFolders[0].uri.fsPath, uri.fsPath);
        const pythonPath = getPythonPath();
        const scriptPath = path.join(context.extensionPath, '..', 'api_wrapper.py');

        const process = spawn(pythonPath, [scriptPath, 'read_file', filePath], {
            cwd: workspaceFolders[0].uri.fsPath
        });

        let output = '';
        process.stdout.on('data', (data) => {
            output += data.toString();
        });

        process.on('close', (code) => {
            if (code === 0) {
                const panel = vscode.window.createWebviewPanel(
                    'fileContent',
                    `Content of ${filePath}`,
                    vscode.ViewColumn.One,
                    {}
                );
                panel.webview.html = getWebviewContent(output);
            } else {
                vscode.window.showErrorMessage(`Error reading file: ${output}`);
            }
        });
    });

    // Command to ask AI
    let askAIDisposable = vscode.commands.registerCommand('coding-assist-gemini.askAI', async () => {
        const question = await vscode.window.showInputBox({
            prompt: 'Ask the AI a question'
        });

        if (question) {
            const workspaceFolders = vscode.workspace.workspaceFolders;
            if (!workspaceFolders) {
                vscode.window.showErrorMessage('No workspace folder open');
                return;
            }

            const pythonPath = getPythonPath();
            const scriptPath = path.join(context.extensionPath, '..', 'api_wrapper.py');

            const process = spawn(pythonPath, [scriptPath, 'ask_ai', question], {
                cwd: workspaceFolders[0].uri.fsPath
            });

            let output = '';
            process.stdout.on('data', (data) => {
                output += data.toString();
            });

            process.on('close', (code) => {
                if (code === 0) {
                    const panel = vscode.window.createWebviewPanel(
                        'aiResponse',
                        'AI Response',
                        vscode.ViewColumn.One,
                        {}
                    );
                    panel.webview.html = getWebviewContent(output);
                } else {
                    vscode.window.showErrorMessage(`Error asking AI: ${output}`);
                }
            });
        }
    });

    // Command to analyze code complexity
    let analyzeCodeDisposable = vscode.commands.registerCommand('coding-assist-gemini.analyzeCode', (uri: vscode.Uri) => {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showErrorMessage('No workspace folder open');
            return;
        }

        const filePath = path.relative(workspaceFolders[0].uri.fsPath, uri.fsPath);
        const pythonPath = getPythonPath();
        const scriptPath = path.join(context.extensionPath, '..', 'api_wrapper.py');

        const process = spawn(pythonPath, [scriptPath, 'analyze_complexity', filePath], {
            cwd: workspaceFolders[0].uri.fsPath
        });

        let output = '';
        process.stdout.on('data', (data) => {
            output += data.toString();
        });

        process.on('close', (code) => {
            if (code === 0) {
                const panel = vscode.window.createWebviewPanel(
                    'complexityAnalysis',
                    `Complexity Analysis of ${filePath}`,
                    vscode.ViewColumn.One,
                    {}
                );
                panel.webview.html = getWebviewContent(output);
            } else {
                vscode.window.showErrorMessage(`Error analyzing code: ${output}`);
            }
        });
    });

    // Command to find duplicates
    let findDuplicatesDisposable = vscode.commands.registerCommand('coding-assist-gemini.findDuplicates', (uri: vscode.Uri) => {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showErrorMessage('No workspace folder open');
            return;
        }

        const filePath = path.relative(workspaceFolders[0].uri.fsPath, uri.fsPath);
        const pythonPath = getPythonPath();
        const scriptPath = path.join(context.extensionPath, '..', 'api_wrapper.py');

        const process = spawn(pythonPath, [scriptPath, 'find_duplicates', filePath], {
            cwd: workspaceFolders[0].uri.fsPath
        });

        let output = '';
        process.stdout.on('data', (data) => {
            output += data.toString();
        });

        process.on('close', (code) => {
            if (code === 0) {
                const panel = vscode.window.createWebviewPanel(
                    'duplicateCode',
                    `Duplicate Code in ${filePath}`,
                    vscode.ViewColumn.One,
                    {}
                );
                panel.webview.html = getWebviewContent(output);
            } else {
                vscode.window.showErrorMessage(`Error finding duplicates: ${output}`);
            }
        });
    });

    context.subscriptions.push(listFilesDisposable);
    context.subscriptions.push(readFileDisposable);
    context.subscriptions.push(askAIDisposable);
    context.subscriptions.push(analyzeCodeDisposable);
    context.subscriptions.push(findDuplicatesDisposable);
}

function getPythonPath(): string {
    const config = vscode.workspace.getConfiguration('python');
    return config.get('pythonPath', 'python');
}

function getWebviewContent(content: string): string {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Content</title>
</head>
<body>
    <pre>${content}</pre>
</body>
</html>`;
}

export function deactivate() {}