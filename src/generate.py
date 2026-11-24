# -*- coding: utf-8 -*-
"""Static generator for AppRank Toolkit."""
from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C
import locales as L

ROOT = Path(__file__).resolve().parent.parent

STYLE = (
    ":root{--fg:#15181d;--muted:#5c6672;--line:#dfe4ea;--accent:#1f6feb;--accent2:#0b7285;"
    "--paper:#fbfcfe;--card:#ffffff;--soft:#eef4ff;--serif:Georgia,serif}"
    "*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--fg);"
    "font-family:system-ui,-apple-system,'Segoe UI',sans-serif;line-height:1.6}"
    "a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}"
    ".wrap{max-width:1060px;margin:0 auto;padding:0 24px}header{border-bottom:1px solid var(--line);"
    "background:#fff;position:sticky;top:0;z-index:5}header .wrap{display:flex;gap:16px;align-items:center;"
    "justify-content:space-between;min-height:64px;flex-wrap:wrap}.brand{font-weight:800;letter-spacing:-.02em;"
    "font-size:1.05rem;color:var(--fg)}nav{display:flex;gap:14px;flex-wrap:wrap;font-size:.9rem}"
    ".langs{display:flex;gap:10px;flex-wrap:wrap;font-size:.82rem;padding:10px 0;border-bottom:1px solid var(--line)}"
    ".langs a[aria-current=page]{font-weight:800;color:var(--fg)}"
    ".hero{padding:64px 0 42px;border-bottom:1px solid var(--line)}.eyebrow{color:var(--accent2);"
    "font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;font-weight:800}"
    "h1{font-family:var(--serif);font-size:3rem;line-height:1.1;margin:.35em 0 .4em;letter-spacing:-.02em}"
    "h2{font-size:1.4rem;margin:2.2rem 0 .8rem}.lead{font-size:1.15rem;color:var(--muted);max-width:720px}"
    ".grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px;margin:28px 0}"
    ".card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px;"
    "box-shadow:0 6px 20px rgba(20,30,50,.04)}.card h3{margin:0 0 .4rem;font-size:1.1rem}"
    ".card p{color:var(--muted);margin:.3rem 0 1rem}.pill{display:inline-block;background:var(--soft);"
    "color:var(--accent2);border-radius:999px;padding:.2rem .7rem;font-size:.76rem;font-weight:700}"
    "form{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin-top:18px}"
    "label{display:block;font-size:.82rem;color:var(--muted);margin-bottom:5px}input,select{width:100%;"
    "padding:10px 12px;border:1px solid var(--line);border-radius:9px;background:#fff;font:inherit}"
    "button{grid-column:1/-1;border:0;background:var(--accent);color:#fff;border-radius:9px;padding:12px 16px;"
    "font:inherit;font-weight:700;cursor:pointer}.result{margin-top:20px;padding:18px;border-radius:10px;"
    "background:var(--soft);border:1px solid #cfe0ff;min-height:58px;font-weight:600}"
    "table{width:100%;border-collapse:collapse;font-size:.9rem}th,td{text-align:left;padding:10px 8px;"
    "border-bottom:1px solid var(--line)}th{color:var(--muted);font-size:.78rem;text-transform:uppercase;"
    "letter-spacing:.04em}.note{color:var(--muted);font-size:.88rem}code{background:#f1f3f6;padding:2px 6px;"
    "border-radius:5px}footer{border-top:1px solid var(--line);margin-top:56px;padding:28px 0 48px;"
    "color:var(--muted);font-size:.85rem}@media(max-width:640px){h1{font-size:2.2rem}.hero{padding:40px 0 30px}}"
)

JS_HEAD = """
const DATA=__DATA__;
const T=__T__;
const CFG=__CFG__;
const money=n=>new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:2}).format(n);
const num=n=>new Intl.NumberFormat('en-US',{maximumFractionDigits:1}).format(n);
function band(r){r=Number(r)||1;if(r<=1)return 1;if(r<=3)return .75;if(r<=10)return .45;if(r<=20)return .25;if(r<=30)return .12;return .05;}
function put(html){document.getElementById('result').innerHTML=html;}
"""

