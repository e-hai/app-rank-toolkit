# 社区发帖草稿（2026-11-25）

针对三站的第一轮外链与流量投放。原则：帖子本身必须能独立成立（有数据、有结论），链接只作为末尾补充；否则会被判为自我推广并删帖。

发布顺序：先 r/ASO（最垂直、容忍工具）→ 再 Indie Hackers（容忍 build log）→ 最后 r/iOSProgramming 或 r/androiddev（审核最严，需完全去掉推销语气）。每篇间隔至少两天，不要同一天跨版轰炸。

---

## 一、r/ASO

**标题**：I pulled the top-10 charts of 6 storefronts for one day. Taiwan's free chart has zero overlap with US, UK, JP, KR and TR

**正文**：

Been building a small free tool around public ranking data, and one thing surprised me enough to share: how little the free charts have in common across markets.

Top-10 overlap, free chart, one day's snapshot:

- US–UK: 5/10
- US–JP: 4/10
- US–KR: 1/10
- JP–KR: 0/10
- Anything vs TW: 0/10 (all five pairs)

And the grossing chart flips it: JP–TW is 5/10, US–TR is 5/10. Different apps dominate each chart type.

The "unique apps" list is what made it click for me. Korea's free top 10 has a bank app, a job board, an online fashion store, a coffee membership. Taiwan's has a food delivery app and a McDonald's app. UK's has GOV.UK One Login. These don't travel — so "localize the listing" can't get you into those charts, you need a local product or partner.

Two things I'd flag before anyone over-reads this:

1. Top 10 is the head, not the market. One day's snapshot moves cells.
2. Overlap counts hide *which* app leads. ChatGPT is #4 in US and #1 in the same chart elsewhere — the count says "shared", the ranks say "not the same position".

The full matrix (6 markets × free/grossing, pick any pair) is at https://apprank-toolkit.pages.dev/tools/market-compare/ — free, no signup. I maintain it; happy to answer questions about the data pipeline or add markets if there's demand.

---

## 二、Indie Hackers

**标题**：I built four free ASO calculators because every "revenue estimator" I found hid its math

**正文**：

Short version of why: I kept landing on ASO calculators that returned a single number with no breakdown. You type downloads and conversion, get "$3,143 net", and have no way to check whether the rank multiplier, the fee tier, or the conversion assumption did the damage. So I rebuilt the four I actually use, with the math visible.

What's in it:

- **Rank change** — previous vs current rank, returns the band multiplier shift (e.g. 0.25 → 0.45) and the visibility multiple (1.80×) instead of one sentence.
- **Revenue estimator** — full funnel: downloads after rank band → paying users → gross → store fee → net, plus revenue per download.
- **Fee calculator** — same gross across the 30% and 15% tiers side by side.
- **Market compare** — pick two of six storefronts (US/UK/JP/KR/TR/TW) and a chart, get shared apps with both ranks.

Two design decisions worth mentioning because they were deliberate:

Every input is written to the URL (`?rank=3&downloads=500000`), so a scenario is shareable and survives a language switch. And empty fields return an explicit "invalid input" instead of silently computing $0.00 — the original version of the revenue estimator did exactly that, which is worse than an error.

Stack is deliberately boring: Python static generator, no framework, no database, Cloudflare Pages free tier. 110 indexable pages across five languages. Data comes from public storefront ranking endpoints refreshed daily by a GitHub Action.

Link: https://apprank-toolkit.pages.dev/tools/

What I'd like feedback on: the calculators assume a rank-band multiplier model (1.0 at rank 1 down to 0.05 past rank 30). That's a rough proxy for impression volume, and I'd rather expose the assumption than pretend it is measured. If anyone has better public data on rank → impression curves, I'd love to replace it.

---

## 三、r/iOSProgramming

**标题**：A worked example of why the 15% vs 30% store fee is not a rounding error

**正文**：

Ran the numbers on the small-business tier vs standard for three revenue levels, because the percentage hides how linear the gap is:

| Gross | 30% net | 15% net |
|---|---|---|
| $10k | $7,000 | $8,500 |
| $50k | $35,000 | $42,500 |
| $250k | $175,000 | $212,500 |

It is 15 points of gross, always — $37,500 at the $250k level. The part that is easy to miss: the fee comes off gross, before infrastructure and ad spend, so the hit to margin is bigger than the percentage suggests. And crossing the $1M threshold is not gradual — the higher rate applies to revenue above the line, so a developer just over the line can net less than one just under it, depending on how much they clear.

The other thing I'd check before modeling anything: subscriptions don't follow the same rules as one-time purchases, and Apple and Google don't line them up perfectly. If subscriptions are most of your revenue, model per product rather than a blended rate.

I put a side-by-side calculator up while working this out (no signup, no JS-heavy page): https://apprank-toolkit.pages.dev/tools/fee-calculator/ — it shows the same gross under both tiers at once. Not affiliated with either store; the rates are inputs, not facts I'm asserting about your account.

If anyone has run into edge cases on the threshold (mid-year program switches, refunds at year end), I'd be curious how you modeled them.

---

## 发布检查清单

- [ ] 发帖前 15 分钟先在本版潜水，确认当天没有同类工具帖
- [ ] 正文里的链接只出现一次，且不在第一段
- [ ] 图片：矩阵截图一张（自己从工具页截，不要带浏览器边框）
- [ ] r/iOSProgramming 版规禁止「self promotion」帖，发布时用 text post 且不加 flair
- [ ] Indie Hackers 发在 "Products" 或 "Growth" 分区，标题别用 emoji
- [ ] 收到评论优先回答方法论问题，不推销；有人要链接再给
- [ ] 两周后统计：各帖点击数、dev.to 阅读数、GSC 里新增的引用域名
