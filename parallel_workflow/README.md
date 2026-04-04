# parallel_workflow

3つのエージェントを**並列実行**し、JoinNode で結果を集約してからサマリーを生成する**パラレルワークフロー**のサンプルです。

参考: https://adk.dev/workflows/graph-routes/

## ワークフロー

```
START
  ├──▶ sports_agent  ──┐
  ├──▶ tech_agent    ──┼──▶ join_node ──▶ summary_agent
  └──▶ science_agent ──┘
```

`join_node` はすべての上流タスクが完了するまで待機し、まとめて次のノードへ渡します。

## JoinNode の仕組み

```python
from google.adk.workflow import JoinNode

join_node = JoinNode(name="join_node")

edges=[
    ("START", sports_agent, join_node),
    ("START", tech_agent,   join_node),
    ("START", science_agent, join_node),
    (join_node, summary_agent),
]
```

## 構成

```
agents/
├── agent.py              # Workflow 定義 (エントリポイント)
├── prompts.py            # 各エージェントの instruction 関数
├── models/
│   └── headlines.py      # Headlines スキーマ
├── subagents/
│   ├── sports.py         # 並列ブランチA: スポーツニュース生成
│   ├── tech.py           # 並列ブランチB: テックニュース生成
│   ├── science.py        # 並列ブランチC: サイエンスニュース生成
│   └── summary.py        # 集約後: サマリー生成
└── tools/
    └── join.py           # JoinNode インスタンス
```

## 実行

```bash
source .venv/bin/activate
adk web parallel_workflow
```