JS = {
    "rank-change": JS_HEAD + """
function run(){const p=Number(document.getElementById('prev').value);const c=Number(document.getElementById('curr').value);
if(!p||!c){put(T.scenario_note);return;}const d=p-c;let msg=d>0?T.improved.replace('{n}',d):d<0?T.declined.replace('{n}',Math.abs(d)):T.no_change;put(T.result+': '+msg);}
document.getElementById('tool-form').addEventListener('submit',e=>{e.preventDefault();run();});run();
""",
    "revenue-estimator": JS_HEAD + """
function run(){const rank=Number(document.getElementById('rank').value)||1;const base=Number(document.getElementById('downloads').value)||0;
const conv=Number(document.getElementById('conversion').value)||0;const price=Number(document.getElementById('price').value)||0;
const tier=document.getElementById('tier').value;const rate=CFG.fees[tier];const downloads=base*band(rank);const paying=downloads*conv/100;
const gross=paying*price;const net=gross*(1-rate);put(T.gross+': '+money(gross)+' · '+T.net+': '+money(net)+'<br><span class="note">'+T.scenario_note+'</span>');}
document.getElementById('tool-form').addEventListener('submit',e=>{e.preventDefault();run();});run();
""",
    "market-compare": JS_HEAD + """
function run(){const a=document.getElementById('a').value,b=document.getElementById('b').value,ch=document.getElementById('chart').value;
const ra=DATA.markets[a].charts[ch].rows,rb=DATA.markets[b].charts[ch].rows;
const ids=new Set(ra.map(r=>r.app_id));const shared=rb.filter(r=>ids.has(r.app_id));
const names=shared.length?shared.map(r=>htmlEscape(r.name)).join(', '):T.no_overlap;
put(T.overlap+': '+shared.length+'/10<br>'+T.shared_apps+': '+names);}
function htmlEscape(s){const d=document.createElement('div');d.textContent=s;return d.innerHTML;}
document.getElementById('tool-form').addEventListener('submit',e=>{e.preventDefault();run();});run();
""",
    "fee-calculator": JS_HEAD + """
function run(){const gross=Number(document.getElementById('gross').value)||0;const tier=document.getElementById('tier').value;
const rate=CFG.fees[tier];const net=gross*(1-rate);put(T.fee_gross+': '+money(gross)+' · '+T.net_revenue+': '+money(net));}
document.getElementById('tool-form').addEventListener('submit',e=>{e.preventDefault();run();});run();
""",
}

TOOL_SLUGS = C.TOOLS


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def script_json(value) -> str:
    return json.dumps(value, ensure_ascii=False).replace("</", "<\\/")


def hreflang_tags(mapping: dict[str, str]) -> str:
    parts = []
    for lang, url in mapping.items():
        code = "x-default" if lang == "x-default" else C.HREFLANG.get(lang, lang)
        parts.append(f'<link rel="alternate" hreflang="{code}" href="{esc(url)}"/>')
    return "\n".join(parts)


def alternates(path: str, base: str) -> dict[str, str]:
    mapping = {lang: base + ("" if lang == "en" else f"/{lang}") + path for lang in C.LANGS}
    mapping["x-default"] = base + path
    return mapping


def language_nav(lang: str, path: str, base: str) -> str:
    links = []
    for code in C.LANGS:
        href = base + ("" if code == "en" else f"/{code}") + path
        current = ' aria-current="page"' if code == lang else ""
        links.append(f'<a href="{esc(href)}"{current}>{esc(code.upper())}</a>')
    return '<div class="langs">' + "".join(links) + "</div>"


def strip_lang_prefix(path: str, lang: str) -> str:
    if lang == "en":
        return path
    prefix = f"/{lang}"
    if path == prefix:
        return "/"
    if path.startswith(prefix + "/"):
        return path[len(prefix):]
    return path


def page(title: str, description: str, path: str, body: str, lang: str,
         base: str, script: str = "", schema: dict | None = None) -> str:
    t = L.get(lang)
    logical = strip_lang_prefix(path, lang)
    alts = hreflang_tags(alternates(logical, base))
    ld = ""
    if schema:
        ld = '<script type="application/ld+json">' + script_json(schema) + "</script>"
    return f"""<!doctype html>
<html lang="{esc(lang)}">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}"/>
<meta name="robots" content="index,follow"/>
<link rel="canonical" href="{esc(base + path)}"/>
{alts}
<style>{STYLE}</style>
{ld}
</head>
<body>
<header><div class="wrap"><a class="brand" href="{esc(base + ('' if lang=='en' else '/'+lang) + '/')}">{esc(C.SITE_NAME)}</a>
<nav><a href="{esc(base + ('' if lang=='en' else '/'+lang) + '/')}">Home</a><a href="{esc(base + ('' if lang=='en' else '/'+lang) + '/methodology/')}">{esc(t['method_title'])}</a></nav></div></header>
{language_nav(lang, logical, base)}
<main>{body}</main>
<footer><div class="wrap">{esc(t['footer_note'])} · {esc(C.AUTHOR)} · <a href="{esc(C.API_BASE)}">{esc(t['source'])}</a></div></footer>
{('<script>' + script + '</script>') if script else ''}
</body>
</html>
"""


def rank_result(prev, curr) -> str:
    if prev in (None, "", 0) or curr in (None, "", 0):
        return "new"
    delta = int(prev) - int(curr)
    return "up" if delta > 0 else "down" if delta < 0 else "flat"


