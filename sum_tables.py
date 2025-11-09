# sum_tables.py
import asyncio
import re
from playwright.async_api import async_playwright

# --- Configuration ---
BASE_URL = 'https://sanand0.github.io/tdsdata/js_table/'
SEEDS = range(25, 35) # Generates seeds 25 to 34

async def run():
    total_sum = 0
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        print(f"Starting scraping process for {len(SEEDS)} reports.")

        for seed in SEEDS:
            url = f"{BASE_URL}?seed={seed}"
            
            try:
                # 1. Navigate to the page
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                
                # 2. Get all text content from all tables
                # This selects all <table> elements and extracts their inner text
                table_locators = page.locator('table')
                table_text_contents = await table_locators.all_text_contents()
                
                # 3. Combine text and use regex to find all numbers
                combined_text = ' '.join(table_text_contents)
                
                # Regex to find integers and decimals (handles optional negative sign)
                numbers_str = re.findall(r'[-]?\d+\.?\d*', combined_text)
                
                page_sum = 0
                for num_str in numbers_str:
                    try:
                        num = float(num_str)
                        page_sum += num
                    except ValueError:
                        # Should not happen if regex is correct, but safe check
                        pass
                
                total_sum += page_sum
                print(f"Visited {url}. Page sum: {page_sum:.2f}")

            except Exception as e:
                print(f"Error visiting {url}: {e}")

        await browser.close()

    # 4. Print the final total sum, which is the required output
    print('\n--- FINAL QA SUM ---')
    print(total_sum)

if __name__ == "__main__":
    asyncio.run(run())
