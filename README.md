# Google ADK 2.0 検証プロジェクト (adk2)

Google ADK 2.0 (Agent Development Kit) の検証用リポジトリ。
Vertex AI (Gemini) を使用した様々なマルチエージェント・ワークフローのサンプルを収録しています。

## ワークフロー・サンプル

各ディレクトリに、それぞれのパターンの実装が含まれています。

1. **[sequential_workflow](./sequential_workflow/)**: 
   - 複数のノードを一本道で繋ぐ、最も基本的な逐次実行ワークフロー。
2. **[parallel_workflow](./parallel_workflow/)**: 
   - 複数の処理を並列に実行し、結果を最終的に集約するワークフロー。
3. **[nested_workflow](./nested_workflow/)**: 
   - ワークフローの中から別のワークフローを呼び出す、階層構造を持つワークフロー。
4. **[graph_workflow](./graph_workflow/)**: 
   - ループや複雑な分岐を含む、グラフベースの高度なルーティング・ワークフロー。
5. **[human_in_the_loop_workflow](./human_in_the_loop_workflow/)**: 
   - ユーザーのフィードバックを求め、その内容を反映して再生成したり確定したりする、人間が介在するワークフロー。

## セットアップ

### 前提条件

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (推奨) または pip
- Google Cloud プロジェクト (Vertex AI / Model Garden が有効)

### インストール・認証

```bash
# 依存関係のインストール
uv sync

# 認証設定
gcloud auth application-default login
```

## 実行方法

ADK Web を使用して、各ワークフローをブラウザ上で実行・確認できます。

```bash
# 例: Human-in-the-Loop ワークフローを起動
adk web human_in_the_loop_workflow
```

各ディレクトリ内の `README.md` に、それぞれのワークフローのより詳細な仕様が記載されています。
