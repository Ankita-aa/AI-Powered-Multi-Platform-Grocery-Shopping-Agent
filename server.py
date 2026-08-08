import asyncio
import re
import sys
from mcp.server.fastmcp import FastMCP
from playwright.async_api import async_playwright

# Initialize the FastMCP server
mcp = FastMCP("grocery-server")


@mcp.tool()
async def search_grocery(item: str) -> dict:
    """Search grocery item price and stock on Zepto."""
    print(f"Received search request for item: {item}", file=sys.stderr)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # 1. Load homepage
            await page.goto(
                "https://www.zeptonow.com",
                wait_until="domcontentloaded",
                timeout=60000,
            )
            print("Homepage loaded", file=sys.stderr)
            await page.wait_for_timeout(3000)

            # 2. Set location if pop-up appears
            try:
                location_btn = page.get_by_text("Select Location")
                if await location_btn.is_visible(timeout=5000):
                    await location_btn.click()
                    print("Location popup opened", file=sys.stderr)

                    location_input = 'input[placeholder*="Search"]'
                    await page.wait_for_selector(location_input, timeout=10000)
                    await page.fill(location_input, "Wakad Pune")
                    print("Typed location", file=sys.stderr)
                    await page.wait_for_timeout(2000)

                    await page.locator("text=Wakad").first.click()
                    print("Location selected", file=sys.stderr)
                    await page.wait_for_timeout(3000)
            except Exception as loc_err:
                print(
                    f"Location selection skipped/failed: {loc_err}",
                    file=sys.stderr,
                )

            # 3. Search product
            await page.goto(
                f"https://www.zeptonow.com/search?query={item}",
                wait_until="domcontentloaded",
                timeout=60000,
            )
            print("Search page loaded", file=sys.stderr)
            await page.wait_for_timeout(5000)

            # 4. Extract product details from visible text
            text = await page.locator("body").inner_text()
            lines = [
                line.strip() for line in text.split("\n") if line.strip()
            ]

            products = []
            for i, line in enumerate(lines):
                if line.startswith("₹"):
                    price_digits = re.sub(r"[^\d]", "", line.replace("₹", ""))
                    if not price_digits:
                        continue
                    price = int(price_digits)

                    product = ""
                    for j in range(i + 1, min(i + 9, len(lines))):
                        candidate = lines[j]
                        invalid = (
                            candidate.startswith("₹")
                            or candidate == "ADD"
                            or candidate.startswith("(")
                            or re.match(r"^\d+(\.\d+)?$", candidate)
                            or "OFF" in candidate
                            or "pack" in candidate
                            or "ml" in candidate
                            or len(candidate) < 5
                        )
                        if not invalid:
                            product = candidate
                            break

                    if product and price:
                        products.append({"name": product, "price": price})

            # Deduplicate products by name
            unique_products = []
            seen_names = set()
            for prod in products:
                if prod["name"] not in seen_names:
                    seen_names.add(prod["name"])
                    unique_products.append(prod)

            await browser.close()
            return {
                "location": "Wakad Pune",
                "available": len(unique_products) > 0,
                "products": unique_products[:5],
            }

        except Exception as err:
            print(f"Scraper Error: {err}", file=sys.stderr)
            await browser.close()
            return {"available": False, "error": str(err)}


if __name__ == "__main__":
    # Runs the MCP server using stdio transport
    mcp.run(transport="stdio")