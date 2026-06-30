import { _ as uniqueStrings } from "./string-normalization-CRyoFBPt.js";
import { L as readClaudeCliCredentialsCached, R as readCodexCliCredentialsCached, n as ensureAuthProfileStore, u as loadAuthProfileStoreWithoutExternalProfiles } from "./store-DcJR3uqo.js";
import { i as resolveAuthProfileDisplayLabel } from "./auth-profiles-1uAhtKBU.js";
import { n as externalCliDiscoveryForProviderAuth } from "./external-cli-discovery-M9rNixFC.js";
import { i as resolveAuthProfileOrder, n as isStoredCredentialCompatibleWithAuthProvider } from "./order-BFHwZMUJ.js";
import { o as normalizeProviderId } from "./model-selection-normalize-BvNI1t-G.js";
import "./model-selection-60FiczuZ.js";
import { t as resolveEnvApiKey } from "./model-auth-env-C63WdfwU.js";
import { h as resolveUsableCustomProviderApiKey, m as resolveProviderEntryApiKeyProfileReference } from "./model-auth-GMzbnR3o.js";
//#region src/agents/model-auth-label.ts
/**
* Formats user-facing auth labels for resolved provider/model credentials.
*/
/** Resolve the display label that describes how a provider is authenticated. */
function resolveModelAuthLabel(params) {
	const resolvedProvider = params.provider?.trim();
	if (!resolvedProvider) return;
	const providerKey = normalizeProviderId(resolvedProvider);
	const store = params.includeExternalProfiles === false ? loadAuthProfileStoreWithoutExternalProfiles(params.agentDir) : ensureAuthProfileStore(params.agentDir, { externalCli: externalCliDiscoveryForProviderAuth({
		cfg: params.cfg,
		provider: providerKey,
		preferredProfile: params.sessionEntry?.authProfileOverride
	}) });
	const profileOverride = params.sessionEntry?.authProfileOverride?.trim();
	const acceptedProviderKeys = uniqueStrings([...(params.acceptedProviderIds ?? []).map(normalizeProviderId), providerKey].filter(Boolean));
	const candidates = [profileOverride, ...uniqueStrings(acceptedProviderKeys.flatMap((acceptedProvider) => resolveAuthProfileOrder({
		cfg: params.cfg,
		store,
		provider: acceptedProvider,
		preferredProfile: profileOverride
	})))].filter(Boolean);
	for (const profileId of candidates) {
		const profile = store.profiles[profileId];
		if (!profile || !acceptedProviderKeys.some((acceptedProvider) => isStoredCredentialCompatibleWithAuthProvider({
			cfg: params.cfg,
			provider: acceptedProvider,
			credential: profile
		}))) continue;
		const label = resolveAuthProfileDisplayLabel({
			cfg: params.cfg,
			store,
			profileId
		});
		if (profile.type === "oauth") return `oauth${label ? ` (${label})` : ""}`;
		if (profile.type === "token") return `token${label ? ` (${label})` : ""}`;
		return `api-key${label ? ` (${label})` : ""}`;
	}
	const providerEntryProfileRef = resolveProviderEntryApiKeyProfileReference({
		cfg: params.cfg,
		provider: providerKey,
		store
	});
	if (providerEntryProfileRef.kind === "profile") {
		const label = resolveAuthProfileDisplayLabel({
			cfg: params.cfg,
			store,
			profileId: providerEntryProfileRef.profileId
		});
		if (providerEntryProfileRef.mode === "token") return `token${label ? ` (${label})` : ""}`;
		return `api-key${label ? ` (${label})` : ""}`;
	}
	if (providerEntryProfileRef.kind === "profile-incompatible") return "unknown";
	const envKey = resolveEnvApiKey(providerKey, process.env, {
		config: params.cfg,
		workspaceDir: params.workspaceDir
	});
	if (envKey?.apiKey) {
		if (envKey.source.includes("OAUTH_TOKEN")) return `oauth (${envKey.source})`;
		return `api-key (${envKey.source})`;
	}
	if (providerKey === "codex" && readCodexCliCredentialsCached({
		ttlMs: 5e3,
		allowKeychainPrompt: false
	})) return "oauth (codex-cli)";
	if (providerKey === "claude-cli" && readClaudeCliCredentialsCached({
		ttlMs: 5e3,
		allowKeychainPrompt: false
	})) return "oauth (claude-cli)";
	if (resolveUsableCustomProviderApiKey({
		cfg: params.cfg,
		provider: providerKey
	})) return `api-key (models.json)`;
	return "unknown";
}
//#endregion
export { resolveModelAuthLabel as t };
