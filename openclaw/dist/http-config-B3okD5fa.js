import { c as normalizeOptionalString } from "./string-coerce-DW4mBlAt.js";
import { p as resolveProviderHttpRequestConfig } from "./shared-BO9QPTqO.js";
import "./string-coerce-runtime-BtLK_KtO.js";
import { a as resolveApiKeyForProvider } from "./provider-auth-runtime-D0_G_kOZ.js";
import "./provider-http-b4uHLlJ1.js";
//#region extensions/fal/http-config.ts
const DEFAULT_FAL_BASE_URL = "https://fal.run";
function resolveFalConfiguredBaseUrl(cfg) {
	return normalizeOptionalString(cfg?.models?.providers?.fal?.baseUrl);
}
async function resolveFalHttpRequestConfig(params) {
	const auth = await resolveApiKeyForProvider({
		provider: "fal",
		cfg: params.req.cfg,
		agentDir: params.req.agentDir,
		store: params.req.authStore
	});
	if (!auth.apiKey) throw new Error("fal API key missing");
	return resolveProviderHttpRequestConfig({
		baseUrl: params.baseUrl ?? resolveFalConfiguredBaseUrl(params.req.cfg),
		defaultBaseUrl: DEFAULT_FAL_BASE_URL,
		allowPrivateNetwork: false,
		defaultHeaders: {
			Authorization: `Key ${auth.apiKey}`,
			"Content-Type": "application/json"
		},
		provider: "fal",
		capability: params.capability,
		transport: "http"
	});
}
//#endregion
export { resolveFalHttpRequestConfig as t };