def revenue_scenario(rank: int, downloads_base: float, conversion: float,
                     price: float, fee_rate: float) -> dict:
    mult = 1.0 if rank <= 1 else .75 if rank <= 3 else .45 if rank <= 10 else .25 if rank <= 20 else .12 if rank <= 30 else .05
    downloads = downloads_base * mult
    paying = downloads * conversion / 100
    gross = paying * price
    return {"multiplier": mult, "downloads": downloads, "paying": paying,
            "gross": gross, "net": gross * (1 - fee_rate)}


def compare_markets(snapshot: dict, market_a: str, market_b: str, chart: str) -> dict:
    ra = snapshot["markets"][market_a]["charts"][chart]["rows"]
    rb = snapshot["markets"][market_b]["charts"][chart]["rows"]
    ids = {r["app_id"] for r in ra}
    shared = [r for r in rb if r["app_id"] in ids]
    return {"overlap": len(shared), "shared": shared}


def fee_scenario(gross: float, fee_rate: float) -> dict:
    return {"gross": gross, "fee": gross * fee_rate, "net": gross * (1 - fee_rate)}


def form_html(lang: str, slug: str, snapshot: dict) -> str:
    t = L.get(lang)
    common = f'<button type="submit">{esc(t["calculate"])}</button>'
    if slug == "rank-change":
        return f'<form id="tool-form"><div><label>{esc(t["prev_rank"])}</label><input id="prev" type="number" min="1" value="12"/></div><div><label>{esc(t["curr_rank"])}</label><input id="curr" type="number" min="1" value="7"/></div>{common}</form>'
    if slug == "revenue-estimator":
        opts = "".join(f'<option value="{key}">{esc(val)}</option>' for key, val in C.FEE_RATES.items())
        return (f'<form id="tool-form"><div><label>{esc(t["rank_band"])}</label><input id="rank" type="number" min="1" value="8"/></div>'
                f'<div><label>{esc(t["downloads"])}</label><input id="downloads" type="number" min="0" value="50000"/></div>'
                f'<div><label>{esc(t["conversion"])}</label><input id="conversion" type="number" min="0" max="100" value="4"/></div>'
                f'<div><label>{esc(t["price"])}</label><input id="price" type="number" min="0" step="0.01" value="4.99"/></div>'
                f'<div><label>{esc(t["tier"])}</label><select id="tier">{opts}</select></div>{common}</form>')
    if slug == "market-compare":
        markets = "".join(f'<option value="{m}">{esc(C.market_name(m, lang))}</option>' for m in C.MARKETS)
        markets_b = "".join(f'<option value="{m}">{esc(C.market_name(m, lang))}</option>' for m in C.MARKETS if m != "gb")
        charts = "".join(f'<option value="{c}">{esc(t[c])}</option>' for c in C.CHARTS)
        return (f'<form id="tool-form"><div><label>{esc(t["market_a"])}</label><select id="a">{markets}</select></div>'
                f'<div><label>{esc(t["market_b"])}</label><select id="b"><option value="gb">{esc(C.market_name("gb", lang))}</option>{markets_b}</select></div>'
                f'<div><label>{esc(t["chart"])}</label><select id="chart">{charts}</select></div>{common}</form>')
    opts = "".join(f'<option value="{key}">{esc(t[key])}</option>' for key in C.FEE_RATES)
    return (f'<form id="tool-form"><div><label>{esc(t["fee_gross"])}</label><input id="gross" type="number" min="0" step="0.01" value="10000"/></div>'
            f'<div><label>{esc(t["tier"])}</label><select id="tier">{opts}</select></div>{common}</form>')


def reference_table(lang: str, snapshot: dict) -> str:
    rows = snapshot["markets"]["us"]["charts"]["free"]["rows"][:5]
    body = "".join(f'<tr><td>{esc(r["rank"])}</td><td>{esc(r["name"])}</td><td>{esc(r["developer"])}</td><td>{esc(r["rating"])}</td></tr>' for r in rows)
    return f'<h2>{esc(L.get(lang)["source"])} · United States · {esc(L.get(lang)["free"])}</h2><table><thead><tr><th>#</th><th>App</th><th>Developer</th><th>Rating</th></tr></thead><tbody>{body}</tbody></table>'


