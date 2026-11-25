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
import content as K

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
    ".actions{grid-column:1/-1;display:flex;gap:10px}.actions button{flex:1;grid-column:auto}"
    ".ghost{background:#fff!important;color:var(--fg)!important;border:1px solid var(--line)!important}"
    ".res-head{margin:0 0 10px;font-size:1rem}.bad{color:#b42318;margin:0;font-weight:600}"
    ".result table.res{font-size:.92rem}.result table.res td{border-bottom:1px solid var(--line);padding:8px 6px}"
    ".result table.res td:last-child{text-align:right;font-variant-numeric:tabular-nums}"
    ".result h3{font-size:.95rem;margin:14px 0 6px}"
    "button{grid-column:1/-1;border:0;background:var(--accent);color:#fff;border-radius:9px;padding:12px 16px;"
    "font:inherit;font-weight:700;cursor:pointer}.result{margin-top:20px;padding:18px;border-radius:10px;"
    "background:var(--soft);border:1px solid #cfe0ff;min-height:58px;font-weight:600}"
    "table{width:100%;border-collapse:collapse;font-size:.9rem}th,td{text-align:left;padding:10px 8px;"
    "border-bottom:1px solid var(--line)}th{color:var(--muted);font-size:.78rem;text-transform:uppercase;"
    "letter-spacing:.04em}.note{color:var(--muted);font-size:.88rem}code{background:#f1f3f6;padding:2px 6px;"
    "border-radius:5px}.editorial{display:flex;gap:14px;flex-wrap:wrap;font-size:.88rem;margin:22px 0 8px}"
    ".editorial a{color:var(--accent2)}.crumbs{font-size:.84rem;color:var(--muted);padding:18px 0 0}"
    ".crumbs a{color:var(--muted)}.crumbs span{color:var(--fg);font-weight:600}"
    ".rel{font-size:.9rem;margin:6px 0 26px}.rel a{color:var(--accent2)}.prose{max-width:760px;margin:26px 0}.prose section{margin:0 0 22px}.prose h2{font-size:1.15rem;"
    "margin:0 0 .4rem;color:var(--fg)}.prose p{color:var(--muted);margin:0}"
    "footer{border-top:1px solid var(--line);margin-top:56px;padding:28px 0 48px;"
    "color:var(--muted);font-size:.85rem}@media(max-width:640px){h1{font-size:2.2rem}.hero{padding:40px 0 30px}}"
)

JS_HEAD = """
const DATA=__DATA__;
const T=__T__;
const CFG=__CFG__;
const money=n=>new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:2}).format(n);
const num=n=>new Intl.NumberFormat('en-US',{maximumFractionDigits:1}).format(n);
function band(r){r=Number(r)||1;const bands=CFG.rank_bands;for(const [ceil,mult] of bands){if(r<=ceil)return mult;}return CFG.floor;}
const foot='<p class="note"><a href="'+CFG.method+'">'+T.method_title+'</a></p>';
function put(html){document.getElementById('result').innerHTML=html+foot;}
const row=(k,v)=>'<tr><td>'+k+'</td><td>'+v+'</td></tr>';
const tbl=rows=>'<table class="res">'+rows+'</table>';
const bad=m=>'<p class="bad">'+m+'</p>';
const head=m=>'<p class="res-head">'+m+'</p>';
const val=id=>{const s=document.getElementById(id).value.trim();return s===''?NaN:Number(s);};
function bind(run){const f=document.getElementById('tool-form');
f.addEventListener('submit',e=>{e.preventDefault();run();});
f.addEventListener('reset',()=>setTimeout(run,0));run();}
"""

