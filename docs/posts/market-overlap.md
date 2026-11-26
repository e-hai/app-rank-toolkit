---
title: "I compared the top 10 apps in 6 storefronts. Taiwan's free chart shares nothing with the US"
canonical_url: "https://apprank-toolkit.pages.dev/guides/market-overlap/"
tags: aso, appstore, data, marketing
---

Store charts look like one product category. They behave like six unrelated ecosystems. To check that, I pulled the public top-10 charts for six storefronts — US, UK, Japan, South Korea, Türkiye, Taiwan — for both the free and the top-grossing chart, and counted how many of the ten apps appear in two markets at once. A single day's snapshot is small, so treat this as a snapshot rather than a law, but the shape is consistent across the pairs.

## Free chart: overlap collapses fast

How many of the ten free apps appear in both markets:

| | US | UK | JP | KR | TR | TW |
|---|---|---|---|---|---|---|
| **US** | — | 5 | 4 | 1 | 3 | **0** |
| **UK** | 5 | — | 3 | 1 | 3 | **0** |
| **JP** | 4 | 3 | — | **0** | 2 | **0** |
| **KR** | 1 | 1 | 0 | — | 1 | **0** |
| **TR** | 3 | 3 | 2 | 1 | — | **0** |
| **TW** | 0 | 0 | 0 | 0 | 0 | — |

The diagonal is the same market (always 10). Every cell involving Taiwan is zero: Taiwan's free top 10 has no app in common with any other storefront in the set. Japan and South Korea share nothing either.

That is not a coincidence of one day. The unique apps tell the story better — Korea's top 10 includes a bank app, a job-listing app, an online fashion store, a coffee membership card and a local AI agent. Taiwan's includes a food-delivery app, a McDonald's app and a language-learning app. The UK's includes a government login app (`GOV.UK One Login`) and a resale marketplace. None of these travel.

By contrast the US and UK free charts are the closest pair at 5/10, which makes sense: same language, overlapping ad markets, and the same short-drama apps shipping into both.

## Top-grossing chart: the opposite pattern

| | US | UK | JP | KR | TR | TW |
|---|---|---|---|---|---|---|
| **US** | — | 5 | 2 | 4 | 5 | 2 |
| **UK** | 5 | — | 2 | 3 | 4 | 2 |
| **JP** | 2 | 2 | — | 2 | 2 | **5** |
| **KR** | 4 | 3 | 2 | — | 4 | 2 |
| **TR** | 5 | 4 | 2 | 4 | — | 2 |
| **TW** | 2 | 2 | 5 | 2 | 2 | — |

Now the closest pair is Japan–Taiwan at 5/10, and the US, UK, Korea and Türkiye cluster around each other. What shows up in these charts is a different animal: subscription streaming, dating apps, big-publisher mobile games, and regional payment/loyalty apps. Japan's list carries LINE Manga, Piccoma, U-NEXT and Puzzle & Dragons; Korea's carries KakaoTalk, Naver Webtoon, TVING and Coupang Play. Local payment rails and local content libraries dominate, which is why the overlap is lower than in the free chart but spread across a different set of pairs.

## Three things this changes about ASO

**Localization of strings is not enough for the free chart.** If a market's free top 10 is made of domestic services with local logins, local fulfillment and local content, no amount of translated screenshots will move you into it. You need a local partner, a local payment method, or a genuinely local use case. That is a product decision, not an ASO decision.

**The grossing chart is a subscriptions competition.** The apps you are bidding against there are global franchises with retention engines and studio budgets. Competing on screenshots is not the lever; competing on retention and pricing is.

**Market selection should be pair-based.** "Which market should I launch in" is usually the wrong question. The right one is "which pair of markets shares enough audience that one creative can serve both" — and the matrix answers that directly. US–TR at 5/10 on the grossing chart is a stronger pairing signal than either market's absolute size suggests.

## Caveats

Top 10 is a tiny slice: it is the head, not the market. A single day's snapshot will move a few cells. The data behind this comes from public storefront ranking endpoints, and the full matrix — six markets, both charts, updatable — is here:

**https://apprank-toolkit.pages.dev/tools/market-compare/**

Pick any two markets and a chart, and it returns the two-sided ranks for the overlapping apps, so you can see whether a shared app leads in one market and trails in the other. That is often the more useful number than the count itself.
