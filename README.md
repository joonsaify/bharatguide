# BharatGuide

**India's digital services guide** — Aadhaar, PAN, DigiLocker, passport, driving license, scholarships and more.

**Live:** https://joonsaify.github.io/bharatguide/

## What It Does

SEO-optimized static site with step-by-step guides for India's most popular digital services. Designed for programmatic SEO targeting high-volume Indian search queries.

## Tech Stack

- **Python** — Static site generator
- **GitHub Pages** — Free hosting and auto-deploy
- **GitHub Actions** — Auto-deploy on push
- **Cron jobs** — Weekly content generation via Hermes Agent

## How to Regenerate

```
python3 build.py              # Regenerate all HTML
git push                      # Deploys to GitHub Pages
```

Or use the auto-generator:

```
python3 scripts/generate_content.py
```

## Monetization

1. **Google AdSense** — Replace YOUR_PUB_ID in style.css and generated HTML
2. **Amazon Affiliate** — Add affiliate links in article content
3. **Local Business Services** — Use lead gen to find Bhopal clients

## Automation

- **Weekly content** (Mon 9AM IST): Generates 6 new articles from templates
- **Lead scraping** (Daily 8AM IST): Finds freelancing opportunities
- **Auto-deploy** on git push via GitHub Pages

Built for APD Travels and Passport Services, Bhopal.
