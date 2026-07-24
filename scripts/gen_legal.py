# -*- coding: utf-8 -*-
"""Generate PolicyPal legal HTML from FortuneDiary strings_legal.xml."""
import re
import html
import pathlib

def parse_xml(path):
    text = pathlib.Path(path).read_text(encoding="utf-8")
    pairs = re.findall(r'<string name="([^"]+)">(.*?)</string>', text, re.S)
    out = {}
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


def fill(s, app, ver):
    return s.replace("%1$s", app).replace("%2$s", ver)


def paras(body):
    parts = [p.strip() for p in body.split("\n\n") if p.strip()]
    return "\n".join(
        f"<p>{html.escape(p).replace(chr(10), '<br>')}</p>" for p in parts
    )


zh = parse_xml(
    r"D:\AndroidStudioProjects\FortuneDiary\feature\setting\pal\src\commonMain\composeResources\values-zh\strings_legal.xml"
)
en = parse_xml(
    r"D:\AndroidStudioProjects\FortuneDiary\feature\setting\pal\src\commonMain\composeResources\values\strings_legal.xml"
)
APP_ZH, APP_EN, VER = "保管（PolicyPal）", "PolicyPal (保管)", "1.0.0"


def sections(lang, prefix, app):
    d = zh if lang == "zh" else en
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


def page(doc, title_zh, title_en, zh_secs, en_secs, other_href, other_label_zh, other_label_en):
    meta_zh = fill(zh["legal_document_meta"], APP_ZH, VER)
    meta_en = fill(en["legal_document_meta"], APP_EN, VER)
    notice_zh = zh["legal_builtin_notice"]
    notice_en = en["legal_builtin_notice"]
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title_zh)} · PolicyPal · Panda Studio</title>
  <meta name="description" content="{html.escape(title_en)} for PolicyPal by Hangzhou Panda Studio Technology Co., Ltd.">
  <link rel="canonical" href="https://pandastudio.hk/legal/policypal/{doc}.html">
  <link rel="stylesheet" href="../../assets/site.css">
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
      <p class="muted-note"><a href="./">PolicyPal · 法律文档</a> · <a href="{other_href}">{html.escape(other_label_zh)} / {html.escape(other_label_en)}</a></p>
      <section class="lang-block" lang="zh-CN">
        <p class="lang-label">中文（正式）</p>
        <h1>{html.escape(title_zh)}</h1>
        <p class="meta">{html.escape(meta_zh)}</p>
        <p class="muted-note">{html.escape(notice_zh)}</p>
        {zh_secs}
      </section>
      <section class="lang-block" lang="en">
        <p class="lang-label">English</p>
        <h1>{html.escape(title_en)}</h1>
        <p class="meta">{html.escape(meta_en)}</p>
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


out = pathlib.Path(r"d:\Projects\PandaStudio\legal\policypal")
out.mkdir(parents=True, exist_ok=True)
(out / "privacy.html").write_text(
    page(
        "privacy",
        "隐私政策",
        "Privacy Policy",
        sections("zh", "legal_privacy", APP_ZH),
        sections("en", "legal_privacy", APP_EN),
        "terms.html",
        "用户协议与免责声明",
        "Terms",
    ),
    encoding="utf-8",
)
(out / "terms.html").write_text(
    page(
        "terms",
        "用户协议与免责声明",
        "Terms of Service and Disclaimer",
        sections("zh", "legal_terms", APP_ZH),
        sections("en", "legal_terms", APP_EN),
        "privacy.html",
        "隐私政策",
        "Privacy Policy",
    ),
    encoding="utf-8",
)
print("ok", (out / "privacy.html").stat().st_size, (out / "terms.html").stat().st_size)
