# ML Coffee

A scraper + ML models for coffee review data from coffeereview.com.

## What it does

Scrapes ~9,000 reviews and trains two models to predict which coffee bean matches a given set of tasting attributes (roast level, aroma, structure, body, flavour, aftertaste).

## Files

- `Scraper.py` - pulls review data from coffeereview.com and saves to CSV
- `knn_model.ipynb` - KNN classifier using Euclidean distance
- `cosine_model.ipynb` - cosine similarity recommender
- `coffee_data.csv` - the scraped data (~9k rows)

## How to run

**Scraper** (only needed if you want fresh data):
```bash
pip install requests beautifulsoup4 polars
python Scraper.py
```
Takes a while - there are 450 pages with a 2s delay between requests.

**Models**:
```bash
pip install pandas numpy scikit-learn
jupyter notebook knn_model.ipynb
# or
jupyter notebook cosine_model.ipynb
```
Run all cells top to bottom.

## Models

### KNN (`knn_model.ipynb`)

Uses K-Nearest Neighbours with Euclidean distance. K is chosen automatically by sweeping k=1–15 with 5-fold cross-validation and picking the best. Call `predict_coffee()` with tasting attributes to get a ranked shortlist.

```python
predict_coffee('Light', aroma=9, structure=9, body=9, flavour=10, aftertaste=9)
```

### Cosine Similarity (`cosine_model.ipynb`)

Computes cosine similarity between the query and every training example, then ranks coffees by their mean similarity score. Call `recommend_coffee()` with the same attributes.

```python
recommend_coffee('Light', aroma=9, structure=9, body=9, flavour=10, aftertaste=9)
```

## Feature encoding

| Feature | Encoding |
|---|---|
| `roast_level` | OrdinalEncoder (Light=0 → Dark=4) then StandardScaler |
| `aroma`, `body`, `flavour`, `aftertaste` | SimpleImputer (median) then StandardScaler |
| `structure` | Same as above — missing values imputed so you can pass `None` |

Ordinal encoding preserves the natural ordering of roast levels, which matters for distance-based models. StandardScaler ensures no single feature dominates due to scale differences.

## Results

Both models surface the right beans in the top-5 shortlist but exact-match accuracy is low (~0.3%). This is expected — many distinct coffees share identical integer scores, making them indistinguishable from tasting attributes alone. Top-N accuracy is the more meaningful metric for a recommender use case.

The cosine model can return similarity scores of 1.0 for multiple coffees simultaneously, which means the query profile matches those beans exactly but the model cannot rank between them.

Adding more discriminative features (origin, process method, cultivar) would improve separation between similarly-scored beans.

## Notes

- `structure` (acidity) is missing for a lot of reviews — espresso-only reviews don't include it. Both models impute with the median so you can pass `None` if you don't have it.
- Scores are on a 1–10 scale per category; overall score is out of 100.
