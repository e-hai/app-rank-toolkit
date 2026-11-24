# -*- coding: utf-8 -*-
"""AppRank Toolkit configuration."""
from __future__ import annotations

import os

DEFAULT_BASE_URL = "https://apprank-toolkit.pages.dev"
BASE_URL = os.environ.get("SITE_BASE_URL", DEFAULT_BASE_URL).rstrip("/")

API_BASE = "https://e-hai.github.io/Appstore_Top_30/api"
REQUEST_TIMEOUT = 30
UA = "AppRankToolkitBot/1.0 (+https://apprank-toolkit.pages.dev; data from App Store public rankings)"

SITE_NAME = "AppRank Toolkit"
WORK_TITLE = "AppRank Toolkit"
AUTHOR = "apprank studio"
DESCRIPTION = (
    "Free app-store calculators and market comparison tools built from public ranking data. "
    "Estimate rank movement, revenue scenarios, fees, and cross-market overlap."
)

LANGS = ("en", "ko", "ja", "zh", "tr")
LANG_MARKETS = {
    "ko": ["kr"],
    "ja": ["jp"],
    "zh": ["tw", "hk", "mo"],
    "tr": ["tr"],
}

MARKETS = ["us", "gb", "jp", "kr", "tr", "tw"]
CHARTS = ["free", "grossing"]

MARKET_NAMES = {
    "us": "United States", "gb": "United Kingdom", "jp": "Japan",
    "kr": "South Korea", "tr": "Türkiye", "tw": "Taiwan, China",
}

LOCAL_MARKET_NAMES = {
    "ko": {"kr": "한국"},
    "ja": {"jp": "日本"},
    "zh": {"tw": "中国台湾"},
    "tr": {"tr": "Türkiye"},
}

HREFLANG = {
    "en": "en", "ko": "ko-KR", "ja": "ja-JP",
    "zh": "zh-Hans", "tr": "tr-TR",
}

TOOLS = ("rank-change", "revenue-estimator", "market-compare", "fee-calculator")

# Free App Store / Google Play fee scenarios. These are assumptions, not billing advice.
FEE_RATES = {"standard": 0.30, "small": 0.15}


def market_name(code: str, lang: str = "en") -> str:
    if lang in LOCAL_MARKET_NAMES and code in LOCAL_MARKET_NAMES[lang]:
        return LOCAL_MARKET_NAMES[lang][code]
    return MARKET_NAMES.get(code, code.upper())
