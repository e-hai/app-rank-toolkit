"""Offline tests for AppRank Toolkit. No network, no git, no deploy."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

import config as C
import generate as G
import locales as L


class ToolkitTests(unittest.TestCase):
    _shared = None
    _temp = None

    @classmethod
    def setUpClass(cls):
        cls.snapshot = json.loads((G.ROOT / "data/snapshot.json").read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls):
        if cls._temp is not None:
            cls._temp.cleanup()

    def build(self):
        # Build once per class: the site now has 700+ pages, so rebuilding it
        # for every test is slow and provides no extra coverage.
        if ToolkitTests._shared is None:
            temp = tempfile.TemporaryDirectory()
            ToolkitTests._temp = temp
            with patch.object(C, "BASE_URL", "https://toolkit.example"):
                G.build_site(self.snapshot, Path(temp.name))
            ToolkitTests._shared = Path(temp.name)
        return ToolkitTests._shared

    def test_formulas(self):
        self.assertEqual(G.rank_result(None, 7), "new")
        self.assertEqual(G.rank_result(12, 7), "up")
        self.assertEqual(G.rank_result(7, 12), "down")
        self.assertEqual(G.rank_result(8, 8), "flat")
        r = G.revenue_scenario(5, 10000, 5, 2, 0.3)
        self.assertEqual(r["multiplier"], .45)
        self.assertEqual(r["gross"], 450.0)
        self.assertAlmostEqual(r["net"], 315.0)
        self.assertEqual(G.fee_scenario(100, .15)["net"], 85)

    def test_snapshot_shape(self):
        self.assertRegex(self.snapshot["date"], r"^\d{4}-\d{2}-\d{2}$")
        for market in C.MARKETS:
            self.assertIn(market, self.snapshot["markets"])
            for chart in C.CHARTS:
                rows = self.snapshot["markets"][market]["charts"][chart]["rows"]
                self.assertTrue(rows)
                self.assertLessEqual(len(rows), 10)

    def test_build_and_sitemap(self):
        out = self.build()
        import content as K
        app_pages = sum(1 for m, v in self.snapshot["markets"].items()
                        for c, ch in v["charts"].items() for a in ch.get("trend", {}))
        pages = list(out.rglob("index.html"))
        # 薄 app 页仍然生成（可被内链访问），但 noindex 且不进 sitemap
        indexable_per_lang = 6 + 2 + len(C.MARKETS) + 3 + len(K.GUIDE_SLUGS) + 1
        self.assertEqual(len(pages), len(C.LANGS) * (indexable_per_lang + app_pages))
        root = ET.parse(out / "sitemap.xml").getroot()
        urls = [x.text for x in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        self.assertEqual(len(urls), len(C.LANGS) * indexable_per_lang)
        self.assertFalse(any("/apps/" in u for u in urls))
        for url in urls:
            path = urlparse(url).path.strip("/")
            self.assertTrue((out / path / "index.html").exists())

    def test_sitemap_lastmod(self):
        out = self.build()
        document = (out / "sitemap.xml").read_text(encoding="utf-8")
        import content as K
        app_pages = sum(1 for m, v in self.snapshot["markets"].items()
                        for c, ch in v["charts"].items() for a in ch.get("trend", {}))
        self.assertIn(f"<lastmod>{self.snapshot['date']}</lastmod>", document)
        per_lang = 6 + 2 + len(C.MARKETS) + 3 + len(K.GUIDE_SLUGS) + 1
        self.assertEqual(document.count("<lastmod>"), len(C.LANGS) * per_lang)

    def test_tool_prose(self):
        out = self.build()
        document = (out / "tools/rank-change/index.html").read_text(encoding="utf-8")
        self.assertIn('class="prose"', document)
        self.assertIn("How this tool works", document)
        self.assertIn("Worked example", document)
        self.assertIn("Common questions", document)


    def test_tool_pages_have_breadcrumbs_and_related_links(self):
        out = self.build()
        for slug in C.TOOLS:
            document = (out / "tools" / slug / "index.html").read_text(encoding="utf-8")
            self.assertIn('class="crumbs"', document, slug)
            self.assertIn("BreadcrumbList", document, slug)
            self.assertIn('class="rel"', document, slug)
            self.assertIn("https://apprank.pages.dev/", document, slug)
            others = [o for o in C.TOOLS if o != slug]
            for other in others:
                self.assertIn(f'/tools/{other}/', document, (slug, other))

    def test_tool_payload_is_trimmed_per_tool(self):
        out = self.build()
        for slug in ("rank-change", "revenue-estimator", "fee-calculator"):
            document = (out / "tools" / slug / "index.html").read_text(encoding="utf-8")
            self.assertIn("const DATA={};", document, slug)
            self.assertNotIn('"trend"', document, slug)
        compare = (out / "tools/market-compare/index.html").read_text(encoding="utf-8")
        self.assertIn('"markets"', compare)

    def test_inner_pages_have_breadcrumbs(self):
        out = self.build()
        for path in ("methodology", "markets", "movers", "guides", "about", "data"):
            document = (out / path / "index.html").read_text(encoding="utf-8")
            self.assertIn('class="crumbs"', document, path)


    def test_calculator_usability_markup(self):
        out = self.build()
        for slug in C.TOOLS:
            document = (out / "tools" / slug / "index.html").read_text(encoding="utf-8")
            self.assertIn('aria-live="polite"', document, slug)
            self.assertIn('type="reset"', document, slug)
            self.assertIn("<noscript>", document, slug)
            self.assertIn('for="', document, slug)
        fee = (out / "tools/fee-calculator/index.html").read_text(encoding="utf-8")
        self.assertIn('<option value="standard">Standard 30%</option>', fee)
        rev = (out / "tools/revenue-estimator/index.html").read_text(encoding="utf-8")
        self.assertIn('<option value="standard">Standard 30%</option>', rev)
        compare = (out / "tools/market-compare/index.html").read_text(encoding="utf-8")
        self.assertIn('"rank"', compare)


    def test_calculators_keep_state_across_language_switch(self):
        out = self.build()
        for slug in C.TOOLS:
            document = (out / "tools" / slug / "index.html").read_text(encoding="utf-8")
            self.assertIn("const F=[", document, slug)
            self.assertIn("keepLangState", document, slug)
            self.assertIn("history.replaceState", document, slug)
            self.assertIn("new URLSearchParams(location.search)", document, slug)

    def test_market_pages(self):
        out = self.build()
        index = (out / "markets/index.html").read_text(encoding="utf-8")
        self.assertIn("App Store rankings by market", index)
        for market in C.MARKETS:
            self.assertTrue((out / "markets" / market / "index.html").exists())
            self.assertIn(f'href="{market}/"', index)
        us = (out / "markets/us/index.html").read_text(encoding="utf-8")
        self.assertIn("Top apps in United States", us)
        self.assertIn("<table>", us)
        self.assertIn("TikTok", us)
        self.assertIn('hreflang="x-default"', us)
        zh = (out / "zh/markets/tw/index.html").read_text(encoding="utf-8")
        self.assertIn("热门应用", zh)
        self.assertIn("中国台湾", zh)

    def test_about_and_data_pages(self):
        import content as K
        out = self.build()
        about = (out / "about/index.html").read_text(encoding="utf-8")
        self.assertIn("About AppRank Toolkit", about)
        self.assertIn("apprank studio", about)
        self.assertIn('class="editorial"', about)
        data = (out / "data/index.html").read_text(encoding="utf-8")
        self.assertIn("Data source and field dictionary", data)
        for name, _ in K.FIELDS:
            self.assertIn(f"<code>{name}</code>", data)
        zh = (out / "zh/data/index.html").read_text(encoding="utf-8")
        self.assertIn("字段字典", zh)

    def test_guides_and_internal_links(self):
        import content as K
        out = self.build()
        index = (out / "guides/index.html").read_text(encoding="utf-8")
        self.assertIn("Guides and explainers", index)
        for slug in K.GUIDE_SLUGS:
            self.assertTrue((out / "guides" / slug / "index.html").exists())
            self.assertIn(f'href="guides/{slug}/"', index)
        guide = (out / "guides/rank-bands/index.html").read_text(encoding="utf-8")
        self.assertIn("Understanding rank bands", guide)
        self.assertIn("Related pages", guide)
        self.assertIn("/tools/revenue-estimator/", guide)
        self.assertIn("/markets/", guide)
        home = (out / "index.html").read_text(encoding="utf-8")
        self.assertIn("guides/rank-bands/", home)
        self.assertIn("/markets/", home)

    def test_movers_dashboard(self):
        out = self.build()
        doc = (out / "movers/index.html").read_text(encoding="utf-8")
        self.assertIn("Biggest rank movers", doc)
        self.assertIn("not an estimate", doc)
        self.assertGreaterEqual(doc.count("<tr>"), 10)
        self.assertIn('class="editorial"', doc)
        self.assertIn("/apps/", doc)
        zh = (out / "zh/movers/index.html").read_text(encoding="utf-8")
        self.assertIn("波动最大的应用", zh)

    def test_app_trend_pages(self):
        out = self.build()
        us = self.snapshot["markets"]["us"]["charts"]["free"]
        app_id = next(a for a, pts in us["trend"].items() if pts)
        path = out / "apps" / f"us-free-{app_id}" / "index.html"
        self.assertTrue(path.exists())
        doc = path.read_text(encoding="utf-8")
        self.assertIn("<svg", doc)
        self.assertIn("rank history", doc)
        self.assertIn("14-day change", doc)
        # 薄页策略：不进索引、不给 hreflang 集群信号，但保持 follow 传递权重
        self.assertIn('content="noindex,follow"', doc)
        self.assertNotIn('hreflang="x-default"', doc)
        # market table links into the trend page
        market = (out / "markets/us/index.html").read_text(encoding="utf-8")
        self.assertIn(f"/apps/us-free-{app_id}/", market)

    def test_social_meta_and_dataset_schema(self):
        out = self.build()
        doc = (out / "tools/fee-calculator/index.html").read_text(encoding="utf-8")
        self.assertIn('property="og:title"', doc)
        self.assertIn('property="og:locale" content="en"', doc)
        self.assertIn('name="twitter:card" content="summary"', doc)
        app = next((out / "apps").glob("us-free-*/index.html"))
        t = app.read_text(encoding="utf-8")
        # app 薄页 noindex 后不再挂 Dataset schema，避免与索引状态自相矛盾
        self.assertIn('content="noindex,follow"', t)
        self.assertNotIn('"@type": "Dataset"', t)
        m = (out / "movers/index.html").read_text(encoding="utf-8")
        self.assertIn('"@type": "Dataset"', m)

    def test_formula_single_source(self):
        rate = C.rank_multiplier(8)
        self.assertEqual(rate, 0.45)
        self.assertEqual(rate, C.rank_multiplier(10))
        self.assertEqual(C.rank_multiplier(11), 0.25)
        self.assertEqual(C.rank_multiplier(31), C.FLOOR_MULTIPLIER)
        self.assertEqual(G.revenue_scenario(8, 10000, 100, 1, 0)["multiplier"], rate)
        out = self.build()
        document = (out / "tools/revenue-estimator/index.html").read_text(encoding="utf-8")
        self.assertIn("CFG.rank_bands", document)
        self.assertIn('"rank_bands": [[1, 1.0]', document)

    def test_hreflang_and_canonical(self):
        out = self.build()
        document = (out / "tools/rank-change/index.html").read_text(encoding="utf-8")
        self.assertIn('hreflang="x-default"', document)
        for code in ("en", "ko-KR", "ja-JP", "zh-Hans", "tr-TR"):
            self.assertIn(f'hreflang="{code}"', document)
        self.assertIn('rel="canonical" href="https://toolkit.example/tools/rank-change/"', document)

    def test_scripts_and_sources(self):
        out = self.build()
        document = (out / "ko/tools/revenue-estimator/index.html").read_text(encoding="utf-8")
        self.assertIn("const DATA=", document)
        self.assertIn("id=\"tool-form\"", document)
        self.assertIn(C.API_BASE, document)
        self.assertNotIn("example.com", document)

    def test_no_non_chinese_locale_leaks(self):
        out = self.build()
        for path in out.rglob("index.html"):
            document = path.read_text(encoding="utf-8")
            self.assertNotIn("游戏", document)
            self.assertNotIn("总榜", document)
            if "/zh/" not in str(path):
                self.assertNotIn("数据来源", document)


    def test_overlap_matrix_and_presets(self):
        out = self.build()
        matrix = G.overlap_matrix("en", self.snapshot)
        self.assertIn("Cross-market overlap matrix", matrix)
        self.assertEqual(matrix.count("<table>"), len(C.CHARTS))
        self.assertEqual(matrix.count('class="num diag"'), len(C.MARKETS) * len(C.CHARTS))
        self.assertEqual(matrix.count('<td class="num"'), len(C.CHARTS) * len(C.MARKETS) * (len(C.MARKETS) - 1))
        us_gb = G.compare_markets(self.snapshot, "us", "gb", "free")["overlap"]
        self.assertIn(f'<td class="num">{us_gb}</td>', matrix)
        # symmetry: overlap(a,b) == overlap(b,a) for every pair and chart
        for chart in C.CHARTS:
            for a in C.MARKETS:
                for b in C.MARKETS:
                    if a != b:
                        self.assertEqual(G.compare_markets(self.snapshot, a, b, chart)["overlap"],
                                         G.compare_markets(self.snapshot, b, a, chart)["overlap"])
        compare = (out / "tools/market-compare/index.html").read_text(encoding="utf-8")
        self.assertIn('class="matrix"', compare)
        zh = (out / "zh/tools/market-compare/index.html").read_text(encoding="utf-8")
        self.assertIn("跨市场重合矩阵", zh)
        tr = (out / "tr/tools/market-compare/index.html").read_text(encoding="utf-8")
        self.assertIn("Pazarlar arası örtüşme matrisi", tr)

    def test_revenue_presets_and_number_locale(self):
        out = self.build()
        rev = (out / "tools/revenue-estimator/index.html").read_text(encoding="utf-8")
        self.assertIn('class="presets"', rev)
        for dl in ("5000", "50000", "500000"):
            self.assertIn(f'data-dl="{dl}"', rev)
        self.assertIn('"locale": "en-US"', rev)
        ko = (out / "ko/tools/revenue-estimator/index.html").read_text(encoding="utf-8")
        self.assertIn('"locale": "ko-KR"', ko)
        self.assertIn("다운로드 프리셋", ko)
        # 币种仍是美元，只有分隔符随语言变化
        for code in C.LANGS:
            prefix = "" if code == "en" else f"/{code}"
            doc = (out / (prefix.strip("/") + "/" if prefix else "") / "tools/revenue-estimator/index.html").read_text(encoding="utf-8")
            self.assertIn("currency:'USD'", doc, code)
            self.assertNotIn("currency:'KRW'", doc, code)


if __name__ == "__main__":
    unittest.main()
