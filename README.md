# E-commerce Customer Behavior & Prediction

Data Science final project analyzing the **Olist Brazilian E-commerce** dataset (Sep 2016 – Aug 2018). The pipeline cleans 7 raw tables, integrates them into a master DataFrame, produces 9 visualizations, and trains two machine learning models — K-Means customer segmentation and a Random Forest review-score classifier.

## Research Questions

1. Which customers are high-value, and what are their buying behaviours?
2. What factors (delivery time, freight cost, category) affect review score?
3. Can we predict which orders will receive a low review score?
4. Which product categories generate the most revenue per month?

## Project Structure

```
final-project-datasci/
├── main.py                    # Pipeline entry point
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Containerized run
├── raw-data/                  # 9 Olist CSV source tables
├── src/
│   ├── config.py              # Paths, constants, hyperparameters
│   ├── data_loader.py         # Reads raw CSVs
│   ├── data_cleaner.py        # Datetime parsing, fillna, filtering
│   ├── data_integrator.py     # Merges all tables into one master DataFrame
│   ├── eda.py                 # Groupby+Agg (RFM) and Pivot Table
│   ├── visualizer.py          # 9 charts → outputs/
│   ├── ml_unsupervised.py     # K-Means clustering pipeline
│   └── ml_supervised.py       # Random Forest classifier pipeline
├── outputs/                   # Generated PNG charts
├── ecommerce_analysis.ipynb   # Notebook version of the analysis
├── report.md                  # Written project report
└── index.html                 # Standalone HTML report
```

## Pipeline

| Step | Task |
|---|---|
| 1 | Load 7 raw CSVs |
| 2 | Clean — parse dates, filter to delivered orders, fill missing comments |
| 3 | Integrate — chain merges into one master DataFrame; derive `delivery_days`, `delay_days` |
| 4 | EDA — RFM table (Groupby+Agg) and category × month Pivot Table |
| 5 | Visualize — 9 charts saved to `outputs/` |
| 6 | ML Unsupervised — K-Means (K=4) on RFM features |
| 7 | ML Supervised — Random Forest predicts satisfied (4–5★) vs not satisfied (1–3★) |

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

All charts are written to `outputs/`. Console logs print the progress of each step.

### Docker

```bash
docker build -t ecommerce-analysis .
docker run --rm -v "$(pwd)/outputs:/app/outputs" ecommerce-analysis
```

## Dataset

The [Olist Brazilian E-commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) dataset contains ~100k orders from 2016–2018 across 9 related tables:

- `olist_orders_dataset.csv`
- `olist_customers_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_order_reviews_dataset.csv`
- `olist_order_payments_dataset.csv`
- `olist_products_dataset.csv`
- `olist_sellers_dataset.csv`
- `olist_geolocation_dataset.csv`
- `product_category_name_translation.csv`

## Key Findings

- **Delivery time is the dominant driver of review score** (Pearson r = −0.31). Orders arriving within ~10 days almost always score 4–5★; orders taking 40+ days frequently score 1–2★.
- **~76% of customers are satisfied** (4–5★). Angry customers skip the middle and go straight to 1★.
- **Top revenue categories**: `health_beauty`, `watches_gifts`, `bed_bath_table`.
- **Random Forest classifier** reaches ~76% accuracy; `delay_days` and `delivery_days` together account for ~65% of feature importance.
- **K-Means** segments customers into VIP, Regular, Recent Buyer, and At Risk groups — directly usable for targeted marketing.

See `report.md` for the full write-up.

## Tech Stack

- Python 3.11
- pandas, numpy
- matplotlib, seaborn
- scikit-learn (Pipeline, StandardScaler, KMeans, RandomForestClassifier)
