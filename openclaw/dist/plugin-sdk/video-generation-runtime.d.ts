import { i as OpenClawConfig } from "./types.openclaw-CXiJ86ZN.js";
import { oc as GenerateVideoParams, sc as GenerateVideoRuntimeResult } from "./types-B70zVumi.js";
import { t as SubsystemLogger } from "./subsystem-n4Y4vCcQ.js";
import { n as getProviderEnvVars } from "./provider-env-vars-Ds4p-9h7.js";
import { s as VideoGenerationProvider } from "./types-PF_3icEY.js";
import { n as listVideoGenerationProviders, t as getVideoGenerationProvider } from "./provider-registry-CvYxe_s1.js";

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
export { type GenerateVideoParams, type GenerateVideoRuntimeResult, generateVideo, listRuntimeVideoGenerationProviders };