def build_site(snapshot: dict, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    base = C.BASE_URL
    paths = []
    for lang in C.LANGS:
        t = L.get(lang)
        prefix = "" if lang == "en" else f"/{lang}"
        home_path = prefix + "/"
        cards = []
        for slug in TOOL_SLUGS:
            desc_key = {"rank-change": "rank_desc", "revenue-estimator": "rev_desc",
                        "market-compare": "cmp_desc", "fee-calculator": "fee_desc"}[slug]
            title_key = {"rank-change": "rank_title", "revenue-estimator": "rev_title",
                         "market-compare": "cmp_title", "fee-calculator": "fee_title"}[slug]
            href = base + prefix + f"/tools/{slug}/"
            cards.append(f'<article class="card"><span class="pill">{esc(t["tool_label"])}</span><h3>{esc(t[title_key])}</h3><p>{esc(t[desc_key])}</p><a href="{esc(href)}">{esc(t["open"])} →</a></article>')
        body = (f'<section class="hero"><div class="wrap"><span class="eyebrow">{esc(t["home_eyebrow"])}</span>'
                f'<h1>{esc(t["home_h1"])}</h1><p class="lead">{esc(t["home_sub"])}</p>'
                f'<p class="note">{esc(t["data_fresh"].format(date=snapshot["date"]))} · <a href="{esc(base+prefix+"/methodology/")}">{esc(t["method_hint"])}</a></p></div></section>'
                f'<div class="wrap"><div class="grid">{"".join(cards)}</div>{reference_table(lang, snapshot)}</div>')
        schema = {"@context": "https://schema.org", "@type": "WebSite", "name": C.SITE_NAME,
                  "url": base + home_path, "publisher": {"@type": "Organization", "name": C.AUTHOR}}
        (out / home_path.strip("/") / "index.html").parent.mkdir(parents=True, exist_ok=True)
        (out / home_path.strip("/") / "index.html").write_text(
            page(f"{C.WORK_TITLE} — {C.SITE_NAME}", t["home_sub"], home_path, body, lang, base, schema=schema), encoding="utf-8")
        paths.append(home_path)

        for slug in TOOL_SLUGS:
            title_key = {"rank-change": "rank_title", "revenue-estimator": "rev_title",
                         "market-compare": "cmp_title", "fee-calculator": "fee_title"}[slug]
            desc_key = {"rank-change": "rank_desc", "revenue-estimator": "rev_desc",
                        "market-compare": "cmp_desc", "fee-calculator": "fee_desc"}[slug]
            tool_path = prefix + f"/tools/{slug}/"
            body = (f'<section class="hero"><div class="wrap"><span class="eyebrow">{esc(t["tool_label"])}</span>'
                    f'<h1>{esc(t[title_key])}</h1><p class="lead">{esc(t[desc_key])}</p></div></section>'
                    f'<div class="wrap"><div class="card">{form_html(lang, slug, snapshot)}<div id="result" class="result"></div>'
                    f'<p class="note">{esc(t["scenario_note"])}</p></div><p class="note">{esc(t["disclosure"])}</p></div>')
            script = JS[slug].replace("__DATA__", script_json(snapshot)).replace("__T__", script_json(t)).replace(
                "__CFG__", script_json({"fees": C.FEE_RATES}))
            schema = {"@context": "https://schema.org", "@type": "WebApplication", "name": t[title_key],
                      "url": base + tool_path, "applicationCategory": "UtilitiesApplication",
                      "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
                      "publisher": {"@type": "Organization", "name": C.AUTHOR}}
            dest = out / tool_path.strip("/") / "index.html"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(page(t[title_key], t[desc_key], tool_path, body, lang, base, script=script, schema=schema), encoding="utf-8")
            paths.append(tool_path)

        method_path = prefix + "/methodology/"
        method_body = (f'<section class="hero"><div class="wrap"><span class="eyebrow">{esc(t["method_title"])}</span>'
                       f'<h1>{esc(t["method_title"])}</h1><p class="lead">{esc(t["method_desc"])}</p></div></section>'
                       f'<div class="wrap"><div class="card"><h2>1. {esc(t["source"])}</h2><p><a href="{esc(C.API_BASE)}">{esc(C.API_BASE)}</a></p>'
                       f'<h2>2. Rank bands</h2><p><code>1→1.0, 3→0.75, 10→0.45, 20→0.25, 30→0.12, worse→0.05</code></p>'
                       f'<h2>3. Revenue</h2><p><code>gross = downloads × multiplier × conversion × price</code>; <code>net = gross × (1 - fee)</code></p>'
                       f'<h2>4. Limits</h2><p>{esc(t["scenario_note"])}</p></div></div>')
        dest = out / method_path.strip("/") / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page(t["method_title"], t["method_desc"], method_path, method_body, lang, base), encoding="utf-8")
        paths.append(method_path)

    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap += [f"  <url><loc>{esc(base + p)}</loc></url>" for p in paths]
    sitemap.append("</urlset>")
    (out / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n", encoding="utf-8")
    print(f"[done] {len(paths)} indexable URLs -> {out}/")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", default="data/snapshot.json")
    parser.add_argument("--out", default="site")
    args = parser.parse_args()
    snapshot = json.loads(Path(args.snapshot).read_text(encoding="utf-8"))
    build_site(snapshot, Path(args.out))


if __name__ == "__main__":
    main()
