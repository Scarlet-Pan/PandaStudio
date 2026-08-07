# -*- coding: utf-8 -*-
"""Generate PolicyPal legal HTML from FortuneDiary strings_legal.xml.

Global (AI/BYOK): feature/setting/pal/.../commonMain or globalMain strings_legal
China (local archive, no AI): .../chinaMain/strings_legal

Usage (from PandaStudio repo root):
  python scripts/gen_legal.py
"""
from __future__ import annotations

import html
import pathlib
import re

REPO = pathlib.Path(__file__).resolve().parents[1]
FD = pathlib.Path(r"D:\AndroidStudioProjects\FortuneDiary")
SETTING_PAL = FD / "feature" / "setting" / "pal" / "src"

APP_ZH, APP_EN, VER = "保管（PolicyPal）", "PolicyPal (保管)", "1.0.0"

REGIONS = {
    "global": {
        "zh": SETTING_PAL / "globalMain" / "composeResources" / "values-zh" / "strings_legal.xml",
        "en": SETTING_PAL / "globalMain" / "composeResources" / "values" / "strings_legal.xml",
        # fallback if globalMain missing older trees used commonMain
        "zh_fallback": SETTING_PAL / "commonMain" / "composeResources" / "values-zh" / "strings_legal.xml",
        "en_fallback": SETTING_PAL / "commonMain" / "composeResources" / "values" / "strings_legal.xml",
        "out_dir": REPO / "legal" / "policypal",
        "css": "../../assets/site.css",
        "canonical_base": "https://pandastudio.hk/legal/policypal",
        "hub_href": "./",
        "hub_label": "PolicyPal · 法律文档",
        "track_note_zh": None,
        "track_note_en": None,
    },
    "china": {
        "zh": SETTING_PAL / "chinaMain" / "composeResources" / "values-zh" / "strings_legal.xml",
        "en": SETTING_PAL / "chinaMain" / "composeResources" / "values" / "strings_legal.xml",
        "zh_fallback": None,
        "en_fallback": None,
        "out_dir": REPO / "legal" / "policypal" / "cn",
        "css": "../../../assets/site.css",
        "canonical_base": "https://pandastudio.hk/legal/policypal/cn",
        "hub_href": "./",
        "hub_label": "PolicyPal · 大陆版法律文档",
        "track_note_zh": "本页适用于大陆安卓商店发行的 保管 版本（无生成式 AI / 无 BYOK），与应用内嵌全文一致。全球版（含 AI）请见上级目录法律页。",
        "track_note_en": "This page applies to the mainland Android store build of PolicyPal (no generative AI / no BYOK) and matches the in-app full text. For the global (AI) build, see the parent legal pages.",
    },
}


