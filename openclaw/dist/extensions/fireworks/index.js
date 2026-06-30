import "../../defaults-mDjiWzE5.js";
import { a as normalizeModelCompat } from "../../provider-model-compat-AbDhi5c3.js";
import { r as OPENAI_COMPATIBLE_REPLAY_HOOKS, u as cloneFirstTemplateModel } from "../../provider-model-shared-CKFakuj-.js";
import { t as defineSingleProviderPluginEntry } from "../../provider-entry-BhS0gICf.js";
import { t as isFireworksKimiModelId } from "../../model-id-BhN5iHky.js";
import { n as FIREWORKS_DEFAULT_CONTEXT_WINDOW, o as buildFireworksProvider, r as FIREWORKS_DEFAULT_MAX_TOKENS, s as isFireworksCatalogModelId, t as FIREWORKS_BASE_URL } from "../../provider-catalog-CmIwITKE.js";
import { n as applyFireworksConfig, t as FIREWORKS_DEFAULT_MODEL_REF } from "../../onboard-DLU5AQha.js";
import { n as wrapFireworksProviderStream } from "../../stream-lVb6VATb.js";
import { t as resolveFireworksThinkingProfile } from "../../thinking-policy-D67HZmJf.js";
//#region extensions/fireworks/index.ts
const PROVIDER_ID = "fireworks";
function isFireworksGlmModelId(modelId) {
	const normalized = modelId.trim().toLowerCase();
	const lastSegment = normalized.split("/").pop() ?? normalized;
	return /^glm[-_.]/.test(lastSegment);
}
function resolveFireworksDynamicInput(modelId) {
	return isFireworksGlmModelId(modelId) ? ["text"] : ["text", "image"];
}
function resolveFireworksDynamicModel(ctx) {
	const modelId = ctx.modelId.trim();
	if (!modelId) return;
	if (isFireworksCatalogModelId(modelId)) return;
	const isKimiModel = isFireworksKimiModelId(modelId);
	const input = resolveFireworksDynamicInput(modelId);
	return cloneFirstTemplateModel({
		providerId: PROVIDER_ID,
		modelId,
		templateIds: ["accounts/fireworks/routers/kimi-k2p5-turbo"],
		ctx,
		patch: {
			provider: PROVIDER_ID,
			reasoning: !isKimiModel,
			input
		}
	}) ?? normalizeModelCompat({
		id: modelId,
		name: modelId,
		provider: PROVIDER_ID,
		api: "openai-completions",
		baseUrl: FIREWORKS_BASE_URL,
		reasoning: !isKimiModel,
		input,
		cost: {
			input: 0,
			output: 0,
			cacheRead: 0,
			cacheWrite: 0
		},
		contextWindow: FIREWORKS_DEFAULT_CONTEXT_WINDOW,
		maxTokens: FIREWORKS_DEFAULT_MAX_TOKENS || 2e5
	});
}
var fireworks_default = defineSingleProviderPluginEntry({
	id: PROVIDER_ID,
	name: "Fireworks Provider",
	description: "Bundled Fireworks AI provider plugin",
	provider: {
		label: "Fireworks",
		aliases: ["fireworks-ai"],
		docsPath: "/providers/fireworks",
		auth: [{
			methodId: "api-key",
			label: "Fireworks API key",
			hint: "API key",
			optionKey: "fireworksApiKey",
			flagName: "--fireworks-api-key",
			envVar: "FIREWORKS_API_KEY",
			promptMessage: "Enter Fireworks API key",
			defaultModel: FIREWORKS_DEFAULT_MODEL_REF,
			applyConfig: (cfg) => applyFireworksConfig(cfg)
		}],
		catalog: {
			buildProvider: buildFireworksProvider,
			allowExplicitBaseUrl: true
		},
		...OPENAI_COMPATIBLE_REPLAY_HOOKS,
		wrapStreamFn: wrapFireworksProviderStream,
		resolveThinkingProfile: ({ modelId }) => resolveFireworksThinkingProfile(modelId),
		resolveDynamicModel: (ctx) => resolveFireworksDynamicModel(ctx),
		isModernModelRef: () => true
	}
});
//#endregion
export { fireworks_default as default };
