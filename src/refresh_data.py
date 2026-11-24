# -*- coding: utf-8 -*-
"""Fetch a small public ranking snapshot for the toolkit."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C


def fetch(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": C.UA})
    with urllib.request.urlopen(req, timeout=C.REQUEST_TIMEOUT) as r:
        return json.load(r)


def slim_rows(rows: list[dict]) -> list[dict]:
    out = []
    for row in rows[:10]:
        out.append({
            "app_id": str(row.get("app_id", "")),
            "name": row.get("name", ""),
            "developer": row.get("developer", ""),
            "rank": row.get("curr_rank"),
            "prev_rank": row.get("prev_rank"),
            "price": row.get("price_amount", 0),
            "currency": row.get("price_currency", "USD"),
            "rating": row.get("rating"),
            "rating_count": row.get("rating_count"),
        })
    return out


def build_snapshot() -> dict:
    dates = fetch(f"{C.API_BASE}/dates.json")["dates"]
    date = dates[-1]["date"]
    markets: dict = {}
    for market in C.MARKETS:
        entry: dict = {"name": C.market_name(market), "charts": {}}
        for chart in C.CHARTS:
            try:
                data = fetch(f"{C.API_BASE}/rankings/app_store_{market}_{chart}_{date}.json")
            except Exception as exc:
                print(f"[warn] skip {market}/{chart}: {exc}", file=sys.stderr)
                continue
            rows = slim_rows(data.get("rows", []))
            try:
                trend_all = fetch(f"{C.API_BASE}/trend/app_store_{market}_{chart}.json").get("trends", {})
            except Exception:
                trend_all = {}
            trend = {}
            for row in rows:
                app_id = row["app_id"]
                if app_id in trend_all:
                    trend[app_id] = [
                        {"date": p.get("date"), "best_rank": p.get("best_rank")}
                        for p in trend_all[app_id][-14:]
                    ]
            entry["charts"][chart] = {
                "rows": rows,
                "summary": data.get("quant_summary", {}),
                "trend": trend,
            }
        markets[market] = entry
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "date": date,
        "source": C.API_BASE,
        "markets": markets,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="data/snapshot.json")
    args = parser.parse_args()
    snapshot = build_snapshot()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[done] {out} date={snapshot['date']} markets={len(snapshot['markets'])}")


if __name__ == "__main__":
    main()
