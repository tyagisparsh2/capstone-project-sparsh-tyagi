import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "visualizations"

OUTPUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------
# Load raw CSV files
# ---------------------------------------------------------
orders = pd.read_csv(DATA_DIR / "orders.csv")
products = pd.read_csv(DATA_DIR / "products.csv")
customers = pd.read_csv(DATA_DIR / "customers.csv")

# ---------------------------------------------------------
# Clean orders exactly as required
# ---------------------------------------------------------

# Clean payment method
orders["payment_method"] = (
    orders["payment_method"]
    .str.strip()
    .str.upper()
)

# Detect natural-key duplicates
natural_key = [
    "customer_id",
    "product_id",
    "order_date",
    "quantity",
    "discount_pct",
    "payment_method",
    "rating",
    "returned"
]

# Drop duplicates, keeping the first occurrence
orders = orders.drop_duplicates(
    subset=natural_key,
    keep="first"
).copy()

# Fill missing discount with 0
orders["discount_pct"] = orders["discount_pct"].fillna(0)

# Fill missing rating with median
orders["rating"] = orders["rating"].fillna(
    orders["rating"].median()
)

# ---------------------------------------------------------
# TASK 9 — Return rate by payment method
# ---------------------------------------------------------

payment_returns = (
    orders.groupby("payment_method")["returned"]
    .agg(["count", "mean"])
    .sort_values("mean", ascending=False)
)

payment_returns["return_rate"] = payment_returns["mean"] * 100

print("\nReturn rate by payment method:")
print(payment_returns)

# ---------------------------------------------------------
# Create return-rate bar chart
# ---------------------------------------------------------

plt.figure(figsize=(8, 5))

bars = plt.bar(
    payment_returns.index,
    payment_returns["return_rate"]
)

# Exact percentage on every bar
for bar, rate in zip(bars, payment_returns["return_rate"]):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{rate:.1f}%",
        ha="center",
        va="bottom"
    )

# Highest-risk payment method
highest_payment = payment_returns.index[0]
highest_rate = payment_returns["return_rate"].iloc[0]

card_rate = payment_returns.loc["CARD", "return_rate"]
ratio = highest_rate / card_rate

plt.title(
    f"{highest_payment} Returns at {highest_rate:.1f}% — "
    f"{ratio:.0f}x Card"
)

plt.xlabel("Payment Method")
plt.ylabel("Return Rate (%)")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "return_rate_by_payment.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ---------------------------------------------------------
# TASK 10 — Monthly revenue
# ---------------------------------------------------------

# Merge orders with products
orders_products = orders.merge(
    products[["product_id", "price"]],
    on="product_id",
    how="left"
)

# Calculate order value
orders_products["order_value"] = (
    orders_products["quantity"]
    * orders_products["price"]
    * (1 - orders_products["discount_pct"] / 100)
)

# Convert date
orders_products["order_date"] = pd.to_datetime(
    orders_products["order_date"]
)

# Month
orders_products["month"] = (
    orders_products["order_date"]
    .dt.to_period("M")
)

# ---------------------------------------------------------
# Outlier correction
# ---------------------------------------------------------
# Quantity outliers identified in Task 7:
# O0011 = quantity 25
# O0098 = quantity 30
#
# Task 10 requires the corrected monthly revenue,
# excluding the inflated contribution from these outliers.
# ---------------------------------------------------------

outlier_order_ids = ["O0011", "O0098"]

outlier_values = orders_products.loc[
    orders_products["order_id"].isin(outlier_order_ids),
    ["order_id", "month", "order_value"]
]

# Normal monthly revenue before correction
monthly_revenue = (
    orders_products
    .groupby("month")["order_value"]
    .sum()
)

# Remove the identified outlier contributions
outlier_monthly = (
    outlier_values
    .groupby("month")["order_value"]
    .sum()
)

corrected_monthly_revenue = (
    monthly_revenue
    .subtract(outlier_monthly, fill_value=0)
    .sort_index()
)

print("\nOutlier-corrected monthly revenue:")
print(corrected_monthly_revenue)

# ---------------------------------------------------------
# Find actual peak month AFTER correction
# ---------------------------------------------------------

peak_month = corrected_monthly_revenue.idxmax()
peak_revenue = corrected_monthly_revenue.max()

print(
    f"\nActual peak month after outlier correction: "
    f"{peak_month} — ₹{peak_revenue:.2f}"
)

# ---------------------------------------------------------
# Create corrected monthly revenue line chart
# ---------------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    corrected_monthly_revenue.index.astype(str),
    corrected_monthly_revenue.values,
    marker="o"
)

plt.xlabel("Month")
plt.ylabel("Revenue (₹)")

plt.title(
    f"Outlier-Corrected Monthly Revenue — "
    f"Peak: {peak_month} (₹{peak_revenue:,.2f})"
)

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "monthly_revenue_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nVisualization files created successfully:")
print(OUTPUT_DIR / "return_rate_by_payment.png")
print(OUTPUT_DIR / "monthly_revenue_trend.png")

