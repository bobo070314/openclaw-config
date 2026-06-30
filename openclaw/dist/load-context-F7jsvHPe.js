import { t as createSubsystemLogger } from "./subsystem-BTVUlTIB.js";
import "./agent-scope-CESPhp3L.js";
import { c as resolveDefaultAgentId, o as resolveAgentWorkspaceDir } from "./agent-scope-config-ChfGvhEr.js";
import { i as isReusableCurrentPluginMetadataSnapshot, n as clearCurrentPluginMetadataSnapshot, o as setCurrentPluginMetadataSnapshot } from "./current-plugin-metadata-snapshot-nGeSY76G.js";
import { f as extractPluginInstallRecordsFromInstalledPluginIndex } from "./installed-plugin-index-UYExs-Ey.js";
import { a as resolvePluginMetadataSnapshot } from "./plugin-metadata-snapshot-O_ETy0qj.js";
import { i as getRuntimeConfig } from "./io-CwmOK6NP.js";
import "./config-CxwD7EO_.js";
import { t as applyPluginAutoEnable } from "./plugin-auto-enable-3CSAR1D4.js";
import { m as resolvePluginActivationSourceConfig } from "./loader-CXafBhxY.js";
import "./logging-DotGwuOD.js";
//#region src/plugins/runtime/load-context.ts
const log = createSubsystemLogger("plugins");
/** Creates the default plugin runtime loader logger. */
function createPluginRuntimeLoaderLogger() {
	return {
		info: (message) => log.info(message),
		warn: (message) => log.warn(message),
		error: (message) => log.error(message),
		debug: (message) => log.debug(message)
	};
}
/** Resolves config, manifests, install records, and auto-enable state for runtime loads. */
function resolvePluginRuntimeLoadContext(options) {
	const env = options?.env ?? process.env;
	const rawConfig = options?.config ?? getRuntimeConfig();
	const rawWorkspaceDir = options?.workspaceDir ?? resolveAgentWorkspaceDir(rawConfig, resolveDefaultAgentId(rawConfig));
	const metadataSnapshot = options?.manifestRegistry ? void 0 : resolvePluginMetadataSnapshot({
		config: rawConfig,
		env,
		workspaceDir: rawWorkspaceDir,
		allowWorkspaceScopedCurrent: true
	});
	const manifestRegistry = options?.manifestRegistry ?? metadataSnapshot?.manifestRegistry;
	const installRecords = metadataSnapshot ? extractPluginInstallRecordsFromInstalledPluginIndex(metadataSnapshot.index) : void 0;
	const activationSourceConfig = resolvePluginActivationSourceConfig({
		config: rawConfig,
		activationSourceConfig: options?.activationSourceConfig
	});
	const autoEnabled = applyPluginAutoEnable({
		config: rawConfig,
		env,
		manifestRegistry,
		discovery: metadataSnapshot?.discovery
	});
	const config = autoEnabled.config;
	const workspaceDir = options?.workspaceDir ?? resolveAgentWorkspaceDir(config, resolveDefaultAgentId(config));
	if (metadataSnapshot) if (isReusableCurrentPluginMetadataSnapshot(metadataSnapshot)) setCurrentPluginMetadataSnapshot(metadataSnapshot, {
		config: rawConfig,
		compatibleConfigs: [config, activationSourceConfig],
		env,
		workspaceDir
	});
	else clearCurrentPluginMetadataSnapshot();
	return {
		rawConfig,
		config,
		activationSourceConfig,
		autoEnabledReasons: autoEnabled.autoEnabledReasons,
		workspaceDir,
		env,
		logger: options?.logger ?? createPluginRuntimeLoaderLogger(),
		manifestRegistry,
		installRecords
	};
}
/** Builds plugin load options from a resolved runtime load context. */
function buildPluginRuntimeLoadOptions(context, overrides) {
	return buildPluginRuntimeLoadOptionsFromValues(context, overrides);
}
/** Builds plugin load options from explicit runtime load values. */
function buildPluginRuntimeLoadOptionsFromValues(values, overrides) {
	return {
		config: values.config,
		activationSourceConfig: values.activationSourceConfig,
		autoEnabledReasons: values.autoEnabledReasons,
		workspaceDir: values.workspaceDir,
		env: values.env,
		logger: values.logger,
		manifestRegistry: values.manifestRegistry,
		installRecords: values.installRecords,
		...overrides
	};
}
//#endregion
export { resolvePluginRuntimeLoadContext as i, buildPluginRuntimeLoadOptionsFromValues as n, createPluginRuntimeLoaderLogger as r, buildPluginRuntimeLoadOptions as t };
