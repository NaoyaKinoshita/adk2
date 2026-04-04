# graph_workflow

トピックに応じて処理を分岐する**グラフルートワークフロー**のサンプルです。
ルーター関数の戻り値によって実行ブランチを動的に切り替えます。

参考: https://adk.dev/workflows/graph-routes/

## ワークフロー

```
START
  │
  ▼
topic_generator_agent        # ランダムなトピックを選択 ("sports" or "tech")
  │
  ▼
topic_router                 # トピックに応じてルーティング
  │
  ├─── RUN_SPORTS_AGENT ───▶ sports_agent   # スポーツニュースの見出しを生成
  │
  └─── RUN_TECH_AGENT ─────▶ tech_agent     # テックニュースの見出しを生成
```

`topic_router` が返す `Event(route="...")` の値によって、どちらのブランチを実行するかが決定されます。

## ルーティングの仕組み

```python
def topic_router(node_input: str) -> Event:
    if "sport" in node_input:
        return Event(route="RUN_SPORTS_AGENT")
    else:
        return Event(route="RUN_TECH_AGENT")
```

`Workflow` の `edges` で分岐先をディクショナリとして定義します:

```python
(
    topic_router,
    {
        "RUN_SPORTS_AGENT": sports_agent,
        "RUN_TECH_AGENT": tech_agent,
    },
)
```

## 構成

```
agents/
├── agent.py                 # Workflow 定義 (エントリポイント)
├── models/
│   └── article.py           # Article スキーマ
├── subagents/
│   ├── topic_generator.py   # ステップ1: トピック生成エージェント
│   ├── sports.py            # ブランチA: スポーツエージェント
│   └── tech.py              # ブランチB: テックエージェント
└── tools/
    └── router.py            # ルーター関数
```

## 実行

```bash
uv run adk web graph_workflow/agents/
```