JS = {
    "rank-change": JS_HEAD + """
function run(){const p=val('prev'),c=val('curr');
if(!(p>=1)||!(c>=1)){put(bad(T.invalid_input));return;}
const d=p-c,msg=d>0?T.improved.replace('{n}',d):d<0?T.declined.replace('{n}',Math.abs(d)):T.no_change;
const mb=band(p),mc=band(c);
put(head(T.result+': '+msg)+tbl(row(T.band_multiplier,mb+' \u2192 '+mc)+row(T.visibility,(mc/mb).toFixed(2)+'\u00d7')));}
bind(run);
""",
    "revenue-estimator": JS_HEAD + """
function run(){const rank=val('rank'),base=val('downloads'),conv=val('conversion'),price=val('price');
if(!(rank>=1)||!(conv>=0)||!(conv<=100)||!(base>=0)){put(bad(T.invalid_input));return;}
const rate=CFG.fees[document.getElementById('tier').value];
const downloads=base*band(rank),paying=downloads*conv/100,gross=paying*price,fee=gross*rate,net=gross-fee;
put(head(T.net+': '+money(net))+tbl(row(T.downloads_after,num(downloads))+row(T.paying_users,num(paying))+row(T.gross,money(gross))+row(T.fee_amount,money(fee))+row(T.arpu,money(downloads?gross/downloads:0))));}
bind(run);
""",
    "market-compare": JS_HEAD + """
function run(){const a=document.getElementById('a').value,b=document.getElementById('b').value,ch=document.getElementById('chart').value;
const ma=DATA.markets[a]&&DATA.markets[a].charts[ch],mb=DATA.markets[b]&&DATA.markets[b].charts[ch];
if(!ma||!mb){put(bad(T.invalid_input));return;}
const ra=ma.rows,rb=mb.rows,ids=new Set(ra.map(r=>r.app_id));
const shared=rb.filter(r=>ids.has(r.app_id));
const rows=shared.slice(0,10).map(r=>{const o=ra.find(x=>x.app_id===r.app_id);return row(htmlEscape(r.name),'#'+o.rank+' \u2192 #'+r.rank);}).join('');
put(head(T.overlap+': '+shared.length+'/10')+(rows?'<table class="res">'+rows+'</table>':bad(T.no_overlap)));}
function htmlEscape(s){const d=document.createElement('div');d.textContent=s;return d.innerHTML;}
bind(run);
""",
    "fee-calculator": JS_HEAD + """
function run(){const gross=val('gross');
if(!(gross>=0)){put(bad(T.invalid_input));return;}
const rate=CFG.fees[document.getElementById('tier').value],fee=gross*rate,net=gross-fee;
const cmp=Object.entries(CFG.fees).map(([k,r])=>row(T[k],money(gross*(1-r)))).join('');
put(head(T.net_revenue+': '+money(net))+tbl(row(T.fee_gross,money(gross))+row(T.fee_amount,money(fee)))+'<h3>'+T.tier_compare+'</h3>'+tbl(cmp));}
bind(run);
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


def crumbs_html(items: list[tuple[str, str]]) -> str:
    parts = [f'<a href="{esc(h)}">{esc(l)}</a>' if h else f'<span>{esc(l)}</span>' for l, h in items]
    return '<div class="wrap"><nav class="crumbs">' + ' / '.join(parts) + "</nav></div>"


def breadcrumb_schema(items: list[tuple[str, str]], base: str) -> dict:
    entries = []
    for i, (label, href) in enumerate(items, start=1):
        entry = {"@type": "ListItem", "position": i, "name": label}
        if href:
            entry["item"] = base + href
        entries.append(entry)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": entries}


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
         base: str, script: str = "", schema: dict | None = None,
         noindex: bool = False) -> str:
    t = L.get(lang)
    logical = strip_lang_prefix(path, lang)
    alts = "" if noindex else hreflang_tags(alternates(logical, base))
    ld = ""
    if schema and not noindex:
        for item in (schema if isinstance(schema, list) else [schema]):
            ld += '<script type="application/ld+json">' + script_json(item) + "</script>"
    return f"""<!doctype html>
<html lang="{esc(lang)}">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}"/>
<meta name="robots" content="{'noindex,follow' if noindex else 'index,follow'}"/>
<link rel="canonical" href="{esc(base + path)}"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="{esc(C.SITE_NAME)}"/>
<meta property="og:title" content="{esc(title)}"/>
<meta property="og:description" content="{esc(description)}"/>
<meta property="og:url" content="{esc(base + path)}"/>
<meta property="og:locale" content="{esc(C.HREFLANG.get(lang, lang).replace('-', '_'))}"/>
<meta name="twitter:card" content="summary"/>
<meta name="twitter:title" content="{esc(title)}"/>
<meta name="twitter:description" content="{esc(description)}"/>
{alts}
<style>{STYLE}</style>
{ld}
</head>
<body>
<header><div class="wrap"><a class="brand" href="{esc(base + ('' if lang=='en' else '/'+lang) + '/')}">{esc(C.SITE_NAME)}</a>
<nav><a href="{esc(base + ('' if lang=='en' else '/'+lang) + '/')}">Home</a><a href="{esc(base + ('' if lang=='en' else '/'+lang) + '/methodology/')}">{esc(t['method_title'])}</a></nav></div></header>
{'<div class="wrap">' + language_nav(lang, logical, base) + '</div>'}
<main>{body}</main>
<footer><div class="wrap">{esc(t['footer_note'])} · {esc(C.AUTHOR)} · <a href="{esc(C.API_BASE)}">{esc(t['source'])}</a></div></footer>
{('<script>' + script + '</script>') if script else ''}
</body>
</html>
"""


def not_found_page(base: str) -> str:
    """404 页面：未知路径返回真 404，避免整站软 404。"""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Page not found — {esc(C.SITE_NAME)}</title>
<meta name="robots" content="noindex,follow"/>
<meta name="description" content="This page does not exist."/>
<meta name="twitter:card" content="summary"/>
<style>{STYLE}</style>
</head>
<body>
<header><div class="wrap"><a class="brand" href="{esc(base)}/">{esc(C.SITE_NAME)}</a>
<nav><a href="{esc(base)}/">Home</a><a href="{esc(base)}/methodology/">{esc(L.get('en')['method_title'])}</a></nav></div></header>
<main><div class="wrap">
<p class="eyebrow">404</p>
<h1>That page is not here</h1>
<p class="lead">The URL you opened does not match any page on this site. It may have moved, or the app or market you were looking for was never published.</p>
<p>Try one of these instead:</p>
<ul>
<li><a href="{esc(base)}/">All calculators and guides</a></li>
<li><a href="{esc(base)}/tools/rank-change/">Rank change calculator</a></li>
<li><a href="{esc(base)}/markets/">Market rankings</a></li>
<li><a href="{esc(base)}/movers/">Rank movers</a></li>
</ul>
</div></main>
<footer><div class="wrap">{esc(L.get('en')['footer_note'])} · {esc(C.AUTHOR)}</div></footer>
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
    mult = C.rank_multiplier(rank)
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
    actions = (f'<div class="actions"><button type="submit">{esc(t["calculate"])}</button>'
               f'<button type="reset" class="ghost">{esc(t["reset_label"])}</button></div>')
    noscript = f'<noscript><p class="note">{esc(t["fallback"])}</p></noscript>'
    if slug == "rank-change":
        return (f'<form id="tool-form">'
                f'<div><label for="prev">{esc(t["prev_rank"])}</label><input id="prev" name="prev" type="number" min="1" step="1" value="12"/></div>'
                f'<div><label for="curr">{esc(t["curr_rank"])}</label><input id="curr" name="curr" type="number" min="1" step="1" value="7"/></div>'
                f'{actions}</form>{noscript}')
    if slug == "revenue-estimator":
        opts = "".join(f'<option value="{key}">{esc(t[key])}</option>' for key in C.FEE_RATES)
        return (f'<form id="tool-form"><div><label for="rank">{esc(t["rank_band"])}</label>'
                f'<input id="rank" name="rank" type="number" min="1" step="1" value="8"/></div>'
                f'<div><label for="downloads">{esc(t["downloads"])}</label>'
                f'<input id="downloads" name="downloads" type="number" min="0" step="1000" value="50000"/></div>'
                f'<div><label for="conversion">{esc(t["conversion"])}</label>'
                f'<input id="conversion" name="conversion" type="number" min="0" max="100" step="0.1" value="4"/></div>'
                f'<div><label for="price">{esc(t["price"])}</label>'
                f'<input id="price" name="price" type="number" min="0" step="0.01" value="4.99"/></div>'
                f'<div><label for="tier">{esc(t["tier"])}</label><select id="tier" name="tier">{opts}</select></div>'
                f'{actions}</form>{noscript}')
    if slug == "market-compare":
        markets = "".join(f'<option value="{m}">{esc(C.market_name(m, lang))}</option>' for m in C.MARKETS)
        markets_b = "".join(f'<option value="{m}">{esc(C.market_name(m, lang))}</option>' for m in C.MARKETS if m != "gb")
        charts = "".join(f'<option value="{c}">{esc(t[c])}</option>' for c in C.CHARTS)
        return (f'<form id="tool-form"><div><label for="a">{esc(t["market_a"])}</label><select id="a" name="a">{markets}</select></div>'
                f'<div><label for="b">{esc(t["market_b"])}</label><select id="b" name="b"><option value="gb">{esc(C.market_name("gb", lang))}</option>{markets_b}</select></div>'
                f'<div><label for="chart">{esc(t["chart"])}</label><select id="chart" name="chart">{charts}</select></div>'
                f'{actions}</form>{noscript}')
    opts = "".join(f'<option value="{key}">{esc(t[key])}</option>' for key in C.FEE_RATES)
    return (f'<form id="tool-form"><div><label for="gross">{esc(t["fee_gross"])}</label>'
            f'<input id="gross" name="gross" type="number" min="0" step="0.01" value="10000"/></div>'
            f'<div><label for="tier">{esc(t["tier"])}</label><select id="tier" name="tier">{opts}</select></div>'
            f'{actions}</form>{noscript}')


TOOL_COPY_KEYS = {
    "rank-change": ("rank_how", "rank_use", "rank_ex", "rank_faq"),
    "revenue-estimator": ("rev_how", "rev_use", "rev_ex", "rev_faq"),
    "market-compare": ("cmp_how", "cmp_use", "cmp_ex", "cmp_faq"),
    "fee-calculator": ("fee_how", "fee_use", "fee_ex", "fee_faq"),
}


TOOL_TITLE_KEYS = {"rank-change": "rank_title", "revenue-estimator": "rev_title",
                   "market-compare": "cmp_title", "fee-calculator": "fee_title"}


def related_tools(lang: str, prefix: str, base: str, exclude: str = "") -> str:
    t = L.get(lang)
    gc = K.GUIDES[lang]
    links = [f'<a href="{esc(base + prefix + "/tools/" + s + "/")}">{esc(t[TOOL_TITLE_KEYS[s]])}</a>'
             for s in TOOL_SLUGS if s != exclude]
    links.append(f'<a href="{esc(base + prefix + "/guides/")}">{esc(gc["guides_h1"])}</a>')
    links.append(f'<a href="{esc(base + prefix + "/markets/")}">{esc(t["markets_title"])}</a>')
    links.append(f'<a href="{esc(base + prefix + "/movers/")}">{esc(t["movers_title"])}</a>')
    links.append(f'<a href="https://apprank.pages.dev/">{esc(t["charts_live"])}</a>')
    return f'<h2>{esc(t["tool_label"])}</h2><p class="rel">{" · ".join(links)}</p>'


def tool_prose(lang: str, slug: str) -> str:
    t = L.get(lang)
    how, use, ex, faq = TOOL_COPY_KEYS[slug]
    def section(key: str, body: str) -> str:
        return f'<section><h2>{esc(t[key])}</h2><p>{esc(body)}</p></section>'
    return (
        '<div class="prose">'
        + section("what_title", t[how])
        + section("use_title", t[use])
        + section("example_title", t[ex])
        + section("faq_title", t[faq])
        + '<section><h2>' + esc(t["method_title"]) + '</h2><p>' + esc(t["limits_text"]) + '</p></section>'
        + '</div>'
    )


def reference_table(lang: str, snapshot: dict, prefix: str = "", base: str = "") -> str:
    t = L.get(lang)
    rows = snapshot["markets"]["us"]["charts"]["free"]["rows"][:5]
    body = "".join(f'<tr><td>{esc(r["rank"])}</td><td>{esc(r["name"])}</td><td>{esc(r["developer"])}</td><td>{esc(r["rating"])}</td></tr>' for r in rows)
    head = (f'<th>{esc(t["col_rank"])}</th><th>{esc(t["col_app"])}</th>'
            f'<th>{esc(t["col_developer"])}</th><th>{esc(t["col_rating"])}</th>')
    link = f'<a href="{esc(base + prefix + "/markets/us/")}">{esc(C.market_name("us", lang))} →</a>'
    return (f'<h2>{esc(t["source"])} · {esc(C.market_name("us", lang))} · {esc(t["free"])}</h2>'
            f'<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'
            f'<p class="note"><a href="{esc(base + prefix + "/markets/")}">{esc(t["markets_title"])} →</a> · {link}</p>')


def sparkline(points: list[dict], width: int = 560, height: int = 150) -> str:
    """Render a rank-history line chart as inline SVG. Lower rank = higher on the chart."""
    vals = [(p.get("date", ""), p.get("best_rank")) for p in points]
    vals = [(d, v) for d, v in vals if v is not None]
    if not vals:
        return '<p class="note">—</p>'
    ranks = [v for _, v in vals]
    lo, hi = min(ranks), max(ranks)
    if hi == lo:
        hi = lo + 1
    pad_l, pad_r, pad_t, pad_b = 34, 12, 12, 26
    plot_w, plot_h = width - pad_l - pad_r, height - pad_t - pad_b
    n = len(vals)
    def xy(i, v):
        x = pad_l + (plot_w * i / (n - 1) if n > 1 else plot_w / 2)
        y = pad_t + (v - lo) / (hi - lo) * plot_h
        return x, y
    coords = [xy(i, v) for i, (_, v) in enumerate(vals)]
    line = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f},{y:.1f}" for i, (x, y) in enumerate(coords))
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="#1f6feb"/>' for x, y in coords)
    grid = (f'<line x1="{pad_l}" y1="{pad_t}" x2="{width-pad_r}" y2="{pad_t}" stroke="#dfe4ea"/>'
            f'<line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{width-pad_r}" y2="{pad_t+plot_h}" stroke="#dfe4ea"/>'
            f'<text x="2" y="{pad_t+4}" font-size="10" fill="#5c6672">#{lo}</text>'
            f'<text x="2" y="{pad_t+plot_h+4}" font-size="10" fill="#5c6672">#{hi}</text>')
    first_date, last_date = vals[0][0], vals[-1][0]
    labels = (f'<text x="{pad_l}" y="{height-4}" font-size="10" fill="#5c6672">{esc(first_date)}</text>'
              f'<text x="{width-pad_r}" y="{height-4}" font-size="10" fill="#5c6672" text-anchor="end">{esc(last_date)}</text>')
    return (f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" '
            f'aria-label="Rank history from {esc(first_date)} to {esc(last_date)}">'
            f'{grid}<path d="{line}" fill="none" stroke="#1f6feb" stroke-width="2"/>{dots}{labels}</svg>')


def rank_movers(snapshot: dict) -> list[dict]:
    """Real 14-day movement per (market, chart, app): first vs last best_rank."""
    out = []
    for market, me in snapshot["markets"].items():
        for chart, ch in me.get("charts", {}).items():
            names = {r["app_id"]: r for r in ch.get("rows", [])}
            for app_id, pts in ch.get("trend", {}).items():
                clean = [p for p in pts if p.get("best_rank") is not None]
                if len(clean) < 2:
                    continue
                first, last = clean[0]["best_rank"], clean[-1]["best_rank"]
                best = min(p["best_rank"] for p in clean)
                worst = max(p["best_rank"] for p in clean)
                row = names.get(app_id, {})
                out.append({
                    "app_id": app_id, "name": row.get("name") or app_id,
                    "developer": row.get("developer", ""), "market": market,
                    "chart": chart, "first": first, "last": last,
                    "delta": first - last, "best": best, "worst": worst,
                    "swing": worst - best, "points": clean,
                })
    return out


def app_slug(market: str, chart: str, app_id: str) -> str:
    return f"{market}-{chart}-{app_id}"


def bands_text() -> str:
    parts = [f"{ceil}→{mult}" for ceil, mult in C.RANK_BANDS]
    parts.append(f"worse→{C.FLOOR_MULTIPLIER}")
    return ", ".join(parts)


def move_label(prev, curr) -> str:
    if prev in (None, "", 0):
        return "new"
    delta = int(prev) - int(curr)
    return "up" if delta > 0 else "down" if delta < 0 else "flat"


def chart_table(lang: str, rows: list[dict], market: str = "", chart: str = "",
                prefix: str = "", base: str = "") -> str:
    t = L.get(lang)
    headers = ("col_rank", "col_app", "col_developer", "col_rating", "col_ratings", "col_price", "col_move")
    head = "".join(f'<th>{esc(t[h])}</th>' for h in headers)
    body = []
    for r in rows:
        move = move_label(r.get("prev_rank"), r.get("rank"))
        move_text = t["move_" + move]
        price = t["price_free"] if not r.get("price") else f'{esc(r.get("price"))} {esc(r.get("currency", "USD"))}'
        rating = "—" if r.get("rating") in (None, "") else esc(r["rating"])
        count = "—" if r.get("rating_count") in (None, "") else esc(r["rating_count"])
        name = esc(r.get("name"))
        if market and chart and r.get("app_id"):
            href = base + prefix + f"/apps/{app_slug(market, chart, r['app_id'])}/"
            name = f'<a href="{esc(href)}">{name}</a>'
        body.append(
            f'<tr><td>{esc(r.get("rank"))}</td><td>{name}</td>'
            f'<td>{esc(r.get("developer"))}</td><td>{rating}</td><td>{count}</td>'
            f'<td>{price}</td><td>{esc(move_text)}</td></tr>'
        )
    return f'<table><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table>'


def market_index(lang: str, snapshot: dict) -> str:
    t = L.get(lang)
    cards = []
    for m in C.MARKETS:
        entry = snapshot["markets"].get(m)
        if not entry:
            continue
        free = entry["charts"].get("free", {}).get("rows", [])
        lead = esc(free[0]["name"]) if free else "—"
        cards.append(
            f'<article class="card"><span class="pill">{esc(C.market_name(m, lang))}</span>'
            f'<h3>#1 · {lead}</h3><p>{esc(t["free"])} / {esc(t["grossing"])} · {esc(t["data_fresh"].format(date=snapshot["date"]))}</p>'
            f'<a href="{m}/">{esc(t["open"])} →</a></article>'
        )
    return (
        f'<section class="hero"><div class="wrap"><span class="eyebrow">{esc(t["markets_title"])}</span>'
        f'<h1>{esc(t["markets_h1"])}</h1><p class="lead">{esc(t["markets_sub"])}</p></div></section>'
        f'<div class="wrap"><p class="note">{esc(t["markets_intro"])}</p>'
        f'<div class="grid">{"".join(cards)}</div></div>'
    )


def market_detail(lang: str, market: str, snapshot: dict,
                  prefix: str = "", base: str = "") -> str | None:
    entry = snapshot["markets"].get(market)
    if not entry:
        return None
    t = L.get(lang)
    name = C.market_name(market, lang)
    parts = []
    for chart in C.CHARTS:
        data = entry["charts"].get(chart)
        if not data or not data.get("rows"):
            continue
        parts.append(f'<h2>{esc(t[chart])}</h2>' + chart_table(lang, data["rows"], market, chart, prefix, base))
    return (
        f'<section class="hero"><div class="wrap"><span class="eyebrow">{esc(t["markets_title"])}</span>'
        f'<h1>{esc(t["market_h1"].format(market=name))}</h1>'
        f'<p class="lead">{esc(t["market_sub"].format(date=snapshot["date"]))}</p></div></section>'
        f'<div class="wrap"><p><a href="../">{esc("← " + t["back_markets"])}</a></p>'
        f'{"".join(parts)}'
        f'<p class="note">{esc(t["market_note"].format(date=snapshot["date"]))}</p></div>'
    )


def sections_html(sections) -> str:
    return "".join(f'<section><h2>{esc(h)}</h2><p>{esc(p)}</p></section>' for h, p in sections)


def movers_page(lang: str, snapshot: dict, prefix: str, base: str,
                movers: list[dict] | None = None) -> str:
    t = L.get(lang)
    if movers is None:
        movers = rank_movers(snapshot)
    def section(title: str, items: list[dict]) -> str:
        if not items:
            return ""
        rows = []
        for m in items:
            href = base + prefix + f"/apps/{app_slug(m['market'], m['chart'], m['app_id'])}/"
            where = f"{esc(C.market_name(m['market'], lang))} · {esc(t['chart_free_label'] if m['chart']=='free' else t['chart_grossing_label'])}"
            delta = m["delta"]
            delta_text = f"+{delta}" if delta > 0 else str(delta)
            rows.append(
                f'<tr><td><a href="{esc(href)}">{esc(m["name"])}</a></td><td>{esc(m["developer"])}</td>'
                f'<td>{esc(where)}</td><td>#{esc(m["best"])}</td><td>{esc(delta_text)}</td></tr>'
            )
        head = (f'<tr><th>{esc(t["col_app"])}</th><th>{esc(t["col_developer"])}</th>'
                f'<th>{esc(t["markets_title"])}</th><th>{esc(t["col_best"])}</th>'
                f'<th>{esc(t["col_change"])}</th></tr>')
        return f'<h2>{esc(title)}</h2><table><thead>{head}</thead><tbody>{"".join(rows)}</tbody></table>'
    risers = sorted([m for m in movers if m["delta"] > 0], key=lambda m: -m["delta"])[:10]
    fallers = sorted([m for m in movers if m["delta"] < 0], key=lambda m: m["delta"])[:10]
    volatile = sorted(movers, key=lambda m: -m["swing"])[:10]
    change = t["col_change"]
    return (
        f'<section class="hero"><div class="wrap"><span class="eyebrow">{esc(t["movers_title"])}</span>'
        f'<h1>{esc(t["movers_h1"])}</h1><p class="lead">{esc(t["movers_sub"])}</p></div></section>'
        f'<div class="wrap">{editorial_nav(lang, prefix, base, "movers")}'
        + section(t["move_up"] + " · " + change, risers)
        + section(t["move_down"] + " · " + change, fallers)
        + section(t["movers_h1"] + " · " + change, volatile)
        + f'<p class="note">{esc(t["movers_note"].format(date=snapshot["date"]))}</p></div>'
    )


def trend_page(lang: str, market: str, chart: str, app_id: str,
               snapshot: dict, prefix: str, base: str,
               movers: list[dict] | None = None) -> str | None:
    entry = snapshot["markets"].get(market, {}).get("charts", {}).get(chart)
    if not entry:
        return None
    pts = entry.get("trend", {}).get(app_id)
    if not pts:
        return None
    t = L.get(lang)
    row = next((r for r in entry.get("rows", []) if r["app_id"] == app_id), {})
    name = row.get("name") or app_id
    developer = row.get("developer", "")
    pool = movers if movers is not None else rank_movers(snapshot)
    key = (app_id, market, chart)
    index = {(m["app_id"], m["market"], m["chart"]): m for m in pool}
    mover = index.get(key)
    chart_label = t["chart_free_label"] if chart == "free" else t["chart_grossing_label"]
    meta = []
    if mover:
        meta.append(f'{esc(t["col_best"])}: #{esc(mover["best"])}')
        d = mover["delta"]
        meta.append(f'{esc(t["col_change"])}: {esc("+"+str(d) if d>0 else str(d))}')
    return (
        f'<section class="hero"><div class="wrap"><span class="eyebrow">{esc(t["trend_title"])}</span>'
        f'<h1>{esc(t["trend_h1"].format(app=name, market=C.market_name(market, lang)))}</h1>'
        f'<p class="lead">{esc(t["trend_sub"].format(date=snapshot["date"]))}</p></div></section>'
        f'<div class="wrap">{editorial_nav(lang, prefix, base, "movers")}'
        f'<p class="note">{esc(chart_label)} · {esc(developer)} · {" · ".join(meta)}</p>'
        f'<div class="card">{sparkline(pts)}</div>'
        f'<p class="note">{esc(t["trend_note"])}</p>'
        f'<p><a href="{esc(base + prefix + "/markets/" + market + "/")}">{esc(C.market_name(market, lang))} →</a> · '
        f'<a href="{esc(base + prefix + "/movers/")}">{esc(t["back_movers"])} →</a></p></div>'
    )


def editorial_nav(lang: str, prefix: str, base: str, exclude: str = "") -> str:
    t = L.get(lang)
    links = [
        ("methodology", t["method_title"]),
        ("markets", t["markets_title"]),
        ("movers", t["movers_title"]),
        ("guides", K.GUIDES[lang]["guides_title"]),
        ("about", K.ABOUT[lang]["title"]),
        ("data", K.DATA[lang]["title"]),
    ]
    items = []
    for path, label in links:
        if path == exclude:
            continue
        items.append(f'<a href="{esc(base + prefix + "/" + path + "/")}">{esc(label)}</a>')
    return '<nav class="editorial">' + " · ".join(items) + '</nav>'


def about_page(lang: str, prefix: str, base: str) -> str:
    c = K.ABOUT[lang]
    t = L.get(lang)
    return (
        f'<section class="hero"><div class="wrap"><span class="eyebrow">{esc(c["title"])}</span>'
        f'<h1>{esc(c["h1"])}</h1><p class="lead">{esc(c["sub"])}</p></div></section>'
        f'<div class="wrap">{editorial_nav(lang, prefix, base, "about")}'
        f'<div class="prose">{sections_html(c["sections"])}</div>'
        f'<p class="note">{esc(t["disclosure"])}</p></div>'
    )


def data_page(lang: str, prefix: str, base: str) -> str:
    c = K.DATA[lang]
    t = L.get(lang)
    rows = "".join(
        f'<tr><td><code>{esc(name)}</code></td><td>{esc(desc)}</td></tr>' for name, desc in K.FIELDS
    )
    field_table = (
        f'<table><thead><tr><th>{esc(K.FIELD_LABELS[lang])}</th>'
        f'<th>{esc(K.FIELD_DESC_LABELS[lang])}</th></tr></thead><tbody>{rows}</tbody></table>'
    )
    parts = []
    for i, (h, p) in enumerate(c["sections"]):
        parts.append(f'<section><h2>{esc(h)}</h2><p>{esc(p)}</p></section>')
        if i == 1:
            parts.append(f'<section><h2>{esc(K.FIELD_LABELS[lang])}</h2>{field_table}</section>')
    return (
        f'<section class="hero"><div class="wrap"><span class="eyebrow">{esc(c["title"])}</span>'
        f'<h1>{esc(c["h1"])}</h1><p class="lead">{esc(c["sub"])}</p></div></section>'
        f'<div class="wrap">{editorial_nav(lang, prefix, base, "data")}'
        f'<div class="prose">{"".join(parts)}</div>'
        f'<p class="note">{esc(t["disclosure"])}</p></div>'
    )


def guides_index(lang: str, prefix: str, base: str) -> str:
    c = K.GUIDES[lang]
    cards = []
    for slug in K.GUIDE_SLUGS:
        g = c[slug]
        cards.append(
            f'<article class="card"><h3>{esc(g["title"])}</h3><p>{esc(g["desc"])}</p>'
            f'<a href="guides/{slug}/">{esc(c["read_guide"])} →</a></article>'
        )
    return (
        f'<section class="hero"><div class="wrap"><span class="eyebrow">{esc(c["guides_title"])}</span>'
        f'<h1>{esc(c["guides_h1"])}</h1><p class="lead">{esc(c["guides_sub"])}</p></div></section>'
        f'<div class="wrap">{editorial_nav(lang, prefix, base, "guides")}'
        f'<div class="grid">{"".join(cards)}</div></div>'
    )


def guide_detail(lang: str, slug: str, prefix: str, base: str) -> str | None:
    c = K.GUIDES[lang]
    if slug not in c:
        return None
    g = c[slug]
    t = L.get(lang)
    tool_link = {
        "rank-bands": ("revenue-estimator", "rev_title"),
        "fee-tiers": ("fee-calculator", "fee_title"),
        "market-overlap": ("market-compare", "cmp_title"),
        "charts-explained": (None, None),
    }[slug]
    related = [f'<a href="../">{esc(c["guides_h1"])}</a>',
               f'<a href="{esc(base + prefix + "/methodology/")}">{esc(t["method_title"])}</a>']
    if tool_link[0]:
        related.insert(1, f'<a href="{esc(base + prefix + "/tools/" + tool_link[0] + "/")}">{esc(t[tool_link[1]])}</a>')
    related.append(f'<a href="{esc(base + prefix + "/markets/")}">{esc(t["markets_title"])}</a>')
    return (
        f'<section class="hero"><div class="wrap"><span class="eyebrow">{esc(c["guides_title"])}</span>'
        f'<h1>{esc(g["title"])}</h1><p class="lead">{esc(g["desc"])}</p></div></section>'
        f'<div class="wrap">{editorial_nav(lang, prefix, base, "guides")}'
        f'<div class="prose">{sections_html(g["sections"])}</div>'
        f'<h2>{esc(c["related_title"])}</h2><p>{" · ".join(related)}</p>'
        f'<p class="note">{esc(t["disclosure"])}</p></div>'
    )


def build_site(snapshot: dict, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    base = C.BASE_URL
    paths = []
    app_pages = 0
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
        gc = K.GUIDES[lang]
        guide_cards = "".join(
            f'<article class="card"><span class="pill">{esc(gc["guides_title"])}</span>'
            f'<h3>{esc(gc[s]["title"])}</h3><p>{esc(gc[s]["desc"])}</p>'
            f'<a href="{esc(base + prefix + "/guides/" + s + "/")}">{esc(gc["read_guide"])} →</a></article>'
            for s in K.GUIDE_SLUGS[:2]
        )
        body = (f'<section class="hero"><div class="wrap"><span class="eyebrow">{esc(t["home_eyebrow"])}</span>'
                f'<h1>{esc(t["home_h1"])}</h1><p class="lead">{esc(t["home_sub"])}</p>'
                f'<p class="note">{esc(t["data_fresh"].format(date=snapshot["date"]))} · <a href="{esc(base+prefix+"/methodology/")}">{esc(t["method_hint"])}</a></p></div></section>'
                f'<div class="wrap">{editorial_nav(lang, prefix, base)}'
                f'<h2>{esc(t["tool_label"])}</h2><div class="grid">{"".join(cards)}</div>'
                f'{reference_table(lang, snapshot, prefix, base)}'
                f'<h2>{esc(gc["guides_title"])}</h2><div class="grid">{guide_cards}</div>'
                f'<p class="note"><a href="{esc(base + prefix + "/guides/")}">{esc(gc["guides_h1"])} →</a></p>'
                f'<p class="note"><a href="{esc(base + prefix + "/movers/")}">{esc(t["movers_h1"])} →</a></p></div>')
        schema = {"@context": "https://schema.org", "@type": "WebSite", "name": C.SITE_NAME,
                  "url": base + home_path, "publisher": {"@type": "Organization", "name": C.AUTHOR}}
        (out / home_path.strip("/") / "index.html").parent.mkdir(parents=True, exist_ok=True)
        (out / home_path.strip("/") / "index.html").write_text(
            page(f'{t["home_h1"].rstrip("。.")} — {C.SITE_NAME}', t["home_sub"], home_path, body, lang, base, schema=schema), encoding="utf-8")
        paths.append(home_path)

        tools_path = prefix + "/tools/"
        hub_cards = []
        for slug in TOOL_SLUGS:
            title_key = TOOL_TITLE_KEYS[slug]
            desc_key = {"rank-change": "rank_desc", "revenue-estimator": "rev_desc",
                        "market-compare": "cmp_desc", "fee-calculator": "fee_desc"}[slug]
            hub_cards.append(f'<article class="card"><span class="pill">{esc(t["tool_label"])}</span>'
                             f'<h3>{esc(t[title_key])}</h3><p>{esc(t[desc_key])}</p>'
                             f'<a href="{esc(base + prefix + "/tools/" + slug + "/")}">{esc(t["open"])} →</a></article>')
        hub_body = (crumbs_html([("Home", prefix + "/"), (t["tool_label"], None)])
                    + f'<section class="hero"><div class="wrap"><span class="eyebrow">{esc(t["home_eyebrow"])}</span>'
                    f'<h1>{esc(t["tool_label"])}</h1><p class="lead">{esc(t["home_sub"])}</p>'
                    f'<p class="note">{esc(t["data_fresh"].format(date=snapshot["date"]))}</p></div></section>'
                    f'<div class="wrap"><div class="grid">{"".join(hub_cards)}</div>'
                    f'{related_tools(lang, prefix, base)}'
                    f'{editorial_nav(lang, prefix, base)}'
                    f'<p class="note">{esc(t["disclosure"])}</p></div>')
        dest = out / tools_path.strip("/") / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page(f'{t["tool_label"]} — {C.SITE_NAME}', t["home_sub"], tools_path, hub_body, lang, base), encoding="utf-8")
        paths.append(tools_path)

        for slug in TOOL_SLUGS:
            title_key = {"rank-change": "rank_title", "revenue-estimator": "rev_title",
                         "market-compare": "cmp_title", "fee-calculator": "fee_title"}[slug]
            desc_key = {"rank-change": "rank_desc", "revenue-estimator": "rev_desc",
                        "market-compare": "cmp_desc", "fee-calculator": "fee_desc"}[slug]
            tool_path = prefix + f"/tools/{slug}/"
            trail = [("Home", prefix + "/"), (t["tool_label"], prefix + "/tools/"),
                     (t[title_key], None)]
            body = (crumbs_html(trail)
                    + f'<section class="hero"><div class="wrap"><span class="eyebrow">{esc(t["tool_label"])}</span>'
                    f'<h1>{esc(t[title_key])}</h1><p class="lead">{esc(t[desc_key])}</p>'
                    f'<p class="note">{esc(t["data_fresh"].format(date=snapshot["date"]))}</p></div></section>'
                    f'<div class="wrap"><div class="card">{form_html(lang, slug, snapshot)}<div id="result" class="result" role="status" aria-live="polite"></div>'
                    f'<p class="note">{esc(t["scenario_note"])}</p></div>'
                    f'{tool_prose(lang, slug)}'
                    f'{related_tools(lang, prefix, base, slug)}'
                    f'<p class="note">{esc(t["disclosure"])}</p></div>')
            if slug == "market-compare":
                mini = {"markets": {m: {"charts": {c: {"rows": [
                    {"app_id": r["app_id"], "name": r.get("name", ""), "rank": r.get("rank")}
                    for r in ch.get("rows", [])]}
                    for c, ch in me.get("charts", {}).items()}} for m, me in snapshot["markets"].items()}}
                payload = script_json(mini)
            else:
                payload = "{}"
            script = JS[slug].replace("__DATA__", payload).replace("__T__", script_json(t)).replace(
                "__CFG__", script_json({"fees": C.FEE_RATES, "rank_bands": C.RANK_BANDS,
                                    "floor": C.FLOOR_MULTIPLIER, "method": prefix + "/methodology/"}))
            schema = [{"@context": "https://schema.org", "@type": "WebApplication", "name": t[title_key],
                       "url": base + tool_path, "applicationCategory": "UtilitiesApplication",
                       "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
                       "publisher": {"@type": "Organization", "name": C.AUTHOR}},
                      breadcrumb_schema(trail, base)]
            dest = out / tool_path.strip("/") / "index.html"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(page(t[title_key], t[desc_key], tool_path, body, lang, base, script=script, schema=schema), encoding="utf-8")
            paths.append(tool_path)

        method_path = prefix + "/methodology/"
        method_body = (crumbs_html([("Home", prefix + "/"), (t["method_title"], None)])
                       + f'<section class="hero"><div class="wrap"><span class="eyebrow">{esc(t["method_title"])}</span>'
                       f'<h1>{esc(t["method_title"])}</h1><p class="lead">{esc(t["method_desc"])}</p></div></section>'
                       f'<div class="wrap"><div class="card"><h2>1. {esc(t["source"])}</h2><p><a href="{esc(C.API_BASE)}">{esc(C.API_BASE)}</a></p>'
                       f'<h2>2. Rank bands</h2><p><code>{esc(bands_text())}</code></p>'
                       f'<h2>3. Revenue</h2><p><code>gross = downloads × multiplier × conversion × price</code>; <code>net = gross × (1 - fee)</code></p>'
                       f'<h2>4. Limits</h2><p>{esc(t["scenario_note"])}</p></div></div>')
        dest = out / method_path.strip("/") / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page(t["method_title"], t["method_desc"], method_path, method_body, lang, base), encoding="utf-8")
        paths.append(method_path)

        markets_path = prefix + "/markets/"
        markets_body = crumbs_html([("Home", prefix + "/"), (t["markets_title"], None)]) + market_index(lang, snapshot)
        dest = out / markets_path.strip("/") / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page(t["markets_title"], t["markets_sub"], markets_path, markets_body, lang, base), encoding="utf-8")
        paths.append(markets_path)

        for market in C.MARKETS:
            detail_body = crumbs_html([("Home", prefix + "/"),
                                       (t["markets_title"], prefix + "/markets/"),
                                       (C.market_name(market, lang), None)]) + market_detail(lang, market, snapshot, prefix, base)
            if not detail_body:
                continue
            detail_path = prefix + f"/markets/{market}/"
            dest = out / detail_path.strip("/") / "index.html"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(page(C.market_name(market, lang), t["market_sub"].format(date=snapshot["date"]), detail_path, detail_body, lang, base), encoding="utf-8")
            paths.append(detail_path)

        movers_data = rank_movers(snapshot)
        movers_path = prefix + "/movers/"
        movers_body = crumbs_html([("Home", prefix + "/"), (t["movers_title"], None)]) + movers_page(lang, snapshot, prefix, base, movers_data)

        dest = out / movers_path.strip("/") / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        movers_schema = {"@context": "https://schema.org", "@type": "Dataset",
                         "name": t["movers_h1"], "url": base + movers_path,
                         "temporalCoverage": snapshot["date"],
                         "creator": {"@type": "Organization", "name": C.AUTHOR},
                         "isAccessibleForFree": True, "sameAs": C.API_BASE}
        dest.write_text(page(t["movers_title"], t["movers_sub"], movers_path, movers_body, lang, base, schema=movers_schema), encoding="utf-8")
        paths.append(movers_path)

        for market, me in snapshot["markets"].items():
            for chart, ch in me.get("charts", {}).items():
                names = {r["app_id"]: r.get("name", "") for r in ch.get("rows", [])}
                for app_id in ch.get("trend", {}):
                    body = trend_page(lang, market, chart, app_id, snapshot, prefix, base, movers_data)
                    if not body:
                        continue
                    slug = app_slug(market, chart, app_id)
                    app_path = prefix + f"/apps/{slug}/"
                    dest = out / app_path.strip("/") / "index.html"
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    title = names.get(app_id, app_id) + " — " + t["trend_title"]
                    schema = {"@context": "https://schema.org", "@type": "Dataset",
                              "name": title, "url": base + app_path,
                              "temporalCoverage": snapshot["date"],
                              "creator": {"@type": "Organization", "name": C.AUTHOR},
                              "isAccessibleForFree": True,
                              "sameAs": C.API_BASE}
                    # 600 个 app 页每页仅 50–130 词，属薄页：保留为可达的辅助页但排除出索引
                    dest.write_text(page(title, t["trend_sub"].format(date=snapshot["date"]), app_path, body, lang, base, schema=schema, noindex=True), encoding="utf-8")
                    app_pages += 1

        about_path = prefix + "/about/"
        dest = out / about_path.strip("/") / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        about_body = crumbs_html([("Home", prefix + "/"), (K.ABOUT[lang]["title"], None)]) + about_page(lang, prefix, base)
        dest.write_text(page(K.ABOUT[lang]["title"], K.ABOUT[lang]["sub"], about_path, about_body, lang, base), encoding="utf-8")
        paths.append(about_path)

        data_path = prefix + "/data/"
        dest = out / data_path.strip("/") / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        data_body = crumbs_html([("Home", prefix + "/"), (K.DATA[lang]["title"], None)]) + data_page(lang, prefix, base)
        dest.write_text(page(K.DATA[lang]["title"], K.DATA[lang]["sub"], data_path, data_body, lang, base), encoding="utf-8")
        paths.append(data_path)

        guides_path = prefix + "/guides/"
        dest = out / guides_path.strip("/") / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        guides_body = crumbs_html([("Home", prefix + "/"), (K.GUIDES[lang]["guides_title"], None)]) + guides_index(lang, prefix, base)
        dest.write_text(page(K.GUIDES[lang]["guides_title"], K.GUIDES[lang]["guides_sub"], guides_path, guides_body, lang, base), encoding="utf-8")
        paths.append(guides_path)

        for slug in K.GUIDE_SLUGS:
            guide_body = guide_detail(lang, slug, prefix, base)
            if guide_body:
                g = K.GUIDES[lang][slug]
                guide_body = crumbs_html([("Home", prefix + "/"),
                                          (K.GUIDES[lang]["guides_title"], prefix + "/guides/"),
                                          (g["title"], None)]) + guide_body
            if not guide_body:
                continue
            guide_path = prefix + f"/guides/{slug}/"
            dest = out / guide_path.strip("/") / "index.html"
            dest.parent.mkdir(parents=True, exist_ok=True)
            g = K.GUIDES[lang][slug]
            dest.write_text(page(g["title"], g["desc"], guide_path, guide_body, lang, base), encoding="utf-8")
            paths.append(guide_path)

    lastmod = esc(snapshot.get("date", ""))
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap += [f"  <url><loc>{esc(base + p)}</loc><lastmod>{lastmod}</lastmod></url>" for p in paths]
    sitemap.append("</urlset>")
    (out / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n", encoding="utf-8")
    (out / "404.html").write_text(not_found_page(base), encoding="utf-8")
    print(f"[done] {len(paths)} indexable URLs -> {out}/ ({app_pages} thin app pages built, noindex)" )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", default="data/snapshot.json")
    parser.add_argument("--out", default="site")
    args = parser.parse_args()
    snapshot = json.loads(Path(args.snapshot).read_text(encoding="utf-8"))
    build_site(snapshot, Path(args.out))


if __name__ == "__main__":
    main()
