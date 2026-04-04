# nested_workflow

ルーティングで分岐し、各ブランチを**子ワークフロー**として実行する**ネストワークフロー**のサンプルです。
子ワークフローは親ワークフローのノードとして扱われ、複雑なロジックをカプセル化できます。

参考: https://adk.dev/workflows/graph-routes/

## ワークフロー

```
START
  │
  ▼
topic_generator_agent          # トピックを生成 ("sports" or "tech")
  │
  ▼
topic_router                   # トピックに応じて子ワークフローへルーティング
  │
  ├─── RUN_SPORTS_WORKFLOW ───▶ sports_workflow
  │                               │
  │                               ├─▶ sports_headline_agent  # 見出し生成
  │                               └─▶ sports_report_agent    # 記事生成
  │
  └─── RUN_TECH_WORKFLOW ─────▶ tech_workflow
                                  │
                                  ├─▶ tech_headline_agent    # 見出し生成
                                  └─▶ tech_report_agent      # 記事生成
```

各ブランチの内部も `Workflow` として定義されており、独立して再利用できます。

## 子ワークフローの定義

```python
sports_workflow = Workflow(
    name="sports_workflow",
    edges=[("START", sports_headline_agent, sports_report_agent)],
)
```

親ワークフローでは通常のノードと同様にブランチ先として指定します:

```python
(
    topic_router,
    {
        "RUN_SPORTS_WORKFLOW": sports_workflow,
        "RUN_TECH_WORKFLOW": tech_workflow,
    },
)
```

## 構成

```
agents/
├── agent.py                   # 親 Workflow 定義 (エントリポイント)
├── prompts.py                 # 各エージェントの instruction 関数
├── models/
│   └── article.py             # Article スキーマ
├── subagents/
│   ├── topic_generator.py     # トピック生成エージェント
│   ├── sports_headline.py     # スポーツ見出し生成エージェント
│   ├── sports_report.py       # スポーツ記事生成エージェント
│   ├── tech_headline.py       # テック見出し生成エージェント
│   └── tech_report.py         # テック記事生成エージェント
├── tools/
│   └── router.py              # ルーター関数
└── workflows/
    ├── sports.py              # 子ワークフロー: sports_workflow
    └── tech.py                # 子ワークフロー: tech_workflow
```

## 実行

```bash
source .venv/bin/activate
adk web nested_workflow
```
