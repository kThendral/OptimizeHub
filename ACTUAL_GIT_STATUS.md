# Git Commands - Based on Actual Git Status

## ✅ Actual Files to Add (from `git status`)

Run these commands from the **root of OptimizeHub**:

---

## 📦 Modified Files (Already Tracked)

```bash
# Core files we intentionally modified
git add README.md
git add backend/app/config.py
git add frontend/src/App.jsx
git add frontend/src/api.js
git add frontend/src/components/AlgorithmSelector.jsx
git add frontend/src/index.css
git add frontend/tailwind.config.js

# Files modified but may not need committing (check first):
# These were old components - likely just had minor changes
git add frontend/src/components/LandingPage.jsx
git add frontend/src/components/ParameterForm.jsx
git add frontend/src/components/ProblemSelector.jsx
git add frontend/src/components/UploadForm.jsx
```

---

## 🆕 New Files (Untracked)

```bash
# Documentation files
git add CLEANUP_AND_YAML_SUMMARY.md
git add FRONTEND_BACKEND_ANALYSIS.md
git add GIT_ADD_INSTRUCTIONS.md
git add TROUBLESHOOTING.md
git add frontend/COMPONENT_STRUCTURE.md

# Sample YAML files
git add frontend/public/sample_ga.yaml
git add frontend/public/sample_pso.yaml

# New API module
git add frontend/src/api/

# New form components (hybrid architecture)
git add frontend/src/components/forms/

# New styles
git add frontend/src/styles/

# Package lock (Node.js dependency lock file)
git add frontend/package-lock.json
```

---

## 🗑️ Files to IGNORE (Do NOT Add)

```bash
# This was just a backup/reference file - we already integrated changes
# DELETE or ignore it:
rm frontend/src/components/AlgorithmSelector.refactored.jsx

# Or add to .gitignore if you want to keep it locally
```

---

## 🚀 Quick Add All (Recommended)

```bash
# Remove the backup file first
rm frontend/src/components/AlgorithmSelector.refactored.jsx

# Add all modified files
git add README.md
git add backend/app/config.py
git add frontend/src/App.jsx
git add frontend/src/api.js
git add frontend/src/components/AlgorithmSelector.jsx
git add frontend/src/components/LandingPage.jsx
git add frontend/src/components/ParameterForm.jsx
git add frontend/src/components/ProblemSelector.jsx
git add frontend/src/components/UploadForm.jsx
git add frontend/src/index.css
git add frontend/tailwind.config.js

# Add all new files
git add CLEANUP_AND_YAML_SUMMARY.md
git add FRONTEND_BACKEND_ANALYSIS.md
git add GIT_ADD_INSTRUCTIONS.md
git add TROUBLESHOOTING.md
git add frontend/COMPONENT_STRUCTURE.md
git add frontend/public/sample_ga.yaml
git add frontend/public/sample_pso.yaml
git add frontend/src/api/
git add frontend/src/components/forms/
git add frontend/src/styles/
git add frontend/package-lock.json
```

---

## 📋 Even Faster (One Command)

```bash
# Delete backup file
rm frontend/src/components/AlgorithmSelector.refactored.jsx

# Add everything except the backup
git add .

# This adds all modified and untracked files
```

---

## ✅ Verify What You're Committing

```bash
# Check status
git status

# Review changes
git diff --staged

# If something shouldn't be included:
git restore --staged <filename>
```

---

## 💾 Commit Message

```bash
git commit -m "feat: hybrid component architecture with YAML upload support

🎨 Frontend Refactoring:
- Refactored AlgorithmSelector with hybrid architecture
- Created shared ProblemDefinitionForm component
- Created algorithm-specific forms (PSOParametersForm, GAParametersForm)
- Added YAML file upload feature with live preview
- Implemented tab-based UI (Manual Input / YAML Upload)
- Applied Deep Violet color theme (60/30/10 rule)
- Cleaned up App.jsx (removed redundant cards)

🔧 Backend Updates:
- Updated config.py (if changes were made)

🐛 Bug Fixes:
- Fixed API client port issue (5000 → 8000)
- Fixed YAML parser for nested sections
- Fixed browser back button navigation

📚 Documentation:
- Comprehensive README with setup instructions
- Added COMPONENT_STRUCTURE.md (architecture guide)
- Added TROUBLESHOOTING.md (common issues)
- Added FRONTEND_BACKEND_ANALYSIS.md (integration guide)
- Added sample YAML files (sample_pso.yaml, sample_ga.yaml)

✨ New Features:
- YAML configuration upload
- Parameter tooltips and descriptions
- Better error handling and validation
- Beginner-friendly UI with explanations
"
```

---

## 🔍 Differences from Expected

### Extra Modified Files (Not Originally Tracked):
- ✅ `backend/app/config.py` - This is good if you made changes
- ⚠️ `frontend/src/components/LandingPage.jsx` - Review changes
- ⚠️ `frontend/src/components/ParameterForm.jsx` - Old component, may be minor
- ⚠️ `frontend/src/components/ProblemSelector.jsx` - Old component, may be minor
- ⚠️ `frontend/src/components/UploadForm.jsx` - Old component, may be minor
- ✅ `frontend/src/index.css` - Likely theme imports
- ✅ `frontend/tailwind.config.js` - Likely color config

### Extra Untracked File:
- ❌ `frontend/src/components/AlgorithmSelector.refactored.jsx` - **DELETE THIS** (backup file)

### Expected but Not Listed:
All expected files are present! ✅

---

## 🎯 Summary

| Status | Count | Notes |
|--------|-------|-------|
| Modified files to add | 11 | Includes some old components with minor changes |
| New files to add | 10 | All documentation and new components |
| Files to delete | 1 | AlgorithmSelector.refactored.jsx (backup) |
| **Total to commit** | **21** | After deleting backup |

---

## ⚡ Final Commands

```bash
# 1. Delete backup file
rm frontend/src/components/AlgorithmSelector.refactored.jsx

# 2. Add everything
git add .

# 3. Check what's staged
git status

# 4. Commit
git commit -m "feat: hybrid component architecture with YAML upload support

- Refactored frontend with hybrid component architecture
- Added YAML upload feature
- Applied Deep Violet theme
- Fixed API client bugs
- Added comprehensive documentation
"

# 5. Push
git push origin main
```

**You're ready to push! 🚀**
