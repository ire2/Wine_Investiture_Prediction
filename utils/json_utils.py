import re


def extract_price_history(raw_text):
    """
    Extracts historical price data from the malformed JavaScript-like data in WineBid pages.

    :param raw_text: Extracted JavaScript-based text from WineBid
    :return: List of tuples containing parsed historical price data
    """
    if not raw_text:
        print("Error: No data provided.")
        return []

    try:
        match_rows = re.search(
            r'"rows"\s*:\s*\[(.*?)\]\s*,', raw_text, re.DOTALL)
        if not match_rows:
            print("Error: Could not locate 'rows' section in data.")
            return []

        rows_text = match_rows.group(1)
        # print("Rows Text: ", rows_text)
        row_pattern = re.compile(
            r'Date\((\d{4}), (\d{1,2}), (\d{1,2})\).*?(\d+), "f": "\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)"')
        matches = row_pattern.findall(rows_text)

        history = []
        for match in matches:
            year, month, day, price_value, formatted_price = match
            date_tuple = (int(year), int(month), int(day))
            history.append(
                [date_tuple, int(price_value), f"${formatted_price}"])

        return history

    except Exception as e:
        # error log
        print(f"Error extracting historical price data: {e}")
        return []


raw_text = '{"cols": [{"type": "date" ,"id": "Date" ,"label": "Date" }, {"type": "number" ,"id": "Price" ,"label": "Price" }], "rows" : [{"c" : [{"v": "Date(2006, 2, 19)"}, {"v": 386, "f": "$386"}]}, {"c" : [{"v": "Date(2012, 11, 23)"}, {"v": 455, "f": "$455"}]}, {"c" : [{"v": "Date(2018, 4, 31)"}, {"v": 702, "f": "$702"}]}, {"c" : [{"v": "Date(2018, 5, 10)"}, {"v": 936, "f": "$936"}]}, {"c" : [{"v": "Date(2022, 0, 6)"}, {"v": 1053, "f": "$1,053"}]}, {"c" : [{"v": "Date(2024, 0, 29)"}, {"v": 1053, "f": "$1,053"}]}, {"c" : [{"v": "Date(2025, 1, 22)"}, {"v": 1053, "f": "$1,053"}]}, {"c" : [{"v": "Date(2025, 2, 6)"}, {"v": 1053, "f": "$1,053"}]}]}, {"hAxis":{"format":"MMM d\ny","baselineColor":"#888783","gridlines":{"color":"transparent"},"textPosition":"out"},"vAxis":{"minValue":0,"baselineColor":"#888783","gridlines":{"color":"#e8e6df"},"ticks":[{"v":0,"f":"$0"},{"v":350,"f":""},{"v":700,"f":"$700"},{"v":1050,"f":""},{"v":1400,"f":"$1.4K"}],"textPosition":"out"},"series":[{"color":"#ff7828","lineWidth":4}],"fontName":"ClarendonTextPro","legend":{"alignment":null,"position":"none"},"chartArea":{"left":"15%","top":"10%","width":"70%","height":"75%"},"areaOpacity":0,"tooltip":{"trigger":"focus"}}'

history = extract_price_history(raw_text)


print("\nExtracted Historical Price Data:\n", history)

# TODO - Should i save csv here or in preprocess_tabular.py?
