import pandas as pd
from src.config import REGION_MAP


def integrate(dfs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Merge / Join step — combines all tables into one master DataFrame.
    Returns the master DataFrame enriched with derived features.
    """
    df = _merge_tables(dfs)
    df = _add_derived_features(df)
    print(f"  [integrate] master DataFrame: {df.shape}")
    return df


def _merge_tables(dfs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    # Translate product category names
    products = dfs["products"].merge(
        dfs["category"], on="product_category_name", how="left"
    )
    products["product_category_name_english"].fillna("unknown", inplace=True)

    # Aggregate payments per order
    pay_agg = (
        dfs["payments"]
        .groupby("order_id", as_index=False)
        .agg(
            payment_value=("payment_value", "sum"),
            payment_installments=("payment_installments", "max"),
        )
    )

    # Keep one review score per order (first occurrence)
    reviews_dedup = (
        dfs["reviews"][["order_id", "review_score"]]
        .drop_duplicates(subset="order_id", keep="first")
    )

    df = (
        dfs["orders"]
        .merge(dfs["customers"],                             on="customer_id",  how="left")
        .merge(dfs["items"][["order_id", "product_id",
                              "price", "freight_value"]],    on="order_id",     how="left")
        .merge(reviews_dedup,                                on="order_id",     how="left")
        .merge(products[["product_id",
                          "product_category_name_english"]], on="product_id",   how="left")
        .merge(pay_agg,                                      on="order_id",     how="left")
    )

    df.rename(columns={"product_category_name_english": "category"}, inplace=True)
    return df


def _add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    df["delivery_days"] = (
        df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
    ).dt.days

    df["delay_days"] = (
        df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]
    ).dt.days

    df["order_month"] = df["order_purchase_timestamp"].dt.to_period("M")
    df["region"]      = df["customer_state"].map(REGION_MAP).fillna("Other")
    return df
