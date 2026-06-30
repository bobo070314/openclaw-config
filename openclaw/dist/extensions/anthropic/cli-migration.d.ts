import { i as OpenClawConfig } from "../../types.openclaw-BhmF31_h.js";
import { jt as ProviderAuthResult } from "../../types-C6Y8zGKi.js";
import { n as readClaudeCliCredentialsForSetup } from "../../cli-auth-seam-B2l-su4H.js";
//#region extensions/anthropic/cli-migration.d.ts
type ClaudeCliCredential = NonNullable<ReturnType<typeof readClaudeCliCredentialsForSetup>>;
/** Build the config migration result for adopting Claude CLI-backed Anthropic defaults. */
declare function buildAnthropicCliMigrationResult(config: OpenClawConfig, credential?: ClaudeCliCredential | null): ProviderAuthResult;
//#endregion
export { buildAnthropicCliMigrationResult };