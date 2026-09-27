import { CopilotChat, CopilotKit, useRenderTool } from "@copilotkit/react-core/v2";

import { ChartToolCall } from "./components/ChartToolCall";
import { chartSpecSchema } from "./types";

const RUNTIME_URL = "/api/copilotkit";
// 開発用 Inspector を表示したい場合は VITE_ENABLE_INSPECTOR=true で起動する
const ENABLE_INSPECTOR = import.meta.env.VITE_ENABLE_INSPECTOR === "true";

function Chat() {
  useRenderTool(
    {
      name: "render_chart",
      parameters: chartSpecSchema,
      render: (props) => <ChartToolCall {...props} />,
    },
    [],
  );

  return <CopilotChat className="chat" />;
}

export default function App() {
  return (
    <CopilotKit runtimeUrl={RUNTIME_URL} enableInspector={ENABLE_INSPECTOR}>
      <main className="layout">
        <h1>Generative UI PoC (ADK × BigQuery)</h1>
        <Chat />
      </main>
    </CopilotKit>
  );
}
