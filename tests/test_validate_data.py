from __future__ import annotations

import csv
from pathlib import Path

from scripts.validate_data import PRODUCTS_REQUIRED, SALES_REQUIRED, validate_dataset


ROOT = Path(__file__).resolve().parents[1]


def _write_csv(path: Path, columns: set[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=sorted(columns))
        writer.writeheader()
        writer.writerows(rows)


def _valid_sale(**overrides: str) -> dict[str, str]:
    row = {
        "order_id": "O0001",
        "customer_id": "C0001",
        "order_date": "2025-01-01",
        "category": "Higiene",
        "channel": "Email",
        "country": "AR",
        "city": "Buenos Aires",
        "quantity": "2",
        "unit_price": "10.00",
        "discount_rate": "0.10",
        "net_revenue": "18.00",
        "cost": "12.00",
        "payment_method": "Card",
        "device": "Mobile",
    }
    row.update(overrides)
    return row


def _valid_product(**overrides: str) -> dict[str, str]:
    row = {
        "product_id": "P0001",
        "product_name": "Higiene Gel",
        "category": "Higiene",
        "brand": "Demo",
        "active": "Yes",
    }
    row.update(overrides)
    return row


def test_repository_datasets_pass_quality_checks() -> None:
    result = validate_dataset()

    assert result["sales_rows"] == 3500
    assert result["product_rows"] == 500
    assert result["unique_customers"] == 877
    assert result["errors"] == []


def test_validator_detects_duplicate_ids_and_invalid_sales_values(
    tmp_path: Path,
) -> None:
    sales_path = tmp_path / "sales.csv"
    products_path = tmp_path / "products.csv"
    _write_csv(
        sales_path,
        SALES_REQUIRED,
        [
            _valid_sale(),
            _valid_sale(discount_rate="0.30", net_revenue="99.00"),
        ],
    )
    _write_csv(products_path, PRODUCTS_REQUIRED, [_valid_product()])

    result = validate_dataset(sales_path, products_path)

    assert result["sales_rows"] == 2
    assert any("Duplicate order_id" in error for error in result["errors"])
    assert any("discount_rate outside" in error for error in result["errors"])
    assert any("net_revenue does not match" in error for error in result["errors"])


def test_validator_reports_missing_required_columns(tmp_path: Path) -> None:
    sales_path = tmp_path / "sales.csv"
    products_path = tmp_path / "products.csv"
    _write_csv(
        sales_path,
        {"order_id", "customer_id"},
        [{"order_id": "O1", "customer_id": "C1"}],
    )
    _write_csv(products_path, PRODUCTS_REQUIRED, [_valid_product()])

    result = validate_dataset(sales_path, products_path)

    assert any("Sales CSV missing columns" in error for error in result["errors"])


def test_validator_detects_category_missing_from_product_catalog(
    tmp_path: Path,
) -> None:
    sales_path = tmp_path / "sales.csv"
    products_path = tmp_path / "products.csv"
    _write_csv(sales_path, SALES_REQUIRED, [_valid_sale(category="OTC")])
    _write_csv(products_path, PRODUCTS_REQUIRED, [_valid_product(category="Higiene")])

    result = validate_dataset(sales_path, products_path)

    assert any(
        "Sales categories missing from products catalog" in error
        for error in result["errors"]
    )
