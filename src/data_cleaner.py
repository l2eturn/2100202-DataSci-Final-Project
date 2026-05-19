import pandas as pd
from src.config import DATE_COLS


def clean(dfs: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """
    Cleansing step — operates on raw DataFrames in-place.
    Returns the same dict with cleaned tables.
    """
    dfs = {k: v.copy() for k, v in dfs.items()}

    _clean_orders(dfs["orders"])
    _clean_reviews(dfs["reviews"])
    _clean_products(dfs["products"], dfs["category"])

    return dfs


def _clean_orders(df: pd.DataFrame) -> None:
    # Convert string timestamps to datetime
    for col in DATE_COLS:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    before = len(df)
    mask = (
        (df["order_status"] == "delivered")
        & df["order_delivered_customer_date"].notna()
        & df["order_estimated_delivery_date"].notna()
    )
    # Filter in-place via boolean index stored back on the caller's reference
    rows_to_drop = df.index[~mask]
    df.drop(index=rows_to_drop, inplace=True)
    df.reset_index(drop=True, inplace=True)
    print(f"  [clean] orders: {before} → {len(df)} rows (kept 'delivered' with valid dates)")


def _clean_reviews(df: pd.DataFrame) -> None:
    filled_msg   = df["review_comment_message"].isna().sum()
    filled_title = df["review_comment_title"].isna().sum()
    df["review_comment_message"].fillna("(no comment)", inplace=True)
    df["review_comment_title"].fillna("(no title)", inplace=True)
    print(f"  [clean] reviews: filled {filled_msg} missing messages, {filled_title} missing titles")


def _clean_products(df_products: pd.DataFrame, df_category: pd.DataFrame) -> None:
    df_products.merge(df_category, on="product_category_name", how="left")
    # Translation is applied during integration; just flag missing categories
    missing = df_products["product_category_name"].isna().sum()
    if missing:
        df_products["product_category_name"].fillna("unknown", inplace=True)
    print(f"  [clean] products: {missing} missing category names filled")
