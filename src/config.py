from pathlib import Path

ROOT       = Path(__file__).resolve().parent.parent
DATA_PATH  = ROOT / "raw-data"
OUTPUT_DIR = ROOT / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

CSV_FILES = {
    "orders":    "olist_orders_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "items":     "olist_order_items_dataset.csv",
    "reviews":   "olist_order_reviews_dataset.csv",
    "payments":  "olist_order_payments_dataset.csv",
    "products":  "olist_products_dataset.csv",
    "category":  "product_category_name_translation.csv",
}

DATE_COLS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

REGION_MAP = {
    "SP": "Southeast", "RJ": "Southeast", "MG": "Southeast", "ES": "Southeast",
    "SC": "South",     "PR": "South",     "RS": "South",
    "BA": "Northeast", "CE": "Northeast", "PE": "Northeast", "MA": "Northeast",
    "PB": "Northeast", "RN": "Northeast", "AL": "Northeast", "SE": "Northeast",
    "PI": "Northeast",
    "DF": "Center-West", "GO": "Center-West", "MT": "Center-West", "MS": "Center-West",
    "AM": "North", "PA": "North", "RO": "North", "RR": "North",
    "AC": "North", "AP": "North", "TO": "North",
}

KMEANS_K      = 4
RF_ESTIMATORS = 200
RF_MAX_DEPTH  = 10
TOP_N_CATS    = 15
TEST_SIZE     = 0.2
RANDOM_STATE  = 42
