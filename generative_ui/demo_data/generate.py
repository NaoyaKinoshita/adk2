"""デモ用の EC 売上データ (顧客・商品・注文・注文明細) を生成する"""

import datetime
import math
import random
from dataclasses import dataclass
from typing import Any

from demo_data.config import (
    BASE_DAILY_ORDERS,
    CUSTOMER_COUNT,
    MAX_ITEMS_PER_ORDER,
    ORDER_END,
    ORDER_GROWTH,
    ORDER_START,
    SIGNUP_START,
)

Row = dict[str, Any]

PREFECTURES = {
    "東京都": 22, "神奈川県": 12, "大阪府": 11, "愛知県": 8, "埼玉県": 8,
    "千葉県": 7, "福岡県": 6, "北海道": 6, "兵庫県": 6, "京都府": 4,
    "宮城県": 3, "広島県": 3, "沖縄県": 2, "新潟県": 2,
}
AGE_GROUPS = {"10代": 5, "20代": 22, "30代": 26, "40代": 22, "50代": 15, "60代以上": 10}
GENDERS = {"女性": 55, "男性": 43, "その他": 2}
RANKS = {"ブロンズ": 70, "シルバー": 22, "ゴールド": 8}
# 会員ランクごとの購入頻度の重み
RANK_ORDER_WEIGHT = {"ブロンズ": 1.0, "シルバー": 2.5, "ゴールド": 5.0}

# (カテゴリ, 商品名, 単価, 原価率)
PRODUCTS = [
    ("食品", "有機玄米 5kg", 3480, 0.62), ("食品", "国産はちみつ 500g", 2380, 0.55),
    ("食品", "ドライフルーツミックス", 1280, 0.50), ("食品", "北海道チーズセット", 4200, 0.60),
    ("食品", "高級和牛ハンバーグ", 5800, 0.65), ("食品", "グラノーラ 1kg", 1580, 0.48),
    ("飲料", "ミネラルウォーター 24本", 1980, 0.45), ("飲料", "有機緑茶ティーバッグ", 980, 0.40),
    ("飲料", "スペシャルティコーヒー豆", 2480, 0.52), ("飲料", "クラフトビール 6本", 3300, 0.58),
    ("飲料", "炭酸水 24本", 2160, 0.44), ("飲料", "フルーツジュース詰合せ", 3600, 0.55),
    ("日用品", "詰め替え洗剤 3個", 1480, 0.50), ("日用品", "トイレットペーパー 12ロール", 880, 0.60),
    ("日用品", "キッチンペーパー 6ロール", 680, 0.58), ("日用品", "除菌スプレー", 780, 0.45),
    ("日用品", "収納ボックス", 2980, 0.48), ("日用品", "バスタオル 2枚", 3200, 0.42),
    ("家電", "ワイヤレスイヤホン", 12800, 0.68), ("家電", "コードレス掃除機", 29800, 0.70),
    ("家電", "電気ケトル", 5980, 0.62), ("家電", "空気清浄機", 24800, 0.66),
    ("家電", "ドライヤー", 9800, 0.60), ("家電", "モバイルバッテリー", 3980, 0.55),
    ("ファッション", "オーガニックコットンTシャツ", 3900, 0.38), ("ファッション", "デニムパンツ", 8900, 0.40),
    ("ファッション", "スニーカー", 11800, 0.45), ("ファッション", "ダウンジャケット", 19800, 0.42),
    ("ファッション", "リネンシャツ", 6900, 0.38), ("ファッション", "トートバッグ", 4500, 0.35),
    ("美容", "保湿化粧水", 2800, 0.30), ("美容", "日焼け止め", 1980, 0.32),
    ("美容", "ヘアオイル", 3200, 0.30), ("美容", "ハンドクリーム", 1200, 0.28),
    ("美容", "フェイスマスク 30枚", 2400, 0.33), ("美容", "ボディソープ", 1600, 0.35),
]

# 月ごとの全体の季節性 (1〜12月)
MONTH_FACTOR = [0.85, 0.80, 0.95, 0.95, 1.00, 0.95, 1.15, 1.05, 0.90, 0.95, 1.10, 1.40]
# 曜日ごとの係数 (月〜日)
WEEKDAY_FACTOR = [0.90, 0.90, 0.95, 0.95, 1.05, 1.20, 1.15]
# カテゴリごとに売れやすい月 (その月は重みを上げる)
CATEGORY_PEAK_MONTHS = {
    "飲料": {6, 7, 8},
    "家電": {3, 12},
    "ファッション": {4, 10, 11},
    "美容": {5, 6, 7},
    "食品": {12},
    "日用品": set(),
}
PEAK_MONTH_WEIGHT = 2.0
# セール月は一部の明細に割引がかかる
SALE_MONTHS = {7, 12}
DISCOUNT_RATES = [0.1, 0.2]
SALE_DISCOUNT_PROBABILITY = 0.4
NORMAL_DISCOUNT_PROBABILITY = 0.05
STATUSES = {"completed": 90, "cancelled": 5, "returned": 5}


