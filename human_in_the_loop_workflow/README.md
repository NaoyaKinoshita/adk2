# Human-in-the-Loop 観光プランナー

人間の入力をワークフローの途中に挟み、必要に応じてプランを調整・再生成する **Human-in-the-Loop** パターンのサンプルです。
`RequestInput` による入力待ち、ループ構造、および `ctx.state` を利用したセッション跨ぎの状態管理を実証します。

## ワークフロー

```mermaid
graph TD
    START --> request_city["request_city<br>(都市入力を待つ)"]
    request_city --> itinerary_agent["itinerary_agent<br>(プラン生成)"]
    itinerary_agent --> cache_itinerary["cache_itinerary<br>(状態に保存)"]
    cache_itinerary --> request_feedback["request_feedback<br>(FB入力を待つ)"]
    request_feedback --> feedback_router{"feedback_router<br>(分岐)"}
    
    feedback_router -- "やり直し" --> request_city
    feedback_router -- "OK / その他" --> build_finalize_input["build_finalize_input<br>(データ結合)"]
    
    build_finalize_input --> finalize_agent["finalize_agent<br>(最終調整)"]
    finalize_agent --> final_itinerary_message["final_itinerary_message<br>(確定表示)"]
    final_itinerary_message --> END["終了"]
```

## 主な機能と特徴

1. **ワークフローの一時停止 (`RequestInput`)**:
   - `yield RequestInput` を使用して、ユーザーが入力を終えるまで実行を一時停止します。
2. **状態管理 (`ctx.state`)**:
   - 途中で入力された都市名や生成されたプランをキャッシュし、ルーティング後の後続ノードで再利用します。
3. **動的ルーティング**:
   - ユーザーのフィードバック内容に応じて、最初からやり直すか、プランを確定させるかを動的に分岐させます。
4. **一貫したUIカード表示**:
   - Pydantic モデル (`Itinerary`) を出力スキーマに指定することで、ADK Web 上でリッチな情報カードを表示します。

## ディレクトリ構成

```
agents/
├── agent.py               # ワークフローのエッジ定義
├── prompts.py             # プロンプト・インストラクション
├── models/
│   └── itinerary.py       # 観光プランのデータ構造 (Pydantic)
├── subagents/
│   ├── itinerary.py       # 初期プラン生成エージェント
│   └── finalize.py        # 最終調整用エージェント
└── tools/
    ├── human_steps.py     # RequestInput を含むヒューマンステップ
    ├── router.py          # フィードバック内容に基づくルーティング
    └── cache.py           # 状態保存および最終メッセージ生成
```

## 実行方法

```bash
adk web human_in_the_loop_workflow
```