def parse_xml(path: pathlib.Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    pairs = re.findall(r'<string name="([^"]+)">(.*?)</string>', text, re.S)
    out: dict[str, str] = {}
    for k, v in pairs:
        v = (
            v.replace("\\n", "\n")
            .replace("\\'", "'")
            .replace('\\"', '"')
            .replace("&quot;", '"')
            .replace("&amp;", "&")
            .replace("&lt;", "<")
            .replace("&gt;", ">")
        )
        out[k] = v
    return out


def load_region(region: str) -> tuple[dict[str, str], dict[str, str]]:
    cfg = REGIONS[region]

    def load(primary, fallback):
        if primary.is_file():
            return parse_xml(primary)
        if fallback and fallback.is_file():
            return parse_xml(fallback)
        raise FileNotFoundError(primary)

    return load(cfg["zh"], cfg["zh_fallback"]), load(cfg["en"], cfg["en_fallback"])


def fill(s: str, app: str, ver: str) -> str:
    return s.replace("%1$s", app).replace("%2$s", ver)


def paras(body: str) -> str:
    parts = [p.strip() for p in body.split("\n\n") if p.strip()]
    return "\n".join(
        f"<p>{html.escape(p).replace(chr(10), '<br>')}</p>" for p in parts
    )


def sections(d: dict[str, str], prefix: str, app: str) -> str:
    keys = sorted(
        [k for k in d if k.startswith(prefix) and k.endswith("_title")],
        key=lambda k: int(re.search(r"_s(\d+)_", k).group(1)),
    )
    chunks = []
    for tk in keys:
        n = re.search(r"_s(\d+)_", tk).group(1)
        bk = prefix + f"_s{n}_body"
        title = fill(d[tk], app, VER)
        body = fill(d[bk], app, VER)
        chunks.append(f"<h2>{html.escape(title)}</h2>\n{paras(body)}")
    return "\n".join(chunks)


def page(
    *,
    region: str,
    doc: str,
    title_zh: str,
    title_en: str,
    zh_map: dict[str, str],
    en_map: dict[str, str],
    other_href: str,
    other_label_zh: str,
    other_label_en: str,
) -> str:
    cfg = REGIONS[region]
    meta_zh = fill(zh_map["legal_document_meta"], APP_ZH, VER)
    meta_en = fill(en_map["legal_document_meta"], APP_EN, VER)
    notice_zh = zh_map["legal_builtin_notice"]
    notice_en = en_map["legal_builtin_notice"]
    track_zh = cfg["track_note_zh"]
    track_en = cfg["track_note_en"]
    track_zh_html = (
        f'\n        <p class="muted-note">{html.escape(track_zh)}</p>' if track_zh else ""
    )
    track_en_html = (
        f'\n        <p class="muted-note">{html.escape(track_en)}</p>' if track_en else ""
    )
    zh_secs = sections(zh_map, f"legal_{'privacy' if doc == 'privacy' else 'terms'}", APP_ZH)
    en_secs = sections(en_map, f"legal_{'privacy' if doc == 'privacy' else 'terms'}", APP_EN)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title_zh)} · PolicyPal · Panda Studio</title>
  <meta name="description" content="{html.escape(title_en)} for PolicyPal by Hangzhou Panda Studio Technology Co., Ltd.">
  <link rel="canonical" href="{cfg['canonical_base']}/{doc}.html">
  <link rel="stylesheet" href="{cfg['css']}">
</head>
<body>
  <div class="wrap legal-doc">
    <header class="site-header">
      <a class="brand" href="/">
        <span class="logo-mark" aria-hidden="true">潘达</span>
        <span class="brand-text">Panda Studio<span>潘达工房</span></span>
      </a>
      <nav class="nav" aria-label="Primary">
        <a href="/">Home / 首页</a>
        <a href="/products/">Products / 产品</a>
        <a href="/about/">About / 关于</a>
        <a href="/contact/">Contact / 联系</a>
      </nav>
    </header>
    <main>
      <p class="muted-note"><a href="{cfg['hub_href']}">{html.escape(cfg['hub_label'])}</a> · <a href="{other_href}">{html.escape(other_label_zh)} / {html.escape(other_label_en)}</a></p>
      <section class="lang-block" lang="zh-CN">
        <p class="lang-label">中文（正式）</p>
        <h1>{html.escape(title_zh)}</h1>
        <p class="meta">{html.escape(meta_zh)}</p>{track_zh_html}
        <p class="muted-note">{html.escape(notice_zh)}</p>
        {zh_secs}
      </section>
      <section class="lang-block" lang="en">
        <p class="lang-label">English</p>
        <h1>{html.escape(title_en)}</h1>
        <p class="meta">{html.escape(meta_en)}</p>{track_en_html}
        <p class="muted-note">{html.escape(notice_en)}</p>
        {en_secs}
      </section>
    </main>
    <footer class="site-footer">
      <nav aria-label="Footer">
        <a href="/">Home</a>
        <a href="/products/">Products</a>
        <a href="/about/">About</a>
        <a href="/contact/">Contact</a>
        <a href="/legal/">Legal</a>
      </nav>
      <p>© Hangzhou Panda Studio Technology Co., Ltd. / 杭州潘达工房科技有限公司</p>
    </footer>
  </div>
