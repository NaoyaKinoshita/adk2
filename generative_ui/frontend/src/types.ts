import { z } from "zod";

// バックエンドの ui_agent/models/chart.py (ChartSpec) と揃える
export const chartSpecSchema = z.object({
  chart_type: z.enum(["bar", "line", "area", "pie", "table"]),
  title: z.string(),
  result_id: z.string(),
  x_key: z.string().nullable(),
  y_keys: z.array(z.string()),
});

export type ChartSpec = z.infer<typeof chartSpecSchema>;

export type Row = Record<string, unknown>;

// バックエンドの data_agent/callbacks.py が state に保存する形
export interface QueryResult {
  query: string;
  columns: string[];
  rows: Row[];
  truncated: boolean;
}

export const QUERY_RESULT_STATE_PREFIX = "query_result:";
