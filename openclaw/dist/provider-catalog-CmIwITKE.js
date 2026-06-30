import { n as buildManifestModelProviderConfig } from "./provider-catalog-shared-DOIVdnKn.js";
//#region extensions/fireworks/openclaw.plugin.json
var modelCatalog = {
	"providers": { "fireworks": {
		"baseUrl": "https://api.fireworks.ai/inference/v1",
		"api": "openai-completions",
		"models": [{
			"id": "accounts/fireworks/models/kimi-k2p6",
			"name": "Kimi K2.6",
			"reasoning": false,
			"input": ["text", "image"],
			"contextWindow": 262144,
			"maxTokens": 262144,
			"cost": {
				"input": .95,
				"output": 4,
				"cacheRead": 0,
				"cacheWrite": 0
			}
		}, {
			"id": "accounts/fireworks/routers/kimi-k2p5-turbo",
			"name": "Kimi K2.5 Turbo (Fire Pass)",
			"reasoning": false,
			"input": ["text", "image"],
			"contextWindow": 256e3,
			"maxTokens": 256e3,
			"compat": { "unsupportedToolSchemaKeywords": ["not"] },
			"cost": {
				"input": 0,
				"output": 0,
				"cacheRead": 0,
				"cacheWrite": 0
			}
		}]
	} },
	"discovery": { "fireworks": "static" }
};
//#endregion
//#region extensions/fireworks/provider-catalog.ts
const FIREWORKS_MANIFEST_PROVIDER = buildManifestModelProviderConfig({
	providerId: "fireworks",
	catalog: modelCatalog.providers.fireworks
});
const FIREWORKS_BASE_URL = FIREWORKS_MANIFEST_PROVIDER.baseUrl;
const FIREWORKS_DEFAULT_MODEL_ID = "accounts/fireworks/routers/kimi-k2p5-turbo";
function requireFireworksManifestModel(id) {
	const model = FIREWORKS_MANIFEST_PROVIDER.models.find((entry) => entry.id === id);
	if (!model) throw new Error(`Missing Fireworks modelCatalog row ${id}`);
	return model;
}
const FIREWORKS_DEFAULT_MODEL = requireFireworksManifestModel(FIREWORKS_DEFAULT_MODEL_ID);
const FIREWORKS_DEFAULT_CONTEXT_WINDOW = FIREWORKS_DEFAULT_MODEL.contextWindow;
const FIREWORKS_DEFAULT_MAX_TOKENS = FIREWORKS_DEFAULT_MODEL.maxTokens;
function isFireworksCatalogModelId(modelId) {
	return FIREWORKS_MANIFEST_PROVIDER.models.some((model) => model.id === modelId);
}
function buildFireworksCatalogModels() {
	return FIREWORKS_MANIFEST_PROVIDER.models.map((model) => structuredClone(model));
}
function buildFireworksProvider() {
	return buildManifestModelProviderConfig({
		providerId: "fireworks",
		catalog: modelCatalog.providers.fireworks
	});
}
//#endregion
export { buildFireworksCatalogModels as a, FIREWORKS_DEFAULT_MODEL_ID as i, FIREWORKS_DEFAULT_CONTEXT_WINDOW as n, buildFireworksProvider as o, FIREWORKS_DEFAULT_MAX_TOKENS as r, isFireworksCatalogModelId as s, FIREWORKS_BASE_URL as t };
