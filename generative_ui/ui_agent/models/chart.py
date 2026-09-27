from typing import Literal

from pydantic import BaseModel, Field, model_validator

ChartType = Literal["bar", "line", "area", "pie", "table"]


class ChartSpec(BaseModel):
    chart_type: ChartType
    title: str = Field(min_length=1)
    result_id: str = Field(min_length=1)
    # 横軸 (pie はラベル) に使うカラム。table では未使用
    x_key: str | None = None
    # 縦軸 (pie は値) に使う数値カラム。table では未使用
    y_keys: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _check_keys(self) -> "ChartSpec":
        if self.chart_type == "table":
            return self
        if not self.x_key:
            raise ValueError(f"{self.chart_type} には x_key が必要です")
        if not self.y_keys:
            raise ValueError(f"{self.chart_type} には y_keys が1つ以上必要です")
        if self.chart_type == "pie" and len(self.y_keys) != 1:
            raise ValueError("pie の y_keys は1つだけ指定してください")
        return self

    def missing_columns(self, columns: list[str]) -> list[str]:
        """
        結果に存在しないカラム名を返す
        """
        if self.chart_type == "table":
            return []
        requested = [self.x_key, *self.y_keys]
        return [_key for _key in requested if _key not in columns]
