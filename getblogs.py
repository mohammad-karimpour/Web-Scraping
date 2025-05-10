import asyncio
import aiohttp
import hashlib
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


url = input('url:')
item_tag = input('select tag:')
pageing = input('pageing:')
max_pages = 50 




results_B = set()
all_page_links_B = set()
first_page_hash_B = None


def get_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

async def fetch(session, page_url):
    try:
        async with session.get(page_url, timeout=60) as response:
            if response.status == 404:
                return page_url, None
            html = await response.text()
            return page_url, html
    except Exception as e:
        print(f"⚠️ خطا در {page_url}: {e}")
        return page_url, None

async def parse_page(base_url, html, is_first=False):
    global first_page_hash_B

    if not html:
        return set(), True

    soup = BeautifulSoup(html, "html.parser")
    html_hash = get_hash(html)

    if is_first:
        first_page_hash_B = html_hash
    elif html_hash == first_page_hash_B:
        return set(), True

    blocks = soup.select(item_tag)
    page_links = set()

    for block in blocks:
        link = block.select_one("a")
        if link:
            href = link.get("href")
            if href:
                full_url = urljoin(base_url, href)
                parsed_url = urlparse(full_url)
                clean_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
                page_links.add(clean_url)

    return page_links, False

async def scrape_all_pages():
    global results_B, all_page_links_B

    async with aiohttp.ClientSession() as session:
        tasks = []
        if pageing == "":
            tasks.append(fetch(session, url))
        else:
            for page_number in range(1, max_pages + 1):
                page_url = f"{url}{pageing}{page_number}"
                tasks.append(fetch(session, page_url))
        responses = await asyncio.gather(*tasks)

        for index, (page_url, html) in enumerate(responses):
            if html is None:
                continue

            is_first = (index == 0)
            page_links, is_duplicate = await parse_page(url, html, is_first=is_first)

            new_links = page_links - all_page_links_B
            if new_links:
                all_page_links_B.update(new_links)
                results_B.update(new_links)

            if is_duplicate:
                print(f"⚠️ صفحه {page_url} مشابه صفحه اول بود. رد شد.")

asyncio.run(scrape_all_pages())

print('BeautifulSoup:',results_B)
print(f"\n🔢 تعداد لینک‌های یکتا: {len(results_B)}")

    
















results_P = set()
all_page_links = set()
first_page_hash = None

def get_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

async def scrape_page(page, page_url, is_first=False):
    global first_page_hash

    await page.goto(page_url, timeout=90000, wait_until='load')
    html = await page.content()
    html_hash = get_hash(html)

    if is_first:
        first_page_hash = html_hash
    elif html_hash == first_page_hash:
        print("محتوای صفحه مشابه صفحه اول است. توقف.")
        return None, True

    blocks = await page.query_selector_all(item_tag)
    current_links = set()

    for block in blocks:
        link = await block.query_selector("a")
        if link:
            href = await link.get_attribute("href")
            if href:
                full_url = urljoin(url, href)
                parsed_url = urlparse(full_url)
                clean_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
                current_links.add(clean_url)

    if not current_links:
        print("هیچ لینکی یافت نشد. توقف.")
        return None, True

    return current_links, False

async def main():
    global results_P, all_page_links
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        if pageing == "":
            links, _ = await scrape_page(page, url, is_first=True)
            if links:
                results_P.update(links)
        else:
            page_number = 1
            while True:
                page_url = f"{url}{pageing}{page_number}"
                links, stop = await scrape_page(page, page_url, is_first=(page_number == 1))

                if stop or not links:
                    break

                # بررسی لینک‌های جدید نسبت به کل صفحات قبلی
                new_links = links - all_page_links
                if not new_links:
                    print("⛔ لینک جدیدی نسبت به صفحات قبلی پیدا نشد. توقف.")
                    break

                results_P.update(new_links)
                all_page_links.update(new_links)
                page_number += 1
                await asyncio.sleep(1)  # وقفه بین صفحات

        await browser.close()

    print('playwright:',results_P)
    print(f"\n🔢 تعداد کل لینک‌های یکتا: {len(results_P)}")

asyncio.run(main())