import { i as OpenClawConfig } from "./types.openclaw-CXiJ86ZN.js";
import { cc as GenerateImageParams, lc as GenerateImageRuntimeResult } from "./types-B70zVumi.js";
import { t as SubsystemLogger } from "./subsystem-n4Y4vCcQ.js";
import { n as getProviderEnvVars } from "./provider-env-vars-Ds4p-9h7.js";
import { l as ImageGenerationProvider } from "./types-DQfRKZ5p.js";
import { n as listImageGenerationProviders, t as getImageGenerationProvider } from "./provider-registry-Bfb5Ke7i.js";

//#region src/image-generation/runtime.d.ts
declare const log: SubsystemLogger;
/** Dependency seam used by image-generation runtime tests and plugin host callers. */
type ImageGenerationRuntimeDeps = {
  getProvider?: typeof getImageGenerationProvider;
  listProviders?: typeof listImageGenerationProviders;
  getProviderEnvVars?: typeof getProviderEnvVars;
  log?: Pick<typeof log, "warn">;
};
/** Lists image-generation providers visible for the current config. */
declare function listRuntimeImageGenerationProviders(params?: {
  config?: OpenClawConfig;
}, deps?: ImageGenerationRuntimeDeps): ImageGenerationProvider[];
declare function generateImage(params: GenerateImageParams, deps?: ImageGenerationRuntimeDeps): Promise<GenerateImageRuntimeResult>;
//#endregion
export { type GenerateImageParams, type GenerateImageRuntimeResult, generateImage, listRuntimeImageGenerationProviders };