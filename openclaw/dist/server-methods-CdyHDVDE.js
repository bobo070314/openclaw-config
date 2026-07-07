import { i as gatewayStartupUnavailableDetails } from "./startup-unavailable-CRTM-3cy.js";
import { r as getPluginRegistryState } from "./runtime-state-CDEoJIrS.js";
import { n as createCoreGatewayMethodDescriptors, r as isCoreGatewayMethodClassified } from "./core-descriptors-B2lASufG.js";
import { s as isOperatorScope, t as ADMIN_SCOPE } from "./operator-scopes-CS3xdS-V.js";
import { n as authorizeOperatorScopesForMethod, r as authorizeOperatorScopesForRequiredScope } from "./method-scopes-D5SEXRvS.js";
import { i as createPluginGatewayMethodDescriptors, n as createGatewayMethodRegistry, t as createGatewayMethodDescriptorsFromHandlers } from "./registry-CHAIc2bg.js";
import { n as withPluginRuntimeGatewayRequestScope } from "./gateway-request-scope-BAEdAUQ6.js";
import { mn as errorShape, pn as ErrorCodes } from "./schema-BrDi0lZs.js";
import "./src-BNueln22.js";
import { t as consumeControlPlaneWriteBudget } from "./control-plane-rate-limit-DcNqNwry.js";
import { n as resolveControlPlaneActor, t as formatControlPlaneActor } from "./control-plane-audit-CfUQZQQ4.js";
import { n as parseGatewayRole, t as isRoleAuthorizedForMethod } from "./role-policy-NaU7HGwg.js";
//#region src/gateway/server-methods.ts
function lazyHandlerModule(loadModule, selectHandlers) {
	let handlersPromise = null;
	return () => handlersPromise ??= loadModule().then(selectHandlers);
}
function createLazyCoreHandlers(params) {
	return Object.fromEntries(params.methods.map((method) => [method, async (opts) => {
		const handler = (await params.loadHandlers())[method];
		if (!handler) throw new Error(`lazy gateway handler not found: ${method}`);
		await handler(opts);
	}]));
}
const loadAgentHandlers = lazyHandlerModule(() => import("./agent-CnYmTiHt.js"), (module) => module.agentHandlers);
const loadAgentsHandlers = lazyHandlerModule(() => import("./agents-BJC6PtN2.js"), (module) => module.agentsHandlers);
const loadArtifactsHandlers = lazyHandlerModule(() => import("./artifacts-DW6qWd5W.js"), (module) => module.artifactsHandlers);
const loadChannelsHandlers = lazyHandlerModule(() => import("./channels-nLP6UG29.js"), (module) => module.channelsHandlers);
const loadChatHandlers = lazyHandlerModule(() => import("./chat-DZ8XD7AO.js"), (module) => module.chatHandlers);
const loadCommandsHandlers = lazyHandlerModule(() => import("./commands-611OHnhy.js"), (module) => module.commandsHandlers);
const loadConfigHandlers = lazyHandlerModule(() => import("./config-Brb3npnt.js"), (module) => module.configHandlers);
const loadConnectHandlers = lazyHandlerModule(() => import("./connect-Dq4dvLpe.js"), (module) => module.connectHandlers);
const loadCronHandlers = lazyHandlerModule(() => import("./cron-BvAp322e.js"), (module) => module.cronHandlers);
const loadDeviceHandlers = lazyHandlerModule(() => import("./devices-CWjPlrBt.js"), (module) => module.deviceHandlers);
const loadDiagnosticsHandlers = lazyHandlerModule(() => import("./diagnostics-DNj-vUeM.js"), (module) => module.diagnosticsHandlers);
const loadDoctorHandlers = lazyHandlerModule(() => import("./doctor-Bly9uVfq.js"), (module) => module.doctorHandlers);
const loadEnvironmentsHandlers = lazyHandlerModule(() => import("./environments-wsmfZgO9.js"), (module) => module.environmentsHandlers);
const loadExecApprovalsHandlers = lazyHandlerModule(() => import("./exec-approvals-C5Kcj8Gk.js"), (module) => module.execApprovalsHandlers);
const loadHealthHandlers = lazyHandlerModule(() => import("./health-BBGjCXIN.js"), (module) => module.healthHandlers);
const loadLogsHandlers = lazyHandlerModule(() => import("./logs-DOt4ZXqt.js"), (module) => module.logsHandlers);
const loadModelsAuthStatusHandlers = lazyHandlerModule(() => import("./models-auth-status-CHesXJgo.js"), (module) => module.modelsAuthStatusHandlers);
const loadModelsHandlers = lazyHandlerModule(() => import("./models-C-xg4SwV.js"), (module) => module.modelsHandlers);
const loadNativeHookRelayHandlers = lazyHandlerModule(() => import("./native-hook-relay-e6Ca6I4E.js"), (module) => module.nativeHookRelayHandlers);
const loadNodePendingHandlers = lazyHandlerModule(() => import("./nodes-pending-Cmz6XuVM.js"), (module) => module.nodePendingHandlers);
const loadNodeHandlers = lazyHandlerModule(() => import("./nodes-DGMIkn_M.js"), (module) => module.nodeHandlers);
const loadPluginHostHookHandlers = lazyHandlerModule(() => import("./plugin-host-hooks-BqWXNVrX.js"), (module) => module.pluginHostHookHandlers);
const loadPushHandlers = lazyHandlerModule(() => import("./push-wqYMjBQU.js"), (module) => module.pushHandlers);
const loadRestartHandlers = lazyHandlerModule(() => import("./restart-sYEUVucm.js"), (module) => module.restartHandlers);
const loadSendHandlers = lazyHandlerModule(() => import("./send-BMn-S3XR.js"), (module) => module.sendHandlers);
const loadSessionsFilesHandlers = lazyHandlerModule(() => import("./sessions-files-lV0Rrinu.js"), (module) => module.sessionsFilesHandlers);
const loadSessionsHandlers = lazyHandlerModule(() => import("./sessions-FHKRhZK9.js"), (module) => module.sessionsHandlers);
const loadSkillsHandlers = lazyHandlerModule(() => import("./skills-70_a8Zr-.js"), (module) => module.skillsHandlers);
const loadSystemHandlers = lazyHandlerModule(() => import("./system-BKyNtoIt.js"), (module) => module.systemHandlers);
const loadTalkHandlers = lazyHandlerModule(() => import("./talk-CcL_kGNo.js"), (module) => module.talkHandlers);
const loadTasksHandlers = lazyHandlerModule(() => import("./tasks-Ca9vHkfg.js"), (module) => module.tasksHandlers);
const loadToolsCatalogHandlers = lazyHandlerModule(() => import("./tools-catalog-Cw7cEGCF.js"), (module) => module.toolsCatalogHandlers);
const loadToolsEffectiveHandlers = lazyHandlerModule(() => import("./tools-effective-kJI_6s7q.js"), (module) => module.toolsEffectiveHandlers);
const loadToolsInvokeHandlers = lazyHandlerModule(() => import("./tools-invoke-Cv8jVt_l.js"), (module) => module.toolsInvokeHandlers);
const loadTtsHandlers = lazyHandlerModule(() => import("./tts-BsdwXtLn.js"), (module) => module.ttsHandlers);
const loadUpdateHandlers = lazyHandlerModule(() => import("./update-CPRQmUQz.js"), (module) => module.updateHandlers);
const loadUsageHandlers = lazyHandlerModule(() => import("./usage-CjMtWzJR.js"), (module) => module.usageHandlers);
const loadVoicewakeRoutingHandlers = lazyHandlerModule(() => import("./voicewake-routing-CCBlNn85.js"), (module) => module.voicewakeRoutingHandlers);
const loadVoicewakeHandlers = lazyHandlerModule(() => import("./voicewake-BoK0Ptft.js"), (module) => module.voicewakeHandlers);
const loadWebHandlers = lazyHandlerModule(() => import("./web-8NJTyC4p.js"), (module) => module.webHandlers);
const loadWizardHandlers = lazyHandlerModule(() => import("./wizard-BansH2cW.js"), (module) => module.wizardHandlers);
function authorizeGatewayMethod(method, client, params, methodRegistry) {
	if (!client?.connect) return null;
	if (method === "health") return null;
	const roleRaw = client.connect.role ?? "operator";
	const role = parseGatewayRole(roleRaw);
	if (!role) return errorShape(ErrorCodes.INVALID_REQUEST, `unauthorized role: ${roleRaw}`);
	const scopes = client.connect.scopes ?? [];
	if (!isRoleAuthorizedForMethod(role, method)) return errorShape(ErrorCodes.INVALID_REQUEST, `unauthorized role: ${role}`);
	if (role === "node") return null;
	if (scopes.includes("operator.admin")) return null;
	const registeredScope = methodRegistry.getScope(method);
	const scopeAuth = isOperatorScope(registeredScope) ? authorizeOperatorScopesForRequiredScope(registeredScope, scopes) : authorizeOperatorScopesForMethod(method, scopes, params);
	if (!scopeAuth.allowed) return errorShape(ErrorCodes.INVALID_REQUEST, `missing scope: ${scopeAuth.missingScope}`);
	return null;
}
const coreGatewayHandlers = {
	...createLazyCoreHandlers({
		methods: ["connect"],
		loadHandlers: loadConnectHandlers
	}),
	...createLazyCoreHandlers({
		methods: ["logs.tail"],
		loadHandlers: loadLogsHandlers
	}),
	...createLazyCoreHandlers({
		methods: ["voicewake.get", "voicewake.set"],
		loadHandlers: loadVoicewakeHandlers
	}),
	...createLazyCoreHandlers({
		methods: ["voicewake.routing.get", "voicewake.routing.set"],
		loadHandlers: loadVoicewakeRoutingHandlers
	}),
	...createLazyCoreHandlers({
		methods: ["health", "status"],
		loadHandlers: loadHealthHandlers
	}),
	...createLazyCoreHandlers({
		methods: [
			"channels.status",
			"channels.start",
			"channels.stop",
			"channels.logout"
		],
		loadHandlers: loadChannelsHandlers
	}),
	...createLazyCoreHandlers({
		methods: [
			"chat.history",
			"chat.startup",
			"chat.metadata",
			"chat.message.get",
			"chat.abort",
			"chat.send",
			"chat.inject"
		],
		loadHandlers: loadChatHandlers
	}),
	...createLazyCoreHandlers({
		methods: ["commands.list"],
		loadHandlers: loadCommandsHandlers
	}),
	...createLazyCoreHandlers({
		methods: [
			"wake",
			"cron.list",
			"cron.status",
			"cron.get",
			"cron.add",
			"cron.update",
			"cron.remove",
			"cron.run",
			"cron.runs"
		],
		loadHandlers: loadCronHandlers
	}),
	...createLazyCoreHandlers({
		methods: [
			"device.pair.list",
			"device.pair.approve",
			"device.pair.reject",
			"device.pair.remove",
			"device.token.rotate",
			"device.token.revoke"
		],
		loadHandlers: loadDeviceHandlers
	}),
	...createLazyCoreHandlers({
		methods: ["diagnostics.stability"],
		loadHandlers: loadDiagnosticsHandlers
	}),
	...createLazyCoreHandlers({
		methods: [
			"doctor.memory.status",
			"doctor.memory.dreamDiary",
			"doctor.memory.backfillDreamDiary",
			"doctor.memory.resetDreamDiary",
			"doctor.memory.resetGroundedShortTerm",
			"doctor.memory.repairDreamingArtifacts",
			"doctor.memory.dedupeDreamDiary",
			"doctor.memory.remHarness"
		],
		loadHandlers: loadDoctorHandlers
	}),
	...createLazyCoreHandlers({
		methods: ["environments.list", "environments.status"],
		loadHandlers: loadEnvironmentsHandlers
	}),
	...createLazyCoreHandlers({
		methods: [
			"exec.approvals.get",
			"exec.approvals.set",
			"exec.approvals.node.get",
			"exec.approvals.node.set"
		],
		loadHandlers: loadExecApprovalsHandlers
	}),
	...createLazyCoreHandlers({
		methods: ["web.login.start", "web.login.wait"],
		loadHandlers: loadWebHandlers
	}),
	...createLazyCoreHandlers({
		methods: ["models.list"],
		loadHandlers: loadModelsHandlers
	}),
	...createLazyCoreHandlers({
		methods: ["models.authLogout", "models.authStatus"],
		loadHandlers: loadModelsAuthStatusHandlers
	}),
	...createLazyCoreHandlers({
		methods: ["nativeHook.invoke"],
		loadHandlers: loadNativeHookRelayHandlers
	}),
	...createLazyCoreHandlers({
		methods: ["plugins.uiDescriptors", "plugins.sessionAction"],
		loadHandlers: loadPluginHostHookHandlers
	}),
	...createLazyCoreHandlers({
		methods: [
			"config.get",
			"config.schema",
			"config.schema.lookup",
			"config.set",
			"config.patch",
			"config.apply",
			"config.openFile"
		],
		loadHandlers: loadConfigHandlers
	}),
	...createLazyCoreHandlers({
		methods: [
			"wizard.start",
			"wizard.next",
			"wizard.cancel",
			"wizard.status"
		],
		loadHandlers: loadWizardHandlers
	}),
	...createLazyCoreHandlers({
		methods: [
			"talk.session.create",
			"talk.session.join",
			"talk.session.appendAudio",
			"talk.session.startTurn",
			"talk.session.endTurn",
			"talk.session.cancelTurn",
			"talk.session.cancelOutput",
			"talk.session.submitToolResult",
			"talk.session.steer",
			"talk.session.close",
			"talk.client.create",
			"talk.client.toolCall",
			"talk.client.steer",
			"talk.catalog",
			"talk.config",
			"talk.speak",
			"talk.mode"
		],
		loadHandlers: loadTalkHandlers
	}),
	...createLazyCoreHandlers({
		methods: [
			"tasks.list",
			"tasks.get",
			"tasks.cancel"
		],
		loadHandlers: loadTasksHandlers
	}),
	...createLazyCoreHandlers({
		methods: ["tools.catalog"],
		loadHandlers: loadToolsCatalogHandlers
	}),
	...createLazyCoreHandlers({
		methods: ["tools.effective"],
		loadHandlers: loadToolsEffectiveHandlers
	}),
	...createLazyCoreHandlers({
		methods: ["tools.invoke"],
		loadHandlers: loadToolsInvokeHandlers
	}),
	...createLazyCoreHandlers({
		methods: [
			"tts.status",
			"tts.enable",
			"tts.disable",
			"tts.convert",
			"tts.setProvider",
			"tts.personas",
			"tts.setPersona",
			"tts.providers"
		],
		loadHandlers: loadTtsHandlers
	}),
	...createLazyCoreHandlers({
		methods: [
			"skills.upload.begin",
			"skills.upload.chunk",
			"skills.upload.commit",
			"skills.status",
			"skills.bins",
			"skills.search",
			"skills.detail",
			"skills.securityVerdicts",
			"skills.skillCard",
			"skills.install",
			"skills.update",
			"skills.proposals.list",
			"skills.proposals.inspect",
			"skills.proposals.create",
			"skills.proposals.update",
			"skills.proposals.revise",
			"skills.proposals.requestRevision",
			"skills.proposals.apply",
			"skills.proposals.reject",
			"skills.proposals.quarantine"
		],
		loadHandlers: loadSkillsHandlers
	}),
	...createLazyCoreHandlers({
		methods: [
			"sessions.list",
			"sessions.cleanup",
			"sessions.subscribe",
			"sessions.unsubscribe",
			"sessions.messages.subscribe",
			"sessions.messages.unsubscribe",
			"sessions.preview",
			"sessions.describe",
			"sessions.resolve",
			"sessions.compaction.list",
			"sessions.compaction.get",
			"sessions.create",
			"sessions.compaction.branch",
			"sessions.compaction.restore",
			"sessions.send",
			"sessions.steer",
			"sessions.abort",
			"sessions.patch",
			"sessions.pluginPatch",
			"sessions.reset",
			"sessions.delete",
			"sessions.get",
			"sessions.compact"
		],
		loadHandlers: loadSessionsHandlers
	}),
	...createLazyCoreHandlers({
		methods: [
			"gateway.identity.get",
			"last-heartbeat",
			"set-heartbeats",
			"system-presence",
			"system-event"
		],
		loadHandlers: loadSystemHandlers
	}),
	...createLazyCoreHandlers({
		methods: ["update.status", "update.run"],
		loadHandlers: loadUpdateHandlers
	}),
	...createLazyCoreHandlers({
		methods: [
			"node.pair.request",
			"node.pair.list",
			"node.pair.approve",
			"node.pair.reject",
			"node.pair.remove",
			"node.pair.verify",
			"node.rename",
			"node.list",
			"node.describe",
			"node.pluginSurface.refresh",
			"node.pending.pull",
			"node.pending.ack",
			"node.invoke",
			"node.invoke.result",
			"node.event"
		],
		loadHandlers: loadNodeHandlers
	}),
	...createLazyCoreHandlers({
		methods: ["node.pending.drain", "node.pending.enqueue"],
		loadHandlers: loadNodePendingHandlers
	}),
	...createLazyCoreHandlers({
		methods: [
			"push.test",
			"push.web.vapidPublicKey",
			"push.web.subscribe",
			"push.web.unsubscribe",
			"push.web.test"
		],
		loadHandlers: loadPushHandlers
	}),
	...createLazyCoreHandlers({
		methods: ["gateway.restart.request", "gateway.restart.preflight"],
		loadHandlers: loadRestartHandlers
	}),
	...createLazyCoreHandlers({
		methods: [
			"message.action",
			"send",
			"poll"
		],
		loadHandlers: loadSendHandlers
	}),
	...createLazyCoreHandlers({
		methods: [
			"usage.status",
			"usage.cost",
			"sessions.usage",
			"sessions.usage.timeseries",
			"sessions.usage.logs"
		],
		loadHandlers: loadUsageHandlers
	}),
	...createLazyCoreHandlers({
		methods: [
			"agent",
			"agent.identity.get",
			"agent.wait"
		],
		loadHandlers: loadAgentHandlers
	}),
	...createLazyCoreHandlers({
		methods: [
			"agents.list",
			"agents.create",
			"agents.update",
			"agents.delete",
			"agents.files.list",
			"agents.files.get",
			"agents.files.set"
		],
		loadHandlers: loadAgentsHandlers
	}),
	...createLazyCoreHandlers({
		methods: [
			"artifacts.list",
			"artifacts.get",
			"artifacts.download"
		],
		loadHandlers: loadArtifactsHandlers
	}),
	...createLazyCoreHandlers({
		methods: ["sessions.files.list", "sessions.files.get"],
		loadHandlers: loadSessionsFilesHandlers
	})
};
/** Builds the per-request method registry from core, plugin, and explicit extra handlers. */
function createRequestGatewayMethodRegistry(extraHandlers) {
	const activePluginRegistry = getPluginRegistryState()?.activeRegistry;
	const activePluginHandlers = activePluginRegistry?.gatewayHandlers ?? {};
	const extraHandlerEntries = Object.entries(extraHandlers ?? {});
	const pluginMethodNames = new Set(Object.keys(activePluginHandlers));
	const coreDescriptorHandlers = { ...coreGatewayHandlers };
	for (const [method, extraHandler] of extraHandlerEntries) if (!pluginMethodNames.has(method) && isCoreGatewayMethodClassified(method)) coreDescriptorHandlers[method] = extraHandler;
	const coreDescriptors = createCoreGatewayMethodDescriptors(coreDescriptorHandlers);
	for (const descriptor of coreDescriptors) {
		const extraHandler = extraHandlers?.[descriptor.name];
		if (extraHandler && !pluginMethodNames.has(descriptor.name)) descriptor.handler = extraHandler;
	}
	const coreMethodNames = new Set(coreDescriptors.map((descriptor) => descriptor.name));
	const auxHandlers = Object.fromEntries(extraHandlerEntries.filter(([method]) => !pluginMethodNames.has(method) && !coreMethodNames.has(method)));
	return createGatewayMethodRegistry([
		...coreDescriptors,
		...activePluginRegistry ? createPluginGatewayMethodDescriptors(activePluginRegistry) : [],
		...createGatewayMethodDescriptorsFromHandlers({
			handlers: auxHandlers,
			owner: {
				kind: "aux",
				area: "gateway-extra"
			},
			defaultScope: ADMIN_SCOPE
		})
	]);
}
/** Authorizes and dispatches one gateway JSON-RPC-style request. */
async function handleGatewayRequest(opts) {
	const { req, respond, client, isWebchatConnect, context } = opts;
	const methodRegistry = opts.methodRegistry ?? createRequestGatewayMethodRegistry(opts.extraHandlers);
	const authError = authorizeGatewayMethod(req.method, client, req.params, methodRegistry);
	if (authError) {
		respond(false, void 0, authError);
		return;
	}
	if (context.unavailableGatewayMethods?.has(req.method)) {
		respond(false, void 0, errorShape(ErrorCodes.UNAVAILABLE, `${req.method} unavailable during gateway startup`, {
			retryable: true,
			retryAfterMs: 500,
			details: {
				...gatewayStartupUnavailableDetails(),
				method: req.method
			}
		}));
		return;
	}
	if (methodRegistry.isControlPlaneWrite(req.method)) {
		const budget = consumeControlPlaneWriteBudget({ client });
		if (!budget.allowed) {
			const actor = resolveControlPlaneActor(client);
			context.logGateway.warn(`control-plane write rate-limited method=${req.method} ${formatControlPlaneActor(actor)} retryAfterMs=${budget.retryAfterMs} key=${budget.key}`);
			respond(false, void 0, errorShape(ErrorCodes.UNAVAILABLE, `rate limit exceeded for ${req.method}; retry after ${Math.ceil(budget.retryAfterMs / 1e3)}s`, {
				retryable: true,
				retryAfterMs: budget.retryAfterMs,
				details: {
					method: req.method,
					limit: "3 per 60s"
				}
			}));
			return;
		}
	}
	const handler = methodRegistry.getHandler(req.method);
	if (!handler) {
		respond(false, void 0, errorShape(ErrorCodes.INVALID_REQUEST, `unknown method: ${req.method}`));
		return;
	}
	const invokeHandler = () => handler({
		req,
		params: req.params ?? {},
		client,
		isWebchatConnect,
		respond,
		context
	});
	await withPluginRuntimeGatewayRequestScope({
		context,
		client,
		isWebchatConnect
	}, invokeHandler);
}
//#endregion
export { coreGatewayHandlers, handleGatewayRequest };