</body>
</html>
"""


def write_docs(region: str) -> None:
    cfg = REGIONS[region]
    zh_map, en_map = load_region(region)
    out = cfg["out_dir"]
    out.mkdir(parents=True, exist_ok=True)
    (out / "privacy.html").write_text(
        page(
            region=region,
            doc="privacy",
            title_zh="隐私政策",
            title_en="Privacy Policy",
            zh_map=zh_map,
            en_map=en_map,
            other_href="terms.html",
            other_label_zh="用户协议与免责声明",
            other_label_en="Terms",
        ),
        encoding="utf-8",
    )
    (out / "terms.html").write_text(
        page(
            region=region,
            doc="terms",
            title_zh="用户协议与免责声明",
            title_en="Terms of Service and Disclaimer",
            zh_map=zh_map,
            en_map=en_map,
            other_href="privacy.html",
            other_label_zh="隐私政策",
            other_label_en="Privacy Policy",
        ),
        encoding="utf-8",
    )
    print(f"ok {region}", (out / "privacy.html").stat().st_size, (out / "terms.html").stat().st_size)


def write_cn_index() -> None:
    path = REGIONS["china"]["out_dir"] / "index.html"
    path.write_text(
        """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PolicyPal · 大陆版法律文档 · Panda Studio</title>
  <meta name="description" content="Mainland Android store legal pages for PolicyPal (保管) — no generative AI.">
  <link rel="canonical" href="https://pandastudio.hk/legal/policypal/cn/">
  <link rel="stylesheet" href="../../../assets/site.css">
</head>
<body>
  <div class="wrap">
    <header class="site-header">
      <a class="brand" href="/">
        <span class="logo-mark" aria-hidden="true">潘达</span>
        <span class="brand-text">Panda Studio<span>潘达工房</span></span>
      </a>
      <nav class="nav" aria-label="Primary">
        <a href="/">Home / 首页</a>
        <a href="/products/">Products / 产品</a>
        <a href="/about/">About / 关于</a>
        <a href="/contact/">Contact / 联系</a>
      </nav>
    </header>

    <main>
      <section class="lang-block" lang="zh-CN">
        <p class="lang-label">中文</p>
        <h1>保管 · 大陆版法律文档</h1>
        <p class="meta">杭州潘达工房科技有限公司 · 文档版本 1.0.0 · 无生成式 AI / 无 BYOK</p>
        <p class="muted-note">供小米、腾讯应用宝、华为等大陆安卓商店登记；正文与大陆包应用内嵌全文一致。全球版（含 AI）见 <a href="../">上级法律文档</a>。</p>
        <ul class="matrix-list">
          <li><a href="privacy.html">隐私政策</a> — <code>https://pandastudio.hk/legal/policypal/cn/privacy.html</code></li>
          <li><a href="terms.html">用户协议与免责声明</a> — <code>https://pandastudio.hk/legal/policypal/cn/terms.html</code></li>
        </ul>
        <p class="muted-note"><a href="../../">全部产品 · 法律与合规</a></p>
      </section>

      <section class="lang-block" lang="en">
        <p class="lang-label">English</p>
        <h1>PolicyPal · Mainland Legal</h1>
        <p class="meta">Hangzhou Panda Studio Technology Co., Ltd. · Document version 1.0.0 · No generative AI / no BYOK</p>
        <p class="muted-note">For mainland Android store listings. Matches the china-flavor in-app full text. Global (AI) build: <a href="../">parent legal hub</a>.</p>
        <ul class="matrix-list">
          <li><a href="privacy.html">Privacy Policy</a> — <code>https://pandastudio.hk/legal/policypal/cn/privacy.html</code></li>
          <li><a href="terms.html">Terms of Service and Disclaimer</a> — <code>https://pandastudio.hk/legal/policypal/cn/terms.html</code></li>
        </ul>
      </section>
    </main>

    <footer class="site-footer">
      <nav aria-label="Footer">
        <a href="/">Home</a>
        <a href="/products/">Products</a>
        <a href="/about/">About</a>
        <a href="/contact/">Contact</a>
        <a href="/legal/">Legal</a>
      </nav>
      <p>© Hangzhou Panda Studio Technology Co., Ltd. / 杭州潘达工房科技有限公司</p>
    </footer>
  </div>
