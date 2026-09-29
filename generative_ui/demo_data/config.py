import datetime

DEFAULT_PROJECT_ID = "healthy-matter-465806-v4"
DEFAULT_DATASET_ID = "genui_demo"
DEFAULT_LOCATION = "asia-northeast1"

# 乱数シード (同じシードなら毎回同じデータになる)
SEED = 20260929

CUSTOMER_COUNT = 3000
SIGNUP_START = datetime.date(2023, 1, 1)
ORDER_START = datetime.date(2024, 1, 1)
ORDER_END = datetime.date(2026, 8, 31)

# 1日あたりの基準注文数と、期間全体での成長率 (最終日は基準の 1 + GROWTH 倍)
BASE_DAILY_ORDERS = 30
ORDER_GROWTH = 0.8
MAX_ITEMS_PER_ORDER = 4

# BigQuery のロードジョブ・クエリのタイムアウト (秒)
BQ_JOB_TIMEOUT_SECONDS = 300
