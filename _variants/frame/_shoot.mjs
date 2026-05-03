import puppeteer from "/Users/iisalman/Desktop/ClaudeTests/Hadeel/node_modules/puppeteer/lib/esm/puppeteer/puppeteer.js";
import fs from "node:fs";

const OUT = "_shots";
fs.mkdirSync(OUT, { recursive: true });
const BASE = "http://localhost:8766/_variants/frame/";

const browser = await puppeteer.launch({ headless: "new" });

async function shoot(name, url, viewport, actions = []) {
  const page = await browser.newPage();
  await page.setViewport(viewport);
  await page.goto(url, { waitUntil: "networkidle0" });
  await new Promise((r) => setTimeout(r, 800));
  for (const a of actions) await a(page);
  await page.screenshot({ path: `${OUT}/${name}.png`, fullPage: false });
  console.log(`shot ${name}.png`);
  await page.close();
}

async function shootFull(name, url, viewport) {
  const page = await browser.newPage();
  await page.setViewport(viewport);
  await page.goto(url, { waitUntil: "networkidle0" });
  await new Promise((r) => setTimeout(r, 1200));
  await page.screenshot({ path: `${OUT}/${name}.png`, fullPage: true });
  console.log(`shot ${name}.png (full)`);
  await page.close();
}

const desktop = { width: 1440, height: 900 };
const mobile = { width: 390, height: 844 };

// Desktop — index
await shoot("d1-index-hero", BASE + "index.html", desktop);
await shoot("d2-index-mid", BASE + "index.html", desktop, [
  async (p) => p.evaluate(() => window.scrollTo(0, 1500)),
  async () => new Promise((r) => setTimeout(r, 600)),
]);
await shoot("d3-index-projects", BASE + "index.html", desktop, [
  async (p) => p.evaluate(() => window.scrollTo(0, 2400)),
  async () => new Promise((r) => setTimeout(r, 600)),
]);
await shoot("d4-index-end", BASE + "index.html", desktop, [
  async (p) => p.evaluate(() => window.scrollTo(0, document.body.scrollHeight)),
  async () => new Promise((r) => setTimeout(r, 600)),
]);

// Desktop — almamlaka project page
await shoot("d5-project-hero", BASE + "project-almamlaka.html", desktop);
await shoot("d6-project-essay", BASE + "project-almamlaka.html", desktop, [
  async (p) => p.evaluate(() => window.scrollTo(0, 1300)),
  async () => new Promise((r) => setTimeout(r, 600)),
]);
await shoot("d7-project-plates", BASE + "project-almamlaka.html", desktop, [
  async (p) => p.evaluate(() => window.scrollTo(0, 2400)),
  async () => new Promise((r) => setTimeout(r, 600)),
]);

// Desktop — contact
await shoot("d8-contact", BASE + "contact.html", desktop);

// Mobile — index
await shoot("m1-index-hero", BASE + "index.html", mobile);
await shoot("m2-index-projects", BASE + "index.html", mobile, [
  async (p) => p.evaluate(() => window.scrollTo(0, 1100)),
  async () => new Promise((r) => setTimeout(r, 500)),
]);

// Mobile — project
await shoot("m3-project-hero", BASE + "project-almamlaka.html", mobile);
await shoot("m4-project-plates", BASE + "project-almamlaka.html", mobile, [
  async (p) => p.evaluate(() => window.scrollTo(0, 1800)),
  async () => new Promise((r) => setTimeout(r, 500)),
]);

await browser.close();
console.log("done");
