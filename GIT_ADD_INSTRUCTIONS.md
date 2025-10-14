# Git Add Commands - New and Modified Files

## 📋 Files to Add to Git

Run these commands from the **root of the OptimizeHub repository**:

---

## ✅ New Frontend Files (Created Today)

```bash
# API client module
git add frontend/src/api/index.js

# Form components (hybrid architecture)
git add frontend/src/components/forms/ProblemDefinitionForm.jsx
git add frontend/src/components/forms/PSOParametersForm.jsx
git add frontend/src/components/forms/GAParametersForm.jsx

# Sample YAML configuration files
git add frontend/public/sample_pso.yaml
git add frontend/public/sample_ga.yaml

# Theme CSS
git add frontend/src/styles/theme.css
```

---

## 🔄 Modified Files

```bash
# Main application component (cleaned up)
git add frontend/src/App.jsx

# Algorithm selector (refactored with YAML upload)
git add frontend/src/components/AlgorithmSelector.jsx

# Old API file (updated to redirect)
git add frontend/src/api.js

# Backend genetic algorithm (if modified)
git add backend/app/algorithms/genetic_algorithm.py
```

---

## 📚 Documentation Files

```bash
# Main README
git add README.md

# Architecture and troubleshooting docs
git add frontend/COMPONENT_STRUCTURE.md
git add CLEANUP_AND_YAML_SUMMARY.md
git add TROUBLESHOOTING.md

# If these exist, add them too
git add FRONTEND_BACKEND_ANALYSIS.md
```

---

## 🚀 Quick Commands

### Option 1: Add All New/Modified Files at Once
```bash
# Stage all changes (be careful with this!)
git add .

# OR be more selective:
git add frontend/src/api/
git add frontend/src/components/forms/
git add frontend/public/sample*.yaml
git add frontend/src/styles/theme.css
git add frontend/src/App.jsx
git add frontend/src/components/AlgorithmSelector.jsx
git add *.md
```

### Option 2: Interactive Add (Recommended)
```bash
# Review changes file by file
git add -p
```

### Check What's Staged
```bash
git status
```

---

## 📝 Complete File List

### New Files (Not in Git Yet)
```
frontend/src/api/index.js
frontend/src/components/forms/ProblemDefinitionForm.jsx
frontend/src/components/forms/PSOParametersForm.jsx
frontend/src/components/forms/GAParametersForm.jsx
frontend/public/sample_pso.yaml
frontend/public/sample_ga.yaml
frontend/src/styles/theme.css
frontend/COMPONENT_STRUCTURE.md
CLEANUP_AND_YAML_SUMMARY.md
TROUBLESHOOTING.md
FRONTEND_BACKEND_ANALYSIS.md (if exists)
```

### Modified Files
```
README.md
frontend/src/App.jsx
frontend/src/components/AlgorithmSelector.jsx
frontend/src/api.js
backend/app/algorithms/genetic_algorithm.py (possibly)
```

### Files Created But Not Needed (Can Delete)
```
frontend/src/components/AlgorithmSelector.refactored.jsx  # This was a backup
```

---

## 🗑️ Optional: Clean Up Backup File

```bash
# Remove the refactored backup file (we already applied changes)
rm frontend/src/components/AlgorithmSelector.refactored.jsx
```

---

## 💾 Commit and Push

### After adding all files:

```bash
# Commit with descriptive message
git commit -m "feat: hybrid component architecture with YAML upload support

- Refactored AlgorithmSelector with shared + algorithm-specific forms
- Added YAML configuration file upload feature
- Created ProblemDefinitionForm (shared across all algorithms)
- Created PSOParametersForm and GAParametersForm (algorithm-specific)
- Added sample YAML files (sample_pso.yaml, sample_ga.yaml)
- Implemented Deep Violet color theme
- Fixed API client to use correct port (8000)
- Updated README with comprehensive setup instructions
- Added documentation: COMPONENT_STRUCTURE.md, TROUBLESHOOTING.md
- Cleaned up App.jsx (removed redundant cards)
"

# Push to GitHub
git push origin main
```

---

## 🔍 Verify Before Committing

### Check staged files:
```bash
git status
```

### Review changes:
```bash
git diff --staged
```

### Make sure backend is working:
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# Visit http://localhost:8000/docs
```

### Make sure frontend is working:
```bash
cd frontend
npm run dev
# Visit http://localhost:5173
```

---

## 📊 Summary of Changes

| Category | New Files | Modified Files |
|----------|-----------|----------------|
| **Frontend Components** | 4 | 2 |
| **API Client** | 1 | 1 |
| **YAML Samples** | 2 | 0 |
| **Styles** | 1 | 0 |
| **Documentation** | 4 | 1 |
| **Backend** | 0 | 1? |
| **Total** | **12** | **5** |

---

## ✨ What's New in This Commit

1. **Hybrid Component Architecture**
   - Shared problem definition form
   - Algorithm-specific parameter forms
   - Conditional rendering based on selection

2. **YAML Upload Feature**
   - Tab-based UI (Manual Input / YAML Upload)
   - File upload with live preview
   - Sample configuration files

3. **UI/UX Improvements**
   - Deep Violet color theme (60/30/10 rule)
   - Cleaner single-card layout
   - Parameter tooltips and descriptions

4. **Bug Fixes**
   - Fixed API client port issue (5000 → 8000)
   - Fixed YAML parser for nested sections
   - Fixed browser back button navigation

5. **Documentation**
   - Comprehensive README with setup instructions
   - Component architecture documentation
   - Troubleshooting guide

---

**Ready to commit!** 🚀
