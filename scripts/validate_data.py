from __future__ import annotations

import csv
import math
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SALES_PATH = ROOT / "02-data" / "raw" / "sales.csv"
PRODUCTS_PATH = ROOT / "02-data" / "raw" / "products.csv"

SALES_REQUIRED = {
    "order_id",
    "customer_id",
    "order_date",
    "category",
    "channel",
    "country",
    "city",
    "quantity",
    "unit_price",
    "discount_rate",
    "net_revenue",
    "cost",
    "payment_method",
    "device",
}
PRODUCTS_REQUIRED = {"product_id", "product_name", "category", "brand", "active"}


def _read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None:
            return [], []
        rows = list(reader)
        return rows, [name.strip() for name in reader.fieldnames]


def validate_dataset(
    sales_path: Path = SALES_PATH,
    products_path: Path = PRODUCTS_PATH,
) -> dict[str, Any]:
    errors: list[str] = []
    sales, sales_columns = _read_csv(sales_path)
    products, product_columns = _read_csv(products_path)

    if not sales:
        errors.append("Sales CSV contains no data rows")
    if not products:
        errors.append("Products CSV contains no data rows")

    missing_sales = sorted(SALES_REQUIRED - set(sales_columns))
    missing_products = sorted(PRODUCTS_REQUIRED - set(product_columns))
    if missing_sales:
        errors.append(f"Sales CSV missing columns: {', '.join(missing_sales)}")
    if missing_products:
        errors.append(f"Products CSV missing columns: {', '.join(missing_products)}")
    if missing_sales or missing_products:
        return {
            "sales_rows": len(sales),
            "product_rows": len(products),
            "errors": errors,
        }

    required_sales_values = sorted(SALES_REQUIRED)
    duplicate_orders = [
        order_id
        for order_id, count in Counter(row["order_id"] for row in sales).items()
        if count > 1
    ]
    if duplicate_orders:
        errors.append(f"Duplicate order_id values: {len(duplicate_orders)}")

    revenue_total = 0.0
    cost_total = 0.0
    discount_total = 0.0
    quantity_total = 0
    customer_ids: set[str] = set()
    customer_order_counts: Counter[str] = Counter()
    sales_categories: set[str] = set()

    for row_number, row in enumerate(sales, start=2):
        blanks = [
            column
            for column in required_sales_values
            if not (row.get(column) or "").strip()
        ]
        if blanks:
            errors.append(f"Sales row {row_number}: blank required fields {blanks}")
            continue

        try:
            date.fromisoformat(row["order_date"])
            quantity = int(row["quantity"])
            unit_price = float(row["unit_price"])
            discount_rate = float(row["discount_rate"])
            net_revenue = float(row["net_revenue"])
            cost = float(row["cost"])
        except (TypeError, ValueError):
            errors.append(f"Sales row {row_number}: invalid date or numeric value")
            continue

        numeric_values = (unit_price, discount_rate, net_revenue, cost)
        if not all(math.isfinite(value) for value in numeric_values):
            errors.append(f"Sales row {row_number}: non-finite numeric value")
            continue
        if quantity <= 0:
            errors.append(f"Sales row {row_number}: quantity must be positive")
        if unit_price < 0 or net_revenue < 0 or cost < 0:
            errors.append(
                f"Sales row {row_number}: price, revenue, and cost must be non-negative"
            )
        if not 0 <= discount_rate <= 0.20:
            errors.append(f"Sales row {row_number}: discount_rate outside 0..0.20")

        expected_revenue = round(quantity * unit_price * (1 - discount_rate), 2)
        if abs(net_revenue - expected_revenue) > 0.011:
            errors.append(
                f"Sales row {row_number}: net_revenue does not match quantity, price, and discount"
            )

        revenue_total += net_revenue
        cost_total += cost
        discount_total += discount_rate
        quantity_total += quantity
        customer_ids.add(row["customer_id"])
        customer_order_counts[row["customer_id"]] += 1
        sales_categories.add(row["category"])

    duplicate_products = [
        product_id
        for product_id, count in Counter(row["product_id"] for row in products).items()
        if count > 1
    ]
    if duplicate_products:
        errors.append(f"Duplicate product_id values: {len(duplicate_products)}")

    product_categories: set[str] = set()
    for row_number, row in enumerate(products, start=2):
        blanks = [
            column
            for column in sorted(PRODUCTS_REQUIRED)
            if not (row.get(column) or "").strip()
        ]
        if blanks:
            errors.append(f"Products row {row_number}: blank required fields {blanks}")
        if row["active"].strip().lower() not in {"yes", "no"}:
            errors.append(f"Products row {row_number}: active must be Yes or No")
        product_categories.add(row["category"])

    missing_product_categories = sorted(sales_categories - product_categories)
    if missing_product_categories:
        errors.append(
            "Sales categories missing from products catalog: "
            + ", ".join(missing_product_categories)
        )

    return {
        "sales_rows": len(sales),
        "product_rows": len(products),
        "unique_customers": len(customer_ids),
        "repeat_customers": sum(count > 1 for count in customer_order_counts.values()),
        "total_units": quantity_total,
        "revenue_total": round(revenue_total, 2),
        "cost_total": round(cost_total, 2),
        "gross_margin": round(revenue_total - cost_total, 2),
        "average_discount_pct": round(discount_total / len(sales) * 100, 2)
        if sales
        else 0.0,
        "errors": errors,
    }


def main() -> int:
    result = validate_dataset()
    print(f"Sales rows: {result['sales_rows']}")
    print(f"Product rows: {result['product_rows']}")
    if "revenue_total" in result:
        print(f"Revenue total: {result['revenue_total']:.2f}")
        print(f"Gross margin: {result['gross_margin']:.2f}")
        print(f"Average discount: {result['average_discount_pct']:.2f}%")

    errors = result["errors"]
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("PASS - Dataset structure and quality checks succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
