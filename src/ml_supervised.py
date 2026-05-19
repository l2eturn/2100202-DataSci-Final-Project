import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from src.config import TOP_N_CATS, RF_ESTIMATORS, RF_MAX_DEPTH, TEST_SIZE, RANDOM_STATE

NUMERIC_FEATURES = [
    "price", "freight_value", "delivery_days",
    "delay_days", "payment_value", "payment_installments",
]


def run(df: pd.DataFrame) -> tuple[RandomForestClassifier, pd.Series, dict]:
    """
    Supervised pipeline: SimpleImputer → StandardScaler → RandomForestClassifier.
    Returns (fitted_pipeline, feature_importances_series, metrics_dict).
    """
    X, y, feature_names = _build_features(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

    pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler",  StandardScaler()),
        ("clf",     RandomForestClassifier(
            n_estimators  = RF_ESTIMATORS,
            max_depth     = RF_MAX_DEPTH,
            class_weight  = "balanced",
            random_state  = RANDOM_STATE,
            n_jobs        = -1,
        )),
    ])

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    cm      = confusion_matrix(y_test, y_pred)
    report  = classification_report(y_test, y_pred,
                                    target_names=["Not Satisfied", "Satisfied"])
    print("\n  [rf] Classification Report:")
    print(report)

    rf_model     = pipeline.named_steps["clf"]
    importances  = pd.Series(rf_model.feature_importances_, index=feature_names)

    metrics = {"confusion_matrix": cm, "report": report}
    return pipeline, importances, metrics


def _build_features(df: pd.DataFrame) -> tuple:
    top_cats = df["category"].value_counts().nlargest(TOP_N_CATS).index
    df       = df.copy()
    df["category_grouped"] = df["category"].where(df["category"].isin(top_cats), "other")

    cat_dummies = pd.get_dummies(df["category_grouped"], prefix="cat", drop_first=True)

    X = pd.concat(
        [df[NUMERIC_FEATURES].reset_index(drop=True),
         cat_dummies.reset_index(drop=True)],
        axis=1,
    )

    # 1 = satisfied (4–5 stars), 0 = not satisfied (1–3 stars)
    y = (df["review_score"] >= 4).astype(int).reset_index(drop=True)

    valid = X.notna().all(axis=1) & y.notna()
    X, y  = X[valid], y[valid]

    feature_names = X.columns.tolist()
    print(f"  [rf] Feature matrix: {X.shape} | class balance: "
          f"satisfied={y.mean():.1%}, not_satisfied={(1-y).mean():.1%}")

    return X.values, y.values, feature_names
