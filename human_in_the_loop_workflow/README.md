# human_in_the_loop_workflow

人間の入力をワークフローの途中に挟む **Human-in-the-Loop** パターンのサンプルです。
`RequestInput` を `yield` することでワークフローを一時停止し、ユーザーからの入力を待ちます。

参考: https://adk.dev/workflows/human-input/

## ワークフロー

```
START
  │
  ▼
request_city        # [human input] 観光したい都市名を入力させる
  │
  ▼
itinerary_agent     # 入力された都市の観光プランを生成 (→ Itinerary)
  │
  ▼
request_feedback    # [human input] プランを提示し、フィードバックを求める
  │
  ▼
finalize_agent      # フィードバックを反映した最終プランを生成 (→ str)
```

## RequestInput の仕組み

`async` 関数の中で `RequestInput` を `yield` するとワークフローが一時停止し、ユーザーの入力を待ちます。

```python
from google.adk.events import RequestInput

async def request_city(node_input: str):
    yield RequestInput(
        message="観光したい都市名を入力してください:",
        response_schema={"city": str},
    )
```

`payload` を渡すと、ユーザーに構造化データを提示した上でフィードバックを求められます:

```python
async def request_feedback(node_input: Itinerary):
    yield RequestInput(
        message="以下のプランを確認してください:\n...",
        payload=node_input,
        response_schema={"feedback": str},
    )
```

## 構成

```
agents/
├── agent.py                  # Workflow 定義 (エントリポイント)
├── prompts.py                # 各エージェントの instruction 関数
├── models/
│   └── itinerary.py          # Itinerary スキーマ
├── subagents/
│   ├── itinerary.py          # ステップ2: 観光プラン生成エージェント
│   └── finalize.py           # ステップ4: 最終プラン生成エージェント
└── tools/
    └── human_steps.py        # ステップ1,3: RequestInput 関数
```

## 実行

```bash
source .venv/bin/activate
adk web human_in_the_loop_workflow
```
