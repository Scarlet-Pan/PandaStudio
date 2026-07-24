# Panda Studio — Company website (MVP)

Official company site for **Hangzhou Panda Studio Technology Co., Ltd.** / **杭州潘达工房科技有限公司**, served at [https://pandastudio.hk/](https://pandastudio.hk/).

Built for Apple Developer Program (Organization) website requirements: public HTTPS pages with company identity, products, and contact — not a marketing or e-commerce site.

## Stack

- Static HTML + CSS (no build step)
- Canonical bilingual copy in [`content/site.json`](content/site.json) for a future Compose Multiplatform Web migration
- GitHub Pages + custom domain `pandastudio.hk`

## Local preview

From the repo root (site root):

```bash
npx --yes serve -l 4173 .
```

Then open `http://localhost:4173/`.

## Deploy

See [`docs/DEPLOY.md`](docs/DEPLOY.md).

## Routes

| Path | Page |
|------|------|
| `/` | Home — Slogan, vision, CTAs, preview screenshots |
| `/about/` | Legal entity + why we built it + product line |
| `/products/` | PolicyPal / 保管 — capabilities, disclaimer, screenshot gallery |
| `/contact/` | Emails + registered address |

Copy source of truth: [`content/site.json`](content/site.json). Soft-copyright screenshots: `assets/screens/`. App icons: `assets/brand/`.

### Store legal URLs (PolicyPal)

| Doc | URL |
|-----|-----|
| Privacy | https://pandastudio.hk/legal/policypal/privacy.html |
| Terms | https://pandastudio.hk/legal/policypal/terms.html |
| Hub | https://pandastudio.hk/legal/ |

Generated from FortuneDiary `strings_legal.xml` via [`scripts/gen_legal.py`](scripts/gen_legal.py). Future products: add `legal/<slug>/`.

## Future KMP

Do not couple this MVP to the PolicyPal app. When moving to Compose Multiplatform Web, reuse `content/site.json` field semantics and keep the same routes; replace the static shell under a new `composeApp/` module while keeping Pages + domain unchanged.
