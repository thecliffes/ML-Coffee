import requests
from bs4 import BeautifulSoup
import polars as pl
import time

url = "https://www.coffeereview.com/review/"
response = requests.get(url)

html = response.text


soup_mainpage = BeautifulSoup(html, "html.parser")

def get_review(soup, selector):
    element = soup.select_one(selector)
    return element['href'] if element else None

def get_text(soup, selector):
    element = soup.select_one(selector)
    return element.get_text(strip=True) if element else None


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

    labels["Score"] = get_text(
        soup,
        "#genesis-content article div.row.row-1 div.column.col-1 span"
    )

    labels["Name"] = get_text(soup, "h1")

    col1 = table_to_dict(
        soup.select_one("div.column.col-1 table.review-template-table")
    )

    col2 = table_to_dict(
        soup.select_one("div.column.col-2 table.review-template-table")
    )

    coffee_data = {
        "name": labels.get("Name"),
        "score": labels.get("Score"),
        "roast_level": col1.get("Roast Level"),
        "aroma": col2.get("Aroma"),
        "structure": col2.get("Acidity/Structure"),
        "body": col2.get("Body"),
        "flavour": col2.get("Flavor"),
        "aftertaste": col2.get("Aftertaste"),
    }
    return coffee_data


url = get_review(soup_mainpage, f"#genesis-content > div:nth-child(5) > div > div.row.row-1 > div.column.col-2 > h2 > a")
response = requests.get(url) 

html = response.text
soup_first_review = BeautifulSoup(html, "html.parser")

coffee_data = get_data(soup_first_review)

df = pl.DataFrame(coffee_data)
df = df.with_columns([pl.col('score').cast(pl.Int8), 
                      pl.col('aroma').cast(pl.Int8),
                      pl.col('structure').cast(pl.Int8),
                      pl.col('body').cast(pl.Int8),
                      pl.col('flavour').cast(pl.Int8),
                      pl.col('aftertaste').cast(pl.Int8)])

print(df)

for i in range(6, 25):
    # ✅ Always search for links in the MAIN PAGE soup
    url = get_review(soup_mainpage, f"#genesis-content > div:nth-child({i}) > div > div.row.row-1 > div.column.col-2 > h2 > a")
    
    if url is not None:
        response = requests.get(url)
        
        # ✅ Parse the individual review page into its own soup
        soup_review = BeautifulSoup(response.text, "html.parser")
        
        # ✅ Extract data from the review soup, not the listing soup
        coffee_data = get_data(soup_review)

        new_row = pl.DataFrame(coffee_data)
        new_row = new_row.with_columns([pl.col('score').cast(pl.Int8), 
                      pl.col('aroma').cast(pl.Int8),
                      pl.col('structure').cast(pl.Int8),
                      pl.col('body').cast(pl.Int8),
                      pl.col('flavour').cast(pl.Int8),
                      pl.col('aftertaste').cast(pl.Int8)])
        
        df = pl.concat([df, new_row])
        print(i)
        time.sleep(2)
    else:
        print(f"Could not find link for {i}, skipping...")

print(df)
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