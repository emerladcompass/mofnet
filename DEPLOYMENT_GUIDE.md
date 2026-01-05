# PyPI Deployment Guide

## Prerequisites
1. PyPI account: https://pypi.org/account/register/
2. Configure trusted publishing on PyPI:
   - Go to: https://pypi.org/manage/account/publishing/
   - Add GitHub repository: `emerladcompass/medical-mof-prediction`
   - Environment: `pypi`

## Creating a Release
1. Update version in `setup.py` and `src/__init__.py`
2. Create a new GitHub Release:
   - Tag: `v1.0.0` (matching setup.py version)
   - Title: `Version 1.0.0`
   - Description: Release notes

## Automated Process
The `.github/workflows/python-publish.yml` will:
1. Trigger on new release creation
2. Build source and wheel distributions
3. Publish to PyPI automatically

## Manual Publishing (if needed)
\`\`\`bash
# Install build tools
pip install build twine

# Build packages
python -m build

# Upload to PyPI
twine upload dist/*
\`\`\`

## Testing Installation
\`\`\`bash
# Test from PyPI
pip install medical-mof-prediction

# Test from local build
pip install dist/medical_mof_prediction-*.whl
\`\`\`

## Troubleshooting
- Ensure version numbers match in all files
- Check PyPI trusted publishing configuration
- Verify GitHub Actions permissions
