#!/usr/bin/env python3
"""BharatGuide static site builder. Reads content.json, generates all HTML pages."""

import json
import os
import re
import html as html_mod

SKILL_DIR = "/home/abdulqadiraq2008/.hermes/skills/media/youtube-content"
CONTENT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "content.json")
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_content():
    with open(CONTENT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def esc(text):
    return html_mod.escape(str(text))

def slugify(text):
    return re.sub(r'[^a-z0-9-]', '', text.lower().replace(' ', '-').replace('–', '-'))

def render_article_content(blocks, site_url):
    """Render content blocks to HTML."""
    html = ""
    for block in blocks:
        t = block.get("type", "")
        if t == "p":
            html += f"<p>{esc(block['text']).replace(chr(10), '<br>')}</p>\n"
        elif t == "h2":
            text = block.get("text", "")
            if text.strip():
                html += f"<h2>{esc(text)}</h2>\n"
        elif t == "h3":
            html += f"<h3>{esc(block['text'])}</h3>\n"
        elif t == "ul":
            items = block.get("items", [])
            html += "<ul>\n"
            for item in items:
                html += f"  <li>{esc(item)}</li>\n"
            html += "</ul>\n"
        elif t == "step":
            html += f'<div class="step-box"><strong>{esc(block["title"])}</strong>{esc(block["text"])}</div>\n'
        elif t == "tip":
            html += f'<div class="tip-box"><strong>💡 Tip:</strong>{esc(block["text"])}</div>\n'
        elif t == "warning":
            html += f'<div class="warning-box"><strong>⚠️ Warning:</strong>{esc(block["text"])}</div>\n'
        elif t == "table":
            html += "<table>\n<thead><tr>"
            for h in block.get("headers", []):
                html += f"<th>{esc(h)}</th>"
            html += "</tr></thead>\n<tbody>\n"
            for row in block.get("rows", []):
                html += "<tr>"
                for cell in row:
                    html += f"<td>{esc(cell)}</td>"
                html += "</tr>\n"
            html += "</tbody>\n</table>\n"
        elif t == "code":
            html += f'<pre style="background:#1e293b;color:#e2e8f0;padding:16px;border-radius:8px;overflow-x:auto;font-size:0.9rem;margin:12px 0;">{esc(block["text"])}</pre>\n'
    return html

def generate_article_page(article, site, categories):
    cat_map = {c["slug"]: c for c in categories}
    cat = cat_map.get(article["category"], {})
    
    content_html = render_article_content(article.get("content", []), site["url"])
    
    # Related articles from same category
    related = []
    for a in site.get("_all_articles", []):
        if a["slug"] != article["slug"] and a["category"] == article["category"]:
            related.append(a)
    related = related[:3]
    
    related_html = ""
    if related:
        related_html = '<div class="related-posts"><h3>📖 Related Guides</h3><ul>\n'
        for r in related:
            related_html += f'<li><a href="/articles/{r["slug"]}.html">{esc(r["title"])}</a></li>\n'
        related_html += '</ul></div>\n'
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(article["title"])} | BharatGuide</title>
  <meta name="description" content="{esc(article["description"])}">
  <meta property="og:title" content="{esc(article["title"])}">
  <meta property="og:description" content="{esc(article["description"])}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{site["url"]}/articles/{article["slug"]}.html">
  <meta property="og:site_name" content="BharatGuide">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="canonical" href="{site["url"]}/articles/{article["slug"]}.html">
  <meta name="robots" content="index, follow">
  <link rel="stylesheet" href="/css/style.css">
  <script type="application/ld+json">{{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{esc(article["title"])}",
    "description": "{esc(article["description"])}",
    "author": {{"@type": "Organization", "name": "BharatGuide"}},
    "datePublished": "{article.get("date", "2026-01-01")}",
    "publisher": {{"@type": "Organization", "name": "BharatGuide"}}
  }}</script>
</head>
<body>
  <header>
    <div class="container">
      <a href="/" class="logo">Bharat<span>Guide</span></a>
      <nav>
        <a href="/">Home</a>
        <a href="/#categories">Topics</a>
        <a href="/#articles">Guides</a>
      </nav>
    </div>
  </header>

  <div class="article-page">
    <div class="container">
      <article>
        <div class="breadcrumb"><a href="/">Home</a> / <a href="/#articles">{esc(cat.get("icon",""))} {esc(cat.get("name",""))}</a> / {esc(article["title"])}</div>
        <h1>{esc(article["title"])}</h1>
        <div class="article-meta">📅 Updated: {article.get("date","")} · ⏱ {article.get("readTime","")}</div>
        {content_html}
        {related_html}
      </article>
    </div>
  </div>

  <footer>
    <div class="container">
      <p>BharatGuide — Your guide to India's digital services | <a href="mailto:contact@bharatguide.vercel.app">Contact</a></p>
      <p style="margin-top:8px;font-size:0.85rem;">Not affiliated with any government agency. Information provided for guidance only.</p>
    </div>
  </footer>
