import { useAgent, UseAgentUpdate } from "@copilotkit/react-core/v2";

import { type ChartSpec, type QueryResult, QUERY_RESULT_STATE_PREFIX } from "../types";
import { ChartView } from "./ChartView";

interface Props {
  status: "inProgress" | "executing" | "complete";
  parameters: Partial<ChartSpec>;
  result?: string;
}

// render_chart ツール呼び出しをチャートとしてチャット内に描画する
export function ChartToolCall({ status, parameters, result }: Props) {
  // 行データはツール引数ではなく、AG-UI の state (query_result:<id>) から受け取る
  const { agent } = useAgent({ updates: [UseAgentUpdate.OnStateChanged] });

  if (status === "inProgress" || !parameters.result_id || !parameters.chart_type) {
    return <div className="chart-card muted">チャートを準備しています…</div>;
  }

  // バックエンドの検証でエラーになった呼び出し (LLM が引数を直して再実行する) は表示しない
  if (status === "complete" && result && parseStatus(result) === "ERROR") {
    return null;
  }

  const state = (agent.state ?? {}) as Record<string, unknown>;
  const queryResult = state[`${QUERY_RESULT_STATE_PREFIX}${parameters.result_id}`] as
    | QueryResult
    | undefined;
  if (!queryResult) {
    return <div className="chart-card muted">データを読み込んでいます…</div>;
  }

  const spec: ChartSpec = {
    chart_type: parameters.chart_type,
    title: parameters.title ?? "",
    result_id: parameters.result_id,
    x_key: parameters.x_key ?? null,
    y_keys: parameters.y_keys ?? [],
  };

  return (
    <div className="chart-card">
      <div className="chart-title">{spec.title}</div>
      <ChartView spec={spec} columns={queryResult.columns} rows={queryResult.rows} />
      <details className="chart-meta">
        <summary>
          {queryResult.rows.length} 行{queryResult.truncated ? " (上限で打ち切り)" : ""} / SQL
        </summary>
        <pre>{queryResult.query}</pre>
      </details>
    </div>
  );
}

function parseStatus(result: string): string | undefined {
  try {
    return (JSON.parse(result) as { status?: string }).status;
  } catch {
    return undefined;
  }
}
