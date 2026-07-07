import { s as ModelDefinitionConfig } from "./types.models-Nc1Z-tAz.js";
//#region extensions/vercel-ai-gateway/models.d.ts
declare const VERCEL_AI_GATEWAY_PROVIDER_ID = "vercel-ai-gateway";
declare const VERCEL_AI_GATEWAY_BASE_URL = "https://ai-gateway.vercel.sh";
declare const VERCEL_AI_GATEWAY_DEFAULT_MODEL_ID = "anthropic/claude-opus-4.6";
declare const VERCEL_AI_GATEWAY_DEFAULT_CONTEXT_WINDOW = 200000;
declare const VERCEL_AI_GATEWAY_DEFAULT_MAX_TOKENS = 128000;
declare const VERCEL_AI_GATEWAY_DEFAULT_COST: {
  readonly input: 0;
  readonly output: 0;
  readonly cacheRead: 0;
  readonly cacheWrite: 0;
};
declare function getStaticVercelAiGatewayModelCatalog(): ModelDefinitionConfig[];
declare function discoverVercelAiGatewayModels(): Promise<ModelDefinitionConfig[]>;
//#endregion
export { VERCEL_AI_GATEWAY_DEFAULT_MODEL_ID as a, getStaticVercelAiGatewayModelCatalog as c, VERCEL_AI_GATEWAY_DEFAULT_MAX_TOKENS as i, VERCEL_AI_GATEWAY_DEFAULT_CONTEXT_WINDOW as n, VERCEL_AI_GATEWAY_PROVIDER_ID as o, VERCEL_AI_GATEWAY_DEFAULT_COST as r, discoverVercelAiGatewayModels as s, VERCEL_AI_GATEWAY_BASE_URL as t };