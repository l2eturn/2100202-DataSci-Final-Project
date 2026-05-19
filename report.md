# Project Report: E-commerce Customer Behavior & Prediction
**Dataset:** Olist Brazilian E-commerce | **Period:** Sep 2016 – Aug 2018

---

## What Was Built

The project is structured as a **7-step modular pipeline** across 8 Python files:

| File | Role |
|---|---|
| `config.py` | Central constants, paths, hyperparameters |
| `data_loader.py` | Reads all 7 raw CSVs |
| `data_cleaner.py` | Cleansing — datetime parsing, filtering, fillna |
| `data_integrator.py` | Merges all tables into one master DataFrame |
| `eda.py` | Groupby+Agg (RFM) and Pivot Table |
| `visualizer.py` | Produces 9 charts saved to `outputs/` |
| `ml_unsupervised.py` | sklearn Pipeline → K-Means clustering |
| `ml_supervised.py` | sklearn Pipeline → Random Forest classifier |
| `main.py` | Orchestrates every step in order |

---

## Step-by-Step: What Happened to the Data

### Step 1–2: Load & Clean
- Loaded **7 tables**: orders, customers, order items, reviews, payments, products, category translations
- Filtered orders to **"delivered" status only** and dropped rows missing actual/estimated delivery dates — this removed incomplete and cancelled orders that would distort the analysis
- Parsed all 5 timestamp columns from string → `datetime`
- Filled ~57,000 missing review comment fields with `"(no comment)"` so they don't become NaN noise downstream
- Translated Portuguese category names to English via a lookup merge

### Step 3: Data Integration
All 7 tables were joined into **one master DataFrame** through a chain of `pd.merge()` calls:

```
orders → customers → order_items → reviews → products → payments
```

Two derived features were engineered:
- `delivery_days` — actual days from purchase to doorstep
- `delay_days` — how many days late (negative = arrived early)

---

## What the Data Showed (Charts)

### Chart 1 — Monthly Revenue Trend (Line)

![Chart 1](outputs/chart1_monthly_sales.png)

Revenue grew **steadily from near zero (Sep 2016) up to 1.55M BRL in Nov 2017** — the spike is almost certainly **Black Friday / holiday season**. After that, revenue stabilized in the **1.2M–1.5M BRL/month** range through 2018, showing a healthy, maturing platform rather than a flash-in-the-pan.

---

### Chart 2 — Top-10 Categories by Revenue (Bar)

![Chart 2](outputs/chart2_top_categories.png)

| Rank | Category | Revenue (BRL) |
|---|---|---|
| 1 | health_beauty | 1,233,132 |
| 2 | watches_gifts | 1,165,899 |
| 3 | bed_bath_table | 1,023,435 |
| 4 | sports_leisure | 954,674 |
| 5 | computers_accessories | 888,614 |

Health & beauty and watches/gifts dominate — these are high-margin, giftable products with strong repeat purchase potential.

---

### Chart 3 — Delivery Days vs. Review Score (Scatter, r = -0.313)

![Chart 3](outputs/chart3_delivery_vs_score.png)

There is a **clear negative correlation**: the longer delivery takes, the lower the review score. Orders arriving within **~10 days** almost exclusively receive 4–5 stars. Orders taking **40+ days** frequently get 1–2 stars. This is the single most actionable insight in the entire project.

---

### Chart 4 — Price by Region (Box Plot)

![Chart 4](outputs/chart4_price_by_region.png)

All 5 regions share a similar median price (~80–100 BRL). The **North and Northeast** have slightly wider boxes and more high-price outliers, suggesting those regions have fewer options and buy higher-priced goods when they do shop. **Southeast** (São Paulo) has the tightest distribution, reflecting a more competitive, price-sensitive market.

---

### Chart 5 — Correlation Heatmap

![Chart 5](outputs/chart5_correlation_heatmap.png)

Key relationships found:

