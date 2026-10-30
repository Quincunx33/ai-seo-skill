# 🌐 Universal SEO Engineer Pro v2

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License" />
  <img src="https://img.shields.io/badge/Python-100%25-3776AB?logo=python&logoColor=white" alt="Python 100%" />
  <img src="https://img.shields.io/badge/SEO-Audit%20%26%20Optimization-blue" alt="SEO audit and optimization" />
</p>

> Evidence-based SEO engineering for websites and web apps.

A compact, high-signal SEO skill package for technical audits, structured data review, page experience checks, and safe implementation guidance.

## ✨ Overview

This repository packages an AI-driven SEO engineering workflow designed to help evaluate websites with a practical, evidence-based approach. It emphasizes:

- technical SEO analysis
- crawlability and indexability review
- canonical, sitemap, and structured data checks
- content quality and topical relevance
- page experience and performance awareness
- safe, minimal, validated implementation

## 🚀 What’s Included

- `SKILL.md` — the complete SEO operating contract and workflow
- `references/` — bundled SEO playbooks and implementation guidance
- `scripts/seo_smoke_check.py` — a lightweight, read-only smoke test for a single URL
- `universal-seo-engineer-pro-v2.skill` — the original packaged skill artifact

## 🧭 Repository Structure

```text
ai-seo-skill/
├── README.md
├── LICENSE
├── SKILL.md
├── universal-seo-engineer-pro-v2.skill
├── references/
│   ├── extended-seo-playbook.md
│   └── original-engineer.md
└── scripts/
    └── seo_smoke_check.py
```

## ⚡ Quick Start

Run the smoke-check script against any public URL:

```bash
python3 scripts/seo_smoke_check.py https://example.com
```

This returns a JSON report with useful metadata such as:

- final resolved URL
- HTTP status
- content type
- `X-Robots-Tag`
- page title
- linked metadata hints

> This is a lightweight validation helper, not a full crawler or browser-based SEO suite.

## 🛠️ Core Principles

This project follows a conservative, user-first workflow:

- verify before recommending changes
- prefer small, well-scoped fixes over risky shortcuts
- optimize for actual user experience and crawl quality
- avoid manipulative SEO patterns
- measure outcomes instead of promising rankings

## 📌 Why This Exists

SEO work is often fragmented across technical, content, and performance concerns. This repository brings those concerns into a single structured process focused on evidence, implementation safety, and measurable improvements.

It is especially useful for:

- technical SEO audits
- site architecture review
- structured data validation
- on-page optimization checks
- content and internal linking assessment
- deployment-safe SEO implementation planning

## 🔒 Safety and Scope

The included workflow strongly discourages:

- unauthorized production edits
- deceptive redirects
- spammy link tactics
- made-up ranking claims
- unsafe indexing or canonical changes without review

## 📚 References

For deeper guidance, start with:

- `SKILL.md`
- `references/extended-seo-playbook.md`
- `references/original-engineer.md`

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

Built for evidence-based SEO engineering, clean implementation, and measurable web growth.
