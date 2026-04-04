# adk2

Google ADK 2.0 の検証プロジェクト。Vertex AI (Gemini) を使ったマルチエージェント・ワークフローのサンプルです。

## 構成

```
sequential_workflow/        # ワークフロー定義
├── agent.py               # エントリポイント (root_agent)
├── models/
│   └── city_time.py       # CityTime Pydantic モデル
├── subagents/
│   ├── city_generator.py  # ランダムな都市名を生成するエージェント
│   └── city_report.py     # 都市の現在時刻を報告するエージェント
└── tools/
    └── time_lookup.py     # 時刻取得・完了メッセージ関数
```

### ワークフロー概要

```
START
  → city_generator_agent   # ランダムな都市名を返す
  → lookup_time_function   # 都市の現在時刻を取得
  → city_report_agent      # 時刻レポートを生成
  → completed_message_function
```

## セットアップ

### 前提条件

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- Google Cloud プロジェクト (Vertex AI が有効)

### インストール

```bash
uv sync
```

### 認証

```bash
gcloud auth application-default login
```

### 環境変数

[sequential_workflow/.env](sequential_workflow/.env) に以下が設定されています:

```env
GOOGLE_CLOUD_PROJECT=<your-project-id>
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=True
```

## 実行

```bash
uv run adk run sequential_workflow/
```