| Pair | Correlation | Meaning |
|---|---|---|
| `price` ↔ `payment_value` | **0.76** | Strong — what you buy ≈ what you pay |
| `delivery_days` ↔ `delay_days` | **0.59** | Longer deliveries tend to also be late |
| `delivery_days` ↔ `review_score` | **-0.30** | Slower delivery → lower satisfaction |
| `delay_days` ↔ `review_score` | **-0.23** | Lateness hurts, but less than raw delivery time |
| `price` ↔ `review_score` | **~0.00** | Price has no effect on how customers rate |

---

### Chart 6 — Review Score Distribution

![Chart 6](outputs/chart6_review_distribution.png)

| Score | Count |
|---|---|
| 5 ★ | 62,960 |
| 4 ★ | 21,076 |
| 3 ★ | 9,183 |
| 2 ★ | 3,669 |
| 1 ★ | 12,474 |

**~76% of customers are satisfied (4–5 stars).** The 1-star group (12,474) is notably larger than 2-star and 3-star combined — customers who are angry tend to give the lowest possible score, skipping the middle.

---

## Machine Learning Results

### Model 1 — K-Means Clustering (Unsupervised, K=4)

**What it did:** Took the RFM table (Recency, Frequency, Monetary per unique customer) and grouped all customers into 4 segments using a `StandardScaler → KMeans` pipeline.

![Chart 7](outputs/chart7_cluster_scatter.png)

**Segments found:**

| Segment | Behaviour |
|---|---|
| **At Risk** | Bought once, a long time ago — low frequency, high recency. The biggest group. |
| **Regular** | Active buyers, 2–7 orders, moderate spend — the backbone of the business |
| **Recent Buyer** | Purchased recently but only once — need nurturing to become regulars |
| **VIP** | High spend, repeat buyers — small but highest value |

**Real-world application:** A marketing team can use these segments directly:
- Send **re-engagement discounts** to the At Risk group
- Offer **loyalty rewards / early access** to VIPs
- Send **"second purchase" incentive** emails to Recent Buyers within 30 days of their first order

---

### Model 2 — Random Forest Classifier (Supervised)

**What it did:** Used a `SimpleImputer → StandardScaler → RandomForestClassifier` pipeline to predict whether an order would receive a **satisfied review (4–5 ★)** or **not satisfied (1–3 ★)**.

#### Feature Importances

![Chart 8](outputs/chart8_feature_importance.png)

| Feature | Importance |
|---|---|
| `delay_days` | **0.38** — most important by far |
| `delivery_days` | **0.27** — second most |
| `payment_value` | 0.11 |
| `price` | 0.10 |
| `freight_value` | 0.06 |
| product category | < 0.02 each |

#### Confusion Matrix

![Chart 9](outputs/chart9_confusion_matrix.png)

| | Predicted Not Satisfied | Predicted Satisfied |
|---|---|---|
| **Actually Not Satisfied** | 2,552 ✓ | 2,678 ✗ |
| **Actually Satisfied** | 2,575 ✗ | 14,233 ✓ |

- **Overall accuracy: ~76%**
- The model is **very good at identifying satisfied customers** (14,233 correct out of 16,808)
- It is **weaker at catching unhappy customers** — it misses about half of them (2,678 false positives)
- This is a class imbalance effect: 76% of training data was "satisfied" so the model leans toward predicting that label

**Real-world application:** Despite the imbalance, this model is still useful:
- Run it **at the moment an order is shipped** — if `delay_days` is already positive and `delivery_days` looks long, flag the order for a **proactive support message** or a compensation voucher
- Even catching 50% of unhappy customers early is far better than catching none
- The model can be improved later with SMOTE (minority class oversampling) or by lowering the classification threshold

---

## Summary

| Research Question | Answer |
|---|---|
| **Q1:** Who are the high-value customers? | Segmented into 4 groups via K-Means; VIPs are rare but high spend, At Risk is the largest group |
| **Q2:** What affects review score? | Delivery time and delay are the dominant factors — price and category barely matter |
| **Q3:** Can we predict bad reviews? | Yes at ~76% accuracy; model flags risky orders using delay & delivery days |
| **Q4:** Which categories make the most money? | health_beauty, watches_gifts, bed_bath_table — all stable high earners |
