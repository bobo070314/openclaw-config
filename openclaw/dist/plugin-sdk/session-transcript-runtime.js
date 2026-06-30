import { u as normalizeAgentId } from "../session-key-BsbwBJwv.js";
import { E as resolveSessionTranscriptRuntimeTarget, M as runSessionTranscriptAppendTransaction, N as streamSessionTranscriptLines, T as resolveSessionTranscriptRuntimeReadTarget, n as appendTranscriptMessage, y as publishTranscriptUpdate } from "../session-accessor-ArmkJJUW.js";
import { n as parseSessionTranscriptMemoryHitKey, r as resolveSessionTranscriptMemoryHitKeyToSessionKeys, t as formatSessionTranscriptMemoryHitKey } from "../session-transcript-memory-hit-Q-JS7EW2.js";
//#region src/plugin-sdk/session-transcript-runtime.ts
/**
* Resolves the public identity for a transcript without returning its file path.
*/
async function resolveSessionTranscriptIdentity(params) {
	const target = await resolveSessionTranscriptRuntimeReadTarget(params);
	const agentId = normalizeAgentId(target.agentId);
	return {
		agentId,
		memoryKey: formatSessionTranscriptMemoryHitKey({
			agentId,
			sessionId: target.sessionId
		}),
		sessionId: target.sessionId,
		sessionKey: target.sessionKey
	};
}
/**
* Resolves the public target for transcript operations without exposing the
* current storage path as identity.
*/
async function resolveSessionTranscriptTarget(params) {
	return projectPublicTarget({
		...await resolveSessionTranscriptRuntimeReadTarget(params),
		targetKind: params.sessionFile?.trim() ? "active-session-file" : "runtime-session"
	});
}
/**
* Reads transcript events by public session identity instead of file path.
*/
async function readSessionTranscriptEvents(params) {
	const target = await resolveSessionTranscriptRuntimeReadTarget(params);
	const events = [];
	for await (const line of streamSessionTranscriptLines(target.sessionFile)) try {
		events.push(JSON.parse(line));
	} catch {
		continue;
	}
	return events;
}
/**
* Appends a transcript message by scoped transcript target.
*/
async function appendSessionTranscriptMessageByIdentity(params) {
	return await appendTranscriptMessage(params, params);
}
/**
* Publishes a transcript update by scoped transcript target.
*/
async function publishSessionTranscriptUpdateByIdentity(params) {
	const target = await resolveSessionTranscriptRuntimeTarget(params);
	await publishTranscriptUpdate({
		...params,
		sessionFile: target.sessionFile
	}, {
		...params.update,
		agentId: target.agentId,
		sessionKey: target.sessionKey
	});
}
/**
* Runs transcript work under the write lock for the resolved scoped target.
*/
async function withSessionTranscriptWriteLock(params, run) {
	const storageTarget = await resolveSessionTranscriptRuntimeTarget(params);
	const target = projectPublicTarget({
		...storageTarget,
		targetKind: params.sessionFile?.trim() ? "active-session-file" : "runtime-session"
	});
	const boundScope = {
		...params,
		sessionFile: storageTarget.sessionFile
	};
	const queuedUpdates = [];
	const result = await runSessionTranscriptAppendTransaction({
		config: params.config,
		transcriptPath: storageTarget.sessionFile
	}, (transaction) => run({
		target,
		readEvents: () => readSessionTranscriptEvents(boundScope),
		appendMessage: (options) => transaction.appendMessage({
			...options,
			sessionId: params.sessionId
		}),
		publishUpdate: async (update) => {
			queuedUpdates.push(update ? { ...update } : void 0);
		}
	}));
	for (const update of queuedUpdates) await publishSessionTranscriptUpdateByIdentity({
		...boundScope,
		update
	});
	return result;
}
function projectPublicTarget(target) {
	const agentId = normalizeAgentId(target.agentId);
	return {
		agentId,
		memoryKey: formatSessionTranscriptMemoryHitKey({
			agentId,
			sessionId: target.sessionId
		}),
		sessionId: target.sessionId,
		sessionKey: target.sessionKey,
		targetKind: target.targetKind
	};
}
//#endregion
export { appendSessionTranscriptMessageByIdentity, formatSessionTranscriptMemoryHitKey, parseSessionTranscriptMemoryHitKey, publishSessionTranscriptUpdateByIdentity, readSessionTranscriptEvents, resolveSessionTranscriptIdentity, resolveSessionTranscriptMemoryHitKeyToSessionKeys, resolveSessionTranscriptTarget, withSessionTranscriptWriteLock };
