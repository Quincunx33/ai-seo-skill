# 🚀 Universal SEO Engineer Pro v2

> Evidence-based SEO engineering for websites and web apps.

A compact AI SEO skill package for technical audits, on-page optimization, structured data review, and safe implementation guidance.

## ✨ What’s inside

- `SKILL.md` — full operating contract and audit workflow
- `references/` — bundled SEO playbooks and guidance
- `scripts/seo_smoke_check.py` — quick read-only smoke test for a single URL
- `universal-seo-engineer-pro-v2.skill` — original packaged skill file

## 🧭 Purpose

This repo helps assess:

- technical SEO health
- crawlability and indexability
- canonical and hreflang correctness
- structured data quality
- performance and page experience
- safe, evidence-based fixes

## 📁 Structure

```text
ai-seo-skill/
├── README.md
├── SKILL.md
├── universal-seo-engineer-pro-v2.skill
├── references/
│   ├── extended-seo-playbook.md
│   └── original-engineer.md
└── scripts/
    └── seo_smoke_check.py
```

## ⚡ Quick start

```bash
python3 scripts/seo_smoke_check.py https://example.com
```

This returns a lightweight JSON report with status, URL, title, and key metadata for a quick sanity check.

## 🛡️ Operating principle

- Verify before recommending changes
- Prefer small, testable fixes
- Favor user experience and technical correctness
- Avoid risky or manipulative SEO tactics

## 📌 Notes

This is a skill/reference package, not a traditional app. For the detailed workflow and audit rules, start with `SKILL.md`.
