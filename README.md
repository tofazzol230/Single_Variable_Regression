# X → Y Regression (Simple Linear)

Browser-based **simple linear regression** calculator for X vs Y, with **prediction + confidence interval**.

## Features

- Paste/enter X and Y values (comma/space/newline separated)
- Predict at a chosen `x0` with 90/95/99% confidence level
- Shows:
  - Totals & cross-products: Σx, Σy, Σx², Σy², Σxy
  - Sxx, Syy, Sxy
  - Fitted model: **ŷ = B0 + B1x**
  - SSE, error variance, SE(B0), SE(B1)
  - t-test for slope + R²
  - Confidence interval for prediction at `x0`
- **Graph**: scatter plot + fitted line + prediction marker
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


## Run locally

This is a static app.

### Option A: Open directly
Open `index.html` in your browser.

### Option B: Use a local server (recommended)
From the project folder:

```bash
python3 -m http.server 5173
# then open http://localhost:5173
```

## Build

Build copies static files into `dist/`:

```bash
npm run build
```

Output: `dist/index.html`, `dist/app.js`, `dist/style.css`


## Tech

- Vanilla HTML/CSS/JS (ES Modules)
- Static build: `build.mjs` (copies files to `dist/`)
