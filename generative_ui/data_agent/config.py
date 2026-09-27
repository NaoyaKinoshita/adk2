import os

from google.genai import types

# --- Gemini ---
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
# 1リクエストあたりのタイムアウト (ミリ秒)
LLM_TIMEOUT_MS = 60_000
# 429 (共有プールの一時的な枯渇) と 503 を指数バックオフでリトライする
LLM_RETRY_OPTIONS = types.HttpRetryOptions(
    attempts=5,
    initial_delay=1.0,
    max_delay=30.0,
    exp_base=2.0,
    jitter=1.0,
    http_status_codes=[429, 503],
)

# --- BigQuery ---
BQ_COMPUTE_PROJECT_ID = os.getenv("BQ_COMPUTE_PROJECT_ID") or os.getenv(
    "GOOGLE_CLOUD_PROJECT"
)
BQ_DATASET = os.getenv("BQ_DATASET", "bigquery-public-data.thelook_ecommerce")
BQ_LOCATION = os.getenv("BQ_LOCATION") or None
# チャート描画に使う最大行数 (execute_sql の LIMIT 相当)
BQ_MAX_RESULT_ROWS = 1000
# 1クエリあたりの最大スキャン量 (1GB)。超えるクエリは BigQuery 側で失敗する
BQ_MAXIMUM_BYTES_BILLED = 1 * 1024**3
BQ_APPLICATION_NAME = "adk2-generative-ui"
# データエージェントに公開する BigQueryToolset のツール (読み取り系のみ)
BQ_TOOL_NAMES = [
    "list_table_ids",
    "get_table_info",
    "execute_sql",
]

# --- 結果の受け渡し ---
EXECUTE_SQL_TOOL_NAME = "execute_sql"
# クエリ結果を保存する state キーのプレフィックス (キー: f"{prefix}{result_id}")
QUERY_RESULT_STATE_PREFIX = "query_result:"
RESULT_ID_LENGTH = 8
# LLM に返すプレビュー行数 (全行は state 経由でフロントに渡す)
PREVIEW_ROW_COUNT = 5
