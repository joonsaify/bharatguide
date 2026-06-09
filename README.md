# BharatGuide 🇮🇳

Your complete guide to India's digital services — Aadhaar, PAN, DigiLocker, government schemes, driving license, passports and more.

## Quick Start

```bash
# Build/rebuild the site
python3 build.py

# Deploy to web (choose one)
./deploy.sh vercel    # Free — recommended
./deploy.sh surge     # Free — simplest
./deploy.sh github    # Free — GitHub Pages
```

## Monetization Roadmap

### Phase 1: Traffic (Immediate — Set Up Now)
1. **Google AdSense** — Replace `ca-pub-YOUR_PUB_ID` in `index.html` with your actual AdSense Publisher ID
   - Sign up: https://adsense.google.com
   - Wait for approval (typically 1-2 weeks)
   - Once approved, ads will appear on the site

2. **Submit to Google Search Console** — https://search.google.com/search-console
   - Add your domain (bharatguide.vercel.app or your surge domain)
   - Submit sitemap: `https://yourdomain.com/sitemap.xml`
   - This gets Google to index your articles

3. **Share on Social Media**
   - Post article links to WhatsApp (especially Bhopal/MP groups)
   - Share on LinkedIn, Twitter/X, Facebook groups
   - Post in Indian subreddits (r/India, r/Bhopal)

### Phase 2: Growth (Month 1-3)
4. **Automated Content Generation** — Already set up!
   - Weekly cron job runs every Monday 9 AM IST — adds 6 new articles
   - Site grows from 14 → ~90+ articles in 3 months
   - More pages = more search traffic = more ad revenue

5. **Affiliate Marketing** — Add affiliate links in articles
   - Amazon India Affiliate: https://affiliate-program.amazon.in
   - Products to promote: laptops, tablets, printers, webcams
   - Add links naturally in tech/utility articles
   - Example: "You'll need a printer for the form — check prices on Amazon"

6. **Local Bhopal SEO**
   - Add articles targeting Bhopal specifically (already have 2!)
   - "Best xerox shop near Bhopal RTO", "How to reach Bhopal PSK"
   - Local keywords have almost zero competition

### Phase 3: Revenue (Month 3-6)
7. **AdSense RPM Targets**
   - Education/government utility content: $2-5 RPM
   - With 10,000 monthly visitors → $20-50/month
   - With 100,000 monthly visitors → $200-500/month
   - Scale up to 500+ articles = significant passive income

8. **Client Ops** — Sell AI automation services to local Bhopal businesses
   - Show them BharatGuide as proof of your work
   - "I can build you a website like this that ranks on Google"
   - Charge ₹5,000-15,000/month per client
   - Use Hermes to do 90% of the work

## Project Structure

```
bharatguide/
├── build.py              # Site builder — reads content.json, outputs HTML
├── content.json          # All articles + site config
├── deploy.sh             # Deployment helper
├── index.html            # Homepage (auto-generated)
├── css/style.css         # Styles
├── articles/             # Article pages (auto-generated)
├── scripts/
│   ├── generate_content.py  # AI content generator for cron job
│   └── lead_gen.py          # Daily lead generator
├── sitemap.xml           # SEO (auto-generated)
├── robots.txt            # SEO (auto-generated)
└── vercel.json           # Vercel config (auto-generated)
```

## Adding New Articles

1. Edit `content.json` and add a new entry to the `articles` array
2. Run `python3 build.py`
3. Deploy

Or let the weekly cron job do it automatically (every Monday at 9 AM IST).

## Cron Jobs (Automatic)

- **Monday 9 AM** — `bharatguide-content` — Generates 6 new SEO articles, rebuilds site
- **Daily 8 AM** — `bharatguide-leads` — Checks freelancing platforms and reports opportunities

View cron jobs: `hermes cron list`

## Tech Stack

- Static HTML/CSS — loads fast, no backend needed
- Free hosting on Vercel / Surge / GitHub Pages
- Python builder for article generation
- SEO optimized: schema.org, Open Graph, sitemap, canonical URLs

---

Made with ❤️ by your Hermes Agent | Bhopal, MP
