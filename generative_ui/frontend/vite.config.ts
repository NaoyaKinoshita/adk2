import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// localhost は環境によって IPv6 (::1) に解決され接続できないため、IPv4 を明示する
const RUNTIME_URL = process.env.RUNTIME_URL ?? "http://127.0.0.1:4000";

export default defineConfig({
  plugins: [react()],
  server: {
    // Copilot Runtime (server/runtime.mjs) へ中継する
    proxy: { "/api/copilotkit": RUNTIME_URL },
  },
});
