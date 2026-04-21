import puppeteer from 'puppeteer';
import { existsSync, mkdirSync, readdirSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const screenshotDir = join(__dirname, 'temporary screenshots');
if (!existsSync(screenshotDir)) mkdirSync(screenshotDir);

const url = process.argv[2] || 'http://localhost:3000';
const label = process.argv[3] || 'mobile';

const existing = readdirSync(screenshotDir).filter(f => f.startsWith('screenshot-'));
const nums = existing.map(f => parseInt(f.match(/screenshot-(\d+)/)?.[1] || '0', 10));
const nextNum = nums.length > 0 ? Math.max(...nums) + 1 : 1;
const filename = `screenshot-${nextNum}-${label}.png`;

const browser = await puppeteer.launch({ headless: true });
const page = await browser.newPage();
await page.setViewport({ width: 390, height: 844 });
await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
await new Promise(r => setTimeout(r, 300));
await page.screenshot({ path: join(screenshotDir, filename), fullPage: false });
console.log(`Screenshot saved: temporary screenshots/${filename}`);
await browser.close();
