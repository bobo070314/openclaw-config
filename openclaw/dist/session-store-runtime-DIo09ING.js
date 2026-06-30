import "./store-CWhnH-Ye.js";
import "./paths-BcGVZo_k.js";
import { t as loadSessionStore$1 } from "./store-load-S40KNQ3r.js";
import { O as updateSessionEntry, S as replaceSessionEntry, f as loadSessionEntry, m as patchSessionEntry$1, u as listSessionEntries$1, x as readSessionUpdatedAt$1 } from "./session-accessor-ArmkJJUW.js";
import "./reset-BZy-g5ii.js";
import "./session-key-BnYUuBC1.js";
import "./transcript-D8-u9kVs.js";
import "./send-policy-2vcMBHiq.js";
//#region src/plugin-sdk/session-store-runtime.ts
function toSessionAccessScope(params) {
	return {
		sessionKey: params.sessionKey,
		...params.agentId !== void 0 ? { agentId: params.agentId } : {},
		...params.env !== void 0 ? { env: params.env } : {},
		...params.hydrateSkillPromptRefs !== void 0 ? { hydrateSkillPromptRefs: params.hydrateSkillPromptRefs } : {},
		...params.storePath !== void 0 ? { storePath: params.storePath } : {}
	};
}
/**
* @deprecated Use getSessionEntry/listSessionEntries for reads and
* patchSessionEntry/upsertSessionEntry for writes. This whole-store helper is
* kept only during the transition before SQLite migration. Callers must
* migrate away from reading sessions.json directly.
*/
const loadSessionStore = loadSessionStore$1;
/** Loads one session entry by agent/session identity. */
function getSessionEntry(params) {
	return loadSessionEntry(toSessionAccessScope(params));
}
/** Lists session entries for one agent. */
function listSessionEntries(params = {}) {
	return listSessionEntries$1({
		...params.agentId !== void 0 ? { agentId: params.agentId } : {},
		...params.env !== void 0 ? { env: params.env } : {},
		...params.hydrateSkillPromptRefs !== void 0 ? { hydrateSkillPromptRefs: params.hydrateSkillPromptRefs } : {},
		...params.storePath !== void 0 ? { storePath: params.storePath } : {}
	});
}
/** Patches one session entry by agent/session identity. */
async function patchSessionEntry(params) {
	return await patchSessionEntry$1(toSessionAccessScope(params), params.update, {
		fallbackEntry: params.fallbackEntry,
		maintenanceConfig: params.maintenanceConfig,
		preserveActivity: params.preserveActivity,
		replaceEntry: params.replaceEntry
	});
}
/** Reads the last activity timestamp for one session entry. */
function readSessionUpdatedAt(params) {
	return readSessionUpdatedAt$1(toSessionAccessScope(params));
}
/** Updates an existing session entry by store path and session key. */
async function updateSessionStoreEntry(params) {
	return await updateSessionEntry({
		sessionKey: params.sessionKey,
		storePath: params.storePath
	}, params.update, {
		skipMaintenance: params.skipMaintenance,
		takeCacheOwnership: params.takeCacheOwnership,
		requireWriteSuccess: params.requireWriteSuccess
	});
}
/** Replaces or creates one session entry by agent/session identity. */
async function upsertSessionEntry(params) {
	await replaceSessionEntry(toSessionAccessScope(params), params.entry);
}
//#endregion
export { readSessionUpdatedAt as a, patchSessionEntry as i, listSessionEntries as n, updateSessionStoreEntry as o, loadSessionStore as r, upsertSessionEntry as s, getSessionEntry as t };
