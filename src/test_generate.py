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
    def setUp(self):
        self.snapshot = json.loads((G.ROOT / "data/snapshot.json").read_text(encoding="utf-8"))

    def build(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        with patch.object(C, "BASE_URL", "https://toolkit.example"):
            G.build_site(self.snapshot, Path(temp.name))
        return Path(temp.name)

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
        self.assertEqual(self.snapshot["date"], "2026-11-23")
        for market in C.MARKETS:
            self.assertIn(market, self.snapshot["markets"])
            for chart in C.CHARTS:
                rows = self.snapshot["markets"][market]["charts"][chart]["rows"]
                self.assertTrue(rows)
                self.assertLessEqual(len(rows), 10)

    def test_build_and_sitemap(self):
        out = self.build()
        pages = list(out.rglob("index.html"))
        self.assertEqual(len(pages), 30)
        root = ET.parse(out / "sitemap.xml").getroot()
        urls = [x.text for x in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        self.assertEqual(len(urls), 30)
        for url in urls:
            path = urlparse(url).path.strip("/")
            self.assertTrue((out / path / "index.html").exists())

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


if __name__ == "__main__":
    unittest.main()
