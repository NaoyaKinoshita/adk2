from pydantic import BaseModel, Field


class QueryResultSummary(BaseModel):
    result_id: str | None = Field(
        description="execute_sql が返した result_id。クエリを実行できなかった場合は null"
    )
    columns: list[str] = Field(description="結果のカラム名 (SELECT 順)")
    row_count: int = Field(description="結果の行数")
    summary: str = Field(description="取得したデータの説明と主な傾向 (日本語で1〜3文)")
