from google.cloud.bigquery import SchemaField

# カラムの説明はエージェントが get_table_info で読むので、集計に必要な意味を書いておく
TABLES: dict[str, tuple[str, list[SchemaField]]] = {
    "customers": (
        "会員 (顧客) マスタ",
        [
            SchemaField("customer_id", "STRING", "REQUIRED", description="顧客ID"),
            SchemaField("prefecture", "STRING", description="居住都道府県"),
            SchemaField("age_group", "STRING", description="年代 (10代〜60代以上)"),
            SchemaField("gender", "STRING", description="性別 (女性 / 男性 / その他)"),
            SchemaField("membership_rank", "STRING", description="会員ランク (ブロンズ / シルバー / ゴールド)"),
            SchemaField("signup_date", "DATE", description="会員登録日"),
        ],
    ),
    "products": (
        "商品マスタ",
        [
            SchemaField("product_id", "STRING", "REQUIRED", description="商品ID"),
            SchemaField("product_name", "STRING", description="商品名"),
            SchemaField("category", "STRING", description="商品カテゴリ (食品 / 飲料 / 日用品 / 家電 / ファッション / 美容)"),
            SchemaField("unit_price", "INT64", description="定価 (円, 税込)"),
            SchemaField("unit_cost", "INT64", description="原価 (円)"),
        ],
    ),
    "orders": (
        "注文ヘッダ (1注文1行)",
        [
            SchemaField("order_id", "STRING", "REQUIRED", description="注文ID"),
            SchemaField("order_date", "DATE", description="注文日"),
            SchemaField("customer_id", "STRING", description="顧客ID (customers.customer_id)"),
            SchemaField("channel", "STRING", description="販売チャネル (店舗 / EC / アプリ)"),
            SchemaField("status", "STRING", description="注文ステータス。売上集計は completed のみを対象にする (cancelled / returned は除外)"),
        ],
    ),
    "order_items": (
        "注文明細 (1注文に1〜4行)",
        [
            SchemaField("order_id", "STRING", "REQUIRED", description="注文ID (orders.order_id)"),
            SchemaField("line_no", "INT64", "REQUIRED", description="明細行番号"),
            SchemaField("product_id", "STRING", description="商品ID (products.product_id)"),
            SchemaField("quantity", "INT64", description="数量"),
            SchemaField("unit_price", "INT64", description="販売時の単価 (円)"),
            SchemaField("discount_rate", "FLOAT64", description="割引率 (0.0〜1.0)"),
            SchemaField("amount", "INT64", description="売上金額 (円) = unit_price × quantity × (1 - discount_rate)"),
        ],
    ),
}

SALES_VIEW_NAME = "sales"
SALES_VIEW_DESCRIPTION = (
    "売上分析用ビュー。completed の注文明細に注文・顧客・商品の属性を結合したもの (1明細1行)。"
    "売上金額は amount、粗利は gross_profit を合計する"
)
SALES_VIEW_SQL = """
SELECT
  o.order_date,
  o.order_id,
  o.channel,
  i.line_no,
  p.product_id,
  p.product_name,
  p.category,
  i.quantity,
  i.discount_rate,
  i.amount,
  i.amount - p.unit_cost * i.quantity AS gross_profit,
  c.customer_id,
  c.prefecture,
  c.age_group,
  c.gender,
  c.membership_rank
FROM `{dataset}.order_items` AS i
JOIN `{dataset}.orders` AS o USING (order_id)
JOIN `{dataset}.products` AS p USING (product_id)
JOIN `{dataset}.customers` AS c USING (customer_id)
WHERE o.status = 'completed'
"""
