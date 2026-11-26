---
title: "App store fees: what 15% vs 30% actually costs (worked numbers)"
canonical_url: "https://apprank-toolkit.pages.dev/guides/fee-tiers/"
tags: aso, appstore, ios, marketing
---

Every indie app developer eventually asks the same question: does the small-business tier actually matter, or is it rounding error on top of everything else? I built a small calculator for this, then ran the numbers for a few realistic revenue levels. The results are less intuitive than the percentages suggest.

## The two rates

- **Standard**: 30% of the transaction. Applies to most developers by default.
- **Small business tier**: 15%. Apple's Small Business Program is for developers who earned at most $1M in proceeds in the prior calendar year; Google Play applies 15% to the first $1M of annual revenue and 30% above it.

Worth re-reading the current program pages before you model anything — the thresholds have moved more than once in the last few years. The calculators I use assume the two rates above and let you switch between them.

## What it looks like at three revenue levels

Same gross, two tiers, fee and take-home:

| Gross revenue | Standard 30% fee | Standard net | Small program 15% fee | 15% net |
|---|---|---|---|---|
| $10,000 | $3,000 | $7,000 | $1,500 | $8,500 |
| $50,000 | $15,000 | $35,000 | $7,500 | $42,500 |
| $250,000 | $75,000 | $175,000 | $37,500 | $212,500 |

The gap is linear, which is the point: it is 15 points of revenue, always. At $250k gross the difference is $37,500 — about one mid-level engineer's annual salary in a lot of markets, or a year of paid user acquisition for a small app.

## Where people get this wrong

**Fees are on gross, not profit.** The 30% comes off the top, before your infrastructure, ad spend, and refunds. So the "real" margin hit is larger than 30% of profit. If your app nets 40% of gross before fees, losing 30 points of gross can wipe out most of that margin.

**The threshold cuts both ways.** Crossing $1M in a year means losing the reduced rate on *subsequent* revenue, and the jump is not gradual. A developer at exactly $1.05M can end up with less net than one at $950k once the higher rate kicks in on the remainder. It is worth modeling the boundary before you push a price increase or a big seasonal campaign.

**Subscriptions are their own puzzle.** Long-running subscriptions are treated differently from one-off purchases, and the rules don't line up perfectly between the two stores. If subscription revenue is most of your business, model the per-product rate rather than the blended 30/15.

**Taxes and refunds sit on top.** The store fee is computed before tax remittance; refunds come out of your proceeds at the same rate. Neither is captured by a simple percentage-of-gross sheet.

## The number I actually use

For planning I keep a single figure per product: **net per paying user**. That is `price × (1 − rate)`, and it is the only number that composes cleanly when you start mixing price points, tiers, and currencies. At $4.99 with the standard rate it is $3.49; on the small program it is $4.24. Multiply by expected paying users and you have a plan that survives contact with a finance spreadsheet.

If you want to run your own numbers, there is a free calculator here — it does the tier comparison side by side instead of making you do two passes:

**https://apprank-toolkit.pages.dev/tools/fee-calculator/**

It also shows the same gross under both tiers at once, which is the fastest way to see whether chasing the small-business tier is worth the paperwork for your revenue level.

*I maintain the calculator and the public ranking dataset behind it; both are free and there is no signup. Numbers above are arithmetic on stated rates, not tax or legal advice.*