@dataclass
class DemoData:
    customers: list[Row]
    products: list[Row]
    orders: list[Row]
    order_items: list[Row]


def _pick(rng: random.Random, weights: dict[str, float]) -> str:
    return rng.choices(list(weights), weights=list(weights.values()))[0]


def _date_range(start: datetime.date, end: datetime.date):
    for offset in range((end - start).days + 1):
        yield start + datetime.timedelta(days=offset)


def _channel_weights(progress: float) -> dict[str, float]:
    """
    期間が進むにつれてアプリ経由の比率が伸びる
    """
    return {"店舗": 40 - 15 * progress, "EC": 40, "アプリ": 20 + 15 * progress}


def generate_customers(rng: random.Random) -> list[Row]:
    signup_days = (ORDER_END - SIGNUP_START).days
    customers = []
    for i in range(CUSTOMER_COUNT):
        customers.append(
            {
                "customer_id": f"C{i + 1:05d}",
                "prefecture": _pick(rng, PREFECTURES),
                "age_group": _pick(rng, AGE_GROUPS),
                "gender": _pick(rng, GENDERS),
                "membership_rank": _pick(rng, RANKS),
                "signup_date": SIGNUP_START
                + datetime.timedelta(days=rng.randint(0, signup_days)),
            }
        )
    # 登録日順に並べ、注文日時点で登録済みの顧客だけを選べるようにする
    customers.sort(key=lambda c: c["signup_date"])
    return customers


def generate_products() -> list[Row]:
    return [
        {
            "product_id": f"P{i + 1:03d}",
            "product_name": name,
            "category": category,
            "unit_price": price,
            "unit_cost": round(price * cost_rate),
        }
        for i, (category, name, price, cost_rate) in enumerate(PRODUCTS)
    ]


def generate_orders(
    rng: random.Random, customers: list[Row], products: list[Row]
) -> tuple[list[Row], list[Row]]:
    total_days = (ORDER_END - ORDER_START).days
    signup_dates = [c["signup_date"] for c in customers]
    customer_weights = [RANK_ORDER_WEIGHT[c["membership_rank"]] for c in customers]

    orders: list[Row] = []
    order_items: list[Row] = []
    registered = 0
    for day in _date_range(ORDER_START, ORDER_END):
        # 注文日までに登録した顧客の数 (customers は登録日順)
        while registered < len(customers) and signup_dates[registered] <= day:
            registered += 1
        if registered == 0:
            continue

        progress = (day - ORDER_START).days / total_days
        expected = (
            BASE_DAILY_ORDERS
            * (1 + ORDER_GROWTH * progress)
            * MONTH_FACTOR[day.month - 1]
            * WEEKDAY_FACTOR[day.weekday()]
        )
        order_count = max(0, round(rng.gauss(expected, math.sqrt(expected))))
        product_weights = [
            PEAK_MONTH_WEIGHT if day.month in CATEGORY_PEAK_MONTHS[p["category"]] else 1.0
            for p in products
        ]
        buyers = rng.choices(
            customers[:registered], weights=customer_weights[:registered], k=order_count
        )
        channels = _channel_weights(progress)
        discount_probability = (
            SALE_DISCOUNT_PROBABILITY if day.month in SALE_MONTHS else NORMAL_DISCOUNT_PROBABILITY
        )

        for customer in buyers:
            order_id = f"O{len(orders) + 1:07d}"
            orders.append(
                {
                    "order_id": order_id,
                    "order_date": day,
                    "customer_id": customer["customer_id"],
                    "channel": _pick(rng, channels),
                    "status": _pick(rng, STATUSES),
                }
            )
            item_count = rng.randint(1, MAX_ITEMS_PER_ORDER)
            for line_no, product in enumerate(
                rng.choices(products, weights=product_weights, k=item_count), start=1
            ):
                discount_rate = (
                    rng.choice(DISCOUNT_RATES) if rng.random() < discount_probability else 0.0
                )
                quantity = rng.choices([1, 2, 3], weights=[75, 20, 5])[0]
                order_items.append(
                    {
                        "order_id": order_id,
                        "line_no": line_no,
                        "product_id": product["product_id"],
                        "quantity": quantity,
                        "unit_price": product["unit_price"],
                        "discount_rate": discount_rate,
                        "amount": round(product["unit_price"] * quantity * (1 - discount_rate)),
                    }
                )
    return orders, order_items


def generate(seed: int) -> DemoData:
    rng = random.Random(seed)
    customers = generate_customers(rng)
    products = generate_products()
    orders, order_items = generate_orders(rng, customers, products)
    return DemoData(customers, products, orders, order_items)
