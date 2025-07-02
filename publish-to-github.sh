#!/bin/bash
# 🚀 CodeGraph GitHub Publication Script
# Run this after creating your GitHub repository

echo "🚀 CodeGraph GitHub Publication Script"
echo "======================================="

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -f "engine/codegraph.py" ]; then
    echo "❌ Error: Please run this script from the CodeGraph root directory"
    exit 1
fi

echo "📍 Current directory: $(pwd)"
echo "📋 Files in directory:"
ls -la

echo ""
echo "🔧 Pre-flight checks..."

# Check git status
echo "📊 Git status:"
git status

echo ""
echo "📦 Ready to connect to GitHub!"
echo ""
echo "⚠️  NEXT STEPS:"
echo "1. Create a new repository on GitHub.com:"
echo "   - Repository name: CodeGraph"
echo "   - Description: Language-agnostic AST analysis and dependency visualization"
echo "   - Visibility: Public"
echo "   - Don't initialize with README, .gitignore, or license"
echo ""
echo "2. After creating the repository, run these commands:"
echo ""
echo "   # Replace YOUR_USERNAME with your actual GitHub username"
echo "   git remote add origin https://github.com/YOUR_USERNAME/CodeGraph.git"
echo ""
echo "   # Push all commits and tags"
echo "   git push -u origin master"
echo "   git push origin --tags"
echo ""
echo "3. Verify the push worked:"
echo "   git remote -v"
echo ""
echo "🎉 Your repository will then be live at:"
echo "   https://github.com/YOUR_USERNAME/CodeGraph"
echo ""

# Show what will be published
echo "📦 What will be published:"
echo "✅ $(git rev-list --count HEAD) commits"
echo "✅ $(git tag | wc -l | tr -d ' ') tags"
echo "✅ $(find . -name "*.py" -o -name "*.js" -o -name "*.go" -o -name "*.md" | wc -l | tr -d ' ') source files"
echo "✅ Complete documentation suite"
echo "✅ Working examples and tests"
echo "✅ VS Code extension package"
echo ""

echo "🎯 Ready for launch! Create your GitHub repository and run the commands above."
