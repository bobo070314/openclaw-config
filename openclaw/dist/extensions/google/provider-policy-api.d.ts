import { f as ModelProviderConfig } from "../../types.models-Nc1Z-tAz.js";
import { Gc as ProviderThinkingProfile } from "../../types-C6Y8zGKi.js";
import { wt as ProviderDefaultThinkingPolicyContext } from "../../plugin-entry-BHVCZwwo.js";
//#region extensions/google/provider-policy-api.d.ts
declare function normalizeConfig(params: {
  provider: string;
  providerConfig: ModelProviderConfig;
}): ModelProviderConfig;
declare function resolveThinkingProfile(context: ProviderDefaultThinkingPolicyContext): ProviderThinkingProfile | undefined;
//#endregion
export { normalizeConfig, resolveThinkingProfile };