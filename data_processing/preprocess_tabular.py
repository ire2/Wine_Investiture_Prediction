import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import json

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

        # Ensure we are only scraping 1900 wines
        if year != "1900":
            continue

        wine_url = f"{BASE_URL}{wine_href}"

        # Step 3: Visit the wine's individual page to get additional details
        wine_page_response = requests.get(wine_url, headers=HEADERS)
        wine_soup = BeautifulSoup(wine_page_response.text, "html.parser")

        # Extract current price
        price_div = wine_soup.find("div", class_="price")
        price = "N/A"
        if price_div:
            price_tag = price_div.find("a", class_="gtmItem")
            if price_tag:
                price = price_tag.text.strip()

        # Extract producer name and description
        producer_tag = wine_soup.find("h3", class_="aboutHeading")
        producer = producer_tag.text.strip() if producer_tag else "N/A"

        producer_desc_div = wine_soup.find(
            "div", id=re.compile("producer-read-more-box"))
        producer_desc = producer_desc_div.text.strip() if producer_desc_div else "N/A"

        # Extract region and description
        region_tag = wine_soup.find("a", class_="gtmItemPageRegion")
        region = region_tag.text.strip() if region_tag else "N/A"

        region_desc_div = wine_soup.find(
            "div", id=re.compile("region-read-more-box"))
        region_desc = region_desc_div.text.strip() if region_desc_div else "N/A"

        # Extract ratings & review
        ratings_tag = wine_soup.find("h3", class_="aboutHeading")
        ratings = ratings_tag.text.strip() if ratings_tag else "N/A"

        ratings_desc_p = wine_soup.find("p")
        ratings_desc = ratings_desc_p.text.strip() if ratings_desc_p else "N/A"

        # Extract wine type
        type_tag = wine_soup.find("a", class_="gtmItemPageType")
        wine_type = type_tag.text.strip() if type_tag else "N/A"

        # Step 4: Extract historical price data from embedded script
        script_tags = wine_soup.find_all("script")
        chart_data_script = None

        for script in script_tags:
            if "initAreaChart(\"marketValueChart1\"" in script.text:
                chart_data_script = script.text
                break

        # Step 3: Extract JSON-like structure from script
        if chart_data_script:
            match = re.search(
                r"initAreaChart\(\"marketValueChart1\", (.*?)\);", chart_data_script, re.DOTALL)

            if match:
                json_text = match.group(1)

                # 🔍 Debugging: Print extracted raw text before any modifications
                print("\n🔍 Extracted Raw JSON-like Text (Before Cleaning):\n", json_text)

                # Save raw text to file for further testing
                with open("raw_wine_price_data.txt", "w") as f:
                    f.write(json_text)

                print(
                    "\n✅ Raw JSON-like data saved to 'raw_wine_price_data.txt'. Now test json_utils separately.")


# Step 5: Save Results
df_wines = pd.DataFrame(wine_data, columns=[
    "Wine Name", "Year", "Unique Code", "Wine URL", "Current Price",
    "Producer", "Producer Description", "Region", "Region Description",
    "Ratings", "Ratings Description", "Wine Type"
])
df_wines.to_csv("wine_prices_1900.csv", index=False)

df_history = pd.DataFrame(history)
df_history.to_csv("wine_price_history_1900.csv", index=False)

print("\n✅ Scraping complete! Data saved to wine_prices_1900.csv and wine_price_history_1900.csv")
