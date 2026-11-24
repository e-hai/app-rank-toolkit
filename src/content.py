# -*- coding: utf-8 -*-
"""Editorial content for the toolkit: about, data dictionary, and guides.

Every statement here is grounded in the public ranking snapshot or in the
documented formulas. Nothing in this file claims measured revenue, store
analytics, or billing advice.
"""
from __future__ import annotations

# Human-readable field dictionary for the data page.
FIELDS = (
    ("app_id", "Stable app identifier used to match an app across storefronts."),
    ("name", "App display name as published in the ranking."),
    ("developer", "Developer or publisher name as published in the ranking."),
    ("rank", "Position in the chart for the snapshot date. Rank 1 is the top."),
    ("prev_rank", "Position in the previous observed snapshot; null means a new entry."),
    ("price", "Listed price in the chart; zero means a free app."),
    ("currency", "Currency code for the price field."),
    ("rating", "Average user rating shown in the ranking."),
    ("rating_count", "Number of user ratings behind the average."),
)

ABOUT = {
    "en": {
        "title": "About",
        "h1": "About AppRank Toolkit",
        "sub": "A small, transparent set of tools built on public App Store ranking data.",
        "sections": [
            ("What this site is", "AppRank Toolkit is a free set of calculators and market comparisons. Every number you see either comes from a public ranking snapshot or is computed in your browser from a formula printed on the page. There is no account, no paywall, and no hidden dataset."),
            ("Why the numbers are scenarios", "A ranking tells you position, not downloads or revenue. Our revenue and fee tools therefore describe scenarios: they apply a stated formula to values you choose. The rank-band multipliers are documented assumptions, not measurements published by any app store. Treat every result as a what-if calculation."),
            ("Where the data comes from", "Rankings are read from a public App Store ranking API and reduced to a daily snapshot of six storefronts. Each snapshot keeps the top 10 apps in the free and grossing charts, with rank, developer, rating, price and prior rank. The snapshot is rebuilt automatically and its date is shown on every page."),
            ("Who makes it", "This site is published by apprank studio. It is an independent project and is not affiliated with or endorsed by any app store. Questions about the data or the formulas can be raised through the repository linked in the footer."),
        ],
    },
    "zh": {
        "title": "关于",
        "h1": "关于 AppRank Toolkit",
        "sub": "一套基于公开 App Store 榜单数据、小而透明的工具。",
        "sections": [
            ("这个站点是什么", "AppRank Toolkit 是一套免费计算器和市场对比工具。你看到的每个数字，要么来自公开榜单快照，要么由页面上的公式在浏览器里现算。没有账号、没有付费墙，也没有隐藏数据集。"),
            ("为什么数字是情景", "榜单告诉你的是名次，不是下载量或收入。因此收入和手续费工具描述的是情景：它们把公开公式应用到你选择的参数上。排名区间乘数是记录在案的假设，不是任何应用商店公布的实测值。请把每个结果都当作假设推演。"),
            ("数据从哪来", "榜单来自公开的 App Store 排名 API，并被压缩成六个商店前台的每日快照。每份快照保留免费榜和畅销榜的前 10 名，含名次、开发者、评分、价格和前一排名。快照自动重建，日期显示在每一页。"),
            ("谁在做", "本站由 apprank studio 发布，是独立项目，与任何应用商店无隶属或背书关系。关于数据或公式的问题，可通过页脚链接指向的代码仓库提出。"),
        ],
    },
    "ko": {
        "title": "소개",
        "h1": "AppRank Toolkit 소개",
        "sub": "공개 App Store 랭킹 데이터로 만든 작고 투명한 도구 모음입니다.",
        "sections": [
            ("이 사이트는 무엇인가요", "AppRank Toolkit은 무료 계산기와 시장 비교 도구 모음입니다. 보이는 모든 숫자는 공개 랭킹 스냅샷에서 오거나 페이지에 적힌 공식으로 브라우저에서 계산됩니다. 계정도, 유료 벽도, 숨겨진 데이터셋도 없습니다."),
            ("숫자가 시나리오인 이유", "랭킹은 순위를 알려줄 뿐 다운로드나 수익을 알려주지 않습니다. 따라서 수익·수수료 도구는 시나리오를 보여줍니다. 선택한 값에 명시된 공식을 적용합니다. 순위 구간 배수는 기록된 가정이며 스토어가 공개한 실측값이 아닙니다. 모든 결과를 가정 계산으로 보세요."),
            ("데이터 출처", "랭킹은 공개 App Store 랭킹 API에서 읽어 여섯 스토어프런트의 일일 스냅샷으로 축약합니다. 각 스냅샷은 무료·매출 차트의 상위 10개를 순위, 개발사, 평점, 가격, 이전 순위와 함께 보관합니다. 스냅샷은 자동으로 다시 만들어지며 날짜가 모든 페이지에 표시됩니다."),
            ("만드는 곳", "이 사이트는 apprank studio가 발행하는 독립 프로젝트이며 어떤 앱 스토어와도 제휴나 보증 관계가 없습니다. 데이터나 공식에 대한 문의는 푸터의 저장소 링크를 통해 할 수 있습니다."),
        ],
    },
    "ja": {
        "title": "概要",
        "h1": "AppRank Toolkit について",
        "sub": "公開された App Store ランキングデータで作った、小さく透明なツール群です。",
        "sections": [
            ("このサイトについて", "AppRank Toolkit は無料の計算機と市場比較ツールの集合です。表示される数値はすべて公開ランキングのスナップショットに由来するか、ページに記載された式でブラウザ内で計算されます。アカウントも課金壁も隠しデータセットもありません。"),
            ("数値がシナリオである理由", "ランキングは順位を示すだけで、ダウンロード数や売上を示しません。そのため売上・手数料ツールはシナリオを扱います。明示された式をあなたが選んだ値に適用します。順位帯倍率は記載された仮定であり、ストアが公表した実測値ではありません。すべての結果を仮定計算として扱ってください。"),
            ("データの出典", "ランキングは公開の App Store ランキング API から読み込み、6 つのストアフロントの日次スナップショットにまとめます。各スナップショットは無料・売上チャートの上位 10 件を順位、開発元、評価、価格、以前の順位とともに保存します。スナップショットは自動で再生成され、日付が全ページに表示されます。"),
            ("運営について", "このサイトは apprank studio が公開する独立プロジェクトで、いずれのアプリストアとも提携・推奨関係はありません。データや式に関する質問はフッターのリポジトリリンクからできます。"),
        ],
    },
    "tr": {
        "title": "Hakkında",
        "h1": "AppRank Toolkit hakkında",
        "sub": "Açık App Store sıralama verileriyle yapılmış küçük ve şeffaf bir araç seti.",
        "sections": [
            ("Bu site nedir", "AppRank Toolkit ücretsiz hesaplayıcılar ve pazar karşılaştırmalarından oluşur. Gördüğünüz her sayı ya açık bir sıralama anlık görüntüsünden gelir ya da sayfada yazılı formülle tarayıcınızda hesaplanır. Hesap yok, ödeme duvarı yok, gizli veri kümesi yok."),
            ("Sayılar neden senaryodur", "Bir sıralama konumu gösterir, indirme veya geliri değil. Bu yüzden gelir ve ücret araçları senaryoları anlatır: belirtilen formülü seçtiğiniz değerlere uygularlar. Sıra aralığı çarpanları belgelenmiş varsayımlardır, mağazaların yayımladığı ölçümler değildir. Her sonucu bir varsayım hesabı olarak görün."),
            ("Veri kaynağı", "Sıralamalar açık bir App Store sıralama API'sinden okunur ve altı mağaza bölgesinin günlük anlık görüntüsüne indirgenir. Her görüntü, ücretsiz ve hasılat listelerinin ilk 10 uygulamasını sıra, geliştirici, puan, fiyat ve önceki sırayla saklar. Görüntü otomatik olarak yenilenir ve tarihi her sayfada gösterilir."),
            ("Yayımcı", "Bu site apprank studio tarafından yayımlanan bağımsız bir projedir ve herhangi bir uygulama mağazasıyla bağlantılı veya onaylı değildir. Veri veya formüllerle ilgili sorular altbilgideki depo bağlantısından iletilebilir."),
        ],
    },
}

