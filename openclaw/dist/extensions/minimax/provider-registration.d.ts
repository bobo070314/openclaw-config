import { cn as ProviderPlugin } from "../../types-C6Y8zGKi.js";
import { g as OpenClawPluginApi } from "../../plugin-entry-BHVCZwwo.js";
//#region extensions/minimax/provider-registration.d.ts
declare function buildMinimaxApiProviderPlugin(): ProviderPlugin;
declare function buildMinimaxPortalProviderPlugin(): ProviderPlugin;
declare function registerMinimaxProviders(api: OpenClawPluginApi): void;
//#endregion
export { buildMinimaxApiProviderPlugin, buildMinimaxPortalProviderPlugin, registerMinimaxProviders };