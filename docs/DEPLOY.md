# Deploy: pandastudio.hk

## 1. Push this repository

Remote: `https://github.com/Scarlet-Pan/PandaStudio`  
Branch: `main`  
Pages source: **Deploy from a branch** → `main` / **/** (root)

This repo root **is** the site root (`index.html`, `about/`, `products/`, `contact/`, `assets/`, `CNAME`).

## 2. GitHub Pages + custom domain

Already applied by this repo (after push to `main`):

- Source: `main` / `/` (root)
- Custom domain from `CNAME` file: `pandastudio.hk`

In GitHub UI, still confirm:

1. Repo **Settings → Pages** shows Custom domain `pandastudio.hk`
2. After DNS verifies (green check), enable **Enforce HTTPS**
3. `CNAME` file at repo root contains exactly:

   ```
   pandastudio.hk
   ```

**Preview before DNS works:** with a custom domain set, `https://scarlet-pan.github.io/PandaStudio/` may **301** to `pandastudio.hk`. Until DNS points at GitHub, that apex URL will fail — finish §3 first, or temporarily clear the custom domain in Pages settings to preview on `*.github.io`.

## 3. DNS records (`.hk` registrar)

**Do not change existing MX records** for `@pandastudio.hk` email.

Add or update **only** web records (GitHub Pages, as of docs — verify [GitHub Pages custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site) if IPs change):

| Type | Host / Name | Value | Notes |
|------|-------------|-------|--------|
| `A` | `@` (apex) | `185.199.108.153` | GitHub Pages |
| `A` | `@` | `185.199.109.153` | |
| `A` | `@` | `185.199.110.153` | |
| `A` | `@` | `185.199.111.153` | |
| `AAAA` | `@` | `2606:50c0:8000::153` | Optional IPv6 |
| `AAAA` | `@` | `2606:50c0:8001::153` | |
| `AAAA` | `@` | `2606:50c0:8002::153` | |
| `AAAA` | `@` | `2606:50c0:8003::153` | |
| `CNAME` | `www` | `scarlet-pan.github.io` | Optional www |

If the registrar offers **ALIAS / ANAME** for apex → `scarlet-pan.github.io`, that may replace the four `A` records.

Propagation: often minutes to a few hours; rarely up to 48h.

## 3b. Demo video (optional but recommended)

1. Put H.264 MP4 at `assets/demo/policypal-demo.mp4` (prefer trim **0:00–2:42**, ideally **&lt; 30 MB**).
2. Commit & push `main`.
3. Pages will serve: `https://pandastudio.hk/assets/demo/policypal-demo.mp4`  
   Home / Products embed a `<video controls>` player pointing at that path.

Details: [`assets/demo/README.md`](../assets/demo/README.md).

If the file is huge, use YouTube/Bilibili embed or object storage instead of committing the binary.

## 4. About `pandastudio.app`

Enrollment and Apple Case replies should use **`https://pandastudio.hk/`** only.  
Do not send reviewers to `pandastudio.app` while it still shows GoDaddy “Launching Soon”. Redirecting `.app` → `.hk` is optional later.

## 5. Public acceptance checklist

Open in a private/incognito window (no login):

- [ ] `https://pandastudio.hk/` loads over HTTPS, not blank, not “Coming Soon / Launching Soon”
- [ ] `/about/` shows legal Chinese + English names and registered addresses
- [ ] `/products/` describes PolicyPal / 保管 and the non-licensed disclaimer
- [ ] `/contact/` lists at least `pandastudio.app@gmail.com`
- [ ] Footer shows: © Hangzhou Panda Studio Technology Co., Ltd. / 杭州潘达工房科技有限公司
- [ ] Not a social-media-only page

Also smoke-test: `https://scarlet-pan.github.io/PandaStudio/` if custom domain is still pending.

## 6. Apple Enrollment + Case reply

**Enrollment website field:** `https://pandastudio.hk/`

**Case:** `102949420469`  
**Enrollment ID:** `7WT24JDLLT`

### Suggested reply (English)

```
Hello,

We have published our organization website at:

https://pandastudio.hk/

It includes company identity (About), product information (Products), and contact details. Please continue review of Organization enrollment.

Enrollment ID: 7WT24JDLLT
Case: 102949420469

Thank you.
```

### 建议回复（中文，如需）

```
您好，

我们已上线组织官网：

https://pandastudio.hk/

站点包含公司主体信息（About）、产品说明（Products）与联系方式。请继续审核 Organization 注册。

Enrollment ID: 7WT24JDLLT
Case: 102949420469

谢谢。
```

Keep the enrollment contact phone reachable for verification calls.
