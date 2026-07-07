import { a as buildOpenAICompatibleReplayPolicy } from "../../provider-replay-helpers-DtVD32X4.js";
import "../../provider-model-shared-CKFakuj-.js";
import { t as defineSingleProviderPluginEntry } from "../../provider-entry-BhS0gICf.js";
import { i as MOONSHOT_THINKING_STREAM_HOOKS } from "../../provider-stream-BMuZ7xmk.js";
import "../../provider-stream-family-DjSMMJXs.js";
import { a as buildMoonshotProvider, i as applyMoonshotNativeStreamingUsageCompat } from "../../provider-catalog-DIiY82Bt.js";
import { n as applyMoonshotConfig, r as applyMoonshotConfigCn, t as MOONSHOT_DEFAULT_MODEL_REF } from "../../onboard-B9WmDhqM.js";
import "../../api-DzmPwn88.js";
import { n as moonshotMediaUnderstandingProvider } from "../../media-understanding-provider-CyZGDmOL.js";
import { n as resolveThinkingProfile, t as KIMI_K2_7_CODE_MODEL_ID } from "../../provider-policy-api-DS1rfVLL.js";
import { t as createKimiWebSearchProvider } from "../../kimi-web-search-provider-BbsS61ZK.js";
//#region extensions/moonshot/index.ts
const PROVIDER_ID = "moonshot";
const moonshotThinkingStreamHooks = MOONSHOT_THINKING_STREAM_HOOKS;
var moonshot_default = defineSingleProviderPluginEntry({
	id: PROVIDER_ID,
	name: "Moonshot Provider",
	description: "Bundled Moonshot provider plugin",
	provider: {
		label: "Moonshot",
		docsPath: "/providers/moonshot",
		aliases: ["moonshotai", "moonshot-ai"],
		auth: [{
			methodId: "api-key",
			label: "Kimi API key (.ai)",
			hint: "Kimi K2.6 + Kimi",
			optionKey: "moonshotApiKey",
			flagName: "--moonshot-api-key",
			envVar: "MOONSHOT_API_KEY",
			promptMessage: "Enter Moonshot API key",
			defaultModel: MOONSHOT_DEFAULT_MODEL_REF,
			applyConfig: (cfg) => applyMoonshotConfig(cfg),
			wizard: { groupLabel: "Moonshot AI (Kimi K2.6)" }
		}, {
			methodId: "api-key-cn",
			label: "Kimi API key (.cn)",
			hint: "Kimi K2.6 + Kimi",
			optionKey: "moonshotApiKey",
			flagName: "--moonshot-api-key",
			envVar: "MOONSHOT_API_KEY",
			promptMessage: "Enter Moonshot API key (.cn)",
			defaultModel: MOONSHOT_DEFAULT_MODEL_REF,
			applyConfig: (cfg) => applyMoonshotConfigCn(cfg),
			wizard: { groupLabel: "Moonshot AI (Kimi K2.6)" }
		}],
		catalog: {
			buildProvider: buildMoonshotProvider,
			buildStaticProvider: buildMoonshotProvider,
			allowExplicitBaseUrl: true
		},
		applyNativeStreamingUsageCompat: ({ providerConfig }) => applyMoonshotNativeStreamingUsageCompat(providerConfig),
		buildReplayPolicy: ({ modelApi, modelId }) => buildOpenAICompatibleReplayPolicy(modelApi, {
			modelId,
			sanitizeToolCallIds: modelApi === "openai-completions",
			duplicateToolCallIdStyle: "openai",
			dropReasoningFromHistory: false
		}),
		...moonshotThinkingStreamHooks,
		wrapSimpleCompletionStreamFn: (ctx) => ctx.modelId.trim().toLowerCase() === "kimi-k2.7-code" ? moonshotThinkingStreamHooks.wrapStreamFn?.(ctx) : ctx.streamFn,
		resolveThinkingProfile,
		isModernModelRef: ({ modelId }) => modelId.trim().toLowerCase() === KIMI_K2_7_CODE_MODEL_ID
	},
	register(api) {
		api.registerMediaUnderstandingProvider(moonshotMediaUnderstandingProvider);
		api.registerWebSearchProvider(createKimiWebSearchProvider());
	}
});
//#endregion
export { moonshot_default as default };
