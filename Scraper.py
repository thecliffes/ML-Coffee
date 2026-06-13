import requests
from bs4 import BeautifulSoup
import polars as pl
import time

# pretend to be a real browser so the site doesn't block us
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.5",
    "Referer": "https://www.google.com/",
})

# pulls the href from a review card on the listing page
def get_review(soup, selector):
    element = soup.select_one(selector)
    return element['href'] if element else None

def get_text(soup, selector):
    element = soup.select_one(selector)
    return element.get_text(strip=True) if element else None

# the scoring breakdown lives in two side-by-side tables, this flattens one into a dict
def table_to_dict(table):
    data = {}
    if not table:
        return data
    for row in table.select("tr"):
        cells = row.select("td")
        if len(cells) >= 2:
            key = cells[0].get_text(strip=True).replace(":", "")
            value = cells[1].get_text(strip=True)
            data[key] = value
    return data

def get_data(soup):
    labels = {}
    labels["Score"] = get_text(soup, "#genesis-content article div.row.row-1 div.column.col-1 span")
    labels["Name"] = get_text(soup, "h1")
    # col1 = roast info, col2 = tasting scores
    col1 = table_to_dict(soup.select_one("div.column.col-1 table.review-template-table"))
    col2 = table_to_dict(soup.select_one("div.column.col-2 table.review-template-table"))
    return {
        "name": labels.get("Name"),
        "score": labels.get("Score"),
        "roast_level": col1.get("Roast Level"),
        "aroma": col2.get("Aroma"),
        "structure": col2.get("Acidity/Structure"),  # not all reviews have this field
        "body": col2.get("Body"),
        "flavour": col2.get("Flavor"),
        "aftertaste": col2.get("Aftertaste"),
    }

all_rows = []
url = "https://www.coffeereview.com/review/"

# page 1 url is different from the rest so we start j at 2 and handle page 1 separately
for j in range(2, 452):
    print(f"Scraping page {j}: {url}")

    try:
        response = session.get(url, timeout=10)
        soup_mainpage = BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch page {j}: {e}")
        time.sleep(5)
        continue

    # review cards start at child index 5, usually up to ~20 per page
    for i in range(5, 25):
        review_url = get_review(soup_mainpage, f"#genesis-content > div:nth-child({i}) > div > div.row.row-1 > div.column.col-2 > h2 > a")

        if review_url is None:
            print(f"  No link at index {i}, skipping...")
            continue

        try:
            soup_review = BeautifulSoup(session.get(review_url, timeout=10).text, "html.parser")
            all_rows.append(get_data(soup_review))
        except requests.exceptions.RequestException as e:
            print(f"  Failed to fetch review {review_url}: {e}")

        time.sleep(2)  # be polite, don't hammer the server

    # save after every page so we don't lose everything if it crashes halfway through
    if all_rows:
        pl.DataFrame(all_rows).with_columns([
            pl.col(['score', 'aroma', 'structure', 'body', 'flavour', 'aftertaste']).cast(pl.Int8, strict=False)
        ]).write_csv("coffee_data.csv")
        print(f"  Saved {len(all_rows)} reviews to coffee_data.csv")

    url = f"https://www.coffeereview.com/review/page/{j}/"

# final save with everything
df = pl.DataFrame(all_rows).with_columns([
    pl.col(['score', 'aroma', 'structure', 'body', 'flavour', 'aftertaste']).cast(pl.Int8, strict=False)
])

print(df)
df.write_csv("coffee_data.csv")

###   Inputs:
#   Strength
#   Roast Level
#   Flavour Notes
#   Time of day
#   Mood
###

###     Outputs:
#   Recommended coffee bean or drink
#   Predicated satisfaction score
#   Similar coffee to try next
###