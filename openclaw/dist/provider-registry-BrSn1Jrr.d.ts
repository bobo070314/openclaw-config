import { i as OpenClawConfig } from "./types.openclaw-BhmF31_h.js";
import { a as ImageGenerationProviderPlugin } from "./types-C6Y8zGKi.js";

//#region src/image-generation/provider-registry.d.ts
/** Lists canonical image-generation providers visible for config. */
declare function listImageGenerationProviders(cfg?: OpenClawConfig): ImageGenerationProviderPlugin[];
/** Resolves an image-generation provider by canonical id or alias. */
declare function getImageGenerationProvider(providerId: string | undefined, cfg?: OpenClawConfig): ImageGenerationProviderPlugin | undefined;
//#endregion
export { listImageGenerationProviders as n, getImageGenerationProvider as t };