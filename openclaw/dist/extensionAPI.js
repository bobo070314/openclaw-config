import "./agent-scope-CESPhp3L.js";
import { a as resolveAgentDir, o as resolveAgentWorkspaceDir } from "./agent-scope-config-ChfGvhEr.js";
import { n as DEFAULT_MODEL, r as DEFAULT_PROVIDER } from "./defaults-mDjiWzE5.js";
import { _ as updateSessionStoreEntry, g as updateSessionStore, m as saveSessionStore } from "./store-CWhnH-Ye.js";
import { i as resolveSessionFilePath, u as resolveStorePath } from "./paths-BcGVZo_k.js";
import { t as loadSessionStore } from "./store-load-S40KNQ3r.js";
import "./sessions-BoPlPkQh.js";
import { t as resolveThinkingDefault } from "./model-thinking-default-CJ6WM7K-.js";
import "./model-selection-60FiczuZ.js";
import { d as ensureAgentWorkspace } from "./workspace-KxGKSHoh.js";
import { t as resolveAgentTimeoutMs } from "./timeout-Drw0_zOv.js";
import { n as resolveAgentIdentity } from "./identity-Ds4isHGf.js";
import { t as runEmbeddedAgent } from "./embedded-agent-BgF2MOkH.js";
//#region src/extensionAPI.ts
if (process.env.VITEST !== "true" && process.env.OPENCLAW_SUPPRESS_EXTENSION_API_WARNING !== "1") process.emitWarning("openclaw/extension-api is deprecated. Migrate to api.runtime.agent.* or focused openclaw/plugin-sdk/<subpath> imports. See https://docs.openclaw.ai/plugins/sdk-migration", {
	code: "OPENCLAW_EXTENSION_API_DEPRECATED",
	detail: "This compatibility bridge is temporary. Bundled plugins should use the injected plugin runtime instead of importing host-side agent helpers directly. Migration guide: https://docs.openclaw.ai/plugins/sdk-migration"
});
//#endregion
export { DEFAULT_MODEL, DEFAULT_PROVIDER, ensureAgentWorkspace, loadSessionStore, resolveAgentDir, resolveAgentIdentity, resolveAgentTimeoutMs, resolveAgentWorkspaceDir, resolveSessionFilePath, resolveStorePath, resolveThinkingDefault, runEmbeddedAgent, runEmbeddedAgent as runEmbeddedPiAgent, saveSessionStore, updateSessionStore, updateSessionStoreEntry };
