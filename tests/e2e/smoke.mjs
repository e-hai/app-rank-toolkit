// End-to-end smoke tests for the four calculators, run against the locally
// generated site (site/). Uses the installed Chrome to avoid downloading a
// Playwright browser.
//
//   npm run test:e2e        (after `python3 src/generate.py --out site`)
import { chromium } from "playwright";
import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { extname, join, normalize } from "node:path";

const ROOT = new URL("../../site/", import.meta.url).pathname;
const PORT = 4319;
const TYPES = { ".html": "text/html; charset=utf-8", ".xml": "application/xml",
                ".json": "application/json", ".css": "text/css", ".js": "text/javascript" };

function serve() {
  const server = createServer(async (req, res) => {
    const url = new URL(req.url, `http://127.0.0.1:${PORT}`);
    let path = join(ROOT, normalize(decodeURIComponent(url.pathname)));
    if (url.pathname.endsWith("/")) path = join(path, "index.html");
    try {
      const body = await readFile(path);
      res.writeHead(200, { "content-type": TYPES[extname(path)] || "application/octet-stream" });
      res.end(body);
    } catch {
      res.writeHead(404).end("not found");
    }
  });
  return new Promise((resolve) => server.listen(PORT, () => resolve(server)));
}

const failures = [];
function check(name, ok, detail = "") {
  if (ok) console.log(`  ok   ${name}`);
  else {
    console.log(`  FAIL ${name} ${detail}`);
    failures.push(name);
  }
}

async function main() {
  const server = await serve();
  const base = `http://127.0.0.1:${PORT}`;
  const browser = await chromium.launch({ channel: "chrome", headless: true });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });

  // 1. Default scenario renders a full funnel, not a bare number.
  await page.goto(`${base}/tools/revenue-estimator/`);
  const result = (await page.locator("#result").innerText()).replace(/\s+/g, " ");
  check("revenue default funnel", /3,143\.70/.test(result) && /Paying users/i.test(result), result);
  check("revenue five rows", await page.locator("#result table.res tr").count() === 5);

  // 2. Download presets change the input and recalculate.
  await page.locator('[data-dl="5000"]').click();
  check("preset sets downloads", await page.locator("#downloads").inputValue() === "5000");
  const presetResult = (await page.locator("#result").innerText()).replace(/\s+/g, " ");
  check("preset recalculates", !/22,500/.test(presetResult), presetResult);

  // 3. State survives reload and the URL carries it.
  await page.goto(`${base}/tools/revenue-estimator/?rank=3&downloads=500000`);
  check("query restores value", await page.locator("#downloads").inputValue() === "500000");
  check("url keeps query", page.url().includes("downloads=500000"));

  // 4. Switching language keeps the selection.
  await page.locator(".langs a", { hasText: "ZH" }).click();
  await page.waitForLoadState("domcontentloaded");
  check("zh url keeps query", page.url().includes("/zh/tools/revenue-estimator/") && page.url().includes("500000"));
  check("zh keeps downloads", await page.locator("#downloads").inputValue() === "500000");
  const zh = (await page.locator("#result").innerText()).replace(/\s+/g, " ");
  check("zh result is chinese", /到手/.test(zh) || /净/.test(zh), zh);

  // 5. Market compare restores a pair and returns two-sided ranks.
  await page.goto(`${base}/tools/market-compare/?a=kr&b=tr&chart=grossing`);
  check("compare selects a", await page.locator("#a").inputValue() === "kr");
  check("compare selects b", await page.locator("#b").inputValue() === "tr");
  check("compare selects chart", await page.locator("#chart").inputValue() === "grossing");
  const cmp = (await page.locator("#result").innerText()).replace(/\s+/g, " ");
  check("compare shows both ranks", /#\d+ . #\d+/.test(cmp), cmp);

  // 6. Same market on both sides is refused, not silently 10/10.
  await page.locator("#b").selectOption("kr");
  await page.locator('button[type="submit"]').click();
  const same = await page.locator("#result").innerText();
  check("same pair rejected", /different markets/i.test(same), same);

  // 7. Invalid input is reported, never rendered as $0.00.
  await page.goto(`${base}/tools/fee-calculator/`);
  await page.locator("#gross").fill("");
  await page.locator('button[type="submit"]').click();
  const bad = await page.locator("#result").innerText();
  check("empty gross rejected", /Invalid input/i.test(bad) && !/\$0\.00/.test(bad), bad);

  // 8. Overlap matrix is present, square and symmetric.
  await page.goto(`${base}/tools/market-compare/`);
  const tableCount = await page.locator(".matrix table").count();
  check("matrix has two charts", tableCount === 2, String(tableCount));
  const rows = await page.locator(".matrix table").first().locator("tbody tr").count();
  check("matrix is 6x6", rows === 6, String(rows));
  const firstCell = await page.locator(".matrix table").first().locator("tbody tr").first().locator("td").first().innerText();
  check("diagonal is 10", firstCell.trim() === "10", firstCell);

  // 9. Phones: no horizontal overflow on the heaviest page.
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(`${base}/tools/market-compare/`);
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  check("no horizontal overflow at 390px", overflow <= 1, String(overflow));

  await browser.close();
  server.close();
  if (failures.length) {
    console.log(`\n${failures.length} failed`);
    process.exit(1);
  }
  console.log("\nall e2e checks passed");
}

main().catch((e) => { console.error(e); process.exit(1); });
