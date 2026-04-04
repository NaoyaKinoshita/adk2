# sequential_workflow

ランダムな都市名を生成し、その都市の現在時刻を報告する**シーケンシャルワークフロー**のサンプルです。

## ワークフロー

各ステップが順番に実行され、前のステップの出力が次のステップの入力になります。

```
START
  │
  ▼
city_generator_agent          # ランダムな都市名を生成 (str)
  │
  ▼
lookup_time_function          # 都市名を受け取り時刻情報を取得 (str → CityTime)
  │
  ▼
city_report_agent             # 時刻レポートを生成 (CityTime → str)
  │
  ▼
completed_message_function    # 完了メッセージを付加 (str → Event)
  │
  ▼
END
```

## 構成

```
agents/
├── agent.py                  # Workflow 定義 (エントリポイント)
├── models/
│   └── city_time.py          # CityTime: 都市名と時刻情報を持つスキーマ
├── subagents/
│   ├── city_generator.py     # ステップ1: 都市名生成エージェント
│   └── city_report.py        # ステップ3: 時刻レポートエージェント
└── tools/
    └── time_lookup.py        # ステップ2,4: 時刻取得・完了メッセージ関数
```

## 実行

```bash
source .venv/bin/activate
adk web sequential_workflow
```