DATA = {
    "en": {
        "title": "Data & fields",
        "h1": "Data source and field dictionary",
        "sub": "What we fetch, how often we refresh it, and what each field means.",
        "sections": [
            ("Source", "Rankings come from a public App Store ranking API. We read the available dates, take the most recent one, and request the free and grossing charts for each market on that date. A separate trend endpoint supplies prior rank information."),
            ("Refresh", "A scheduled job refreshes the snapshot and rebuilds the site. The snapshot date is printed on every page and used as the sitemap lastmod value, so you can always tell how fresh a table is. No data is entered by hand."),
            ("Field dictionary", "Each ranking row keeps the fields below. Values are copied as published; where a value is missing we show a dash rather than inventing one."),
            ("Limits", "The public snapshot exposes only the top 10 apps per chart, for the App Store, across the markets listed on the site. It is a single daily observation, not a live feed, and it says nothing about downloads, revenue, or user spending. Calculated figures are scenarios, not facts about the snapshot."),
        ],
    },
    "zh": {
        "title": "数据与字段",
        "h1": "数据来源与字段字典",
        "sub": "我们抓取什么、多久更新一次、每个字段是什么意思。",
        "sections": [
            ("来源", "榜单来自公开的 App Store 排名 API。我们读取可用日期，取最新一天，再请求该日每个市场的免费榜和畅销榜。另一个趋势接口提供前一排名信息。"),
            ("更新", "定时任务刷新快照并重建站点。快照日期显示在每一页，并作为 sitemap 的 lastmod 值，因此你总能判断表格有多新。没有任何数据是手工录入的。"),
            ("字段字典", "每条榜单记录保留下列字段。数值按公布原样复制；缺失时显示破折号，绝不臆造。"),
            ("限制", "公开快照每个榜单只提供前 10 名，仅覆盖 App Store 及本站列出的市场。它是单日观测，不是实时数据，也不反映下载量、收入或用户支出。计算得出的数字是情景，不是关于快照的事实。"),
        ],
    },
    "ko": {
        "title": "데이터와 필드",
        "h1": "데이터 출처와 필드 사전",
        "sub": "무엇을 가져오고, 얼마나 자주 갱신하며, 각 필드가 무엇을 뜻하는지.",
        "sections": [
            ("출처", "랭킹은 공개 App Store 랭킹 API에서 옵니다. 사용 가능한 날짜를 읽어 가장 최신 날짜를 고르고, 그 날짜의 시장별 무료·매출 차트를 요청합니다. 별도의 추세 엔드포인트가 이전 순위 정보를 제공합니다."),
            ("갱신", "예약 작업이 스냅샷을 새로 고치고 사이트를 다시 만듭니다. 스냅샷 날짜는 모든 페이지와 sitemap의 lastmod 값에 표시되므로 표의 최신성을 항상 확인할 수 있습니다. 어떤 데이터도 수동 입력하지 않습니다."),
            ("필드 사전", "각 랭킹 행은 아래 필드를 보관합니다. 값은 공개된 대로 복사하며, 빠진 값은 숫자를 만들어내지 않고 대시로 표시합니다."),
            ("한계", "공개 스냅샷은 차트별 상위 10개 앱만 제공하며(App Store, 사이트에 표시된 시장 한정), 단일 일일 관측값으로 실시간이 아닙니다. 다운로드, 수익, 사용자 지출에 대한 정보도 없습니다. 계산 결과는 사실이 아닌 시나리오입니다."),
        ],
    },
    "ja": {
        "title": "データと項目",
        "h1": "データ出典と項目辞書",
        "sub": "何を取得し、どの頻度で更新し、各項目が何を意味するか。",
        "sections": [
            ("出典", "ランキングは公開の App Store ランキング API から取得します。利用可能な日付を読み、最新日を選び、その日の市場ごとの無料・売上チャートを要求します。別のトレンド API が以前の順位情報を提供します。"),
            ("更新", "スケジュールされたジョブがスナップショットを更新しサイトを再生成します。スナップショット日付は全ページと sitemap の lastmod に表示されるため、表の新しさを常に確認できます。手入力のデータはありません。"),
            ("項目辞書", "各ランキング行は以下の項目を保持します。値は公開されたままコピーし、欠損時は数値をでっち上げずダッシュで示します。"),
            ("限界", "公開スナップショットはチャートごと上位 10 件のみで、App Store とサイト掲載市場に限られます。単一日次の観測でありリアルタイムではありません。ダウンロード、売上、ユーザー支出については何も示しません。計算値は事実ではなくシナリオです。"),
        ],
    },
    "tr": {
        "title": "Veri ve alanlar",
        "h1": "Veri kaynağı ve alan sözlüğü",
        "sub": "Neyi aldığımız, ne sıklıkla güncellediğimiz ve her alanın anlamı.",
        "sections": [
            ("Kaynak", "Sıralamalar açık bir App Store sıralama API'sinden gelir. Kullanılabilir tarihleri okur, en yeniyi seçer ve o tarihte her pazarın ücretsiz ve hasılat listelerini isteriz. Ayrı bir eğilim uç noktası önceki sıra bilgisini sağlar."),
            ("Yenileme", "Zamanlanmış bir iş anlık görüntüyü yeniler ve siteyi yeniden oluşturur. Görüntü tarihi her sayfada ve sitemap'in lastmod değerinde gösterilir, böylece bir tablonun ne kadar güncel olduğunu her zaman bilirsiniz. Hiçbir veri elle girilmez."),
            ("Alan sözlüğü", "Her sıralama satırı aşağıdaki alanları tutar. Değerler yayımlandığı gibi kopyalanır; eksik bir değerde sayı uydurmak yerine tire gösteririz."),
            ("Sınırlar", "Açık anlık görüntü, yalnızca her liste için ilk 10 uygulamayı ve App Store'un sitede listelenen pazarlarını kapsar. Bu tek bir günlük gözlemidir, canlı akış değildir ve indirme, gelir veya kullanıcı harcaması hakkında bir şey söylemez. Hesaplanan rakamlar olgu değil senaryodur."),
        ],
    },
}

