import { i as formatErrorMessage } from "./errors-DNvW4XW_.js";
import "./store-CWhnH-Ye.js";
import { r as resolveDefaultSessionStorePath } from "./paths-BcGVZo_k.js";
import { V as resolveSessionStoreEntry, t as loadSessionStore } from "./store-load-S40KNQ3r.js";
import { L as isTranscriptOnlyOpenClawAssistantModel, P as streamSessionTranscriptLinesReverse, R as redactTranscriptMessage, _ as persistSessionTranscriptTurn, z as resolveAndPersistSessionFile } from "./session-accessor-ArmkJJUW.js";
import { n as extractAssistantVisibleText } from "./chat-message-content-DacpWQXQ.js";
import path from "node:path";
//#region src/config/sessions/transcript-mirror.ts
function stripQuery(value) {
	const noHash = value.split("#")[0] ?? value;
	return noHash.split("?")[0] ?? noHash;
}
function extractFileNameFromMediaUrl(value) {
	const trimmed = value.trim();
	if (!trimmed) return null;
	const cleaned = stripQuery(trimmed);
	try {
		const parsed = new URL(cleaned);
		const base = path.basename(parsed.pathname);
		if (!base) return null;
		try {
			return decodeURIComponent(base);
		} catch {
			return base;
		}
	} catch {
		const base = path.basename(cleaned);
		if (!base || base === "/" || base === ".") return null;
		return base;
	}
}
/** Resolves compact text to mirror into session transcripts for text or media messages. */
function resolveMirroredTranscriptText(params) {
	const mediaUrls = params.mediaUrls?.filter((url) => url && url.trim()) ?? [];
	if (mediaUrls.length > 0) {
		const names = mediaUrls.map((url) => extractFileNameFromMediaUrl(url)).filter((name) => Boolean(name && name.trim()));
		if (names.length > 0) return names.join(", ");
		return "media";
	}
	const trimmed = (params.text ?? "").trim();
	return trimmed ? trimmed : null;
}
//#endregion
//#region src/config/sessions/transcript.ts
function applyBeforeMessageWriteToAssistant(params) {
	if (!params.beforeMessageWrite) return params.message;
	const nextMessage = params.beforeMessageWrite({
		message: params.message,
		...params.agentId ? { agentId: params.agentId } : {},
		sessionKey: params.sessionKey
	});
	if (nextMessage?.role !== "assistant") return;
	return {
		...nextMessage,
		...params.explicitIdempotencyKey ? { idempotencyKey: params.explicitIdempotencyKey } : {}
	};
}
function parseAssistantTranscriptText(line, options) {
	const parsed = JSON.parse(line);
	const message = parsed.message;
	if (!message || message.role !== "assistant") return;
	if (options?.excludeTranscriptOnlyOpenClawAssistant && isTranscriptOnlyOpenClawAssistantMessage(message)) return;
	const text = extractAssistantVisibleText(message)?.trim();
	if (!text) return;
	return {
		...typeof parsed.id === "string" && parsed.id ? { id: parsed.id } : {},
		text,
		...typeof message.timestamp === "number" && Number.isFinite(message.timestamp) ? { timestamp: message.timestamp } : {}
	};
}
function isTranscriptOnlyOpenClawAssistantMessage(message) {
	return isTranscriptOnlyOpenClawAssistantModel(message.provider, message.model);
}
async function readLatestAssistantTextFromSessionTranscript(sessionFile) {
	if (!sessionFile?.trim()) return;
	for await (const line of streamSessionTranscriptLinesReverse(sessionFile)) try {
		const assistantText = parseAssistantTranscriptText(line, { excludeTranscriptOnlyOpenClawAssistant: true });
		if (assistantText) return assistantText;
	} catch {
		continue;
	}
}
async function readTailAssistantTextFromSessionTranscript(sessionFile) {
	if (!sessionFile?.trim()) return;
	for await (const line of streamSessionTranscriptLinesReverse(sessionFile)) try {
		const parsed = JSON.parse(line);
		if (!parsed.message || typeof parsed.message !== "object") continue;
		return parseAssistantTranscriptText(line);
	} catch {
		continue;
	}
}
async function appendAssistantMessageToSessionTranscript(params) {
	const sessionKey = params.sessionKey.trim();
	if (!sessionKey) return {
		ok: false,
		reason: "missing sessionKey"
	};
	const mirrorText = resolveMirroredTranscriptText({
		text: params.text,
		mediaUrls: params.mediaUrls
	});
	if (!mirrorText) return {
		ok: false,
		reason: "empty text"
	};
	return appendExactAssistantMessageToSessionTranscript({
		agentId: params.agentId,
		sessionKey,
		...params.expectedSessionId ? { expectedSessionId: params.expectedSessionId } : {},
		storePath: params.storePath,
		idempotencyKey: params.idempotencyKey,
		updateMode: params.updateMode,
		config: params.config,
		...params.beforeMessageWrite ? { beforeMessageWrite: params.beforeMessageWrite } : {},
		message: {
			role: "assistant",
			content: [{
				type: "text",
				text: mirrorText
			}],
			api: "openai-responses",
			provider: "openclaw",
			model: "delivery-mirror",
			usage: {
				input: 0,
				output: 0,
				cacheRead: 0,
				cacheWrite: 0,
				totalTokens: 0,
				cost: {
					input: 0,
					output: 0,
					cacheRead: 0,
					cacheWrite: 0,
					total: 0
				}
			},
			stopReason: "stop",
			timestamp: Date.now(),
			...params.deliveryMirror ? { openclawDeliveryMirror: params.deliveryMirror } : {}
		}
	});
}
async function appendExactAssistantMessageToSessionTranscript(params) {
	const sessionKey = params.sessionKey.trim();
	if (!sessionKey) return {
		ok: false,
		reason: "missing sessionKey"
	};
	if (params.message.role !== "assistant") return {
		ok: false,
		reason: "message role must be assistant"
	};
	const storePath = params.storePath ?? resolveDefaultSessionStorePath(params.agentId);
	const store = loadSessionStore(storePath, { skipCache: true });
	const resolved = resolveSessionStoreEntry({
		store,
		sessionKey
	});
	const entry = resolved.existing;
	if (params.expectedSessionId && entry?.sessionId !== params.expectedSessionId) return {
		ok: false,
		code: "session-rebound",
		reason: `session rebound for sessionKey: ${sessionKey}`
	};
	if (!entry?.sessionId) return {
		ok: false,
		reason: `unknown sessionKey: ${sessionKey}`
	};
	const appendToSessionFile = async (currentEntry, sessionFile) => {
		const explicitIdempotencyKey = params.idempotencyKey ?? params.message.idempotencyKey;
		const message = {
			...params.message,
			...explicitIdempotencyKey ? { idempotencyKey: explicitIdempotencyKey } : {}
		};
		const preparedUnkeyedMessage = !explicitIdempotencyKey && params.beforeMessageWrite ? applyBeforeMessageWriteToAssistant({
			message,
			beforeMessageWrite: params.beforeMessageWrite,
			agentId: params.agentId,
			sessionKey: resolved.normalizedKey
		}) : message;
		if (!preparedUnkeyedMessage) return {
			ok: false,
			code: "blocked",
			reason: "blocked by before_message_write"
		};
		const identifiedChannelFinal = Boolean(explicitIdempotencyKey) && isChannelFinalDeliveryMirror(params.message);
		let latestEquivalentAssistantId;
		const turn = await persistSessionTranscriptTurn({
			sessionId: currentEntry.sessionId,
			sessionKey: resolved.normalizedKey,
			storePath,
			...sessionFile ? { sessionFile } : {},
			...params.agentId ? { agentId: params.agentId } : {}
		}, {
			cwd: currentEntry.spawnedCwd,
			...params.expectedSessionId ? { expectedSessionId: params.expectedSessionId } : {},
			...params.config ? { config: params.config } : {},
			updateMode: params.updateMode ?? "inline",
			touchSessionEntry: true,
			messages: [{
				message: preparedUnkeyedMessage,
				...explicitIdempotencyKey ? { idempotencyLookup: "scan" } : {},
				...explicitIdempotencyKey && params.beforeMessageWrite ? { prepareMessageAfterIdempotencyCheck: (candidate) => applyBeforeMessageWriteToAssistant({
					message: candidate,
					beforeMessageWrite: params.beforeMessageWrite,
					explicitIdempotencyKey,
					agentId: params.agentId,
					sessionKey: resolved.normalizedKey
				}) } : {},
				shouldAppend: async (target) => {
					latestEquivalentAssistantId = isRedundantDeliveryMirror(params.message) && !identifiedChannelFinal ? await findLatestEquivalentAssistantMessageId(target.sessionFile, preparedUnkeyedMessage, params.config) : void 0;
					return !latestEquivalentAssistantId;
				}
			}]
		});
		if (turn.rejectedReason === "session-rebound") return {
			ok: false,
			code: "session-rebound",
			reason: `session rebound for sessionKey: ${sessionKey}`
		};
		if (latestEquivalentAssistantId) return {
			ok: true,
			sessionFile: turn.sessionFile,
			messageId: latestEquivalentAssistantId
		};
		const appendedResult = turn.messages[0];
		if (!appendedResult) return {
			ok: false,
			code: "blocked",
			reason: "blocked by before_message_write"
		};
		const { messageId } = appendedResult;
		return {
			ok: true,
			sessionFile: turn.sessionFile,
			messageId
		};
	};
	let result;
	if (params.expectedSessionId) result = await appendToSessionFile(entry);
	else {
		let sessionFile;
		try {
			sessionFile = (await resolveAndPersistSessionFile({
				sessionId: entry.sessionId,
				sessionKey: resolved.normalizedKey,
				sessionStore: store,
				storePath,
				sessionEntry: entry,
				agentId: params.agentId,
				sessionsDir: path.dirname(storePath)
			})).sessionFile;
		} catch (err) {
			return {
				ok: false,
				reason: formatErrorMessage(err)
			};
		}
		result = await appendToSessionFile(entry, sessionFile);
	}
	return result;
}
function isRedundantDeliveryMirror(message) {
	return message.provider === "openclaw" && message.model === "delivery-mirror";
}
function isChannelFinalDeliveryMirror(message) {
	const marker = message.openclawDeliveryMirror;
	return isRedundantDeliveryMirror(message) && marker?.kind === "channel-final";
}
function extractAssistantMessageText(message) {
	if (!Array.isArray(message.content)) return null;
	const parts = message.content.filter((part) => part.type === "text" && typeof part.text === "string" && part.text.trim().length > 0).map((part) => part.text.trim());
	return parts.length > 0 ? parts.join("\n").trim() : null;
}
async function findLatestEquivalentAssistantMessageId(transcriptPath, message, config) {
	const expectedText = extractAssistantMessageText(redactTranscriptMessage(message, config));
	if (!expectedText) return;
	for await (const line of streamSessionTranscriptLinesReverse(transcriptPath)) try {
		const parsed = JSON.parse(line);
		const candidate = parsed.message;
		if (!candidate || candidate.role !== "assistant") continue;
		if (extractAssistantMessageText(redactTranscriptMessage(candidate, config)) !== expectedText) return;
		if (typeof parsed.id === "string" && parsed.id) return parsed.id;
		return;
	} catch {
		continue;
	}
}
//#endregion
export { resolveMirroredTranscriptText as a, readTailAssistantTextFromSessionTranscript as i, appendExactAssistantMessageToSessionTranscript as n, readLatestAssistantTextFromSessionTranscript as r, appendAssistantMessageToSessionTranscript as t };
