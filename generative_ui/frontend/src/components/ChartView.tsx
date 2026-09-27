import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { ChartSpec, Row } from "../types";

const COLORS = ["#2563eb", "#16a34a", "#ea580c", "#9333ea", "#0891b2", "#dc2626"];
const CHART_HEIGHT = 320;
const MAX_TABLE_ROWS = 100;

// BigQuery の NUMERIC 等は文字列で返るため、描画用に数値へ変換する
function toChartRows(rows: Row[], yKeys: string[]): Row[] {
  return rows.map((row) => {
    const converted: Row = { ...row };
    for (const key of yKeys) {
      const value = Number(row[key]);
      converted[key] = Number.isFinite(value) ? value : null;
    }
    return converted;
  });
}

function DataTable({ columns, rows }: { columns: string[]; rows: Row[] }) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column}>{column}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.slice(0, MAX_TABLE_ROWS).map((row, i) => (
            <tr key={i}>
              {columns.map((column) => (
                <td key={column}>{String(row[column] ?? "")}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function ChartView({
  spec,
  columns,
  rows,
}: {
  spec: ChartSpec;
  columns: string[];
  rows: Row[];
}) {
  if (spec.chart_type === "table" || !spec.x_key) {
    return <DataTable columns={columns} rows={rows} />;
  }

  const xKey = spec.x_key;
  const data = toChartRows(rows, spec.y_keys);

  if (spec.chart_type === "pie") {
    const valueKey = spec.y_keys[0];
    return (
      <ResponsiveContainer width="100%" height={CHART_HEIGHT}>
        <PieChart>
          <Pie data={data} dataKey={valueKey} nameKey={xKey} outerRadius="80%" label>
            {data.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    );
  }

  const axes = (
    <>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey={xKey} />
      <YAxis />
      <Tooltip />
      <Legend />
    </>
  );

  return (
    <ResponsiveContainer width="100%" height={CHART_HEIGHT}>
      {spec.chart_type === "line" ? (
        <LineChart data={data}>
          {axes}
          {spec.y_keys.map((key, i) => (
            <Line key={key} dataKey={key} stroke={COLORS[i % COLORS.length]} dot={false} />
          ))}
        </LineChart>
      ) : spec.chart_type === "area" ? (
        <AreaChart data={data}>
          {axes}
          {spec.y_keys.map((key, i) => (
            <Area
              key={key}
              dataKey={key}
              stackId="stack"
              stroke={COLORS[i % COLORS.length]}
              fill={COLORS[i % COLORS.length]}
            />
          ))}
        </AreaChart>
      ) : (
        <BarChart data={data}>
          {axes}
          {spec.y_keys.map((key, i) => (
            <Bar key={key} dataKey={key} fill={COLORS[i % COLORS.length]} />
          ))}
        </BarChart>
      )}
    </ResponsiveContainer>
  );
}
