// Smoke test: load each page, capture console errors, screenshot dark + light, check toggles work.
import puppeteer from "/Users/iisalman/Desktop/ClaudeTests/Hadeel/node_modules/puppeteer/lib/esm/puppeteer/puppeteer.js";
import path from "node:path";
import fs from "node:fs";

const PAGES = [
  "index.html",
  "contact.html",
  "project-almamlaka.html",
  "project-coffee-day.html",
  "project-courtyard.html",
  "project-lavender.html",
  "project-almaarefa.html",
  "project-awjaj.html",
  "project-culinary.html",
  "project-company.html",
];

const BASE = "http://localhost:8766/";
const OUT = "_verify";
fs.mkdirSync(OUT, { recursive: true });

const browser = await puppeteer.launch({
  headless: "new",
  defaultViewport: { width: 1440, height: 900 },
});
const errors = [];

for (const p of PAGES) {
  const page = await browser.newPage();
  const consoleErrors = [];
  page.on("pageerror", (e) => consoleErrors.push(`PAGEERROR: ${e.message}`));
  page.on("console", (m) => {
    if (m.type() === "error") consoleErrors.push(`CONSOLE: ${m.text()}`);
  });
  page.on("requestfailed", (r) => {
    const url = r.url();
    if (url.startsWith("http://localhost")) consoleErrors.push(`requestfailed: ${url}`);
  });
  page.on("response", (r) => {
    const status = r.status();
    const url = r.url();
    if (status === 404 && url.startsWith("http://localhost")) {
      consoleErrors.push(`HTTP_404: ${url}`);
    }
  });

  try {
    // Reset to dark + en first
    await page.evaluateOnNewDocument(() => {
      localStorage.setItem("theme", "dark");
      localStorage.setItem("lang", "en");
    });
    await page.goto(BASE + encodeURI(p), { waitUntil: "networkidle2", timeout: 30000 });
    // Wait for fonts + images
    await new Promise((r) => setTimeout(r, 1200));
    await page.screenshot({ path: path.join(OUT, p.replace(".html", "") + "-dark.png"), fullPage: false });
    if (p === "index.html") {
      await page.screenshot({ path: path.join(OUT, "index-full-dark.png"), fullPage: true });
    }

    // Toggle theme
    await page.click("#theme-toggle");
    await new Promise((r) => setTimeout(r, 350));
    const theme = await page.evaluate(() => document.documentElement.getAttribute("data-theme"));
    if (theme !== "light") consoleErrors.push(`THEME_TOGGLE_FAILED: got ${theme}`);
    await page.screenshot({ path: path.join(OUT, p.replace(".html", "") + "-light.png"), fullPage: false });

    // Toggle language to AR
    await page.click("#lang-toggle");
    await new Promise((r) => setTimeout(r, 350));
    const dir = await page.evaluate(() => document.documentElement.getAttribute("dir"));
    if (dir !== "rtl") consoleErrors.push(`LANG_TOGGLE_FAILED: dir=${dir}`);
  } catch (e) {
    consoleErrors.push(`THROW: ${e.message}`);
  }

  if (consoleErrors.length) {
    errors.push({ page: p, errs: consoleErrors });
  } else {
    console.log(`✓ ${p}`);
  }
  await page.close();
}

await browser.close();

if (errors.length) {
  console.log("\n=== ERRORS ===");
  for (const e of errors) {
    console.log(`\n${e.page}:`);
    for (const m of e.errs) console.log(`  ${m}`);
  }
  process.exit(1);
} else {
  console.log("\nAll pages clean.");
}
