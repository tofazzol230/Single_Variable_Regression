# Finger → Skull Regression (Simple Linear)

Browser-based **simple linear regression** calculator for Finger (X) vs Skull (Y), with **prediction + confidence interval** and a built-in **OCR importer** (Tesseract.js) to extract values from a screenshot/table.

## Features

- Paste/enter `finger` (X) and `skull` (Y) values (comma/space/newline separated)
- Predict at a chosen `x0` with 90/95/99% confidence level
- Shows:
  - Totals & cross-products: Σx, Σy, Σx², Σy², Σxy
  - Sxx, Syy, Sxy
  - Fitted model: **ŷ = B0 + B1x**
  - SSE, error variance, SE(B0), SE(B1)
  - t-test for slope + R²
  - Confidence interval for prediction at `x0`
- **Graph**: scatter plot + fitted line + prediction marker
- **OCR upload**: upload a screenshot of a table and auto-fill values (expects rows like `id finger skull`)
- Everything runs in the browser (no backend).

## Input tips

### 1) Normal lists
You can paste values separated by commas/spaces/newlines.

### 2) Paste a Python snippet
You can paste something like this in either box and the app will parse it:

```py
finger_values = [8.1, 7.9, 8.2]
skull_values  = [53.5, 57.7, 56.8]
```

### 3) OCR table format
From OCR text it tries to parse triples:

```
1 8.1 53.5
2 7.9 57.7
...
```

## Tech

- Vanilla HTML/CSS/JS (ES Modules)
- OCR: `tesseract.js` via CDN
- Static build: `build.mjs` (copies files to `dist/`)

