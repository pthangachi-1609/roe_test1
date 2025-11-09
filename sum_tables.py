# sum_tables.py
import asyncio
import re
from playwright.async_api import async_playwright

# --- Configuration ---
BASE_URL = 'https://sanand0.github.io/tdsdata/js_table/'
SEEDS = range(25, 35) # Generates seeds 25 to 34

async def run():
    # Initialize total_sum as Python's native int, which has arbitrary precision
    total_sum = 0
    
    async with async_playwright() as p:
        # Note: If Playwright itself is converting to float during extraction,
        # you might need to use page.evaluate to force string extraction.
        browser = await p.chromium.launch()
        page = await browser.new_page()

        print(f"Starting scraping process for {len(SEEDS)} reports.")

        for seed in SEEDS:
            url = f"{BASE_URL}?seed={seed}"
            
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                
                # Use page.evaluate to extract the raw text content of the table, 
                # ensuring no intermediate floating-point conversion by Playwright.
                table_text_content = await page.evaluate('''
                    () => {
                        const table = document.querySelector('table');
                        // Ensure text is extracted as a single raw string
                        return table ? table.textContent.replace(/\s+/g, '') : '';
                    }
                ''')
                
                # Regex to find sequences of digits (the large numbers)
                numbers_str = re.findall(r'\d+', table_text_content)
                
                page_sum = 0
                for num_str in numbers_str:
                    try:
                        # CRITICAL FIX: Use int() instead of float() to handle large integers
                        num = int(num_str)
                        page_sum += num
                    except ValueError:
                        pass # Ignore non-integer strings
                
                total_sum += page_sum
                # Print page sum (Python int printing will be correct)
                print(f"Visited {url}. Page sum: {page_sum}")

            except Exception as e:
                print(f"Error visiting {url}: {e}")

        await browser.close()

    # Final result will be a very large, correctly calculated integer
    print('\n--- FINAL QA SUM ---')
    print(total_sum)

if __name__ == "__main__":
    import os
    # Playwright requires the event loop to be properly set up, especially 
    # when running from environments like GitHub Actions.
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run())
