import requests
from bs4 import BeautifulSoup
import polars as pl

url = "https://www.coffeereview.com/review/costa-rica-mirazu-catajo-geisha-blend/"
response = requests.get(url)

html = response.text



soup = BeautifulSoup(html, "html.parser")
labels={}
score = soup.select_one('#genesis-content > article > div > div > div.row.row-1 > div.column.col-1 > span')
labels['Score'] = score.get_text(strip=True)


title = soup.select_one('h1')
labels['Name'] = title.get_text(strip=True)


table_1 = soup.select_one("div.column.col-1 table.review-template-table")


col1 = {}

for row in table_1.select("tr"):
    cells = row.select("td")
    key = cells[0].get_text(strip=True).replace(":", "")
    value = cells[1].get_text(strip=True)
    col1[key] = value


table_2 = soup.select_one("div.column.col-2 table.review-template-table")

col2 = {}

for row in table_2.select("tr"):
    cells = row.select("td")
    key = cells[0].get_text(strip=True).replace(":", "")
    value = cells[1].get_text(strip=True)
    col2[key] = value


roast_level = col1['Roast Level']
name = labels['Name']
score = labels['Score']
aroma = col2['Aroma']
structure = col2['Acidity/Structure']
body = col2['Body']
flavour = col2['Flavor']
aftertaste = col2['Aftertaste']

df = pl.DataFrame(data = {"Name": name, 'Roast Level': roast_level, 'Score': score, 'Aroma': aroma, 'Structure': structure, 'Body': body, 'Flavour': flavour, 'Aftertaste': aftertaste})
df = df.with_columns([pl.col('Score').cast(pl.Int8), 
                      pl.col('Aroma').cast(pl.Int8),
                      pl.col('Structure').cast(pl.Int8),
                      pl.col('Body').cast(pl.Int8),
                      pl.col('Flavour').cast(pl.Int8),
                      pl.col('Aftertaste').cast(pl.Int8)])
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