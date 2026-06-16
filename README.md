# ML Coffee

A scraper + ML models for coffee review data from coffeereview.com.

## What it does

Scrapes ~9,000 reviews and builds two content-based recommenders that return the most similar coffees to a given set of tasting attributes. Both models use weighted cosine similarity over feature vectors — they are recommenders, not classifiers.

## Files

- `Scraper.py` — pulls review data from coffeereview.com and saves to CSV
- `knn_model.ipynb` — cosine recommender using `NearestNeighbors`
- `cosine_model.ipynb` — cosine recommender using `cosine_similarity` directly
- `coffee_data.csv` — the scraped data (~9k rows)

## How to run

**Scraper** (only needed if you want fresh data):
```bash
pip install requests beautifulsoup4 polars
python Scraper.py
```
Takes a while — there are 450 pages with a 2s delay between requests.

**Models**:
```bash
pip install pandas numpy scikit-learn
jupyter notebook knn_model.ipynb
# or
jupyter notebook cosine_model.ipynb
```
Run all cells top to bottom.

## Models (V5)

Both notebooks implement the same weighted cosine retrieval approach. The difference is implementation: `cosine_model.ipynb` uses `cosine_similarity` directly; `knn_model.ipynb` uses sklearn's `NearestNeighbors(metric='cosine')`.

### Usage

```python
recommend_coffee(
    'Light', aroma=9, structure=9, body=9, flavour=10, aftertaste=9,
    process_method='Natural', variety='Geisha'
)
```

```
Top 5 recommended coffees:
  1. Panama Elida Natural Geisha             0.94
  2. Ninety Plus Gesha Estates               0.91
  3. ...
```

All parameters except `roast_level` and the tasting scores are optional — pass `None` or omit them and they default to `'Unknown'`.

## Feature weights

| Feature | Weight | Source |
|:---|:---:|:---|
| flavour | 2.0 | Tasting score |
| aftertaste | 2.0 | Tasting score |
| aroma | 1.5 | Tasting score |
| process_method | 1.5 | Extracted from coffee name |
| variety | 1.5 | Extracted from coffee name |
| structure | 1.2 | Tasting score |
| body | 1.0 | Tasting score |
| score | 1.0 | Overall review score |
| coffee_country | 1.0 | Extracted from coffee_origin |
| agtron_whole | 0.8 | Roast measurement |
| roast_level | 0.8 | Roast category |
| coffee_region | 0.8 | Extracted from coffee_origin |

Weights are applied after preprocessing (scaling/encoding) by multiplying each feature dimension. This biases cosine similarity toward flavour, aftertaste, aroma, process and variety — the dimensions that most define coffee character.

## Feature encoding

| Feature | Encoding |
|:---|:---|
| `roast_level` | OrdinalEncoder (Light=0 → Dark=4), unknown → -1, then StandardScaler |
| Numeric tasting scores | SimpleImputer (median) + StandardScaler |
| `coffee_country`, `coffee_region`, `process_method`, `variety` | OneHotEncoder (min_frequency=10), unknown → ignored |

`process_method` and `variety` are keyword-extracted from the coffee name. `coffee_country` and `coffee_region` are extracted from the `coffee_origin` field. Missing values are filled with `'Unknown'` rather than most-frequent imputation, which would make unrelated coffees look artificially similar.

## Evaluation

Exact-match accuracy is not meaningful here — many coffees share identical tasting profiles. V5 uses recommender metrics evaluated on a held-out 20% split:

| Metric | Description |
|:---|:---|
| Top-5 hit rate | True coffee appears in top 5 results |
| Top-10 hit rate | True coffee appears in top 10 results |
| MRR | Mean Reciprocal Rank |
| NDCG@10 | Normalised Discounted Cumulative Gain at 10 |

## Notes

- `structure` (acidity) is missing for many espresso-only reviews — imputed with median so you can pass `None`.
- Scores are on a 1–10 scale per category; overall `score` is out of 100.
- `roaster` and `roaster_location` were dropped in V5 — high-cardinality categoricals with thousands of unique values created sparse noise that degraded similarity in earlier versions.
