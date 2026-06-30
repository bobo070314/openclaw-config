import { i as OpenClawConfig } from "./types.openclaw-BhmF31_h.js";
import { lc as GenerateVideoParams, uc as GenerateVideoRuntimeResult } from "./types-C6Y8zGKi.js";
import { t as SubsystemLogger } from "./subsystem-CfQVin8T.js";
import { n as getProviderEnvVars } from "./provider-env-vars-ApHcVNnG.js";
import { s as VideoGenerationProvider } from "./types-C1lgmnxf.js";
import { n as listVideoGenerationProviders, t as getVideoGenerationProvider } from "./provider-registry-BtQvkqWO.js";

//#region src/video-generation/runtime.d.ts
declare const log: SubsystemLogger;
type VideoGenerationRuntimeDeps = {
  getProvider?: typeof getVideoGenerationProvider;
  listProviders?: typeof listVideoGenerationProviders;
  getProviderEnvVars?: typeof getProviderEnvVars;
  log?: Pick<typeof log, "debug" | "warn">;
};
declare function listRuntimeVideoGenerationProviders(params?: {
  config?: OpenClawConfig;
}, deps?: VideoGenerationRuntimeDeps): VideoGenerationProvider[];
declare function generateVideo(params: GenerateVideoParams, deps?: VideoGenerationRuntimeDeps): Promise<GenerateVideoRuntimeResult>;
//#endregion
export { listRuntimeVideoGenerationProviders as n, generateVideo as t };