import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# Base URL of WineBid auction site
BASE_URL = "https://www.winebid.com"

# Headers to mimic a browser request
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Step 1: Get the main auction page that lists all available wines
vintage_page_url = f"{BASE_URL}/BuyWine/Vintages/-"
response = requests.get(vintage_page_url, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")

# Step 2: Extract all available wine listings for the year 1900
wine_data = []
wine_links = soup.find_all("a", class_="gtmProducerItem")  # All wine links

for wine_link in wine_links:
    wine_href = wine_link["href"]  # Extract URL path
    wine_name = wine_link.text.strip()  # Extract wine name

    # Extract year and unique code from the link pattern: /BuyWine/Item/Auction/{unique_code}/{year}
    match = re.search(r"/BuyWine/Item/Auction/(\d+)/(\d+)", wine_href)
    if match:
        unique_code, year = match.groups()

        # Test case: Ensure we are only scraping 1900
        if year != "1900":
            continue  # Skip other years

        wine_url = f"{BASE_URL}{wine_href}"

        # Step 3: Visit the wine's individual page to get price
        wine_page_response = requests.get(wine_url, headers=HEADERS)
        wine_soup = BeautifulSoup(wine_page_response.text, "html.parser")

        # Extract price
        price_div = wine_soup.find("div", class_="price")
        price = "N/A"
        if price_div:
            price_tag = price_div.find("a", class_="gtmItem")
            if price_tag:
                price = price_tag.text.strip()

        # Test cases: Verify data extraction
        assert wine_url.startswith(BASE_URL), f"❌ Invalid wine URL: {wine_url}"
        assert "1900" in wine_name, f"❌ Wine name does not contain year: {wine_name}"
        assert price.startswith(
            "$") or price == "N/A", f"❌ Unexpected price format: {price}"

        # Save the data
        wine_data.append([wine_name, year, unique_code, wine_url, price])
        print(f"✅ Scraped: {wine_name} ({year}) - {price}")

        time.sleep(1)  # Respectful delay between requests

# Step 4: Save results to CSV
df = pd.DataFrame(wine_data, columns=[
                  "Wine Name", "Year", "Unique Code", "Wine URL", "Price"])
df.to_csv("data/auction_prices/winebid_prices.csv", index=False)

print("\n✅ Scraping complete! Data saved to wine_prices_1900.csv")
4
