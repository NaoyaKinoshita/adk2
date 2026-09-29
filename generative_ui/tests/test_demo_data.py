import datetime
from dataclasses import asdict
from unittest import mock

import pytest

from demo_data import load as load_module
from demo_data.config import ORDER_END, ORDER_START, SEED
from demo_data.generate import generate
from demo_data.schema import TABLES


@pytest.fixture(scope="module")
def data():
    return generate(SEED)


def test_generate_is_deterministic(data):
    again = generate(SEED)
    assert data.orders[:100] == again.orders[:100]
    assert len(data.order_items) == len(again.order_items)


def test_rows_match_schema(data):
    rows = asdict(data)
    for table_name, (_, schema) in TABLES.items():
        assert set(rows[table_name][0]) == {field.name for field in schema}, table_name


def test_primary_keys_are_unique(data):
    assert len({c["customer_id"] for c in data.customers}) == len(data.customers)
    assert len({p["product_id"] for p in data.products}) == len(data.products)
    assert len({o["order_id"] for o in data.orders}) == len(data.orders)
    assert len({(i["order_id"], i["line_no"]) for i in data.order_items}) == len(
        data.order_items
    )


def test_foreign_keys_exist(data):
    customer_ids = {c["customer_id"] for c in data.customers}
    product_ids = {p["product_id"] for p in data.products}
    order_ids = {o["order_id"] for o in data.orders}
    assert {o["customer_id"] for o in data.orders} <= customer_ids
    assert {i["product_id"] for i in data.order_items} <= product_ids
    assert {i["order_id"] for i in data.order_items} == order_ids


def test_orders_are_after_signup_and_in_range(data):
    signup = {c["customer_id"]: c["signup_date"] for c in data.customers}
    for order in data.orders:
        assert ORDER_START <= order["order_date"] <= ORDER_END
        assert order["order_date"] >= signup[order["customer_id"]]


def test_amount_matches_price_and_discount(data):
    for item in data.order_items[:1000]:
        expected = round(item["unit_price"] * item["quantity"] * (1 - item["discount_rate"]))
        assert item["amount"] == expected


def test_to_json_rows_serializes_dates():
    rows = load_module._to_json_rows([{"d": datetime.date(2026, 1, 2), "n": 1}])
    assert rows == [{"d": "2026-01-02", "n": 1}]


def test_load_creates_dataset_tables_and_view():
    client = mock.MagicMock()
    with mock.patch.object(load_module.bigquery, "Client", return_value=client):
        load_module.load("proj", "ds", "asia-northeast1")

    client.create_dataset.assert_called_once()
    loaded_tables = [call.args[1] for call in client.load_table_from_json.call_args_list]
    assert loaded_tables == [f"proj.ds.{name}" for name in TABLES]
    for call in client.load_table_from_json.call_args_list:
        job_config = call.kwargs["job_config"]
        assert job_config.write_disposition == "WRITE_TRUNCATE"
    view = client.create_table.call_args.args[0]
    assert view.table_id == "sales"
    assert "`proj.ds.order_items`" in view.view_query
