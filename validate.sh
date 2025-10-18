#!/bin/bash
# Validation script for Meeting Agent implementation

echo "======================================"
echo "Meeting Agent - Validation Script"
echo "======================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track validation status
ALL_PASSED=true

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 exists"
    else
        echo -e "${RED}✗${NC} $1 missing"
        ALL_PASSED=false
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 directory exists"
    else
        echo -e "${RED}✗${NC} $1 directory missing"
        ALL_PASSED=false
    fi
}

echo "1. Checking Project Structure..."
echo "-----------------------------------"
check_dir "backend"
check_dir "backend/services"
check_dir "backend/api"
check_dir "frontend"
check_dir "frontend/src"
check_dir "docs"
check_dir "tests"
echo ""

echo "2. Checking Backend Files..."
echo "-----------------------------------"
check_file "backend/main.py"
check_file "backend/requirements.txt"
check_file "backend/services/__init__.py"
check_file "backend/services/transcription.py"
check_file "backend/services/ai_processor.py"
check_file "backend/services/voice.py"
check_file "backend/api/__init__.py"
check_file "backend/api/routes.py"
echo ""

echo "3. Checking Frontend Files..."
echo "-----------------------------------"
check_file "frontend/main.js"
check_file "frontend/package.json"
check_file "frontend/src/index.html"
check_file "frontend/src/styles.css"
check_file "frontend/src/app.js"
echo ""

echo "4. Checking Configuration Files..."
echo "-----------------------------------"
check_file ".env.example"
check_file ".gitignore"
check_file "package.json"
check_file "Dockerfile"
check_file "docker-compose.yml"
echo ""

echo "5. Checking Documentation..."
echo "-----------------------------------"
check_file "README.md"
check_file "QUICKSTART.md"
check_file "docs/API.md"
check_file "docs/IMPLEMENTATION.md"
check_file "projectoverview.md"
check_file "reference.md"
echo ""

echo "6. Checking Tests..."
echo "-----------------------------------"
check_file "tests/conftest.py"
check_file "tests/requirements.txt"
check_file "tests/test_transcription.py"
check_file "tests/test_ai_processor.py"
check_file "tests/test_voice.py"
echo ""

echo "7. Validating Python Syntax..."
echo "-----------------------------------"
if python -m py_compile backend/main.py backend/services/*.py backend/api/*.py 2>/dev/null; then
    echo -e "${GREEN}✓${NC} All Python files have valid syntax"
else
    echo -e "${RED}✗${NC} Python syntax errors found"
    ALL_PASSED=false
fi
echo ""

echo "8. Validating JavaScript Syntax..."
echo "-----------------------------------"
if node -c frontend/main.js 2>/dev/null && node -c frontend/src/app.js 2>/dev/null; then
    echo -e "${GREEN}✓${NC} All JavaScript files have valid syntax"
else
    echo -e "${RED}✗${NC} JavaScript syntax errors found"
    ALL_PASSED=false
fi
echo ""

echo "9. Checking File Counts..."
echo "-----------------------------------"
PYTHON_FILES=$(find backend -name "*.py" | wc -l)
JS_FILES=$(find frontend -name "*.js" | wc -l)
TEST_FILES=$(find tests -name "test_*.py" | wc -l)

echo "  Python files: $PYTHON_FILES"
echo "  JavaScript files: $JS_FILES"
echo "  Test files: $TEST_FILES"
echo ""

echo "======================================"
echo "Validation Summary"
echo "======================================"
if [ "$ALL_PASSED" = true ]; then
    echo -e "${GREEN}✓ All validations passed!${NC}"
    echo ""
    echo "Implementation is complete and validated."
    echo "Next steps:"
    echo "  1. Add API keys to .env file"
    echo "  2. Run: docker-compose up -d"
    echo "  3. Run: cd frontend && npm install && npm start"
    exit 0
else
    echo -e "${RED}✗ Some validations failed${NC}"
    echo "Please review the errors above."
    exit 1
fi
