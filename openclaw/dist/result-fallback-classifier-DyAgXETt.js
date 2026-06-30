import { a as isGpt5ModelId } from "./gpt5-prompt-overlay-BQUfH6bC.js";
import { i as isSilentReplyPayloadText } from "./tokens-DD1fz8gG.js";
import { r as classifyFailoverReason } from "./errors-BmvajW3H.js";
import { f as hasVisibleAgentPayload, l as hasCommittedOutboundDeliveryEvidence } from "./subagent-announce-delivery-PPEx8SZk.js";
//#region src/agents/embedded-agent-runner/result-fallback-classifier.ts
/**
* Classifies embedded-agent run results for model fallback decisions.
*/
/**
* Classifies embedded-agent terminal results for model fallback decisions.
*
* The classifier only flags failed invisible outcomes; delivered messages, deliberate silent
* replies, hook blocks, and aborts must not trigger another model attempt.
*/
function isEmbeddedAgentRunResult(value) {
	return Boolean(value && typeof value === "object" && "meta" in value && value.meta && typeof value.meta === "object");
}
/** Keeps final-candidate bookkeeping while surfacing the best trusted terminal payload. */
function mergeEmbeddedAgentRunResultForModelFallbackExhaustion(params) {
	const executionTrace = params.latestResult.meta.executionTrace;
	const filteredAttempts = executionTrace?.attempts?.filter((attempt) => attempt.result !== "success");
	const traceNeedsNormalization = executionTrace !== void 0 && (executionTrace.winnerProvider !== void 0 || executionTrace.winnerModel !== void 0 || filteredAttempts?.length !== executionTrace.attempts?.length);
	if (params.latestResult === params.preferredResult && !traceNeedsNormalization) return params.latestResult;
	return {
		...params.latestResult,
		payloads: params.preferredResult.payloads,
		meta: {
			...params.latestResult.meta,
			error: params.preferredResult.meta.error,
			...traceNeedsNormalization ? { executionTrace: {
				...executionTrace,
				winnerProvider: void 0,
				winnerModel: void 0,
				attempts: filteredAttempts?.length ? filteredAttempts : void 0
			} } : {}
		}
	};
}
function hasDeliberateSilentTerminalReply(result) {
	if (result.meta.error?.kind === "hook_block") return true;
	return [result.meta.finalAssistantRawText, result.meta.finalAssistantVisibleText].some((text) => typeof text === "string" && isSilentReplyPayloadText(text));
}
function classifyHarnessResult(params) {
	switch (params.result.meta.agentHarnessResultClassification) {
		case "empty": return {
			message: `${params.provider}/${params.model} ended without a visible assistant reply`,
			reason: "format",
			code: "empty_result"
		};
		case "reasoning-only": return {
			message: `${params.provider}/${params.model} ended with reasoning only`,
			reason: "format",
			code: "reasoning_only_result"
		};
		case "planning-only": return {
			message: `${params.provider}/${params.model} ended with a structured plan but no final answer`,
			reason: "format",
			code: "planning_only_result"
		};
		default: return null;
	}
}
/** Maps provider error payloads to fallback-safe business reasons. */
function classifyBusinessDenialErrorPayloadReason(errorText, provider) {
	if (!errorText.trim()) return null;
	const failoverReason = classifyFailoverReason(errorText, { provider });
	switch (failoverReason) {
		case "auth":
		case "auth_permanent":
		case "billing": return failoverReason;
		default: return null;
	}
}
/** Returns a fallback classification when an embedded run failed without user-visible output. */
function classifyEmbeddedAgentRunResultForModelFallback(params) {
	if (!isEmbeddedAgentRunResult(params.result)) return null;
	if (params.result.meta.aborted || params.hasDirectlySentBlockReply === true || params.hasBlockReplyPipelineOutput === true || hasVisibleAgentPayload(params.result, {
		includeErrorPayloads: false,
		includeReasoningPayloads: false
	})) return null;
	const incompleteTurn = params.result.meta.error?.kind === "incomplete_turn";
	if (incompleteTurn && params.result.meta.error?.fallbackSafe !== true) return null;
	const fallbackSafeIncompleteTurn = incompleteTurn;
	if (params.result.meta.replayInvalid === true && !fallbackSafeIncompleteTurn) return null;
	if (hasCommittedOutboundDeliveryEvidence(params.result)) return null;
	if (params.result.meta.error?.kind === "hook_block") return null;
	const payloads = params.result.payloads ?? [];
	if (fallbackSafeIncompleteTurn) return {
		message: payloads.find((payload) => payload.isError === true && typeof payload.text === "string")?.text ?? `${params.provider}/${params.model} ended with an incomplete terminal response`,
		reason: "format",
		code: "incomplete_result",
		preserveResultOnExhaustion: true,
		preserveResultPriority: params.result.meta.error?.terminalPresentation === true ? 1 : 0
	};
	const harnessClassification = classifyHarnessResult({
		provider: params.provider,
		model: params.model,
		result: params.result
	});
	if (harnessClassification) return harnessClassification;
	const errorText = payloads.filter((payload) => payload?.isError === true).map((payload) => typeof payload.text === "string" ? payload.text : "").join("\n");
	const failoverReason = classifyBusinessDenialErrorPayloadReason(errorText, params.provider);
	if (failoverReason) return {
		message: `${params.provider}/${params.model} ended with a provider error: ${errorText}`,
		reason: failoverReason,
		code: "embedded_error_payload",
		rawError: errorText
	};
	if (!isGpt5ModelId(params.model)) return null;
	if (payloads.length === 0 && hasDeliberateSilentTerminalReply(params.result)) return null;
	if (payloads.length === 0) return {
		message: `${params.provider}/${params.model} ended without a visible assistant reply`,
		reason: "format",
		code: "empty_result"
	};
	if (payloads.every((payload) => payload.isReasoning === true)) return {
		message: `${params.provider}/${params.model} ended with reasoning only`,
		reason: "format",
		code: "reasoning_only_result"
	};
	return null;
}
//#endregion
export { mergeEmbeddedAgentRunResultForModelFallbackExhaustion as n, classifyEmbeddedAgentRunResultForModelFallback as t };
