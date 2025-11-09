# sum_tables.py
import asyncio
import re
from playwright.async_api import async_playwright

# --- Configuration ---
BASE_URL = 'https://sanand0.github.io/tdsdata/js_table/'
SEEDS = range(25, 35) 

async def run():
    # Initialize total_sum as Python's native int (arbitrary precision)
    total_sum = 0
    
    async with async_playwright() as p:
        # Launch browser without head (headless mode)
        browser = await p.chromium.launch()
        page = await browser.new_page()

        print(f"Starting scraping process for {len(SEEDS)} reports.")

        for seed in SEEDS:
            url = f"{BASE_URL}?seed={seed}"
            
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                
                # CRITICAL STEP: Use page.evaluate to get the raw text 
                # to prevent floating-point conversion by the browser or Playwright's high-level methods.
                table_text_content = await page.evaluate('''
                    () => {
                        const table = document.querySelector('table');
                        // Get raw text and remove all whitespace for concatenation
                        return table ? table.textContent.replace(/\s+/g, '') : '';
                    }
                ''')
                
                # Regex to find sequences of digits (assuming the numbers are integers)
                numbers_str = re.findall(r'\d+', table_text_content)
                
                page_sum = 0
                for num_str in numbers_str:
                    try:
                        # CRITICAL FIX: Use int() for arbitrary precision
                        num = int(num_str)
                        page_sum += num
                    except ValueError:
                        pass
                
                total_sum += page_sum
                print(f"Visited {url}. Page sum: {page_sum}")

            except Exception as e:
                print(f"Error visiting {url}: {e}")

        await browser.close()

    # The final printout will be the huge, correct integer sum.
    print('\n--- FINAL QA SUM ---')
    print(total_sum)

if __name__ == "__main__":
    import os
    # Setup for compatibility (optional, but good practice)
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run())
