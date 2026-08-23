# -*- coding: utf-8 -*-
"""Generate PolicyPal legal HTML from FortuneDiary strings_legal.xml.

Global (AI/BYOK + Crashlytics): feature/setting/pal/.../globalMain strings_legal
China (local archive, no AI / no Firebase): .../chinaMain/strings_legal

Usage (from PandaStudio repo root):
  python3 scripts/gen_legal.py
  # optional: FORTUNEDIARY=/path/to/FortuneDiary python3 scripts/gen_legal.py
"""
from __future__ import annotations

import html
import os
import pathlib
import re

REPO = pathlib.Path(__file__).resolve().parents[1]


def resolve_fortunediary() -> pathlib.Path:
    env = os.environ.get("FORTUNEDIARY")
    if env:
        return pathlib.Path(env).expanduser().resolve()
    # Common layouts: sibling of PandaStudio, or Windows AndroidStudioProjects path.
    candidates = [
        REPO.parent / "FortuneDiary",
        pathlib.Path(r"D:\AndroidStudioProjects\FortuneDiary"),
        pathlib.Path.home() / "Projects" / "FortuneDiary",
    ]
    for c in candidates:
        if (c / "feature" / "setting" / "pal").is_dir():
            return c.resolve()
    raise SystemExit(
        "FortuneDiary not found. Set FORTUNEDIARY=/path/to/FortuneDiary "
        "or place it next to the PandaStudio repo."
    )


FD = resolve_fortunediary()
SETTING_PAL = FD / "feature" / "setting" / "pal" / "src"
LEGAL_KT = (
    SETTING_PAL
    / "commonMain"
    / "kotlin"
    / "studio"
    / "panda"
    / "insurance"
    / "setting"
    / "pal"
    / "LegalDocuments.kt"
)

APP_ZH, APP_EN = "保管（PolicyPal）", "PolicyPal (保管)"


def read_legal_meta() -> tuple[str, str, str, str]:
    text = LEGAL_KT.read_text(encoding="utf-8")

    def const(name: str) -> str:
        m = re.search(rf'internal const val {name} = "([^"]+)"', text)
        if not m:
            raise SystemExit(f"{name} not found in LegalDocuments.kt")
        return m.group(1)

    return (
        const("UPDATED_DATE"),
        const("DOCUMENT_VERSION"),
        const("APP_VERSION_LINE_ZH"),
        const("APP_VERSION_LINE_EN"),
    )


UPDATED_DATE, DOC_VER, APP_VER_ZH, APP_VER_EN = read_legal_meta()

REGIONS = {
    "global": {
        "zh": SETTING_PAL / "globalMain" / "composeResources" / "values-zh" / "strings_legal.xml",
        "en": SETTING_PAL / "globalMain" / "composeResources" / "values" / "strings_legal.xml",
        "zh_fallback": SETTING_PAL / "commonMain" / "composeResources" / "values-zh" / "strings_legal.xml",
        "en_fallback": SETTING_PAL / "commonMain" / "composeResources" / "values" / "strings_legal.xml",
        "out_dir": REPO / "legal" / "policypal",
        "css": "../../assets/site.css",
        "canonical_base": "https://pandastudio.hk/legal/policypal",
        "hub_href": "./",
        "hub_label": "PolicyPal · 法律文档",
        "track_note_zh": (
            "本页适用于全球版（Google Play / App Store 等，含可选 AI 与 Firebase Crashlytics），"
            "与应用内嵌全文一致。大陆安卓商店版（无生成式 AI / 无 Firebase）请见 cn/ 目录。"
        ),
        "track_note_en": (
            "This page applies to the global build (Google Play / App Store, including optional AI "
            "and Firebase Crashlytics) and matches the in-app full text. For the mainland Android "
            "store build (no generative AI / no Firebase), see the cn/ folder."
        ),
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
        "track_note_zh": (
            "本页适用于大陆安卓商店发行的 保管 版本（无生成式 AI / 无 BYOK / 无 Firebase），"
            "与应用内嵌全文一致。全球版请见上级目录法律页。"
        ),
        "track_note_en": (
            "This page applies to the mainland Android store build of PolicyPal "
            "(no generative AI / no BYOK / no Firebase) and matches the in-app full text. "
            "For the global build, see the parent legal pages."
        ),
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


def fill(s: str, app: str, ver_line: str) -> str:
    # %1$s app name; %2$s used as app-version line in section bodies that pass 2 args
    # (in-app: appName + appVersionLine). Website fills the same.
    return s.replace("%1$s", app).replace("%2$s", ver_line).replace("%3$s", ver_line)


def paras(body: str) -> str:
    parts = [p.strip() for p in body.split("\n\n") if p.strip()]
    return "\n".join(
        f"<p>{html.escape(p).replace(chr(10), '<br>')}</p>" for p in parts
    )


def sections(d: dict[str, str], prefix: str, app: str, ver_line: str) -> str:
    keys = sorted(
        [k for k in d if k.startswith(prefix) and k.endswith("_title")],
        key=lambda k: int(re.search(r"_s(\d+)_", k).group(1)),
    )
    chunks = []
    for tk in keys:
        n = re.search(r"_s(\d+)_", tk).group(1)
        bk = prefix + f"_s{n}_body"
        title = fill(d[tk], app, ver_line)
        body = fill(d[bk], app, ver_line)
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
    zh_secs = sections(
        zh_map, f"legal_{'privacy' if doc == 'privacy' else 'terms'}", APP_ZH, APP_VER_ZH
    )
    en_secs = sections(
        en_map, f"legal_{'privacy' if doc == 'privacy' else 'terms'}", APP_EN, APP_VER_EN
    )
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
        <p class="meta">更新日期：{html.escape(UPDATED_DATE)}</p>
        <p class="meta">适用 {html.escape(APP_ZH)} · 文档版本 {html.escape(DOC_VER)}</p>
        <p class="meta">适用应用版本：{html.escape(APP_VER_ZH)}</p>{track_zh_html}
        <p class="muted-note">{html.escape(notice_zh)}</p>
        {zh_secs}
      </section>
      <section class="lang-block" lang="en">
        <p class="lang-label">English</p>
        <h1>{html.escape(title_en)}</h1>
        <p class="meta">Updated: {html.escape(UPDATED_DATE)}</p>
        <p class="meta">Applies to {html.escape(APP_EN)} · Document version {html.escape(DOC_VER)}</p>
        <p class="meta">App version: {html.escape(APP_VER_EN)}</p>{track_en_html}
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


if __name__ == "__main__":
    print(f"FortuneDiary={FD}")
    print(f"doc={DOC_VER} updated={UPDATED_DATE}")
    write_docs("global")
    write_docs("china")
