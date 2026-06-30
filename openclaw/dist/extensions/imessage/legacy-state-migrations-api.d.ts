import { i as OpenClawConfig } from "../../types.openclaw-BhmF31_h.js";
import { U as ChannelLegacyStateMigrationPlan } from "../../types.core-CrBFyVDB.js";
//#region extensions/imessage/src/state-migrations.d.ts
declare function detectIMessageLegacyStateMigrations(params: {
  cfg: OpenClawConfig;
  env: NodeJS.ProcessEnv;
  stateDir?: string;
}): Promise<ChannelLegacyStateMigrationPlan[]>;
//#endregion
export { detectIMessageLegacyStateMigrations };