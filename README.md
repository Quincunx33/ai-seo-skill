# Universal SEO Engineer Pro v2

Evidence-based SEO engineering for websites and web apps.

This repository contains a packaged AI/automation skill for technical SEO auditing, on-page optimization, structured data review, and safe implementation guidance. It is designed to help evaluate a site with a strong emphasis on evidence, user experience, crawlability, and measurable improvements rather than guesswork or risky shortcuts.

## What this repo includes

- `SKILL.md` — the unpacked skill definition used for browsing and editing.
- `universal-seo-engineer-pro-v2.skill` — the original uploaded package.
- `references/` — supporting SEO playbooks and workflow references.
- `scripts/seo_smoke_check.py` — a read-only smoke test utility for checking a single URL.

## Purpose

The package acts as a senior SEO engineer, information architect, content strategist, and performance engineer. It focuses on:

- technical SEO audits
- indexation, crawlability, and canonical correctness
- structured data and SERP presentation
- content quality and topical relevance
- internal linking and website architecture
- performance and Core Web Vitals awareness
- safe implementation and verification workflows

## Repository structure

```text
.
├── README.md
├── SKILL.md
├── universal-seo-engineer-pro-v2.skill
├── references/
│   ├── extended-seo-playbook.md
│   └── original-engineer.md
└── scripts/
    └── seo_smoke_check.py
```

## Getting started

### 1. Review the skill contract

Open `SKILL.md` for the complete operating contract, audit phases, deliverables, and implementation rules.

### 2. Use the smoke-check script

This script performs a lightweight, read-only HTTP check for a single domain.

```bash
python3 scripts/seo_smoke_check.py https://example.com
```

The script returns a JSON payload including:

- final URL
- HTTP status
- content type
- `X-Robots-Tag`
- page title
- page metadata and link hints

This is not a full crawler and is intended only as a basic validation step.

## Working philosophy

This project follows a conservative, evidence-based approach:

- verify before recommending changes
- prefer small, well-scoped fixes over brittle hacks
- protect user experience while improving crawlability and discoverability
- treat rankings, traffic, and indexation as outcomes to be measured, not promised
- avoid manipulative SEO tactics and deceptive optimization techniques

## Safety and scope

The project explicitly discourages unauthorized production changes, deceptive redirect behavior, spammy link practices, fabricated rankings claims, and unsafe edits to live sites without approval.

When code changes are needed, they should be:

- small and targeted
- aligned with framework conventions
- validated with the appropriate checks
- paired with rollback and monitoring guidance

## References

The repository includes bundled guidance for SEO workflows and implementation patterns:

- `references/extended-seo-playbook.md`
- `references/original-engineer.md`

These files provide deeper operational context and practical audit guidance.

## Notes

This repository is a packaged skill and reference bundle rather than a traditional application. Its primary value is in the structured audit process, implementation guardrails, and validation mindset it provides.

For detailed usage and workflow expectations, start with `SKILL.md`.
