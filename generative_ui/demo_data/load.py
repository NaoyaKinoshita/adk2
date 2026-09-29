"""
デモ用データを BigQuery に作成する (何度実行しても同じ状態になる)

使い方 (generative_ui/ で実行):
    uv run python -m demo_data.load [--project PROJECT] [--dataset DATASET] [--location LOCATION]
"""

import argparse
import datetime
import logging
from dataclasses import asdict
from typing import Any

from google.cloud import bigquery

from demo_data.config import (
    BQ_JOB_TIMEOUT_SECONDS,
    DEFAULT_DATASET_ID,
    DEFAULT_LOCATION,
    DEFAULT_PROJECT_ID,
    SEED,
)
from demo_data.generate import generate
from demo_data.schema import (
    SALES_VIEW_DESCRIPTION,
    SALES_VIEW_NAME,
    SALES_VIEW_SQL,
    TABLES,
)

logger = logging.getLogger(__name__)


def _to_json_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            _key: _value.isoformat() if isinstance(_value, datetime.date) else _value
            for _key, _value in row.items()
        }
        for row in rows
    ]


def load(project_id: str, dataset_id: str, location: str) -> None:
    client = bigquery.Client(project=project_id, location=location)
    dataset_ref = f"{project_id}.{dataset_id}"

    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = location
    dataset.description = "Generative UI 技術検証用のデモ EC 売上データ (架空)"
    client.create_dataset(dataset, exists_ok=True, timeout=BQ_JOB_TIMEOUT_SECONDS)
    logger.info(f"dataset ready: {dataset_ref} ({location})")

    data = asdict(generate(SEED))
    for table_name, (description, schema) in TABLES.items():
        table_ref = f"{dataset_ref}.{table_name}"
        rows = _to_json_rows(data[table_name])
        # バッチロード (無料) で全件を置き換える
        job = client.load_table_from_json(
            rows,
            table_ref,
            job_config=bigquery.LoadJobConfig(
                schema=schema,
                write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            ),
        )
        job.result(timeout=BQ_JOB_TIMEOUT_SECONDS)

        table = client.get_table(table_ref)
        table.description = description
        client.update_table(table, ["description"])
        logger.info(f"loaded: {table_ref} rows={len(rows)}")

    view = bigquery.Table(f"{dataset_ref}.{SALES_VIEW_NAME}")
    view.view_query = SALES_VIEW_SQL.format(dataset=dataset_ref)
    view.description = SALES_VIEW_DESCRIPTION
    client.delete_table(view, not_found_ok=True)
    client.create_table(view, timeout=BQ_JOB_TIMEOUT_SECONDS)
    logger.info(f"view ready: {dataset_ref}.{SALES_VIEW_NAME}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--project", default=DEFAULT_PROJECT_ID)
    parser.add_argument("--dataset", default=DEFAULT_DATASET_ID)
    parser.add_argument("--location", default=DEFAULT_LOCATION)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    load(args.project, args.dataset, args.location)


if __name__ == "__main__":
    main()
