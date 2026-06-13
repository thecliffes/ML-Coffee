# ML Coffee

A scraper + KNN model for coffee review data from coffeereview.com.

## What it does

Scrapes ~9,000 reviews and trains a KNN classifier to predict which coffee bean matches a given set of tasting attributes (roast level, aroma, structure, body, flavour, aftertaste).

## Files

- `Scraper.py` - pulls review data from coffeereview.com and saves to CSV
- `model.ipynb` - cleans the data, trains a KNN model, and lets you query it
- `coffee_data.csv` - the scraped data (~9k rows)

## How to run

**Scraper** (only needed if you want fresh data):
```bash
pip install requests beautifulsoup4 polars
python Scraper.py
```
Takes a while - there are 450 pages with a 2s delay between requests.

**Model**:
```bash
pip install pandas numpy scikit-learn
jupyter notebook model.ipynb
```
Run all cells top to bottom. The `predict_coffee()` function at the bottom is the main thing - pass in tasting attributes and it returns a ranked list of the most likely beans.

## Example

```python
predict_coffee('Light', aroma=9, structure=9, body=9, flavour=10, aftertaste=9)
```

```
Top 5 predicted coffees:
  1. Ethiopia Sidama Bensa Alo Tamiru Tadese Washed  (25.0%)
  2. Banko Gotiti  (25.0%)
  3. Colombia Finca Mikava Gesha Hybrid Washed Process  (12.5%)
  ...
```

## Notes

- `structure` (acidity) is missing for a lot of reviews - espresso-only reviews don't include it. The model imputes with the median so you can leave it as `None` if you don't have it.
- Exact-match accuracy is pretty low given how many beans score identically, but top-5 accuracy is more useful and noticeably higher.
- Scores are on a 1-10 scale per category, overall score is out of 100.
