// sum_tables.js
const { chromium } = require('playwright');

// --- Configuration ---
// Corrected BASE_URL based on user input
const BASE_URL = 'https://sanand0.github.io/tdsdata/js_table/';
const SEEDS = Array.from({ length: 10 }, (_, i) => 25 + i); // Generates seeds 25 to 34

async function run() {
    let totalSum = 0;
    const browser = await chromium.launch();
    const page = await browser.newPage();

    console.log(`Starting scraping process for ${SEEDS.length} reports.`);

    for (const seed of SEEDS) {
        const url = `${BASE_URL}?seed=${seed}`; // Appends the seed as a query parameter
        
        try {
            await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
            
            // 1. Get all text content from all tables
            const tableTextContents = await page.locator('table').allTextContents();
            
            // 2. Combine the text into a single string
            const combinedText = tableTextContents.flat().join(' ');
            
            // 3. Use regex to find all numbers (integers and floats)
            const numbers = combinedText.match(/[-]?\d+(\.\d+)?/g) || [];

            let pageSum = 0;
            for (const numStr of numbers) {
                const num = parseFloat(numStr);
                if (!isNaN(num)) {
                    pageSum += num;
                }
            }
            
            totalSum += pageSum;
            console.log(`Visited ${url}. Page sum: ${pageSum.toFixed(2)}`);

        } catch (error) {
            console.error(`Error visiting ${url}: ${error.message}`);
        }
    }

    await browser.close();

    // 4. Print the final total sum, which is the required output
    console.log('\n--- FINAL QA SUM ---');
    console.log(totalSum); 
}

run();
