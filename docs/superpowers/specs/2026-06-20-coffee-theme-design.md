# Coffee Theme Design — Streamlit App

**Date:** 2026-06-20
**File:** `Scripts/main.py`

## Goal

Apply a Warm & Cozy coffee aesthetic to the Streamlit recommender app without changing any model or recommendation logic.

## Aesthetic Direction

Warm & Cozy: cream and brown tones, soft and approachable, neighbourhood café feel.

| Role | Colour |
|------|--------|
| Page background | `#F5EFE0` (cream) |
| Secondary background | `#EFE4CC` (darker cream, expanders/sidebar) |
| Primary / accent | `#7B4A2A` (warm brown) |
| Text | `#3D1F0D` (dark espresso brown) |
| Card border | `#C9A97A` (tan) |

## Approach

Hybrid: `config.toml` for global palette + targeted CSS injection for result cards.

- `config.toml` handles all Streamlit-managed colours (backgrounds, text, widget highlights) using stable, version-safe theme variables.
- CSS injection (`st.markdown` with `unsafe_allow_html=True`) is scoped only to the result cards, which `config.toml` cannot reach.

## Files Changed

### `.streamlit/config.toml` (new)

```toml
[theme]
base                     = "light"
primaryColor             = "#7B4A2A"
backgroundColor          = "#F5EFE0"
secondaryBackgroundColor = "#EFE4CC"
textColor                = "#3D1F0D"
```

### `Scripts/main.py`

1. Add `st.set_page_config(page_title="Coffee Recommender", page_icon="☕")` at the top.
2. Inject a `<style>` block defining `.coffee-card` and `.coffee-card .score`.
3. Replace `st.write` result rows with `st.markdown` HTML using `.coffee-card`.

## Out of Scope

- No changes to model loading, recommendation logic, or data pipeline.
- No layout restructuring (sidebar, columns, etc.).
- No font changes (system font stack is fine for now).
