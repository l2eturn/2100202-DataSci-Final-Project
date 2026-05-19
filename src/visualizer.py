import matplotlib
matplotlib.use("Agg")  # non-interactive backend — safe for scripts

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.dpi"] = 120


def _save(fig: plt.Figure, name: str, output_dir: Path) -> None:
    path = output_dir / f"{name}.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"  [viz] saved → {path.name}")


def chart_monthly_sales(df: pd.DataFrame, output_dir: Path) -> None:
    """Chart 1 — Line chart: monthly revenue trend."""
    monthly = (
        df.groupby("order_month")["payment_value"]
        .sum()
        .reset_index()
    )
    monthly["order_month"] = monthly["order_month"].astype(str)

    fig, ax = plt.subplots(figsize=(13, 4))
    ax.plot(monthly["order_month"], monthly["payment_value"],
            marker="o", linewidth=2, color="steelblue")
    ax.fill_between(monthly["order_month"], monthly["payment_value"],
                    alpha=0.15, color="steelblue")
    ax.set_title("Monthly Total Revenue — Olist (2016–2018)", fontsize=14, pad=12)
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue (BRL)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1e6:.1f}M"))
    ax.tick_params(axis="x", rotation=45)
    _save(fig, "chart1_monthly_sales", output_dir)


def chart_top_categories(df: pd.DataFrame, output_dir: Path) -> None:
    """Chart 2 — Horizontal bar: top-10 categories by revenue."""
    cat_rev = (
        df.groupby("category")["price"]
        .sum()
        .nlargest(10)
        .sort_values()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(9, 6))
    bars = ax.barh(cat_rev["category"], cat_rev["price"],
                   color=sns.color_palette("muted", 10))
    ax.bar_label(bars, fmt="%.0f", padding=4, fontsize=9)
    ax.set_title("Top-10 Product Categories by Total Revenue", fontsize=14, pad=12)
    ax.set_xlabel("Total Revenue (BRL)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1e6:.1f}M"))
    _save(fig, "chart2_top_categories", output_dir)


def chart_delivery_vs_score(df: pd.DataFrame, output_dir: Path) -> None:
    """Chart 3 — Scatter + regression: delivery days vs review score."""
    sample = (
        df[["delivery_days", "review_score"]]
        .dropna()
        .query("0 <= delivery_days <= 60")
        .sample(min(5_000, len(df)), random_state=42)
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.scatterplot(data=sample, x="delivery_days", y="review_score",
                    alpha=0.25, s=15, color="steelblue", ax=ax)
    sns.regplot(data=sample, x="delivery_days", y="review_score",
                scatter=False, color="crimson", ax=ax,
                line_kws={"linewidth": 2})
    corr = sample["delivery_days"].corr(sample["review_score"])
    ax.set_title(f"Delivery Days vs. Review Score  (r = {corr:.3f})", fontsize=14, pad=12)
    ax.set_xlabel("Actual Delivery Time (days)")
    ax.set_ylabel("Review Score (1–5)")
    _save(fig, "chart3_delivery_vs_score", output_dir)


def chart_price_by_region(df: pd.DataFrame, output_dir: Path) -> None:
    """Chart 4 — Box plot: price distribution by customer region."""
    df_box = df[df["price"].between(0, 500)].dropna(subset=["price", "region"])
    order = (
        df_box.groupby("region")["price"]
        .median()
        .sort_values(ascending=False)
        .index.tolist()
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=df_box, x="region", y="price",
                order=order, palette="Set2", fliersize=2, ax=ax)
    ax.set_title("Product Price Distribution by Customer Region", fontsize=14, pad=12)
    ax.set_xlabel("Region")
    ax.set_ylabel("Price (BRL)")
    _save(fig, "chart4_price_by_region", output_dir)


def chart_correlation_heatmap(df: pd.DataFrame, output_dir: Path) -> None:
    """Chart 5 — Heatmap: correlation matrix of numerical features."""
    cols = ["price", "freight_value", "delivery_days", "delay_days",
            "review_score", "payment_value", "payment_installments"]
    corr_matrix = df[cols].dropna().corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm",
                mask=mask, vmin=-1, vmax=1, linewidths=0.5, ax=ax)
    ax.set_title("Correlation Matrix of Numerical Features", fontsize=14, pad=12)
    _save(fig, "chart5_correlation_heatmap", output_dir)


def chart_review_distribution(df: pd.DataFrame, output_dir: Path) -> None:
    """Chart 6 — Bar chart: review score distribution."""
    counts = df["review_score"].dropna().value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(7, 4))
    colors = ["#d62728", "#ff7f0e", "#bcbd22", "#2ca02c", "#1f77b4"]
    ax.bar(counts.index, counts.values, color=colors, edgecolor="white", width=0.6)
    ax.bar_label(ax.containers[0], fmt="%d", padding=3)
    ax.set_title("Distribution of Review Scores", fontsize=14, pad=12)
    ax.set_xlabel("Review Score")
    ax.set_ylabel("Number of Orders")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    _save(fig, "chart6_review_distribution", output_dir)


def chart_cluster_scatter(rfm: pd.DataFrame, output_dir: Path) -> None:
    """Chart 7 — Scatter: RFM cluster segmentation."""
    rfm_plot = rfm[rfm["monetary"] < rfm["monetary"].quantile(0.99)]
    palette  = {0: "#1f77b4", 1: "#ff7f0e", 2: "#2ca02c", 3: "#d62728"}

    fig, ax = plt.subplots(figsize=(9, 6))
    for c, grp in rfm_plot.groupby("cluster"):
        label = grp["segment"].iloc[0] if "segment" in grp.columns else f"Cluster {c}"
        ax.scatter(grp["frequency"], grp["monetary"],
                   alpha=0.35, s=20, color=palette.get(c, "grey"),
                   label=f"Cluster {c}: {label}")
    ax.set_title("RFM Customer Segmentation (K-Means)", fontsize=14, pad=12)
    ax.set_xlabel("Frequency (# orders)")
    ax.set_ylabel("Monetary (total spend, BRL)")
    ax.legend(title="Segment", markerscale=2)
    _save(fig, "chart7_cluster_scatter", output_dir)


def chart_feature_importance(importances: pd.Series, output_dir: Path) -> None:
    """Chart 8 — Horizontal bar: Random Forest feature importances."""
    top = importances.nlargest(12).sort_values()

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(top.index, top.values,
            color=sns.color_palette("muted", len(top)))
    ax.set_title("Top Feature Importances (Random Forest)", fontsize=14, pad=12)
    ax.set_xlabel("Importance")
    _save(fig, "chart8_feature_importance", output_dir)


def chart_confusion_matrix(cm, output_dir: Path) -> None:
    """Chart 9 — Confusion matrix heatmap."""
    from sklearn.metrics import ConfusionMatrixDisplay
    fig, ax = plt.subplots(figsize=(6, 5))
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=["Not Satisfied", "Satisfied"],
    )
    disp.plot(cmap="Blues", ax=ax, colorbar=False)
    ax.set_title("Random Forest — Confusion Matrix", fontsize=13, pad=10)
    _save(fig, "chart9_confusion_matrix", output_dir)
