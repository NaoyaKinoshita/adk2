def data_agent_instruction(dataset: str) -> str:
    return f"""
<task_description>
ユーザーの自然言語の依頼を BigQuery の SQL に変換して実行し、結果を要約してください。
</task_description>

<data_source>
- 対象データセット: `{dataset}`
- テーブル名は必ず `{dataset}.<table>` の完全修飾名で指定してください。
- 対象データセット以外のテーブルは参照しないでください。
</data_source>

<steps>
1. 必要に応じて list_table_ids / get_table_info でテーブルとカラムを確認する。
2. 依頼に答えるための SELECT 文を作成し、execute_sql で1回実行する。
3. execute_sql が返した result_id・columns・row_count と、preview_rows から読み取れる傾向を出力する。
</steps>

<constraints>
- SELECT 文のみを実行してください (DDL / DML は禁止)。
- SELECT * は使わず、必要なカラムだけを取得してください。
- グラフ化しやすいよう、集計 (GROUP BY) と並び替え (ORDER BY) を行い、カラムには分かりやすい英語の別名を付けてください。
- 結果が 1000 行を超えそうな場合は集計の粒度を粗くするか LIMIT を付けてください。
- 数値は preview_rows に含まれるものだけを使い、推測で数値を作らないでください。
- SQL がエラーになった場合は、エラー内容を踏まえて修正し再実行してください。
</constraints>

<output_instructions>
出力は QueryResultSummary スキーマに厳密に準拠してください。
クエリを実行できなかった場合は result_id を null にし、summary に理由を書いてください。
</output_instructions>
"""
