import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from src.config import KMEANS_K, RANDOM_STATE


def run(rfm: pd.DataFrame) -> pd.DataFrame:
    """
    Unsupervised pipeline: StandardScaler → KMeans.
    Adds 'cluster' and 'segment' columns to rfm.
    Returns the enriched rfm DataFrame.
    """
    features = rfm[["recency", "frequency", "monetary"]].values

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("kmeans", KMeans(n_clusters=KMEANS_K, random_state=RANDOM_STATE, n_init=10)),
    ])

    rfm = rfm.copy()
    rfm["cluster"] = pipeline.fit_predict(features)

    profile = _build_profile(rfm)
    rfm["segment"] = rfm["cluster"].map(profile["segment"])

    print("\n  [kmeans] Cluster profile:")
    print(profile.to_string())
    return rfm


def _build_profile(rfm: pd.DataFrame) -> pd.DataFrame:
    profile = (
        rfm.groupby("cluster")
        .agg(
            count     = ("customer_unique_id", "count"),
            recency   = ("recency",            "mean"),
            frequency = ("frequency",          "mean"),
            monetary  = ("monetary",           "mean"),
        )
        .round(1)
    )

    q75_monetary = profile["monetary"].quantile(0.75)
    q25_recency  = profile["recency"].quantile(0.25)
    q75_recency  = profile["recency"].quantile(0.75)

    def _label(row):
        if row["monetary"] >= q75_monetary:
            return "VIP"
        if row["recency"] <= q25_recency:
            return "Recent Buyer"
        if row["recency"] >= q75_recency:
            return "At Risk"
        return "Regular"

    profile["segment"] = profile.apply(_label, axis=1)
    return profile
