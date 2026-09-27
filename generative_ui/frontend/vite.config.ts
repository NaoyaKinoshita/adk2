import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

const RUNTIME_URL = process.env.RUNTIME_URL ?? "http://localhost:4000";

export default defineConfig({
  plugins: [react()],
  server: {
    // Copilot Runtime (server/runtime.mjs) へ中継する
    proxy: { "/api/copilotkit": RUNTIME_URL },
  },
});
