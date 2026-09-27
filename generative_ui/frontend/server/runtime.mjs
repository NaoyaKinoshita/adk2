// Copilot Runtime: ブラウザ (CopilotKit) と ADK の AG-UI エンドポイントを中継する
import { createServer } from "node:http";

import { HttpAgent } from "@ag-ui/client";
import { CopilotRuntime } from "@copilotkit/runtime/v2";
import { createCopilotNodeListener } from "@copilotkit/runtime/v2/node";

const AGENT_URL = process.env.AGENT_URL ?? "http://localhost:8000/";
// CopilotKit の匿名テレメトリを止める場合は COPILOTKIT_TELEMETRY_DISABLED=true を設定する
const PORT = Number(process.env.RUNTIME_PORT ?? 4000);
const BASE_PATH = "/api/copilotkit";

const runtime = new CopilotRuntime({
  agents: { default: new HttpAgent({ url: AGENT_URL }) },
});

createServer(createCopilotNodeListener({ runtime, basePath: BASE_PATH })).listen(
  PORT,
  () => console.log(`Copilot Runtime: http://localhost:${PORT}${BASE_PATH} -> ${AGENT_URL}`),
);
