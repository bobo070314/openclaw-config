import { l as redactToolDetail } from "./redact-DOrFK54L.js";
import "./errors-DNvW4XW_.js";
import { b as truncateUtf16Safe } from "./utils-BmpsSbZo.js";
import "./version-CeFj_iGk.js";
import { t as createSubsystemLogger } from "./subsystem-BTVUlTIB.js";
import "./agent-scope-CESPhp3L.js";
import "./registry-OLFwZt_S.js";
import { v as listCodexAppServerExtensionFactories } from "./registry-BmAQAf7L.js";
import { c as joinPresentTextSegments, t as getGlobalHookRunner } from "./hook-runner-global-Bm5WihiA.js";
import "./registry-BFS9LOHl.js";
import "./transcript-events-bo5V8PHW.js";
import "./session-write-lock-81JXiIgr.js";
import "./session-accessor-ArmkJJUW.js";
import "./model-auth-GMzbnR3o.js";
import { p as queueEmbeddedAgentMessageWithOutcome } from "./runs-pVtbFfgt.js";
import "./usage-C67Kbb7n.js";
import "./agent-tools.before-tool-call-CDuA0_mC.js";
import "./tools-DWq4toVW.js";
import "./gateway-wg3rzLzQ.js";
import "./hook-helpers-CENBGDuz.js";
import "./heartbeat-tool-response-DqL28SwH.js";
import "./context-engine-lifecycle-CuZ0qH-C.js";
import "./logger-Cc1RIqMU.js";
import "./nodes-utils-rzDwGCc_.js";
import { r as resolveToolDisplay, t as formatToolDetail } from "./tool-display-Da_u6taL.js";
import "./streaming-Dgx_j8xT.js";
import "./sandbox-BsGTve-p.js";
import "./bootstrap-files-CwPA02sG.js";
import "./embedded-agent-messaging-DrnnQY0n.js";
import "./embedded-agent-message-tool-source-reply-BNDmht0w.js";
import { s as buildAgentHookContext } from "./lifecycle-hook-helpers-v00PVIlh.js";
import "./tool-schema-projection-C_uRkhtw.js";
import "./tools-BjIlvREJ.js";
import "./attempt.tool-run-context-DWNz4033.js";
import "./tool-result-middleware-DA6D7k8x.js";
import { p as wrapPluginSystemContextSection } from "./attempt.prompt-helpers-Cuf8j_4K.js";
import "./attempt-tool-construction-plan-C0hAZjzo.js";
import "./result-fallback-classifier-DyAgXETt.js";
import "./build-qAzx5U8o.js";
import "./agent-dir-compat-TFbN3Urf.js";
import "./native-hook-relay-BqNuR7H8.js";
//#region src/agents/harness/prompt-compaction-hook-helpers.ts
/**
* Agent harness prompt and compaction hook helpers.
*
* Harness runtimes use this to run plugin hooks around prompt construction and
* compaction while keeping hook failures non-fatal.
*/
const log$1 = createSubsystemLogger("agents/harness");
/** Runs before-prompt hooks and returns the adjusted prompt fields. */
async function resolveAgentHarnessBeforePromptBuildResult(params) {
	const hookRunner = getGlobalHookRunner();
	const hasPrecomputedBeforeAgentStartResult = "beforeAgentStartResult" in params;
	if (!hasPrecomputedBeforeAgentStartResult && !hookRunner?.hasHooks("before_prompt_build") && !hookRunner?.hasHooks("before_agent_start")) return {
		prompt: params.prompt,
		developerInstructions: params.developerInstructions,
		promptInputRange: {
			start: 0,
			end: params.prompt.length
		}
	};
	const hookCtx = buildAgentHookContext(params.ctx);
	const promptEvent = {
		prompt: params.prompt,
		messages: params.messages
	};
	const promptBuildResult = hookRunner?.hasHooks("before_prompt_build") ? await hookRunner.runBeforePromptBuild(promptEvent, hookCtx).catch((error) => {
		log$1.warn(`before_prompt_build hook failed: ${String(error)}`);
	}) : void 0;
	const beforeAgentStartResult = hasPrecomputedBeforeAgentStartResult ? params.beforeAgentStartResult : hookRunner?.hasHooks("before_agent_start") ? await hookRunner.runBeforeAgentStart(promptEvent, hookCtx).catch((error) => {
		log$1.warn(`deprecated before_agent_start hook failed during prompt build: ${String(error)}`);
	}) : void 0;
	const systemPrompt = resolvePromptBuildSystemPrompt({
		developerInstructions: params.developerInstructions,
		promptBuildResult,
		beforeAgentStartResult
	});
	const promptPrefix = joinPresentTextSegments([promptBuildResult?.prependContext, beforeAgentStartResult?.prependContext]);
	const promptSuffix = joinPresentTextSegments([promptBuildResult?.appendContext, beforeAgentStartResult?.appendContext]);
	const prompt = joinPresentTextSegments([
		promptPrefix,
		params.prompt,
		promptSuffix
	]) ?? params.prompt;
	const promptInputStart = params.prompt.length === 0 ? promptPrefix?.length ?? 0 : promptPrefix ? promptPrefix.length + 2 : 0;
	return {
		prompt,
		developerInstructions: joinPresentTextSegments([
			wrapPluginSystemContextSection(promptBuildResult?.prependSystemContext),
			wrapPluginSystemContextSection(beforeAgentStartResult?.prependSystemContext),
			systemPrompt,
			wrapPluginSystemContextSection(promptBuildResult?.appendSystemContext),
			wrapPluginSystemContextSection(beforeAgentStartResult?.appendSystemContext)
		]) ?? systemPrompt,
		promptInputRange: {
			start: promptInputStart,
			end: promptInputStart + params.prompt.length
		}
	};
}
function resolvePromptBuildSystemPrompt(params) {
	if (typeof params.promptBuildResult?.systemPrompt === "string") return params.promptBuildResult.systemPrompt;
	if (typeof params.beforeAgentStartResult?.systemPrompt === "string") return params.beforeAgentStartResult.systemPrompt;
	return params.developerInstructions;
}
/** Runs best-effort before-compaction hooks for a harness session. */
async function runAgentHarnessBeforeCompactionHook(params) {
	const hookRunner = getGlobalHookRunner();
	if (!hookRunner?.hasHooks("before_compaction")) return;
	try {
		await hookRunner.runBeforeCompaction({
			messageCount: params.messages?.length ?? -1,
			...params.messages ? { messages: params.messages } : {},
			sessionFile: params.sessionFile
		}, buildAgentHookContext(params.ctx));
	} catch (error) {
		log$1.warn(`before_compaction hook failed: ${String(error)}`);
	}
}
/** Runs best-effort after-compaction hooks for a harness session. */
async function runAgentHarnessAfterCompactionHook(params) {
	const hookRunner = getGlobalHookRunner();
	if (!hookRunner?.hasHooks("after_compaction")) return;
	try {
		await hookRunner.runAfterCompaction({
			messageCount: params.messages?.length ?? -1,
			compactedCount: params.compactedCount,
			sessionFile: params.sessionFile
		}, buildAgentHookContext(params.ctx));
	} catch (error) {
		log$1.warn(`after_compaction hook failed: ${String(error)}`);
	}
}
//#endregion
//#region src/agents/harness/codex-app-server-extensions.ts
/**
* Codex app-server extension runner.
*
* Harness integration uses this to let registered extensions observe and adjust
* tool results before they are returned to the agent runtime.
*/
const log = createSubsystemLogger("agents/harness");
/** Creates a runner that applies registered Codex app-server tool-result extensions. */
function createCodexAppServerToolResultExtensionRunner(ctx, factories = listCodexAppServerExtensionFactories()) {
	const handlers = [];
	const runtime = { on(event, handler) {
		if (event === "tool_result") handlers.push(handler);
	} };
	const initPromise = (async () => {
		for (const factory of factories) await factory(runtime);
	})();
	return { async applyToolResultExtensions(event) {
		await initPromise;
		let current = event.result;
		for (const handler of handlers) try {
			const next = await handler({
				...event,
				result: current
			}, ctx);
			if (next?.result) current = next.result;
		} catch (error) {
			const detail = error instanceof Error ? error.message : String(error);
			log.warn(`[codex] tool_result extension failed for ${event.toolName}: ${detail}`);
		}
		return current;
	} };
}
//#endregion
//#region src/plugin-sdk/agent-harness-runtime.ts
/** Default truncation limit for user-facing tool progress output. */
const TOOL_PROGRESS_OUTPUT_MAX_CHARS = 8e3;
/**
* @deprecated Active-run queueing is an internal runtime concern. This legacy
* boolean API only reports immediate queue eligibility and cannot observe async
* runtime rejection; runtime-owned delivery paths should use acceptance-aware
* steering instead of public SDK queueing.
*/
function queueAgentHarnessMessage(sessionId, text, options) {
	return queueEmbeddedAgentMessageWithOutcome(sessionId, text, options).queued;
}
/** Detect prompt image references and load them through the same limits used by embedded runs. */
async function detectAndLoadAgentHarnessPromptImages(params) {
	const [{ resolveImageSanitizationLimits }, { detectAndLoadPromptImages }, { MAX_IMAGE_BYTES }] = await Promise.all([
		import("./image-sanitization-BghTEphW.js"),
		import("./images-CeJb0gMk.js"),
		import("./media-core/constants.js")
	]);
	return detectAndLoadPromptImages({
		prompt: params.prompt,
		workspaceDir: params.workspaceDir,
		model: params.model,
		existingImages: params.existingImages,
		imageOrder: params.imageOrder,
		maxBytes: MAX_IMAGE_BYTES,
		maxDimensionPx: resolveImageSanitizationLimits(params.config).maxDimensionPx,
		workspaceOnly: params.workspaceOnly,
		localRoots: params.localRoots,
		sandbox: params.sandbox
	});
}
/** Load Codex bundle MCP thread config without forcing the heavy config module into SDK imports. */
async function loadCodexBundleMcpThreadConfig(params) {
	const { loadCodexBundleMcpThreadConfig: load } = await import("./codex-mcp-config-cZFqtY6q.js");
	return load(params);
}
/** Infer compact display metadata for one tool invocation from its name and arguments. */
function inferToolMetaFromArgs(toolName, args, options) {
	return formatToolDetail(resolveToolDisplay({
		name: toolName,
		args,
		detailMode: options?.detailMode
	}));
}
/**
* Prepare verbose tool output for user-facing progress messages.
*/
function formatToolProgressOutput(output, options) {
	const trimmed = output.replace(/\r\n/g, "\n").replace(/\r/g, "\n").trim();
	if (!trimmed) return;
	const redacted = redactToolDetail(trimmed);
	const maxChars = options?.maxChars ?? 8e3;
	if (redacted.length <= maxChars) return redacted;
	return `${truncateUtf16Safe(redacted, maxChars)}\n...(truncated)...`;
}
/**
* Classify terminal harness turns that completed without assistant output that
* should advance fallback. Deliberate silent replies such as NO_REPLY count as
* intentional output, while whitespace-only text remains fallback-eligible.
* This is intentionally SDK-level so plugin harness adapters such as Codex
* preserve the same OpenClaw-owned fallback signals as the built-in OpenClaw path
* without re-implementing terminal-result policy.
*/
function classifyAgentHarnessTerminalOutcome(params) {
	if (!params.turnCompleted || params.promptError !== void 0 && params.promptError !== null || hasVisibleAssistantText(params.assistantTexts)) return;
	if (params.planText?.trim()) return "planning-only";
	if (params.reasoningText?.trim()) return "reasoning-only";
	return "empty";
}
function hasVisibleAssistantText(assistantTexts) {
	return assistantTexts.some((text) => text.trim().length > 0);
}
//#endregion
export { inferToolMetaFromArgs as a, createCodexAppServerToolResultExtensionRunner as c, runAgentHarnessBeforeCompactionHook as d, formatToolProgressOutput as i, resolveAgentHarnessBeforePromptBuildResult as l, classifyAgentHarnessTerminalOutcome as n, loadCodexBundleMcpThreadConfig as o, detectAndLoadAgentHarnessPromptImages as r, queueAgentHarnessMessage as s, TOOL_PROGRESS_OUTPUT_MAX_CHARS as t, runAgentHarnessAfterCompactionHook as u };
