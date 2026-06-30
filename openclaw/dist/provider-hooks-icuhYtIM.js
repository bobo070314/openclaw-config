import { a as createGoogleThinkingStreamWrapper } from "./provider-stream-shared-Bs5t-g_E.js";
import { a as buildProviderReplayFamilyHooks } from "./provider-model-shared-CKFakuj-.js";
import { n as buildProviderToolCompatFamilyHooks } from "./provider-tools-VmwDm8UA.js";
import "./thinking-api-CUZjUsIU.js";
import { u as resolveGoogleThinkingProfile } from "./provider-policy-BaZRl3BS.js";
//#region extensions/google/provider-hooks.ts
const GOOGLE_GEMINI_PROVIDER_HOOKS = {
	...buildProviderReplayFamilyHooks({ family: "google-gemini" }),
	...buildProviderToolCompatFamilyHooks("gemini"),
	resolveThinkingProfile: (context) => resolveGoogleThinkingProfile(context),
	wrapStreamFn: createGoogleThinkingStreamWrapper
};
//#endregion
export { GOOGLE_GEMINI_PROVIDER_HOOKS as t };
