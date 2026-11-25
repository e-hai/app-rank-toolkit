# AppRank Toolkit

一个基于公开 App Store 排名数据的免费工具站，目标是提供真正可计算的 ASO 工具，而不是批量 SEO 页面。

当前 MVP：

- 排名变化计算器
- 收入情景计算器
- 市场对比工具
- 商店手续费计算器
- 方法论页面
- 五种语言：英文、韩语、日语、中文、土耳其语
- 30 个可索引 URL

数据源：`https://e-hai.github.io/Appstore_Top_30/api`

所有收入数字都是透明公式下的情景估算，不是实际收入或计费建议。

## 本地运行

```bash
python3 src/refresh_data.py --out data/snapshot.json
python3 src/generate.py --out site
python3 -m unittest discover -s src -p 'test_*.py' -v
```

## 公式

- 排名区间乘数：1→1.0，3→0.75，10→0.45，20→0.25，30→0.12，更差→0.05
- `gross = downloads × rank_multiplier × conversion_rate × price`
- `net = gross × (1 - fee_rate)`
- 标准费率 30%，小型项目费率 15%

## 部署

托管在 Cloudflare Pages 免费 `pages.dev` 域名，不使用 GitHub Pages。

- GitHub 仓库：`e-hai/seo-app-rank-toolkit`
- Cloudflare Pages 项目：`apprank-toolkit`
- 默认线上域名：`https://apprank-toolkit.pages.dev`

GitHub Actions 每次 push 会：

1. 刷新数据快照
2. 运行测试
3. 生成静态站
4. 检查 sitemap / hreflang / 占位符
5. 注入 GSC 验证文件（如果配置了 secret）
6. 部署到 Cloudflare Pages

Bing 提交未启用。

## 测试

```bash
npm run test:py      # 22 项离线单测：公式、生成、sitemap、面包屑、状态持久化、矩阵一致性
npm run build        # 生成 site/
npm run test:e2e     # 真实 Chrome 跑四个计算器（需先 build）
```

`test:e2e` 用本机 Chrome（`channel: "chrome"`），不额外下载浏览器。覆盖 19 项：默认漏斗、下载量预设、URL 还原、切语言保持选择、市场对比双排名、同市场拒绝、空输入报错、矩阵 6×6 与对角线、390px 无横向溢出。CI 不跑 e2e（GitHub runner 无桌面 Chrome），本地改完计算器脚本后跑一次即可。

## 流量统计（Cloudflare Web Analytics）

无 cookie，不需要同意弹窗。开启步骤：

1. Cloudflare Dashboard → Analytics → Web Analytics → Add site
2. 输入 `apprank-toolkit.pages.dev`，安装方式选 **JS snippet**
3. 复制片段里的 `token`
4. `gh secret set CF_WA_TOKEN -R e-hai/seo-app-rank-toolkit`（或写到仓库 Secrets 页）

配置后 `src/config.py` 读取 `CF_WA_TOKEN`，生成时给每页尾部注入一行 beacon 脚本；未配置则完全不输出，不会留下空标签。金额与页面结构不受影响。