FIELD_LABELS = {
    "en": "Field", "zh": "字段", "ko": "필드", "ja": "項目", "tr": "Alan",
}
FIELD_DESC_LABELS = {
    "en": "Meaning", "zh": "含义", "ko": "의미", "ja": "意味", "tr": "Anlamı",
}

GUIDES = {
    "en": {
        "guides_title": "Guides",
        "guides_h1": "Guides and explainers",
        "guides_sub": "Short, source-backed explanations of the ideas behind the tools.",
        "read_guide": "Read guide",
        "related_title": "Related pages",
        "rank-bands": {
            "title": "Understanding rank bands",
            "desc": "Why a rank position is not a download count, and how the multipliers in the estimator work.",
            "sections": [
                ("Position is not volume", "A chart rank orders apps; it does not count downloads. Two apps can sit one place apart yet have very different audience sizes. Any attempt to turn a rank into a download number is a model, not an observation."),
                ("How our bands work", "The revenue estimator applies Step 1 of that model: a multiplier by rank band. Rank 1 keeps the full base, rank 3 keeps 75 percent, rank 10 keeps 45 percent, rank 20 keeps 25 percent, and rank 30 keeps 12 percent. Worse ranks fall to a five percent floor. The exact table is on the methodology page."),
                ("How to use it honestly", "Change one input at a time and read the direction of the change rather than the absolute figure. If your own analytics give you a real download count, enter it directly and set the band to rank 1 so the multiplier drops out. The result is then only a conversion and fee scenario."),
            ],
        },
        "fee-tiers": {
            "title": "30% versus 15% fee scenarios",
            "desc": "What the two fee tiers in the calculator represent, and what they do not tell you.",
            "sections": [
                ("Two common tiers", "The calculator models two widely discussed store fee rates: a standard 30 percent tier and a small-program 15 percent tier. They are included so you can compare outcomes side by side, not to tell you which one applies to you."),
                ("Eligibility is not decided here", "Program rules, thresholds and regional variations change, and they depend on your account. This site does not check any of them. If a payout number matters for a decision, confirm the current rate with the store directly."),
                ("What the tool does show", "Given a gross amount, the difference between the tiers is pure arithmetic: net equals gross times one minus the rate. On 10,000 in gross revenue the two tiers differ by 1,500. That is the entire claim this page makes."),
            ],
        },
        "market-overlap": {
            "title": "Reading market overlap",
            "desc": "How the shared-app count between two top-10 charts can inform a localization decision.",
            "sections": [
                ("What overlap measures", "The comparison tool counts app IDs present in both top-10 lists on the same snapshot date. A shared app means the same product reaches a top position in both storefronts. The count says nothing about revenue in either market."),
                ("High versus low overlap", "High overlap suggests the two markets are served by similar products, so a port enters a familiar competitive shape. Low overlap suggests local incumbents dominate; a direct port then needs more work on discovery and localization."),
                ("Use it as one input", "Overlap is a quick structural signal, not a verdict. Combine it with language, payment habits and category demand. Because the snapshot is rebuilt daily, watch the trend over several days rather than reacting to a single reading."),
            ],
        },
        "charts-explained": {
            "title": "Free charts and grossing charts",
            "desc": "What each chart reflects and why they should not be read as the same signal.",
            "sections": [
                ("Free charts", "A top-free chart reflects acquisition: which apps are being downloaded most. It rewards reach, launch pushes and virality. A high free rank can be short-lived if retention is weak."),
                ("Grossing charts", "A top-grossing chart reflects spending: which apps generate the most revenue. It rewards monetization and loyal paying users. A high grossing rank can persist with modest download volume."),
                ("Reading them together", "An app high in free but low in grossing is acquiring users without converting them strongly. An app high in grossing but low in free is monetizing a smaller, more valuable base. Comparing both charts in the market pages makes this contrast visible."),
            ],
        },
    },
    "zh": {
        "guides_title": "指南",
        "guides_h1": "指南与详解",
        "guides_sub": "围绕工具背后概念的简短、有据可查的解释。",
        "read_guide": "阅读指南",
        "related_title": "相关页面",
        "rank-bands": {
            "title": "理解排名区间",
            "desc": "为什么名次不等于下载量，以及估算器里的乘数如何工作。",
            "sections": [
                ("名次不是体量", "榜单名次是对应用排序，不是下载计数。两个相差一名的应用，受众规模可能差别很大。任何把名次换算成下载数的做法都是模型，而不是观测。"),
                ("我们的区间如何工作", "收入估算器应用这个模型的第一步：按排名区间给出乘数。第 1 名保留全部基准，第 3 名 75%，第 10 名 45%，第 20 名 25%，第 30 名 12%，更靠后降到 5% 的下限。完整表格见方法论页面。"),
                ("如何诚实地使用", "一次只改一个输入，关注变化方向而非绝对数值。如果你自己的分析数据给出了真实下载量，就直接填入该值，并把区间设为第 1 名，让乘数退出计算。此时结果就只是转化与手续费情景。"),
            ],
        },
        "fee-tiers": {
            "title": "30% 与 15% 费率情景",
            "desc": "计算器里两档费率代表什么，以及它不告诉你什么。",
            "sections": [
                ("两种常见档位", "计算器演示两种常被讨论的商店费率：标准 30% 与小型项目 15%。把它们放在一起是为了便于对比结果，不是为了判定你适用哪一档。"),
                ("资格不由本站判定", "项目规则、门槛和地区差异会变化，而且取决于你的账户。本站不核验其中任何一项。如果某个到账金额会影响决策，请直接向商店确认当前费率。"),
                ("工具真正展示的", "给定总收入，两档之间的差异就是纯算术：净收入等于总收入乘以（1 减费率）。总收入 10,000 时，两档相差 1,500。这就是本页提出的全部主张。"),
            ],
        },
        "market-overlap": {
            "title": "如何理解市场重合度",
            "desc": "两个 Top 10 榜单之间的共同应用数，如何为本地化决策提供参考。",
            "sections": [
                ("重合度衡量什么", "对比工具统计同一快照日期上同时出现在两个 Top 10 榜单中的应用 ID。共同应用意味着同一产品在两个商店前台都进入前列。这个数字不反映任一市场的收入。"),
                ("高重合与低重合", "高重合说明两个市场由相似产品服务，直接移植面对的是熟悉的竞争格局。低重合说明本地应用占据主导，此时直接移植需要在发现和本地化上投入更多。"),
                ("只把它当作一个输入", "重合度是快速的结构性信号，不是结论。请结合语言、支付习惯和品类需求一起看。由于快照每天重建，建议观察几天的趋势，而不是对单次读数做反应。"),
            ],
        },
        "charts-explained": {
            "title": "免费榜与畅销榜",
            "desc": "两种榜单各自反映什么，为什么不该把它们当作同一个信号。",
            "sections": [
                ("免费榜", "免费榜反映获取：哪些应用被下载最多。它奖励覆盖面、发布推力和传播性。如果留存差，高免费名次可能很短暂。"),
                ("畅销榜", "畅销榜反映支出：哪些应用产生最多收入。它奖励变现能力和忠诚的付费用户。即使下载量不大，高畅销名次也可能长期保持。"),
                ("结合起来看", "免费榜高而畅销榜低的应用，获得了用户但转化不强。畅销榜高而免费榜低的应用，正在把较小但更有价值的用户群变现。在市场页里对比两种榜单，能让这种差异显现出来。"),
            ],
        },
    },
    "ko": {
        "guides_title": "가이드",
        "guides_h1": "가이드와 해설",
        "guides_sub": "도구 뒤에 있는 개념을 짧고 출처 기반으로 설명합니다.",
        "read_guide": "가이드 읽기",
        "related_title": "관련 페이지",
        "rank-bands": {
            "title": "순위 구간 이해하기",
            "desc": "순위가 다운로드 수가 아닌 이유와 추정기의 배수가 어떻게 작동하는지.",
            "sections": [
                ("순위는 규모가 아니다", "차트 순위는 앱을 정렬할 뿐 다운로드를 세지 않습니다. 한 순위 차이인 두 앱도 대상 사용자 규모가 크게 다를 수 있습니다. 순위를 다운로드 수로 바꾸는 것은 관측이 아니라 모델입니다."),
                ("우리 구간의 동작", "수익 추정기는 그 모델의 첫 단계를 적용합니다. 순위 구간별 배수입니다. 1위는 기준값 전체, 3위는 75%, 10위는 45%, 20위는 25%, 30위는 12%이며 그보다 낮으면 5% 하한으로 떨어집니다. 정확한 표는 방법 페이지에 있습니다."),
                ("정직하게 사용하는 법", "입력을 한 번에 하나씩 바꾸고 절댓값보다 변화 방향을 읽으세요. 자체 분석으로 실제 다운로드 수를 안다면 그 값을 직접 입력하고 구간을 1위로 두어 배수를 빼버리면 됩니다. 그러면 결과는 전환·수수료 시나리오만 남습니다."),
            ],
        },
        "fee-tiers": {
            "title": "30% 대 15% 수수료 시나리오",
            "desc": "계산기의 두 수수료 등급이 나타내는 것과 나타내지 않는 것.",
            "sections": [
                ("두 가지 일반 등급", "계산기는 널리 알려진 두 스토어 수수료율, 표준 30%와 소기업 15%를 모델링합니다. 나란히 비교하기 위한 것이지 어느 등급이 적용되는지 알려주기 위한 것이 아닙니다."),
                ("적용 자격은 여기서 정하지 않는다", "프로그램 규정, 기준선, 지역 차이는 바뀌며 계정에 따라 다릅니다. 이 사이트는 그런 것들을 확인하지 않습니다. 정산액이 결정에 영향을 준다면 스토어에 현재 요율을 직접 확인하세요."),
                ("도구가 보여주는 것", "총수익이 주어지면 두 등급의 차이는 순수 산술입니다. 순수익은 총수익에 (1 − 요율)을 곱한 값입니다. 총수익 10,000이면 두 등급의 차이는 1,500입니다. 이것이 이 페이지의 주장 전부입니다."),
            ],
        },
        "market-overlap": {
            "title": "시장 겹침 읽기",
            "desc": "두 상위 10개 차트의 공통 앱 수가 현지화 결정에 주는 단서.",
            "sections": [
                ("겹침이 측정하는 것", "비교 도구는 같은 스냅샷 날짜에 두 상위 10개 목록에 모두 있는 앱 ID를 셉니다. 공통 앱은 같은 제품이 두 스토어프런트에서 상위에 올랐음을 뜻합니다. 이 숫자는 어느 시장의 수익도 말하지 않습니다."),
                ("높은 겹침과 낮은 겹침", "겹침이 높으면 두 시장이 비슷한 제품으로 채워져 있어 이식이 익숙한 경쟁 구도에 들어갑니다. 겹침이 낮으면 현지 강자가 지배하고 있어 직접 이식은 발견과 현지화에 더 많은 일이 필요합니다."),
                ("하나의 입력으로만", "겹침은 빠른 구조적 신호일 뿐 결론이 아닙니다. 언어, 결제 습관, 카테고리 수요와 함께 보세요. 스냅샷이 매일 갱신되므로 한 번의 수치보다 며칠의 추세를 관찰하세요."),
            ],
        },
        "charts-explained": {
            "title": "무료 순위와 매출 순위",
            "desc": "각 차트가 무엇을 반영하는지, 같은 신호로 읽으면 안 되는 이유.",
            "sections": [
                ("무료 순위", "무료 순위는 획득을 반영합니다. 어떤 앱이 가장 많이 다운로드되는지입니다. 도달, 출시 밀어주기, 바이럴에 유리합니다. 리텐션이 약하면 높은 무료 순위는 오래가지 않습니다."),
                ("매출 순위", "매출 순위는 지출을 반영합니다. 어떤 앱이 가장 많은 수익을 내는지입니다. 수익화와 충성도 높은 유료 사용자가 유리합니다. 다운로드가 적어도 높은 매출 순위는 오래 유지될 수 있습니다."),
                ("함께 읽기", "무료는 높은데 매출이 낮은 앱은 사용자를 모았지만 전환이 약합니다. 매출은 높은데 무료가 낮은 앱은 작지만 가치 있는 기반을 수익화하고 있습니다. 시장 페이지에서 두 차트를 비교하면 이 대비가 드러납니다."),
            ],
        },
    },
    "ja": {
        "guides_title": "ガイド",
        "guides_h1": "ガイドと解説",
        "guides_sub": "ツールの背景にある考え方を、出典付きで短く説明します。",
        "read_guide": "ガイドを読む",
        "related_title": "関連ページ",
        "rank-bands": {
            "title": "順位帯を理解する",
            "desc": "順位がダウンロード数ではない理由と、推定ツールの倍率の働き。",
            "sections": [
                ("順位は規模ではない", "チャート順位はアプリを並べるだけで、ダウンロードを数えません。1 位違う二つのアプリでも対象ユーザーの規模は大きく異なります。順位をダウンロード数に変える試みは観測ではなくモデルです。"),
                ("わたしたちの帯の仕組み", "売上推定ツールはそのモデルの第一步を適用します。順位帯ごとの倍率です。1 位は基準値いっぱい、3 位は 75%、10 位は 45%、20 位は 25%、30 位は 12% で、それより下は 5% の下限になります。正確な表は方法ページにあります。"),
                ("正直に使うには", "入力を一度に一つだけ変え、絶対値より変化の向きを読みましょう。自社分析で実際のダウンロード数が分かるならその値を直接入れ、帯を 1 位にして倍率を外せば、結果は転換・手数料のシナリオだけになります。"),
            ],
        },
        "fee-tiers": {
            "title": "30% と 15% の手数料シナリオ",
            "desc": "計算ツールの二つの等級が表すものと、表さないもの。",
            "sections": [
                ("二つの一般的な等級", "計算ツールは広く知られる二つのストア手数料率、標準 30% と小規模 15% をモデル化します。並べて比較するためのもので、どちらが適用されるかを判定するものではありません。"),
                ("適用資格はここでは決めない", "プログラム規定、基準、地域差は変わり、アカウントによります。このサイトはそれらを確認しません。振込額が判断に影響するなら、ストアに現在の料率を直接確認してください。"),
                ("ツールが示すこと", "総売上が決まれば二つの等級の差は純粋な算術です。純売上は総売上に (1 − 料率) を掛けた値。総売上 10,000 なら差は 1,500 です。これがこのページの主張のすべてです。"),
            ],
        },
        "market-overlap": {
            "title": "市場の重複を読む",
            "desc": "二つの上位 10 件チャートの共通アプリ数が現地化判断に与える手がかり。",
            "sections": [
                ("重複が測るもの", "比較ツールは同じスナップショット日付で二つの上位 10 件に共通して存在するアプリ ID を数えます。共通アプリは同じ製品が両ストアフロントで上位に入ったことを示します。この数はどちらの市場の売上も示しません。"),
                ("高い重複と低い重複", "重複が高いと二つの市場が似た製品で満たされており、移植は見慣れた競争構造に入ります。低いと現地の強者が支配しており、直接の移植には発見と現地化にもっと手間がかかります。"),
                ("一つの入力として", "重複は素早い構造的な手がかりであり結論ではありません。言語、決済習慣、カテゴリ需要と合わせて見ましょう。スナップショットは毎日更新されるので、一度の値より数日の傾向を観察してください。"),
            ],
        },
        "charts-explained": {
            "title": "無料ランキングと売上ランキング",
            "desc": "各チャートが何を反映し、同じ信号として読んではいけない理由。",
            "sections": [
                ("無料ランキング", "無料ランキングは獲得を反映します。どのアプリが最もダウンロードされているかです。リーチ、ローンチ押し、バイラルに有利です。リテンションが弱いと高い順位は長く続きません。"),
                ("売上ランキング", "売上ランキングは支出を反映します。どのアプリが最も売上を生むかです。収益化と忠実な有料ユーザーに有利です。ダウンロードが少なくても高い順位は長く続きます。"),
                ("一緒に読む", "無料は高いが売上が低いアプリはユーザーを集めたが転換が弱い状態です。売上は高いが無料が低いアプリは小さく価値のある基盤を収益化しています。市場ページで二つのチャートを比べるとこの対比が見えます。"),
            ],
        },
    },
    "tr": {
        "guides_title": "Rehberler",
        "guides_h1": "Rehberler ve açıklamalar",
        "guides_sub": "Araçların ardındaki fikirleri kaynaklı ve kısa biçimde açıklar.",
        "read_guide": "Rehberi oku",
        "related_title": "İlgili sayfalar",
        "rank-bands": {
            "title": "Sıra aralıklarını anlamak",
            "desc": "Bir sıranın indirme sayısı olmaması ve tahmin aracındaki çarpanların nasıl çalıştığı.",
            "sections": [
                ("Konum hacim değildir", "Bir sıralama uygulamaları sıralar, indirmeleri saymaz. Bir sıra farklı iki uygulamanın kitle büyüklüğü çok farklı olabilir. Sırayı indirme sayısına çevirme girişimi bir gözlem değil, modeldir."),
                ("Aralıklarımız nasıl çalışır", "Gelir tahmin aracı modelin ilk adımını uygular: sıra aralığına göre çarpan. 1. sıra taban değerin tamamını, 3. sıra yüzde 75'ini, 10. sıra yüzde 45'ini, 20. sıra yüzde 25'ini, 30. sıra yüzde 12'sini korur; daha kötü sıralar yüzde 5 tabana düşer. Tam tablo yöntem sayfasındadır."),
                ("Dürüstçe kullanmak", "Girdileri tek tek değiştirin ve mutlak değer yerine değişimin yönünü okuyun. Kendi analiz bilgileriniz gerçek indirme sayısını veriyorsa o değeri doğrudan girin ve çarpanı devre dışı bırakmak için aralığı 1. sıraya ayarlayın. Sonuç yalnızca dönüşüm ve ücret senaryosu olur."),
            ],
        },
        "fee-tiers": {
            "title": "Yüzde 30 ve yüzde 15 ücret senaryoları",
            "desc": "Hesaplayıcıdaki iki ücret kademesinin neyi gösterdiği ve neyi göstermediği.",
            "sections": [
                ("İki yaygın kademe", "Hesaplayıcı yaygın bilinen iki mağaza ücret oranını modeller: standart yüzde 30 ve küçük program yüzde 15. Bunlar yan yana karşılaştırma içindir, hangisinin size uygulandığını söylemek için değil."),
                ("Uygunluk burada belirlenmez", "Program kuralları, eşikler ve bölgesel farklılıklar değişir ve hesabınıza bağlıdır. Bu site hiçbirini kontrol etmez. Bir ödeme tutarı kararınızı etkiliyorsa güncel oranı doğrudan mağazadan teyit edin."),
                ("Aracın gösterdiği", "Brüt tutar verildiğinde iki kademe arasındaki fark saf aritmetiktir: net, brüt çarpı (1 − oran). Brüt gelir 10.000 ise iki kademe arasındaki fark 1.500'tür. Bu sayfanın iddiası tam olarak budur."),
            ],
        },
        "market-overlap": {
            "title": "Pazar örtüşmesini okumak",
            "desc": "İki ilk 10 listesindeki ortak uygulama sayısının yerelleştirme kararına ipucu vermesi.",
            "sections": [
                ("Örtüşme neyi ölçer", "Karşılaştırma aracı, aynı anlık görüntü tarihinde iki ilk 10 listesinde bulunan uygulama kimliklerini sayar. Ortak uygulama, aynı ürünün iki mağaza bölgesinde de üst sıraya çıktığını gösterir. Bu sayı hiçbir pazarın gelirini anlatmaz."),
                ("Yüksek ve düşük örtüşme", "Yüksek örtüşme, iki pazarın benzer ürünlerle hizmet edildiğini ve taşımanın tanıdık bir rekabet yapısına girdiğini gösterir. Düşük örtüşmede yerel güçler baskındır; doğrudan taşıma keşif ve yerelleştirme için daha fazla iş ister."),
                ("Tek bir girdi olarak", "Örtüşme hızlı yapısal bir sinyaldir, hüküm değil. Dil, ödeme alışkanlıkları ve kategori talebiyle birlikte değerlendirin. Görüntü her gün yenilendiği için tek bir okuma yerine birkaç günün eğilimini izleyin."),
            ],
        },
        "charts-explained": {
            "title": "Ücretsiz ve hasılat listeleri",
            "desc": "Her listenin neyi yansıttığı ve aynı sinyal olarak okunmaması gerektiği.",
            "sections": [
                ("Ücretsiz listeler", "Ücretsiz liste edinimi yansıtır: hangi uygulamalar en çok indiriliyor. Erişim, lansman itmesi ve yayılma avantajlıdır. Tutma zayıfsa yüksek sıra kısa ömürlü olabilir."),
                ("Hasılat listeleri", "Hasılat listesi harcamayı yansıtır: hangi uygulamalar en çok gelir üretiyor. Para kazanma ve sadık ücretli kullanıcılar avantajlıdır. İndirme az olsa da yüksek sıra uzun süre korunabilir."),
                ("Birlikte okumak", "Ücretsizde yüksek ama hasılatta düşük uygulama, kullanıcı toplayıp iyi dönüştüremeyen uygulamadır. Hasılatta yüksek ama ücretsizde düşük uygulama, küçük ama değerli bir kitleyi para kazanandır. Pazar sayfalarında iki listeyi karşılaştırmak bu farkı görünür kılar."),
            ],
        },
    },
}

GUIDE_SLUGS = ("rank-bands", "fee-tiers", "market-overlap", "charts-explained")
