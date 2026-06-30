import { Kc as ProviderRuntimeModel } from "../../types-C6Y8zGKi.js";
import { Kt as ProviderResolveDynamicModelContext } from "../../plugin-entry-BHVCZwwo.js";

//#region extensions/google/provider-models.d.ts
declare function resolveGoogleGeminiForwardCompatModel(params: {
  providerId: string;
  templateProviderId?: string;
  ctx: ProviderResolveDynamicModelContext;
}): ProviderRuntimeModel | undefined;
declare function isModernGoogleModel(modelId: string): boolean;
//#endregion
export { isModernGoogleModel, resolveGoogleGeminiForwardCompatModel };