#!/bin/bash

# 🚀 CodeGraph GitHub Publication Script
# Make CodeGraph public and available to the world!

set -e

echo "🚀 CodeGraph - Making Repository Public!"
echo "========================================="

# Check if we're in the right directory
if [[ ! -f "README.md" ]] || [[ ! -f "engine/codegraph.py" ]]; then
    echo "❌ Error: Please run this script from the CodeGraph root directory"
    exit 1
fi

# Check git status
echo "📋 Checking git status..."
if [[ -n $(git status --porcelain) ]]; then
    echo "❌ Error: Working directory not clean. Please commit all changes first."
    echo "Run: git status"
    exit 1
fi

echo "✅ Working directory is clean"

# Show current repository state
echo ""
echo "📊 Repository Statistics:"
echo "Files: $(find . -name '*.py' -o -name '*.js' -o -name '*.ts' -o -name '*.go' -o -name '*.md' | wc -l | xargs)"
echo "Lines of code: $(find . -name '*.py' -o -name '*.js' -o -name '*.ts' -o -name '*.go' | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}' || echo 'N/A')"
echo "Documentation files: $(find . -name '*.md' | wc -l | xargs)"
echo "Commits: $(git rev-list --count HEAD)"

echo ""
echo "🎯 Next Steps to Make Repository Public:"
echo ""
echo "1. 📱 CREATE GITHUB REPOSITORY"
echo "   - Go to: https://github.com/new"
echo "   - Repository name: CodeGraph"
echo "   - Description: Language-agnostic AST analysis and dependency visualization"
echo "   - Set to PUBLIC ✅"
echo "   - DO NOT initialize with README (we have our own)"
echo ""
echo "2. 🔗 ADD REMOTE AND PUSH"
echo "   After creating the repository, run:"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/CodeGraph.git"
echo "   git branch -M main"
echo "   git push -u origin main --tags"
echo ""
echo "3. 🎉 CONFIGURE GITHUB FEATURES"
echo "   - Enable GitHub Pages (Settings → Pages → Source: Deploy from branch → main /docs)"
echo "   - Enable Issues and Discussions"
echo "   - Add repository topics: ast, code-analysis, dependency-graph, vscode-extension"
echo "   - Set repository description and website URL"
echo ""
echo "4. 🌟 LAUNCH ANNOUNCEMENT"
echo "   - Create first GitHub Release (v1.0.0)"
echo "   - Announce on social media"
echo "   - Submit to developer communities"
echo ""

# Check if GitHub CLI is available
if command -v gh &> /dev/null; then
    echo "🎊 OPTIONAL: GitHub CLI DETECTED!"
    echo ""
    echo "You can create the repository automatically with:"
    echo ""
    echo "gh repo create CodeGraph --public --description 'Language-agnostic AST analysis and dependency visualization for modern development workflows' --homepage 'https://YOUR_USERNAME.github.io/CodeGraph'"
    echo ""
    echo "Then push with:"
    echo "git push -u origin main --tags"
fi

echo ""
echo "🔗 Useful Repository URLs (after creation):"
echo "Repository: https://github.com/YOUR_USERNAME/CodeGraph"
echo "Issues: https://github.com/YOUR_USERNAME/CodeGraph/issues"
echo "Releases: https://github.com/YOUR_USERNAME/CodeGraph/releases"
echo "Pages: https://YOUR_USERNAME.github.io/CodeGraph"

echo ""
echo "🎯 Ready to make CodeGraph public and change the world of code analysis!"
echo "Follow the steps above to complete the launch! 🚀"
