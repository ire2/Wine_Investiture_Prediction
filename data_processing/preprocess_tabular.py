import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import json

# Base URL
BASE_URL = "https://www.winebid.com"

# Headers
HEADERS = {"User-Agent": "Mozilla/5.0"}


vintage_page_url = f"{BASE_URL}/BuyWine/Vintages/-"
response = requests.get(vintage_page_url, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")


wine_data = []
wine_links = soup.find_all("a", class_="gtmProducerItem")

for wine_link in wine_links:
    wine_href = wine_link["href"]
    wine_name = wine_link.text.strip()

    match = re.search(r"/BuyWine/Item/Auction/(\d+)/(\d+)", wine_href)
    if match:
        unique_code, year = match.groups()

        # test 1900 b4 deployment
        # TODO - Remove this line before deployment
        if year != "1900":
            continue

        wine_url = f"{BASE_URL}{wine_href}"

        wine_page_response = requests.get(wine_url, headers=HEADERS)
        wine_soup = BeautifulSoup(wine_page_response.text, "html.parser")

        price_div = wine_soup.find("div", class_="price")
        price = "N/A"
        if price_div:
            price_tag = price_div.find("a", class_="gtmItem")
            if price_tag:
                price = price_tag.text.strip()

        producer_tag = wine_soup.find("h3", class_="aboutHeading")
        producer = producer_tag.text.strip() if producer_tag else "N/A"

        producer_desc_div = wine_soup.find(
            "div", id=re.compile("producer-read-more-box"))
        producer_desc = producer_desc_div.text.strip() if producer_desc_div else "N/A"

        region_tag = wine_soup.find("a", class_="gtmItemPageRegion")
        region = region_tag.text.strip() if region_tag else "N/A"

        region_desc_div = wine_soup.find(
            "div", id=re.compile("region-read-more-box"))
        region_desc = region_desc_div.text.strip() if region_desc_div else "N/A"

        ratings_tag = wine_soup.find("h3", class_="aboutHeading")
        ratings = ratings_tag.text.strip() if ratings_tag else "N/A"

        ratings_desc_p = wine_soup.find("p")
        ratings_desc = ratings_desc_p.text.strip() if ratings_desc_p else "N/A"

        type_tag = wine_soup.find("a", class_="gtmItemPageType")
        wine_type = type_tag.text.strip() if type_tag else "N/A"
        script_tags = wine_soup.find_all("script")
        chart_data_script = None

        for script in script_tags:
            if "initAreaChart(\"marketValueChart1\"" in script.text:
                chart_data_script = script.text
                break
        if chart_data_script:
            match = re.search(
                r"initAreaChart\(\"marketValueChart1\", (.*?)\);", chart_data_script, re.DOTALL)

            if match:
                json_text = match.group(1)

                print("\nExtracted Raw JSON-like Text (Before Cleaning):\n", json_text)
                # TODO - Call JSON utility function to clean and extract historical price data
                with open("raw_wine_price_data.txt", "w") as f:
                    f.write(json_text)

                print(
                    "\n Raw JSON-like data saved to 'raw_wine_price_data.txt'. Now test json_utils separately.")

df_wines = pd.DataFrame(wine_data, columns=[
    "Wine Name", "Year", "Unique Code", "Wine URL", "Current Price",
    "Producer", "Producer Description", "Region", "Region Description",
    "Ratings", "Ratings Description", "Wine Type"
])
df_wines.to_csv("wine_prices_1900.csv", index=False)

print("\n Scraping complete! Data saved to wine_prices_1900.csv and wine_price_history_1900.csv")
