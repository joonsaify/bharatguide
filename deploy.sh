#!/bin/bash
# BharatGuide Deployment Script
# Usage: bash deploy.sh

# 1. Generate new content (if any)
python3 scripts/generate_content.py

# 2. Push to GitHub (auto-deploys to GitHub Pages)
git add -A
git commit -m "Auto-update $(date +'%Y-%m-%d %H:%M')" || echo "Nothing to commit"
git push

echo "Deployed at https://joonsaify.github.io/bharatguide/"
