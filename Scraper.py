import requests
from bs4 import BeautifulSoup
import polars as pl

url = "https://www.coffeereview.com/review/"
response = requests.get(url)

html = response.text


soup = BeautifulSoup(html, "html.parser")

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

url = get_review(soup, "h2.review-title a")
response = requests.get(url)

html = response.text


soup = BeautifulSoup(html, "html.parser")

coffee_data = get_data(soup)
print(coffee_data)
df = pl.DataFrame(coffee_data)
df = df.with_columns([pl.col('score').cast(pl.Int8), 
                      pl.col('aroma').cast(pl.Int8),
                      pl.col('structure').cast(pl.Int8),
                      pl.col('body').cast(pl.Int8),
                      pl.col('flavour').cast(pl.Int8),
                      pl.col('aftertaste').cast(pl.Int8)])
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