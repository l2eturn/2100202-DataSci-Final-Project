"""
E-commerce Customer Behavior & Prediction
==========================================
Data Science Final Project — Olist Brazilian E-commerce Dataset

Research Questions
------------------
Q1: Which customers are high-value and what are their buying behaviours?
Q2: What factors (delivery time, freight cost, category) affect review score?
Q3: Can we predict which orders will receive a low review score?
Q4: Which product categories generate the most revenue per month?

Pipeline Steps
--------------
1. Load     — read all raw CSVs
2. Clean    — handle missing values, parse dates, filter statuses
3. Integrate— merge tables, add derived features
4. EDA      — Groupby+Agg (RFM) and Pivot Table (category × month)
5. Visualize— 9 charts saved to outputs/
6. ML-Unsup — K-Means customer segmentation (sklearn Pipeline)
7. ML-Sup   — Random Forest satisfaction predictor (sklearn Pipeline)
"""

import sys
from pathlib import Path

# Allow `src.*` imports when run as `python main.py` from the project root
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src import config
from src.data_loader     import load_raw_data
from src.data_cleaner    import clean
from src.data_integrator import integrate
from src.eda             import build_rfm, build_pivot_table
from src import visualizer as viz
from src import ml_unsupervised, ml_supervised


def run_pipeline() -> None:
    print("=" * 60)
    print("STEP 1 — Load raw data")
    print("=" * 60)
    dfs = load_raw_data()

    print("\n" + "=" * 60)
    print("STEP 2 — Data Cleansing")
    print("=" * 60)
    dfs = clean(dfs)

    print("\n" + "=" * 60)
    print("STEP 3 — Data Integration (Merge / Join)")
    print("=" * 60)
    master = integrate(dfs)

    print("\n" + "=" * 60)
    print("STEP 4 — EDA (Groupby + Agg  |  Pivot Table)")
    print("=" * 60)
    rfm         = build_rfm(master)
    pivot_table = build_pivot_table(master)

    print("\n" + "=" * 60)
    print("STEP 5 — Data Visualization (9 charts → outputs/)")
    print("=" * 60)
    viz.chart_monthly_sales(master,          config.OUTPUT_DIR)
    viz.chart_top_categories(master,         config.OUTPUT_DIR)
    viz.chart_delivery_vs_score(master,      config.OUTPUT_DIR)
    viz.chart_price_by_region(master,        config.OUTPUT_DIR)
    viz.chart_correlation_heatmap(master,    config.OUTPUT_DIR)
    viz.chart_review_distribution(master,    config.OUTPUT_DIR)

    print("\n" + "=" * 60)
    print("STEP 6 — ML Unsupervised: K-Means Customer Segmentation (Q1)")
    print("=" * 60)
    rfm_clustered = ml_unsupervised.run(rfm)
    viz.chart_cluster_scatter(rfm_clustered, config.OUTPUT_DIR)

    print("\n" + "=" * 60)
    print("STEP 7 — ML Supervised: Random Forest Classifier (Q2, Q3)")
    print("=" * 60)
    pipeline, importances, metrics = ml_supervised.run(master)
    viz.chart_feature_importance(importances,              config.OUTPUT_DIR)
    viz.chart_confusion_matrix(metrics["confusion_matrix"], config.OUTPUT_DIR)

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print(f"All charts saved to: {config.OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline()
