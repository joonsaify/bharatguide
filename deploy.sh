#!/bin/bash
# BharatGuide - Quick Deploy Script
# Usage: ./deploy.sh [surge|vercel]

set -e

SITE_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ "$1" = "surge" ]; then
  echo "Deploying to Surge.sh..."
  echo "Need an email first time. Get started at: https://surge.sh"
  cd "$SITE_DIR"
  npx surge ./ bharatguide.surge.sh
  echo "✅ Deployed to https://bharatguide.surge.sh"

elif [ "$1" = "vercel" ] || [ -z "$1" ]; then
  echo "Deploying to Vercel..."
  echo "Create free account at: https://vercel.com/signup"
  cd "$SITE_DIR"
  npx vercel --prod
  echo "✅ Deployed!"

elif [ "$1" = "github" ]; then
  echo "Deploying to GitHub Pages..."
  echo "Need a GitHub account. Create at: https://github.com/signup"
  cd "$SITE_DIR"
  git init
  git add -A
  git commit -m "Initial BharatGuide site"
  echo "Now: create a repo on GitHub and run:"
  echo "  git remote add origin https://github.com/YOUR_USER/bharatguide.git"
  echo "  git push -u origin main"
  echo '\''  Then enable Pages: Settings → Pages → Deploy from main branch /docs folder'\''
  echo "Or push to gh-pages branch directly"

elif [ "$1" = "generate" ]; then
  cd "$SITE_DIR"
  python3 build.py
  echo "✅ Site regenerated from content.json"

else
  echo "Usage: ./deploy.sh [surge|vercel|github|generate]"
  echo "  surge   - Deploy to Surge.sh (free, simple)"
  echo "  vercel  - Deploy to Vercel (free, recommended)"
  echo "  github  - Deploy to GitHub Pages (free)"
  echo "  generate- Rebuild site from content.json"
fi