</body>
</html>'''

def generate_index_page(site, categories, articles):
    # Category cards
    cat_html = ""
    for cat in categories:
        count = sum(1 for a in articles if a["category"] == cat["slug"])
        cat_html += f'''<a href="/#{cat["slug"]}" style="text-decoration:none;color:inherit;">
          <div class="category-card">
            <div class="icon">{cat["icon"]}</div>
            <h3>{esc(cat["name"])}</h3>
            <p>{esc(cat["description"])}</p>
            <p style="margin-top:6px;font-size:0.8rem;color:var(--primary);font-weight:600;">{count} guide{'' if count==1 else 's'}</p>
          </div>
        </a>\n'''
    
    # Article cards by category
    article_list_html = ""
    for cat in categories:
        cat_articles = [a for a in articles if a["category"] == cat["slug"]]
        if not cat_articles:
            continue
        article_list_html += f'<h3 id="{cat["slug"]}" style="font-size:1.3rem;margin:32px 0 16px;">{cat["icon"]} {esc(cat["name"])} Guides</h3>\n'
        article_list_html += '<div class="article-grid">\n'
        for art in cat_articles:
            article_list_html += f'''<div class="article-card">
              <span class="cat-badge">{esc(cat["name"])}</span>
              <h3><a href="/articles/{art["slug"]}.html">{esc(art["title"])}</a></h3>
              <p>{esc(art["description"])}</p>
              <div class="meta">📅 {art.get("date","")} · ⏱ {art.get("readTime","")}</div>
              <a href="/articles/{art["slug"]}.html" class="read-more">Read Guide →</a>
            </div>\n'''
        article_list_html += '</div>\n'
    
    total = len(articles)
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(site["name"])} — {esc(site["tagline"])}</title>
  <meta name="description" content="{esc(site["description"])}">
  <meta property="og:title" content="{esc(site["name"])} — {esc(site["tagline"])}">
  <meta property="og:description" content="{esc(site["description"])}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{site["url"]}">
  <meta property="og:site_name" content="{esc(site["name"])}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="canonical" href="{site["url"]}">
  <meta name="robots" content="index, follow">
  <link rel="stylesheet" href="/css/style.css">
  <script type="application/ld+json">{{
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "{esc(site["name"])}",
    "url": "{site["url"]}",
    "description": "{esc(site["description"])}"
  }}</script>
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-YOUR_PUB_ID" crossorigin="anonymous"></script>
</head>
<body>
  <header>
    <div class="container">
      <a href="/" class="logo">Bharat<span>Guide</span></a>
      <nav>
        <a href="/">Home</a>
        <a href="#categories">Topics</a>
        <a href="#articles">All Guides</a>
      </nav>
    </div>
  </header>

  <section class="hero">
    <div class="container">
      <h1>{esc(site["tagline"])}</h1>
      <p>Simple, step-by-step guides for Aadhaar, PAN, DigiLocker, driving license, passports, scholarships and more. Updated for 2026.</p>
    </div>
  </section>

  <section class="categories" id="categories">
    <div class="container">
      <h2>📂 Browse by Topic</h2>
      <div class="category-grid">
        {cat_html}
      </div>
    </div>
  </section>

  <section class="articles-section" id="articles">
    <div class="container">
      <h2>📝 {total} Step-by-Step Guides</h2>
      {article_list_html}
    </div>
  </section>

  <footer>
    <div class="container">
      <p>BharatGuide — Your guide to India's digital services | <a href="mailto:contact@bharatguide.vercel.app">Contact</a></p>
      <p style="margin-top:8px;font-size:0.85rem;">Not affiliated with any government agency. Information provided for guidance only.</p>
    </div>
  </footer>
</body>
</html>'''

def generate_sitemap(site, articles):
    urls = [f"  <url><loc>{site['url']}/</loc><priority>1.0</priority></url>"]
    for art in articles:
        urls.append(f"  <url><loc>{site['url']}/articles/{art['slug']}.html</loc><priority>0.8</priority></url>")
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>'''

def generate_robots(site):
    return f"""User-agent: *
Allow: /
Sitemap: {site['url']}/sitemap.xml
"""

def main():
    data = load_content()
    site = data["site"]
    categories = data["categories"]
    articles = data["articles"]
    
    # Store all articles reference for related links
    site["_all_articles"] = articles
    
    # Create output directories
    articles_dir = os.path.join(OUTPUT_DIR, "articles")
    os.makedirs(articles_dir, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "css"), exist_ok=True)
    
    # Generate index page
    index_html = generate_index_page(site, categories, articles)
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"✅ Generated: index.html")
    
    # Generate article pages
    for art in articles:
        page_html = generate_article_page(art, site, categories)
        with open(os.path.join(articles_dir, f"{art['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(page_html)
        print(f"✅ Generated: articles/{art['slug']}.html")
    
    # Generate sitemap
    sitemap = generate_sitemap(site, articles)
    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
    print("✅ Generated: sitemap.xml")
    
    # Generate robots.txt
    robots = generate_robots(site)
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)
    print("✅ Generated: robots.txt")
    
    # Generate vercel.json
    vercel = {
        "version": 2,
        "public": True,
        "cleanUrls": True,
        "trailingSlash": False,
        "headers": [
            {
                "source": "/(.*)",
                "headers": [
                    {"key": "X-Content-Type-Options", "value": "nosniff"},
                    {"key": "X-Frame-Options", "value": "DENY"},
                    {"key": "X-XSS-Protection", "value": "1; mode=block"},
                    {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"}
                ]
            },
            {
                "source": "/css/(.*)",
                "headers": [
                    {"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}
                ]
            }
        ]
    }
    with open(os.path.join(OUTPUT_DIR, "vercel.json"), "w", encoding="utf-8") as f:
        json.dump(vercel, f, indent=2)
    print("✅ Generated: vercel.json")
    
    print(f"\n🎉 Site built! {len(articles)} articles, {len(categories)} categories")
    print("Run: cd bharatguide && npx vercel --prod  (or deploy manually)")

if __name__ == "__main__":
    main()