</body>
</html>
""",
        encoding="utf-8",
    )
    print("ok cn index")


def patch_global_index() -> None:
    path = REPO / "legal" / "policypal" / "index.html"
    text = path.read_text(encoding="utf-8")
    if "policypal/cn/" in text:
        print("global index already links cn")
        return
    needle_zh = """        <ul class="matrix-list">
          <li><a href="privacy.html">隐私政策</a> — <code>https://pandastudio.hk/legal/policypal/privacy.html</code></li>
          <li><a href="terms.html">用户协议与免责声明</a> — <code>https://pandastudio.hk/legal/policypal/terms.html</code></li>
        </ul>
        <p class="muted-note"><a href="../">全部产品 · 法律与合规</a></p>"""
    repl_zh = """        <ul class="matrix-list">
          <li><a href="privacy.html">隐私政策</a>（全球 / AI） — <code>https://pandastudio.hk/legal/policypal/privacy.html</code></li>
          <li><a href="terms.html">用户协议与免责声明</a>（全球 / AI） — <code>https://pandastudio.hk/legal/policypal/terms.html</code></li>
          <li><a href="cn/">大陆安卓商店版</a>（无 AI） — <code>https://pandastudio.hk/legal/policypal/cn/</code></li>
        </ul>
        <p class="muted-note"><a href="../">全部产品 · 法律与合规</a></p>"""
    needle_en = """        <ul class="matrix-list">
          <li><a href="privacy.html">Privacy Policy</a> — <code>https://pandastudio.hk/legal/policypal/privacy.html</code></li>
          <li><a href="terms.html">Terms of Service and Disclaimer</a> — <code>https://pandastudio.hk/legal/policypal/terms.html</code></li>
        </ul>
        <p class="muted-note"><a href="../">All products · Legal</a></p>"""
    repl_en = """        <ul class="matrix-list">
          <li><a href="privacy.html">Privacy Policy</a> (global / AI) — <code>https://pandastudio.hk/legal/policypal/privacy.html</code></li>
          <li><a href="terms.html">Terms of Service and Disclaimer</a> (global / AI) — <code>https://pandastudio.hk/legal/policypal/terms.html</code></li>
          <li><a href="cn/">Mainland Android store</a> (no AI) — <code>https://pandastudio.hk/legal/policypal/cn/</code></li>
        </ul>
        <p class="muted-note"><a href="../">All products · Legal</a></p>"""
    if needle_zh not in text or needle_en not in text:
        raise SystemExit("index.html markers not found; update manually")
    path.write_text(text.replace(needle_zh, repl_zh).replace(needle_en, repl_en), encoding="utf-8")
    print("ok patched global index")


def patch_readme() -> None:
    path = REPO / "README.md"
    text = path.read_text(encoding="utf-8")
    if "policypal/cn/privacy.html" in text:
        print("readme already has cn urls")
        return
    old = """### Store legal URLs (PolicyPal)

| Doc | URL |
|-----|-----|
| Privacy | https://pandastudio.hk/legal/policypal/privacy.html |
| Terms | https://pandastudio.hk/legal/policypal/terms.html |
| Hub | https://pandastudio.hk/legal/ |

Generated from FortuneDiary `strings_legal.xml` via [`scripts/gen_legal.py`](scripts/gen_legal.py). Future products: add `legal/<slug>/`.
"""
    new = """### Store legal URLs (PolicyPal)

| Track | Doc | URL |
|-------|-----|-----|
| Global (AI / Play · iOS) | Privacy | https://pandastudio.hk/legal/policypal/privacy.html |
| Global | Terms | https://pandastudio.hk/legal/policypal/terms.html |
| Mainland Android (no AI) | Privacy | https://pandastudio.hk/legal/policypal/cn/privacy.html |
| Mainland Android | Terms | https://pandastudio.hk/legal/policypal/cn/terms.html |
| Hub | — | https://pandastudio.hk/legal/policypal/ |

Generated from FortuneDiary `strings_legal.xml` (`globalMain` / `chinaMain`) via [`scripts/gen_legal.py`](scripts/gen_legal.py).
"""
    if old not in text:
        raise SystemExit("README markers not found")
    path.write_text(text.replace(old, new), encoding="utf-8")
    print("ok patched readme")


if __name__ == "__main__":
    # Only regenerate china pages here; leave global HTML as currently published
    # unless you intentionally re-run write_docs("global").
    write_docs("china")
    write_cn_index()
    patch_global_index()
    patch_readme()
