import puppeteer from 'puppeteer';
import { existsSync, mkdirSync, readdirSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const screenshotDir = join(__dirname, 'temporary screenshots');
if (!existsSync(screenshotDir)) mkdirSync(screenshotDir);

const url = process.argv[2] || 'http://localhost:3000';

const existing = readdirSync(screenshotDir).filter(f => f.startsWith('screenshot-'));
const nums = existing.map(f => parseInt(f.match(/screenshot-(\d+)/)?.[1] || '0', 10));
let n = nums.length > 0 ? Math.max(...nums) + 1 : 1;

const browser = await puppeteer.launch({ headless: true });
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900 });
await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });

// Scroll down 1200px and wait for nav to hide
await page.evaluate(() => window.scrollTo({ top: 1200, behavior: 'instant' }));
await new Promise(r => setTimeout(r, 500));
// Trigger another scroll-down event so direction is detected as "down"
await page.evaluate(() => window.scrollBy({ top: 40, behavior: 'instant' }));
await new Promise(r => setTimeout(r, 500));
await page.screenshot({ path: join(screenshotDir, `screenshot-${n++}-scroll-down.png`), fullPage: false });

// Scroll up - nav should reappear
await page.evaluate(() => window.scrollBy({ top: -100, behavior: 'instant' }));
await new Promise(r => setTimeout(r, 500));
await page.screenshot({ path: join(screenshotDir, `screenshot-${n++}-scroll-up.png`), fullPage: false });

console.log('Saved scroll-down and scroll-up screenshots');
await browser.close();
