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
| `/` | Home |
| `/about/` | About |
| `/products/` | Products (PolicyPal / 保管) |
| `/contact/` | Contact |

## Future KMP

Do not couple this MVP to the PolicyPal app. When moving to Compose Multiplatform Web, reuse `content/site.json` field semantics and keep the same routes; replace the static shell under a new `composeApp/` module while keeping Pages + domain unchanged.
