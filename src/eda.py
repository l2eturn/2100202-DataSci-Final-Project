import pandas as pd


def build_rfm(df: pd.DataFrame) -> pd.DataFrame:
    """Groupby + Agg — compute Recency, Frequency, Monetary per unique customer."""
    snapshot = df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)

    rfm = (
        df.groupby("customer_unique_id")
        .agg(
            recency   = ("order_purchase_timestamp", lambda x: (snapshot - x.max()).days),
            frequency = ("order_id",                 "nunique"),
            monetary  = ("payment_value",            "sum"),
        )
        .reset_index()
        .dropna()
    )

    print(f"  [eda] RFM table: {rfm.shape}")
    print(rfm[["recency", "frequency", "monetary"]].describe().round(2).to_string())
    return rfm


def build_pivot_table(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Pivot Table — monthly revenue per product category (top-N categories)."""
    df_valid = df.dropna(subset=["category", "order_month"])

    top_cats = (
        df_valid.groupby("category")["price"]
        .sum()
        .nlargest(top_n)
        .index
    )

    pivot = (
        df_valid[df_valid["category"].isin(top_cats)]
        .pivot_table(
            index      = "category",
            columns    = "order_month",
            values     = "price",
            aggfunc    = "sum",
            fill_value = 0,
        )
    )

    print(f"\n  [eda] Pivot table (top-{top_n} categories × month): {pivot.shape}")
    print(pivot.iloc[:, -6:].round(0).to_string())
    return pivot
