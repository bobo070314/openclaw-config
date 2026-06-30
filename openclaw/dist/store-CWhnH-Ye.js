import { a as normalizeLowercaseStringOrEmpty, c as normalizeOptionalString, s as normalizeOptionalLowercaseString } from "./string-coerce-DW4mBlAt.js";
import { i as normalizeHyphenSlug } from "./string-normalization-CRyoFBPt.js";
import { t as createSubsystemLogger } from "./subsystem-BTVUlTIB.js";
import { s as writeTextAtomic } from "./json-files-2umMHm0W.js";
import "./agent-scope-CESPhp3L.js";
import { c as parseAgentSessionKey, o as normalizeSessionKeyPreservingOpaquePeerIds, s as normalizeSessionPeerId } from "./session-key-utils-C7uT9A4s.js";
import { d as normalizeMainKey, f as resolveAgentIdFromSessionKey, u as normalizeAgentId } from "./session-key-BsbwBJwv.js";
import { c as resolveDefaultAgentId, n as listAgentIds } from "./agent-scope-config-ChfGvhEr.js";
import { t as runTasksWithConcurrency } from "./run-with-concurrency-DivrDqxu.js";
import { i as getRuntimeConfig } from "./io-CwmOK6NP.js";
import { i as resolveMainSessionKey, t as canonicalizeMainSessionAlias } from "./main-session-CW3WnlFi.js";
import { i as mergeDeliveryContext, n as deliveryContextFromSession, o as normalizeDeliveryContext, s as normalizeSessionDeliveryFields, t as deliveryContextFromChannelRoute } from "./delivery-context.shared-BjCF5MAj.js";
import { f as formatSessionArchiveTimestamp, g as isSessionStoreTempArtifactName, h as isSessionArchiveArtifactName, i as resolveSessionFilePath, m as isPrimarySessionTranscriptFileName, p as isCompactionCheckpointTranscriptFileName, u as resolveStorePath, y as isTrajectorySessionArtifactName } from "./paths-BcGVZo_k.js";
import { C as capEntryCount, O as shouldPreserveMaintenanceEntry, P as getFileStatSnapshot, S as writeSessionStoreCache, T as pruneStaleEntries, V as resolveSessionStoreEntry, _ as invalidateSessionStoreCache, b as setSerializedSessionStorePromptRefs, d as cloneSessionStoreRecord, f as dropSessionStoreObjectCache, h as getSerializedSessionStorePromptRefs, i as readSessionEntry, k as shouldRunSessionEntryMaintenance, m as getSerializedSessionStore, n as normalizeSessionStore, o as resolveMaintenanceConfig, p as dropSessionStoreSnapshotCache, r as readSessionEntries, s as collectSessionMaintenancePreserveKeys, t as loadSessionStore, u as clearSessionStoreCaches, v as isSessionStoreCacheEnabled, w as getActiveSessionMaintenanceWarning, x as takeMutableSessionStoreCache, y as setSerializedSessionStore } from "./store-load-S40KNQ3r.js";
import { t as emitSessionTranscriptUpdate } from "./transcript-events-bo5V8PHW.js";
import { a as resolveTrajectoryPointerFilePath, i as resolveTrajectoryFilePath } from "./paths-Biq9XkB5.js";
import { a as projectSessionStoreForPersistence, i as isSessionSkillPromptBlobReadable, n as ensureSessionStorePromptBlobsForPersistence } from "./skill-prompt-blobs-CzsZaj42.js";
import { a as normalizeChannelId, i as listChannelPlugins, n as getLoadedChannelPlugin } from "./registry-CK5ins3w2.js";
import { t as normalizeChatType } from "./chat-type-BARlA53h.js";
import { t as resolveConversationLabel } from "./conversation-label-pgUV7Er9.js";
import "./plugins-Ys7IxLOo.js";
import { i as normalizeMessageChannel, r as listDeliverableMessageChannels } from "./message-channel-normalize-B2zqLi2s.js";
import "./message-channel-CtiNqfW0.js";
import { i as mergeSessionEntryPreserveActivity, r as mergeSessionEntry } from "./types-CoDcFuoc.js";
import { n as runQueuedStoreWrite, t as clearStoreWriterQueuesForTest } from "./store-writer-queue-Cs_NM_XG.js";
import "./version-Bsehiavt.js";
import fs from "node:fs";
import path from "node:path";
//#region src/gateway/session-store-key.ts
/** Canonicalize an opaque session key into the agent-scoped store namespace. */
function canonicalizeSessionKeyForAgent(agentId, key) {
	const lowered = normalizeLowercaseStringOrEmpty(key);
	if (lowered === "global" || lowered === "unknown") return lowered;
	const normalized = normalizeSessionKeyPreservingOpaquePeerIds(key);
	if (normalized.startsWith("agent:")) return normalized;
	return `agent:${normalizeAgentId(agentId)}:${normalized}`;
}
function resolveDefaultStoreAgentId(cfg) {
	return normalizeAgentId(resolveDefaultAgentId(cfg));
}
function shouldRemapLegacyDefaultMainAlias(cfg, parsed, options) {
	if (normalizeAgentId(parsed.agentId) !== "main" || listAgentIds(cfg).includes("main")) return false;
	const defaultAgentId = resolveDefaultStoreAgentId(cfg);
	if (options?.storeAgentId && normalizeAgentId(options.storeAgentId) !== defaultAgentId) return false;
	const rest = normalizeLowercaseStringOrEmpty(parsed.rest);
	const mainKey = normalizeMainKey(cfg.session?.mainKey);
	return rest === "main" || rest === mainKey;
}
function resolveParsedSessionStoreKey(cfg, raw, parsed, options) {
	if (!shouldRemapLegacyDefaultMainAlias(cfg, parsed, options)) return {
		agentId: normalizeAgentId(parsed.agentId),
		sessionKey: normalizeSessionKeyPreservingOpaquePeerIds(raw)
	};
	const agentId = resolveDefaultStoreAgentId(cfg);
	return {
		agentId,
		sessionKey: `agent:${agentId}:${normalizeLowercaseStringOrEmpty(parsed.rest)}`
	};
}
/** Resolve any incoming session key into the canonical key used in persisted session stores. */
function resolveSessionStoreKey(params) {
	const raw = normalizeOptionalString(params.sessionKey) ?? "";
	if (!raw) return raw;
	const rawLower = normalizeLowercaseStringOrEmpty(raw);
	if (rawLower === "global" || rawLower === "unknown") return rawLower;
	const parsed = parseAgentSessionKey(raw);
	if (parsed) {
		const resolved = resolveParsedSessionStoreKey(params.cfg, raw, parsed, { storeAgentId: params.storeAgentId });
		const canonical = canonicalizeMainSessionAlias({
			cfg: params.cfg,
			agentId: resolved.agentId,
			sessionKey: resolved.sessionKey
		});
		if (canonical !== resolved.sessionKey) return canonical;
		return resolved.sessionKey;
	}
	const lowered = normalizeLowercaseStringOrEmpty(raw);
	const rawMainKey = normalizeMainKey(params.cfg.session?.mainKey);
	if (lowered === "main" || lowered === rawMainKey) return resolveMainSessionKey(params.cfg);
	return canonicalizeSessionKeyForAgent(resolveDefaultStoreAgentId(params.cfg), raw);
}
/** Resolve the agent that owns a canonical session-store key. */
function resolveSessionStoreAgentId(cfg, canonicalKey) {
	if (canonicalKey === "global" || canonicalKey === "unknown") return resolveDefaultStoreAgentId(cfg);
	const parsed = parseAgentSessionKey(canonicalKey);
	if (parsed?.agentId) return normalizeAgentId(parsed.agentId);
	return resolveDefaultStoreAgentId(cfg);
}
/** Resolve a session key for lookup inside a specific agent's store. */
function resolveStoredSessionKeyForAgentStore(params) {
	const raw = normalizeOptionalString(params.sessionKey) ?? "";
	if (!raw) return raw;
	const lowered = normalizeLowercaseStringOrEmpty(raw);
	if (lowered === "global" || lowered === "unknown") return lowered;
	const key = parseAgentSessionKey(raw) ? raw : canonicalizeSessionKeyForAgent(params.agentId, raw);
	return resolveSessionStoreKey({
		cfg: params.cfg,
		sessionKey: key,
		storeAgentId: params.agentId
	});
}
/** Resolve the owner agent for a stored session key, returning null for global/unknown keys. */
function resolveStoredSessionOwnerAgentId(params) {
	const canonicalKey = resolveStoredSessionKeyForAgentStore(params);
	if (canonicalKey === "global" || canonicalKey === "unknown") return null;
	return resolveSessionStoreAgentId(params.cfg, canonicalKey);
}
/** Canonicalize spawned-by parent references while preserving main-session aliases. */
function canonicalizeSpawnedByForAgent(cfg, agentId, spawnedBy) {
	const raw = normalizeOptionalString(spawnedBy) ?? "";
	if (!raw) return;
	const lower = normalizeLowercaseStringOrEmpty(raw);
	if (lower === "global" || lower === "unknown") return lower;
	let result;
	const normalized = normalizeSessionKeyPreservingOpaquePeerIds(raw);
	if (normalized.startsWith("agent:")) result = normalized;
	else result = `agent:${normalizeAgentId(agentId)}:${normalized}`;
	const parsed = parseAgentSessionKey(result);
	return canonicalizeMainSessionAlias({
		cfg,
		agentId: parsed?.agentId ? normalizeAgentId(parsed.agentId) : agentId,
		sessionKey: result
	});
}
//#endregion
//#region src/config/sessions/disk-budget.ts
const NOOP_LOGGER = {
	warn: () => {},
	info: () => {}
};
function canonicalizePathForComparison(filePath) {
	const resolved = path.resolve(filePath);
	try {
		return fs.realpathSync(resolved);
	} catch {
		return resolved;
	}
}
function measureStoreBytes(store) {
	return Buffer.byteLength(JSON.stringify(store, null, 2), "utf-8");
}
function measureStoreEntryChunkBytes(key, entry) {
	const singleEntryStore = JSON.stringify({ [key]: entry }, null, 2);
	if (!singleEntryStore.startsWith("{\n") || !singleEntryStore.endsWith("\n}")) return measureStoreBytes({ [key]: entry }) - 4;
	const chunk = singleEntryStore.slice(2, -2);
	return Buffer.byteLength(chunk, "utf-8");
}
function buildStoreEntryChunkSizeMap(store) {
	const out = /* @__PURE__ */ new Map();
	for (const [key, entry] of Object.entries(store)) out.set(key, measureStoreEntryChunkBytes(key, entry));
	return out;
}
function resolveProjectedPromptBlobHash(entry) {
	const ref = entry?.skillsSnapshot?.promptRef;
	return ref?.algorithm === "sha256" && typeof ref.hash === "string" ? ref.hash : void 0;
}
function buildProjectedPromptBlobRefCounts(store) {
	const counts = /* @__PURE__ */ new Map();
	for (const entry of Object.values(store)) {
		const hash = resolveProjectedPromptBlobHash(entry);
		if (!hash) continue;
		counts.set(hash, (counts.get(hash) ?? 0) + 1);
	}
	return counts;
}
function getEntryUpdatedAt(entry) {
	if (!entry) return 0;
	const updatedAt = entry.updatedAt;
	return Number.isFinite(updatedAt) ? updatedAt : 0;
}
function buildSessionIdRefCounts(store) {
	const counts = /* @__PURE__ */ new Map();
	for (const entry of Object.values(store)) {
		const sessionId = entry?.sessionId;
		if (!sessionId) continue;
		counts.set(sessionId, (counts.get(sessionId) ?? 0) + 1);
	}
	return counts;
}
function resolveSessionTranscriptPathForEntry(params) {
	if (!params.entry.sessionId) return null;
	try {
		const resolved = resolveSessionFilePath(params.entry.sessionId, params.entry, { sessionsDir: params.sessionsDir });
		const resolvedSessionsDir = canonicalizePathForComparison(params.sessionsDir);
		const resolvedPath = canonicalizePathForComparison(resolved);
		const relative = path.relative(resolvedSessionsDir, resolvedPath);
		if (!relative || relative.startsWith("..") || path.isAbsolute(relative)) return null;
		return resolvedPath;
	} catch {
		return null;
	}
}
function resolveSessionArtifactPathsForEntry(params) {
	const transcriptPath = resolveSessionTranscriptPathForEntry(params);
	if (!transcriptPath) return [];
	const paths = [transcriptPath];
	if (params.entry.sessionId) {
		paths.push(resolveTrajectoryPointerFilePath(transcriptPath));
		paths.push(resolveTrajectoryFilePath({
			env: {},
			sessionFile: transcriptPath,
			sessionId: params.entry.sessionId
		}));
	}
	return paths;
}
function resolveSessionArtifactCanonicalPathsForEntry(params) {
	return resolveSessionArtifactPathsForEntry(params).map(canonicalizePathForComparison);
}
function resolveReferencedSessionArtifactPaths(params) {
	const referenced = /* @__PURE__ */ new Set();
	const resolvedSessionsDir = canonicalizePathForComparison(params.sessionsDir);
	for (const entry of Object.values(params.store)) {
		for (const resolved of resolveSessionArtifactCanonicalPathsForEntry({
			sessionsDir: params.sessionsDir,
			entry
		})) referenced.add(resolved);
		for (const checkpoint of entry.compactionCheckpoints ?? []) {
			const checkpointFiles = [checkpoint.preCompaction.sessionFile?.trim(), checkpoint.postCompaction.sessionFile?.trim()].filter((filePath) => Boolean(filePath));
			for (const checkpointFile of checkpointFiles) {
				const resolvedCheckpointPath = canonicalizePathForComparison(checkpointFile);
				const relative = path.relative(resolvedSessionsDir, resolvedCheckpointPath);
				if (relative && !relative.startsWith("..") && !path.isAbsolute(relative)) referenced.add(resolvedCheckpointPath);
			}
		}
	}
	return referenced;
}
const SESSIONS_DIR_STAT_CONCURRENCY = 8;
async function readSessionsDirFiles(sessionsDir) {
	const { results } = await runTasksWithConcurrency({
		tasks: (await fs.promises.readdir(sessionsDir, { withFileTypes: true }).catch(() => [])).filter((dirent) => dirent.isFile()).map((dirent) => async () => {
			const filePath = path.join(sessionsDir, dirent.name);
			const stat = await fs.promises.stat(filePath).catch(() => null);
			if (!stat?.isFile()) return null;
			return {
				path: filePath,
				canonicalPath: canonicalizePathForComparison(filePath),
				name: dirent.name,
				size: stat.size,
				mtimeMs: stat.mtimeMs
			};
		}),
		limit: SESSIONS_DIR_STAT_CONCURRENCY
	});
	return results.filter((file) => Boolean(file));
}
async function readSessionPromptBlobFiles(sessionsDir) {
	const root = path.join(sessionsDir, "skills-prompts", "sha256");
	const prefixEntries = await fs.promises.readdir(root, { withFileTypes: true }).catch(() => []);
	const files = [];
	for (const prefixEntry of prefixEntries) {
		if (!prefixEntry.isDirectory() || !/^[a-f0-9]{2}$/u.test(prefixEntry.name)) continue;
		const prefixDir = path.join(root, prefixEntry.name);
		const blobEntries = await fs.promises.readdir(prefixDir, { withFileTypes: true }).catch(() => []);
		for (const blobEntry of blobEntries) {
			if (!blobEntry.isFile() || !/^[a-f0-9]{64}\.txt$/u.test(blobEntry.name) && !isSessionPromptBlobTempArtifactName(blobEntry.name)) continue;
			const filePath = path.join(prefixDir, blobEntry.name);
			const stat = await fs.promises.stat(filePath).catch(() => null);
			if (!stat?.isFile()) continue;
			files.push({
				path: filePath,
				canonicalPath: canonicalizePathForComparison(filePath),
				name: blobEntry.name,
				size: stat.size,
				mtimeMs: stat.mtimeMs
			});
		}
	}
	return files;
}
function resolvePromptBlobFileHash(file) {
	return /^[a-f0-9]{64}\.txt$/u.test(file.name) ? file.name.slice(0, -4) : void 0;
}
function isSessionPromptBlobTempArtifactName(name) {
	return /^[a-f0-9]{64}\.txt\.(?:\d+\.)?[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.tmp$/u.test(name);
}
function isUnreferencedSessionArtifactFile(file, referencedPaths) {
	if (referencedPaths.has(file.canonicalPath)) return false;
	return isCompactionCheckpointTranscriptFileName(file.name) || isTrajectorySessionArtifactName(file.name) || isPrimarySessionTranscriptFileName(file.name);
}
const SESSION_STORE_TEMP_STALE_MS = 300 * 1e3;
const SESSION_PROMPT_BLOB_UNREFERENCED_GRACE_MS = SESSION_STORE_TEMP_STALE_MS;
function isUnreferencedPromptBlobFileRemovable(file, projectedPromptBlobRefCounts, cutoffMs) {
	if (file.mtimeMs > cutoffMs) return false;
	const hash = resolvePromptBlobFileHash(file);
	return hash ? !projectedPromptBlobRefCounts.has(hash) : false;
}
function isPromptBlobArtifactRemovable(file, projectedPromptBlobRefCounts, promptBlobCutoffMs, tempCutoffMs) {
	if (isSessionPromptBlobTempArtifactName(file.name)) return file.mtimeMs <= tempCutoffMs;
	return isUnreferencedPromptBlobFileRemovable(file, projectedPromptBlobRefCounts, promptBlobCutoffMs);
}
function isDiskBudgetRemovableSessionFile(file, referencedPaths, tempStaleCutoffMs, storeBasename) {
	if (isSessionStoreTempArtifactName(file.name, storeBasename)) return file.mtimeMs <= tempStaleCutoffMs;
	return isSessionArchiveArtifactName(file.name) || isUnreferencedSessionArtifactFile(file, referencedPaths);
}
async function removeFileIfExists(filePath) {
	const stat = await fs.promises.stat(filePath).catch(() => null);
	if (!stat?.isFile()) return 0;
	await fs.promises.rm(filePath, { force: true }).catch(() => void 0);
	return stat.size;
}
async function removeFileForBudget(params) {
	const resolvedPath = path.resolve(params.filePath);
	const canonicalPath = params.canonicalPath ?? canonicalizePathForComparison(resolvedPath);
	if (params.dryRun) {
		if (params.simulatedRemovedPaths.has(canonicalPath)) return 0;
		const size = params.fileSizesByPath.get(canonicalPath) ?? 0;
		if (size <= 0) return 0;
		params.simulatedRemovedPaths.add(canonicalPath);
		params.onRemovedPath?.(canonicalPath);
		return size;
	}
	const size = await removeFileIfExists(resolvedPath);
	if (size > 0) params.onRemovedPath?.(canonicalPath);
	return size;
}
async function removePromptBlobFileForBudget(params) {
	let file = params.file;
	if (!params.dryRun) {
		const stat = await fs.promises.stat(file.path).catch(() => null);
		if (!stat?.isFile()) return 0;
		file = {
			...file,
			size: stat.size,
			mtimeMs: stat.mtimeMs
		};
	}
	if (!isPromptBlobArtifactRemovable(file, params.projectedPromptBlobRefCounts, params.promptBlobCutoffMs, params.tempCutoffMs)) return 0;
	return await removeFileForBudget({
		filePath: file.path,
		canonicalPath: file.canonicalPath,
		dryRun: params.dryRun,
		fileSizesByPath: params.fileSizesByPath,
		simulatedRemovedPaths: params.simulatedRemovedPaths,
		onRemovedPath: params.onRemovedPath
	});
}
async function pruneUnreferencedSessionArtifacts(params) {
	const olderThanMs = Number.isFinite(params.olderThanMs) && params.olderThanMs > 0 ? params.olderThanMs : 0;
	const sessionsDir = path.dirname(params.storePath);
	const files = await readSessionsDirFiles(sessionsDir);
	const promptBlobFiles = await readSessionPromptBlobFiles(sessionsDir);
	const fileSizesByPath = new Map([...files, ...promptBlobFiles].map((file) => [file.canonicalPath, file.size]));
	const simulatedRemovedPaths = /* @__PURE__ */ new Set();
	const referencedPaths = resolveReferencedSessionArtifactPaths({
		sessionsDir,
		store: params.store
	});
	const projectedPromptBlobRefCounts = buildProjectedPromptBlobRefCounts(projectSessionStoreForPersistence({
		storePath: params.storePath,
		store: params.store
	}).store);
	const cutoffMs = Date.now() - olderThanMs;
	const tempCutoffMs = Date.now() - SESSION_STORE_TEMP_STALE_MS;
	const promptBlobCutoffMs = Date.now() - Math.max(olderThanMs, SESSION_PROMPT_BLOB_UNREFERENCED_GRACE_MS);
	const storeBasename = path.basename(params.storePath);
	const removableStoreFiles = files.filter((file) => {
		if (params.excludeCanonicalPaths?.has(file.canonicalPath)) return false;
		if (isSessionStoreTempArtifactName(file.name, storeBasename)) return file.mtimeMs <= tempCutoffMs;
		return file.mtimeMs <= cutoffMs && isUnreferencedSessionArtifactFile(file, referencedPaths);
	});
	const removablePromptBlobFiles = promptBlobFiles.filter((file) => {
		if (params.excludeCanonicalPaths?.has(file.canonicalPath)) return false;
		return isPromptBlobArtifactRemovable(file, projectedPromptBlobRefCounts, promptBlobCutoffMs, tempCutoffMs);
	});
	const removableFiles = [...removableStoreFiles.map((file) => ({
		kind: "store",
		file
	})), ...removablePromptBlobFiles.map((file) => ({
		kind: "promptBlob",
		file
	}))].filter((file) => {
		return !params.excludeCanonicalPaths?.has(file.file.canonicalPath);
	}).toSorted((a, b) => a.file.mtimeMs - b.file.mtimeMs);
	let removedFiles = 0;
	let freedBytes = 0;
	const dryRun = params.dryRun === true;
	for (const item of removableFiles) {
		const deletedBytes = item.kind === "promptBlob" ? await removePromptBlobFileForBudget({
			file: item.file,
			projectedPromptBlobRefCounts,
			promptBlobCutoffMs,
			tempCutoffMs,
			dryRun,
			fileSizesByPath,
			simulatedRemovedPaths
		}) : await removeFileForBudget({
			filePath: item.file.path,
			canonicalPath: item.file.canonicalPath,
			dryRun,
			fileSizesByPath,
			simulatedRemovedPaths
		});
		if (deletedBytes <= 0) continue;
		removedFiles += 1;
		freedBytes += deletedBytes;
	}
	return {
		scannedFiles: files.length + promptBlobFiles.length,
		removedFiles,
		freedBytes,
		olderThanMs
	};
}
async function enforceSessionDiskBudget(params) {
	const maxBytes = params.maintenance.maxDiskBytes;
	const highWaterBytes = params.maintenance.highWaterBytes;
	if (maxBytes == null || highWaterBytes == null) return null;
	const log = params.log ?? NOOP_LOGGER;
	const dryRun = params.dryRun === true;
	const sessionsDir = path.dirname(params.storePath);
	const files = await readSessionsDirFiles(sessionsDir);
	const promptBlobFiles = await readSessionPromptBlobFiles(sessionsDir);
	const fileSizesByPath = new Map([...files, ...promptBlobFiles].map((file) => [file.canonicalPath, file.size]));
	const simulatedRemovedPaths = /* @__PURE__ */ new Set();
	const resolvedStorePath = canonicalizePathForComparison(params.storePath);
	const storeFile = files.find((file) => file.canonicalPath === resolvedStorePath);
	const projectedPersistence = projectSessionStoreForPersistence({
		storePath: params.storePath,
		store: params.store
	});
	const projectedStore = projectedPersistence.store;
	let projectedStoreBytes = measureStoreBytes(projectedStore);
	const projectedPromptBlobBytesByHash = /* @__PURE__ */ new Map();
	const existingPromptBlobFilesByHash = /* @__PURE__ */ new Map();
	for (const file of promptBlobFiles) {
		const hash = resolvePromptBlobFileHash(file);
		if (hash) existingPromptBlobFilesByHash.set(hash, file);
	}
	for (const [hash, blob] of projectedPersistence.promptBlobs) if (!existingPromptBlobFilesByHash.has(hash)) projectedPromptBlobBytesByHash.set(hash, blob.ref.bytes);
	const projectedPromptBlobRefCounts = buildProjectedPromptBlobRefCounts(projectedStore);
	const projectedPromptBlobBytes = [...projectedPromptBlobBytesByHash.values()].reduce((sum, bytes) => sum + bytes, 0);
	let total = [...files, ...promptBlobFiles].reduce((sum, file) => sum + file.size, 0) - (storeFile?.size ?? 0) + projectedStoreBytes + projectedPromptBlobBytes;
	const totalBefore = total;
	if (total <= maxBytes) return {
		totalBytesBefore: totalBefore,
		totalBytesAfter: total,
		removedFiles: 0,
		removedEntries: 0,
		freedBytes: 0,
		maxBytes,
		highWaterBytes,
		overBudget: false
	};
	if (params.warnOnly) {
		log.warn("session disk budget exceeded (warn-only mode)", {
			sessionsDir,
			totalBytes: total,
			maxBytes,
			highWaterBytes
		});
		return {
			totalBytesBefore: totalBefore,
			totalBytesAfter: total,
			removedFiles: 0,
			removedEntries: 0,
			freedBytes: 0,
			maxBytes,
			highWaterBytes,
			overBudget: true
		};
	}
	let removedFiles = 0;
	let removedEntries = 0;
	let freedBytes = 0;
	const referencedPaths = resolveReferencedSessionArtifactPaths({
		sessionsDir,
		store: params.store
	});
	const tempStaleCutoffMs = Date.now() - SESSION_STORE_TEMP_STALE_MS;
	const promptBlobOrphanCutoffMs = Date.now() - SESSION_PROMPT_BLOB_UNREFERENCED_GRACE_MS;
	const storeBasename = path.basename(params.storePath);
	const unreferencedPromptBlobQueue = promptBlobFiles.filter((file) => {
		return isPromptBlobArtifactRemovable(file, projectedPromptBlobRefCounts, promptBlobOrphanCutoffMs, tempStaleCutoffMs);
	}).toSorted((a, b) => a.mtimeMs - b.mtimeMs);
	for (const file of unreferencedPromptBlobQueue) {
		if (total <= highWaterBytes) break;
		const deletedBytes = await removePromptBlobFileForBudget({
			file,
			projectedPromptBlobRefCounts,
			promptBlobCutoffMs: promptBlobOrphanCutoffMs,
			tempCutoffMs: tempStaleCutoffMs,
			dryRun,
			fileSizesByPath,
			simulatedRemovedPaths,
			onRemovedPath: params.onRemoveFile
		});
		if (deletedBytes <= 0) continue;
		total -= deletedBytes;
		freedBytes += deletedBytes;
		removedFiles += 1;
	}
	const removableFileQueue = files.filter((file) => isDiskBudgetRemovableSessionFile(file, referencedPaths, tempStaleCutoffMs, storeBasename)).toSorted((a, b) => a.mtimeMs - b.mtimeMs);
	for (const file of removableFileQueue) {
		if (total <= highWaterBytes) break;
		const deletedBytes = await removeFileForBudget({
			filePath: file.path,
			canonicalPath: file.canonicalPath,
			dryRun,
			fileSizesByPath,
			simulatedRemovedPaths,
			onRemovedPath: params.onRemoveFile
		});
		if (deletedBytes <= 0) continue;
		total -= deletedBytes;
		freedBytes += deletedBytes;
		removedFiles += 1;
	}
	if (total > highWaterBytes) {
		const activeSessionKey = normalizeOptionalLowercaseString(params.activeSessionKey);
		const sessionIdRefCounts = buildSessionIdRefCounts(params.store);
		const entryChunkBytesByKey = buildStoreEntryChunkSizeMap(projectedStore);
		const keys = Object.keys(params.store).toSorted((a, b) => {
			return getEntryUpdatedAt(params.store[a]) - getEntryUpdatedAt(params.store[b]);
		});
		for (const key of keys) {
			if (total <= highWaterBytes) break;
			if (activeSessionKey && normalizeLowercaseStringOrEmpty(key) === activeSessionKey) continue;
			const entry = params.store[key];
			if (!entry) continue;
			if (shouldPreserveMaintenanceEntry({
				key,
				entry,
				preserveKeys: params.preserveKeys
			})) continue;
			const previousProjectedBytes = projectedStoreBytes;
			const projectedEntry = projectedStore[key];
			const promptBlobHash = resolveProjectedPromptBlobHash(projectedEntry);
			delete params.store[key];
			delete projectedStore[key];
			const chunkBytes = entryChunkBytesByKey.get(key);
			entryChunkBytesByKey.delete(key);
			if (typeof chunkBytes === "number" && Number.isFinite(chunkBytes) && chunkBytes >= 0) projectedStoreBytes = Math.max(2, projectedStoreBytes - (chunkBytes + 2));
			else projectedStoreBytes = measureStoreBytes(projectedStore);
			total += projectedStoreBytes - previousProjectedBytes;
			if (promptBlobHash) {
				const nextRefCount = (projectedPromptBlobRefCounts.get(promptBlobHash) ?? 1) - 1;
				if (nextRefCount > 0) projectedPromptBlobRefCounts.set(promptBlobHash, nextRefCount);
				else {
					projectedPromptBlobRefCounts.delete(promptBlobHash);
					const virtualBlobBytes = projectedPromptBlobBytesByHash.get(promptBlobHash) ?? 0;
					if (virtualBlobBytes > 0) total -= virtualBlobBytes;
					else {
						const blobFile = existingPromptBlobFilesByHash.get(promptBlobHash);
						if (blobFile && isPromptBlobArtifactRemovable(blobFile, projectedPromptBlobRefCounts, promptBlobOrphanCutoffMs, tempStaleCutoffMs)) {
							const deletedBytes = await removePromptBlobFileForBudget({
								file: blobFile,
								projectedPromptBlobRefCounts,
								promptBlobCutoffMs: promptBlobOrphanCutoffMs,
								tempCutoffMs: tempStaleCutoffMs,
								dryRun,
								fileSizesByPath,
								simulatedRemovedPaths,
								onRemovedPath: params.onRemoveFile
							});
							if (deletedBytes > 0) {
								total -= deletedBytes;
								freedBytes += deletedBytes;
								removedFiles += 1;
							}
						}
					}
				}
			}
			removedEntries += 1;
			const sessionId = entry.sessionId;
			if (!sessionId) continue;
			const nextRefCount = (sessionIdRefCounts.get(sessionId) ?? 1) - 1;
			if (nextRefCount > 0) {
				sessionIdRefCounts.set(sessionId, nextRefCount);
				continue;
			}
			sessionIdRefCounts.delete(sessionId);
			for (const artifactPath of resolveSessionArtifactPathsForEntry({
				sessionsDir,
				entry
			})) {
				const deletedBytes = await removeFileForBudget({
					filePath: artifactPath,
					dryRun,
					fileSizesByPath,
					simulatedRemovedPaths,
					onRemovedPath: params.onRemoveFile
				});
				if (deletedBytes <= 0) continue;
				total -= deletedBytes;
				freedBytes += deletedBytes;
				removedFiles += 1;
			}
		}
	}
	if (!dryRun) {
		if (total > highWaterBytes) log.warn("session disk budget still above high-water target after cleanup", {
			sessionsDir,
			totalBytes: total,
			maxBytes,
			highWaterBytes,
			removedFiles,
			removedEntries
		});
		else if (removedFiles > 0 || removedEntries > 0) log.info("applied session disk budget cleanup", {
			sessionsDir,
			totalBytesBefore: totalBefore,
			totalBytesAfter: total,
			maxBytes,
			highWaterBytes,
			removedFiles,
			removedEntries
		});
	}
	return {
		totalBytesBefore: totalBefore,
		totalBytesAfter: total,
		removedFiles,
		removedEntries,
		freedBytes,
		maxBytes,
		highWaterBytes,
		overBudget: true
	};
}
//#endregion
//#region src/config/sessions/group.ts
const getGroupSurfaces = () => new Set([...listDeliverableMessageChannels(), "webchat"]);
function resolveLegacyGroupSessionKey(ctx) {
	for (const plugin of listChannelPlugins()) {
		const resolved = plugin.messaging?.resolveLegacyGroupSessionKey?.(ctx);
		if (resolved) return resolved;
	}
	return null;
}
function normalizeGroupLabel(raw) {
	return normalizeHyphenSlug(raw);
}
function resolveOriginatingGroupTargetId(params) {
	const target = normalizeOptionalString(params.ctx.OriginatingTo ?? params.ctx.To) ?? "";
	if (!target) return null;
	const parts = target.split(":").filter(Boolean);
	if (parts.length < 2) return null;
	const head = normalizeLowercaseStringOrEmpty(parts[0]);
	const second = normalizeOptionalLowercaseString(parts[1]);
	if ((second === "group" || second === "channel") && (head === params.provider || getGroupSurfaces().has(head))) return parts.slice(2).join(":") || null;
	if (head === params.provider || head === "chat" || head === "room" || head === "group") return parts.slice(1).join(":") || null;
	if (head === "channel") return parts.slice(1).join(":") || null;
	return null;
}
function shortenGroupId(value) {
	const trimmed = normalizeOptionalString(value) ?? "";
	if (!trimmed) return "";
	if (trimmed.length <= 14) return trimmed;
	return `${trimmed.slice(0, 6)}...${trimmed.slice(-4)}`;
}
/** Builds a compact display label for group sessions from channel metadata or ids. */
function buildGroupDisplayName(params) {
	const providerKey = normalizeOptionalLowercaseString(params.provider) ?? "group";
	const groupChannel = normalizeOptionalString(params.groupChannel);
	const space = normalizeOptionalString(params.space);
	const subject = normalizeOptionalString(params.subject);
	const detail = (groupChannel && space ? `${space}${groupChannel.startsWith("#") ? "" : "#"}${groupChannel}` : groupChannel || subject || space || "") || "";
	const fallbackId = normalizeOptionalString(params.id) ?? params.key;
	const rawLabel = detail || fallbackId;
	let token = normalizeGroupLabel(rawLabel);
	if (!token) token = normalizeGroupLabel(shortenGroupId(rawLabel));
	if (!params.groupChannel && token.startsWith("#")) token = token.replace(/^#+/, "");
	if (token && !/^[@#]/.test(token) && !token.startsWith("g-") && !token.includes("#")) token = `g-${token}`;
	return token ? `${providerKey}:${token}` : providerKey;
}
/**
* Resolves channel/group chat context into the persisted group session key.
*
* Provider-prefixed ids use channel-owned normalization, while legacy plugin resolvers remain a
* fallback for older channel surfaces that cannot yet express the generic route shape.
*/
function resolveGroupSessionKey(ctx) {
	const from = normalizeOptionalString(ctx.From) ?? "";
	const chatType = normalizeOptionalLowercaseString(ctx.ChatType);
	const normalizedChatType = chatType === "channel" ? "channel" : chatType === "group" ? "group" : void 0;
	const legacyResolution = resolveLegacyGroupSessionKey(ctx);
	if (!(normalizedChatType === "group" || normalizedChatType === "channel" || from.includes(":group:") || from.includes(":channel:") || legacyResolution !== null)) return null;
	const providerHint = normalizeOptionalLowercaseString(ctx.Provider);
	const parts = from.split(":").filter(Boolean);
	const head = normalizeLowercaseStringOrEmpty(parts[0]);
	const headIsSurface = head ? getGroupSurfaces().has(head) : false;
	if (!headIsSurface && !providerHint && legacyResolution) return legacyResolution;
	const provider = headIsSurface ? head : providerHint ?? legacyResolution?.channel;
	if (!provider) return null;
	const second = normalizeOptionalLowercaseString(parts[1]);
	const secondIsKind = second === "group" || second === "channel";
	const kind = secondIsKind ? second : from.includes(":channel:") || normalizedChatType === "channel" ? "channel" : "group";
	const originatingGroupTargetId = !secondIsKind && normalizedChatType ? resolveOriginatingGroupTargetId({
		ctx,
		provider
	}) : null;
	const finalId = normalizeSessionPeerId({
		channel: provider,
		peerKind: kind,
		peerId: originatingGroupTargetId ? originatingGroupTargetId : headIsSurface ? secondIsKind ? parts.slice(2).join(":") : parts.slice(1).join(":") : from
	});
	if (!finalId) return null;
	return {
		key: `${provider}:${kind}:${finalId}`,
		channel: provider,
		id: finalId,
		chatType: kind === "channel" ? "channel" : "group"
	};
}
//#endregion
//#region src/config/sessions/metadata.ts
const mergeOrigin = (existing, next) => {
	if (!existing && !next) return;
	const merged = existing ? { ...existing } : {};
	if (existing != null && (existing.provider != null && next?.provider != null && next.provider !== existing.provider || existing.surface != null && next?.surface != null && next.surface !== existing.surface || existing.accountId != null && next?.accountId != null && next.accountId !== existing.accountId)) {
		delete merged.nativeChannelId;
		delete merged.nativeDirectUserId;
		delete merged.accountId;
		delete merged.threadId;
	}
	if (next?.label) merged.label = next.label;
	if (next?.provider) merged.provider = next.provider;
	if (next?.surface) merged.surface = next.surface;
	if (next?.chatType) merged.chatType = next.chatType;
	if (next?.from) merged.from = next.from;
	if (next?.to) merged.to = next.to;
	if (next?.nativeChannelId) merged.nativeChannelId = next.nativeChannelId;
	if (next?.nativeDirectUserId) merged.nativeDirectUserId = next.nativeDirectUserId;
	if (next?.accountId) merged.accountId = next.accountId;
	if (next?.threadId != null && next.threadId !== "") merged.threadId = next.threadId;
	return Object.keys(merged).length > 0 ? merged : void 0;
};
/** Derives session origin metadata from an inbound message context. */
function deriveSessionOrigin(ctx, opts) {
	const isSystemEventProvider = ctx.Provider === "heartbeat" || ctx.Provider === "cron-event" || ctx.Provider === "exec-event";
	if (opts?.skipSystemEventOrigin && isSystemEventProvider) return;
	const label = normalizeOptionalString(resolveConversationLabel(ctx));
	const provider = normalizeMessageChannel(typeof ctx.OriginatingChannel === "string" && ctx.OriginatingChannel || ctx.Surface || ctx.Provider);
	const surface = normalizeOptionalLowercaseString(ctx.Surface);
	const chatType = normalizeChatType(ctx.ChatType) ?? void 0;
	const from = normalizeOptionalString(ctx.From);
	const to = normalizeOptionalString(typeof ctx.OriginatingTo === "string" ? ctx.OriginatingTo : ctx.To);
	const nativeChannelId = normalizeOptionalString(ctx.NativeChannelId);
	const nativeDirectUserId = normalizeOptionalString(ctx.NativeDirectUserId);
	const accountId = normalizeOptionalString(ctx.AccountId);
	const threadId = ctx.MessageThreadId ?? void 0;
	const origin = {};
	if (label) origin.label = label;
	if (provider) origin.provider = provider;
	if (surface) origin.surface = surface;
	if (chatType) origin.chatType = chatType;
	if (from) origin.from = from;
	if (to) origin.to = to;
	if (nativeChannelId) origin.nativeChannelId = nativeChannelId;
	if (nativeDirectUserId) origin.nativeDirectUserId = nativeDirectUserId;
	if (accountId) origin.accountId = accountId;
	if (threadId != null && threadId !== "") origin.threadId = threadId;
	return Object.keys(origin).length > 0 ? origin : void 0;
}
function snapshotSessionOrigin(entry) {
	if (!entry?.origin) return;
	return { ...entry.origin };
}
function deriveGroupSessionPatch(params) {
	const resolution = params.groupResolution ?? resolveGroupSessionKey(params.ctx);
	if (!resolution?.channel) return null;
	const channel = resolution.channel;
	const subject = params.ctx.GroupSubject?.trim();
	const space = params.ctx.GroupSpace?.trim();
	const explicitChannel = params.ctx.GroupChannel?.trim();
	const subjectLooksChannel = Boolean(subject?.startsWith("#"));
	const normalizedChannel = subjectLooksChannel && resolution.chatType !== "channel" ? normalizeChannelId(channel) : null;
	const isChannelProvider = Boolean(normalizedChannel && getLoadedChannelPlugin(normalizedChannel)?.capabilities.chatTypes.includes("channel"));
	const nextGroupChannel = explicitChannel ?? (subjectLooksChannel && subject && (resolution.chatType === "channel" || isChannelProvider) ? subject : void 0);
	const nextSubject = nextGroupChannel ? void 0 : subject;
	const patch = {
		chatType: resolution.chatType ?? "group",
		channel,
		groupId: resolution.id
	};
	if (nextSubject) patch.subject = nextSubject;
	if (nextGroupChannel) patch.groupChannel = nextGroupChannel;
	if (space) patch.space = space;
	const displayName = buildGroupDisplayName({
		provider: channel,
		subject: nextSubject ?? params.existing?.subject,
		groupChannel: nextGroupChannel ?? params.existing?.groupChannel,
		space: space ?? params.existing?.space,
		id: resolution.id,
		key: params.sessionKey
	});
	if (displayName) patch.displayName = displayName;
	return patch;
}
function deriveSessionMetaPatch(params) {
	const groupPatch = deriveGroupSessionPatch(params);
	const origin = deriveSessionOrigin(params.ctx, { skipSystemEventOrigin: params.skipSystemEventOrigin });
	if (!groupPatch && !origin) return null;
	const patch = groupPatch ? { ...groupPatch } : {};
	const mergedOrigin = mergeOrigin(params.existing?.origin, origin);
	if (mergedOrigin) patch.origin = mergedOrigin;
	return Object.keys(patch).length > 0 ? patch : null;
}
//#endregion
//#region src/config/sessions/store-maintenance-operations.ts
function resolveMaintenanceForOperation(params) {
	return params.maintenanceConfig ? {
		...params.maintenanceConfig,
		...params.maintenanceOverride
	} : {
		...resolveMaintenanceConfig(),
		...params.maintenanceOverride
	};
}
function collectReferencedSessionIds(store) {
	return new Set(Object.values(store).map((entry) => entry?.sessionId).filter((id) => Boolean(id)));
}
function rememberRemovedSessionFile$1(removedSessionFiles, entry) {
	if (!removedSessionFiles.has(entry.sessionId) || entry.sessionFile) removedSessionFiles.set(entry.sessionId, entry.sessionFile);
}
async function applyWarnOnlyMaintenance(params) {
	const activeSessionKey = params.operation.activeSessionKey?.trim();
	if (activeSessionKey && params.shouldRunEntryMaintenance) {
		const warning = getActiveSessionMaintenanceWarning({
			store: params.operation.store,
			activeSessionKey,
			pruneAfterMs: params.maintenance.pruneAfterMs,
			maxEntries: params.maintenance.maxEntries
		});
		if (warning) {
			params.operation.log.warn("session maintenance would evict active session; skipping enforcement", {
				activeSessionKey: warning.activeSessionKey,
				wouldPrune: warning.wouldPrune,
				wouldCap: warning.wouldCap,
				pruneAfterMs: warning.pruneAfterMs,
				maxEntries: warning.maxEntries
			});
			await params.operation.onWarn?.(warning);
		}
	}
	const diskBudget = await enforceSessionDiskBudget({
		store: params.operation.store,
		storePath: params.operation.storePath,
		activeSessionKey: params.operation.activeSessionKey,
		maintenance: params.maintenance,
		warnOnly: true,
		log: params.operation.log
	});
	await params.operation.onMaintenanceApplied?.({
		mode: params.maintenance.mode,
		beforeCount: params.beforeCount,
		afterCount: Object.keys(params.operation.store).length,
		pruned: 0,
		capped: 0,
		diskBudget
	});
}
async function cleanupRemovedSessionArtifacts(params) {
	const archivedDirs = await params.operation.artifacts.archiveRemovedSessionTranscripts({
		removedSessionFiles: params.removedSessionFiles,
		referencedSessionIds: params.referencedSessionIds,
		storePath: params.operation.storePath,
		reason: "deleted",
		restrictToStoreDir: true
	});
	if (params.removedSessionFiles.size > 0) await params.operation.artifacts.removeRemovedSessionTrajectoryArtifacts({
		removedSessionFiles: params.removedSessionFiles,
		referencedSessionIds: params.referencedSessionIds,
		storePath: params.operation.storePath,
		restrictToStoreDir: true
	});
	if (archivedDirs.size === 0 && params.maintenance.resetArchiveRetentionMs == null) return;
	const targetDirs = archivedDirs.size > 0 ? [...archivedDirs] : [path.dirname(path.resolve(params.operation.storePath))];
	await params.operation.artifacts.cleanupArchivedSessionTranscripts({
		directories: targetDirs,
		rules: params.maintenance.resetArchiveRetentionMs != null ? [{
			reason: "deleted",
			olderThanMs: params.maintenance.pruneAfterMs
		}, {
			reason: "reset",
			olderThanMs: params.maintenance.resetArchiveRetentionMs
		}] : [{
			reason: "deleted",
			olderThanMs: params.maintenance.pruneAfterMs
		}]
	});
}
async function applyEnforcedMaintenance(params) {
	const preserveSessionKeys = collectSessionMaintenancePreserveKeys([params.operation.activeSessionKey]);
	const removedSessionFiles = /* @__PURE__ */ new Map();
	const pruned = pruneStaleEntries(params.operation.store, params.maintenance.pruneAfterMs, {
		onPruned: ({ entry }) => {
			rememberRemovedSessionFile$1(removedSessionFiles, entry);
		},
		preserveKeys: preserveSessionKeys
	});
	const countAfterPrune = Object.keys(params.operation.store).length;
	const capped = params.forceMaintenance || shouldRunSessionEntryMaintenance({
		entryCount: countAfterPrune,
		maxEntries: params.maintenance.maxEntries
	}) ? capEntryCount(params.operation.store, params.maintenance.maxEntries, {
		onCapped: ({ entry }) => {
			rememberRemovedSessionFile$1(removedSessionFiles, entry);
		},
		preserveKeys: preserveSessionKeys
	}) : 0;
	const referencedSessionIds = collectReferencedSessionIds(params.operation.store);
	await cleanupRemovedSessionArtifacts({
		operation: params.operation,
		maintenance: params.maintenance,
		removedSessionFiles,
		referencedSessionIds
	});
	const diskBudget = await enforceSessionDiskBudget({
		store: params.operation.store,
		storePath: params.operation.storePath,
		activeSessionKey: params.operation.activeSessionKey,
		preserveKeys: preserveSessionKeys,
		maintenance: params.maintenance,
		warnOnly: false,
		log: params.operation.log
	});
	await params.operation.onMaintenanceApplied?.({
		mode: params.maintenance.mode,
		beforeCount: params.beforeCount,
		afterCount: Object.keys(params.operation.store).length,
		pruned,
		capped,
		diskBudget
	});
	return { changedStore: pruned > 0 || capped > 0 || (diskBudget?.removedEntries ?? 0) > 0 };
}
/**
* Applies automatic session-store maintenance to the in-memory file-store image.
*
* Future SQLite adapters should map this into named boundaries: entry retention,
* removed-session artifact cleanup, disk-budget eviction, and archive retention cleanup.
*/
async function applyFileBackedSessionStoreMaintenance(params) {
	const maintenance = resolveMaintenanceForOperation(params);
	const beforeCount = Object.keys(params.store).length;
	const forceMaintenance = params.maintenanceOverride !== void 0;
	const shouldRunEntryMaintenance = shouldRunSessionEntryMaintenance({
		entryCount: beforeCount,
		maxEntries: maintenance.maxEntries,
		force: forceMaintenance
	});
	if (maintenance.mode === "warn") {
		await applyWarnOnlyMaintenance({
			operation: params,
			maintenance,
			beforeCount,
			shouldRunEntryMaintenance
		});
		return { changedStore: false };
	}
	return await applyEnforcedMaintenance({
		operation: params,
		maintenance,
		beforeCount,
		forceMaintenance
	});
}
//#endregion
//#region src/config/sessions/store-writer-state.ts
const WRITER_QUEUES = /* @__PURE__ */ new Map();
/** Clears session store writer queues and cache for tests. */
function clearSessionStoreCacheForTest() {
	clearSessionStoreCaches();
	clearStoreWriterQueuesForTest(WRITER_QUEUES, "session store queue cleared for test");
}
//#endregion
//#region src/config/sessions/store-writer.ts
async function runExclusiveSessionStoreWrite(storePath, fn) {
	return await runQueuedStoreWrite({
		queues: WRITER_QUEUES,
		storePath,
		label: "runExclusiveSessionStoreWrite",
		fn
	});
}
//#endregion
//#region src/config/sessions/store.ts
const log = createSubsystemLogger("sessions/store");
let sessionArchiveRuntimePromise = null;
let trajectoryCleanupRuntimePromise = null;
const writerStoreFileStats = /* @__PURE__ */ new WeakMap();
function loadSessionArchiveRuntime() {
	sessionArchiveRuntimePromise ??= import("./session-archive.runtime.js");
	return sessionArchiveRuntimePromise;
}
function loadTrajectoryCleanupRuntime() {
	trajectoryCleanupRuntimePromise ??= import("./cleanup-t6GOeWL3.js");
	return trajectoryCleanupRuntimePromise;
}
function removeThreadFromDeliveryContext(context) {
	if (!context || context.threadId == null) return context;
	const next = { ...context };
	delete next.threadId;
	return next;
}
function readSessionUpdatedAt(params) {
	try {
		return resolveSessionStoreEntry({
			store: loadSessionStore(params.storePath, { clone: false }),
			sessionKey: params.sessionKey
		}).existing?.updatedAt;
	} catch {
		return;
	}
}
function cloneSessionEntry(entry) {
	return cloneSessionStoreRecord({ entry }).entry;
}
function resolveSessionWorkflowStorePath(options) {
	if (options.storePath) return options.storePath;
	const agentId = options.agentId ?? resolveAgentIdFromSessionKey(options.sessionKey);
	return resolveStorePath(getRuntimeConfig().session?.store, {
		agentId,
		env: options.env
	});
}
function getSessionEntry(options) {
	const entry = readSessionEntry(resolveSessionWorkflowStorePath(options), options.sessionKey, { hydrateSkillPromptRefs: options.hydrateSkillPromptRefs });
	return entry ? cloneSessionEntry(entry) : void 0;
}
function listSessionEntries(options = {}) {
	return readSessionEntries(resolveSessionWorkflowStorePath(options)).map(([sessionKey, entry]) => ({
		sessionKey,
		entry: cloneSessionEntry(entry)
	}));
}
function updateSessionStoreWriteCaches(params) {
	const fileStat = getFileStatSnapshot(params.storePath);
	setSerializedSessionStore(params.storePath, params.serialized, fileStat?.sizeBytes, params.serializedPromptRefs);
	if (!isSessionStoreCacheEnabled()) {
		dropSessionStoreObjectCache(params.storePath);
		dropSessionStoreSnapshotCache(params.storePath);
		return;
	}
	writeSessionStoreCache({
		storePath: params.storePath,
		store: params.store,
		mtimeMs: fileStat?.mtimeMs,
		sizeBytes: fileStat?.sizeBytes,
		serialized: params.serialized,
		serializedPromptRefs: params.serializedPromptRefs,
		cloneSerialized: params.cloneSerialized,
		takeOwnership: params.takeOwnership
	});
	dropSessionStoreSnapshotCache(params.storePath);
}
function restoreUnchangedSessionStoreCache(storePath, store) {
	if (!isSessionStoreCacheEnabled()) return;
	const loadedFileStat = writerStoreFileStats.get(store) ?? null;
	const currentFileStat = getFileStatSnapshot(storePath) ?? null;
	if (loadedFileStat?.mtimeMs !== currentFileStat?.mtimeMs || loadedFileStat?.sizeBytes !== currentFileStat?.sizeBytes) {
		invalidateSessionStoreCache(storePath);
		return;
	}
	const serialized = getSerializedSessionStore(storePath);
	const serializedPromptRefs = serialized !== void 0 ? getSerializedSessionStorePromptRefs(storePath) : void 0;
	writeSessionStoreCache({
		storePath,
		store,
		mtimeMs: loadedFileStat?.mtimeMs,
		sizeBytes: loadedFileStat?.sizeBytes,
		serialized,
		serializedPromptRefs,
		takeOwnership: true
	});
	if (serialized !== void 0) setSerializedSessionStore(storePath, serialized, loadedFileStat?.sizeBytes, serializedPromptRefs);
}
function findJsonValueEnd(json, valueStart) {
	let depth = 0;
	let inString = false;
	let escaped = false;
	for (let index = valueStart; index < json.length; index += 1) {
		const char = json[index];
		if (inString) {
			if (escaped) escaped = false;
			else if (char === "\\") escaped = true;
			else if (char === "\"") inString = false;
			continue;
		}
		if (char === "\"") {
			inString = true;
			continue;
		}
		if (char === "{" || char === "[") {
			depth += 1;
			continue;
		}
		if (char !== "}" && char !== "]") continue;
		depth -= 1;
		if (depth === 0) return index + 1;
		if (depth < 0) return null;
	}
	return null;
}
function indentTopLevelEntryJson(json) {
	return json.replaceAll("\n", "\n  ");
}
function buildSingleEntrySerializedStore(params) {
	const currentSerialized = getSerializedSessionStore(params.storePath);
	if (currentSerialized === void 0) return null;
	const currentPromptRefs = getSerializedPromptRefs(params.storePath, currentSerialized);
	const marker = `\n  ${JSON.stringify(params.patch.sessionKey)}: `;
	const markerIndex = currentSerialized.indexOf(marker);
	if (markerIndex < 0) return null;
	const valueStart = markerIndex + marker.length;
	if (currentSerialized[valueStart] !== "{") return null;
	const valueEnd = findJsonValueEnd(currentSerialized, valueStart);
	if (valueEnd === null) return null;
	const projected = projectSessionStoreForPersistence({
		storePath: params.storePath,
		store: { [params.patch.sessionKey]: params.patch.entry }
	});
	const projectedEntry = projected.store[params.patch.sessionKey];
	if (!projectedEntry) return null;
	const entryJson = indentTopLevelEntryJson(JSON.stringify(projectedEntry, null, 2));
	const promptRefs = new Map(currentPromptRefs);
	const promptRef = projectedEntry.skillsSnapshot?.promptRef;
	if (promptRef) promptRefs.set(params.patch.sessionKey, promptRef);
	else promptRefs.delete(params.patch.sessionKey);
	return {
		serialized: currentSerialized.slice(0, valueStart) + entryJson + currentSerialized.slice(valueEnd),
		promptBlobs: [...projected.promptBlobs.values()],
		promptRefs
	};
}
function collectSerializedPromptRefs(serialized) {
	const refs = /* @__PURE__ */ new Map();
	try {
		const parsed = JSON.parse(serialized);
		for (const [key, entry] of Object.entries(parsed)) {
			const ref = entry?.skillsSnapshot?.promptRef;
			if (ref) refs.set(key, ref);
		}
	} catch {}
	return refs;
}
function collectStorePromptRefs(store) {
	const refs = /* @__PURE__ */ new Map();
	for (const [key, entry] of Object.entries(store)) {
		const ref = entry?.skillsSnapshot?.promptRef;
		if (ref) refs.set(key, ref);
	}
	return refs;
}
function getSerializedPromptRefs(storePath, serialized) {
	const cached = getSerializedSessionStorePromptRefs(storePath);
	if (cached) return cached;
	const refs = collectSerializedPromptRefs(serialized);
	setSerializedSessionStorePromptRefs(storePath, refs);
	return refs;
}
function storeHasUnsafeUntouchedHydratedSkillPrompts(storePath, store, changedSessionKey) {
	const currentSerialized = getSerializedSessionStore(storePath);
	const serializedPromptRefs = currentSerialized !== void 0 ? getSerializedPromptRefs(storePath, currentSerialized) : void 0;
	for (const [key, entry] of Object.entries(store)) {
		if (key === changedSessionKey || typeof entry.skillsSnapshot?.prompt !== "string") continue;
		const ref = serializedPromptRefs?.get(key);
		if (!ref || !isSessionSkillPromptBlobReadable(storePath, ref)) return true;
		if (serializedPromptRefs?.has(key)) {
			const projected = projectSessionStoreForPersistence({
				storePath,
				store: { [key]: entry }
			});
			for (const blob of projected.promptBlobs.values()) {
				if (!blob.path) continue;
				try {
					const stat = fs.statSync(blob.path);
					if (!stat.isFile() || stat.size !== blob.ref.bytes) return true;
				} catch {
					return true;
				}
			}
		}
	}
	return false;
}
function loadMutableSessionStoreForWriter(storePath) {
	const currentFileStat = getFileStatSnapshot(storePath);
	if (isSessionStoreCacheEnabled()) {
		const cached = takeMutableSessionStoreCache({
			storePath,
			mtimeMs: currentFileStat?.mtimeMs,
			sizeBytes: currentFileStat?.sizeBytes
		});
		if (cached) {
			writerStoreFileStats.set(cached, currentFileStat ?? null);
			return cached;
		}
	}
	const store = loadSessionStore(storePath, {
		skipCache: true,
		clone: false
	});
	writerStoreFileStats.set(store, currentFileStat ?? null);
	return store;
}
function sessionEntriesHaveSameSerializedForm(previous, next) {
	return previous !== void 0 && JSON.stringify(previous) === JSON.stringify(next);
}
function cloneOptionalSessionEntry(entry) {
	return entry ? cloneSessionEntry(entry) : void 0;
}
function resolveLifecyclePrimaryEntry(params) {
	const freshestMatch = resolveFreshestLifecycleStoreMatch({
		store: params.store,
		storeKeys: params.target.storeKeys
	});
	if (freshestMatch) {
		const currentPrimary = params.store[params.target.canonicalKey];
		if (!currentPrimary || (freshestMatch.entry.updatedAt ?? 0) > (currentPrimary.updatedAt ?? 0)) params.store[params.target.canonicalKey] = freshestMatch.entry;
	}
	pruneLifecycleLegacyStoreKeys({
		store: params.store,
		target: params.target
	});
	return params.store[params.target.canonicalKey];
}
function resolveFreshestLifecycleStoreMatch(params) {
	let freshest;
	for (const key of params.storeKeys) {
		const entry = params.store[key];
		if (!entry) continue;
		const match = {
			key,
			entry
		};
		if (!freshest || (entry.updatedAt ?? 0) > (freshest.entry.updatedAt ?? 0)) freshest = match;
	}
	return freshest;
}
function pruneLifecycleLegacyStoreKeys(params) {
	for (const key of params.target.storeKeys) if (key !== params.target.canonicalKey) delete params.store[key];
}
async function archiveLifecycleSessionTranscripts(params) {
	if (!params.sessionId) return [];
	const { archiveSessionTranscriptsDetailed } = await loadSessionArchiveRuntime();
	return archiveSessionTranscriptsDetailed({
		sessionId: params.sessionId,
		storePath: params.storePath,
		sessionFile: params.sessionFile,
		agentId: params.agentId,
		reason: params.reason
	});
}
function ensureLifecycleTranscriptHeader(params) {
	fs.mkdirSync(path.dirname(params.sessionFile), { recursive: true });
	if (fs.existsSync(params.sessionFile)) return;
	const header = {
		type: "session",
		version: 3,
		id: params.sessionId,
		timestamp: (/* @__PURE__ */ new Date()).toISOString(),
		cwd: process.cwd()
	};
	fs.writeFileSync(params.sessionFile, `${JSON.stringify(header)}\n`, {
		encoding: "utf-8",
		mode: 384
	});
}
function normalizePathForLifecycleComparison(filePath) {
	try {
		return path.normalize(fs.realpathSync(filePath));
	} catch {
		return path.normalize(path.resolve(filePath));
	}
}
function sessionKeySegmentStartsWith(sessionKey, prefix) {
	const firstSeparator = sessionKey.indexOf(":");
	if (firstSeparator < 0) return sessionKey.startsWith(prefix);
	const secondSeparator = sessionKey.indexOf(":", firstSeparator + 1);
	return (secondSeparator < 0 ? sessionKey : sessionKey.slice(secondSeparator + 1)).startsWith(prefix);
}
function resolveLifecycleTranscriptPath(params) {
	const sessionId = params.entry?.sessionId?.trim();
	if (!sessionId) return null;
	try {
		return resolveSessionFilePath(sessionId, params.entry, { sessionsDir: params.sessionsDir });
	} catch {
		return null;
	}
}
function lifecycleTranscriptIsReclaimable(params) {
	if (!params.transcriptPath || !fs.existsSync(params.transcriptPath)) return true;
	try {
		const stat = fs.statSync(params.transcriptPath);
		return params.nowMs - stat.mtimeMs >= params.orphanTranscriptMinAgeMs;
	} catch {
		return true;
	}
}
function archiveExactLifecycleTranscriptPath(params) {
	const resolvedSessionsDir = normalizePathForLifecycleComparison(params.sessionsDir);
	const resolvedTranscriptPath = normalizePathForLifecycleComparison(params.transcriptPath);
	const relative = path.relative(resolvedSessionsDir, resolvedTranscriptPath);
	if (!relative || relative.startsWith("..") || path.isAbsolute(relative)) return 0;
	const archivedPath = `${resolvedTranscriptPath}.deleted.${formatSessionArchiveTimestamp()}`;
	try {
		fs.renameSync(resolvedTranscriptPath, archivedPath);
		emitSessionTranscriptUpdate({ sessionFile: archivedPath });
		return 1;
	} catch {
		return 0;
	}
}
async function saveSessionStoreUnlocked(storePath, store, opts) {
	normalizeSessionStore(store);
	let maintenanceChangedStore = false;
	if (!opts?.skipMaintenance) maintenanceChangedStore = (await applyFileBackedSessionStoreMaintenance({
		storePath,
		store,
		activeSessionKey: opts?.activeSessionKey,
		onWarn: opts?.onWarn,
		onMaintenanceApplied: opts?.onMaintenanceApplied,
		maintenanceOverride: opts?.maintenanceOverride,
		maintenanceConfig: opts?.maintenanceConfig,
		log,
		artifacts: {
			archiveRemovedSessionTranscripts,
			removeRemovedSessionTrajectoryArtifacts: async (params) => {
				const { removeRemovedSessionTrajectoryArtifacts } = await loadTrajectoryCleanupRuntime();
				await removeRemovedSessionTrajectoryArtifacts(params);
			},
			cleanupArchivedSessionTranscripts: async (params) => {
				const { cleanupArchivedSessionTranscripts } = await loadSessionArchiveRuntime();
				await cleanupArchivedSessionTranscripts(params);
			}
		}
	})).changedStore;
	if (opts?.skipSerializeForUnchangedStore && !maintenanceChangedStore && getSerializedSessionStore(storePath) !== void 0) {
		restoreUnchangedSessionStoreCache(storePath, store);
		return;
	}
	await fs.promises.mkdir(path.dirname(storePath), { recursive: true });
	if (opts?.singleEntryPersistence && !maintenanceChangedStore && !storeHasUnsafeUntouchedHydratedSkillPrompts(storePath, store, opts.singleEntryPersistence.sessionKey)) {
		const normalizedEntry = store[opts.singleEntryPersistence.sessionKey];
		const singleEntrySerialized = buildSingleEntrySerializedStore({
			storePath,
			patch: normalizedEntry ? {
				sessionKey: opts.singleEntryPersistence.sessionKey,
				entry: normalizedEntry
			} : opts.singleEntryPersistence
		});
		if (singleEntrySerialized) {
			await writeSessionStoreAtomic({
				storePath,
				store,
				serialized: singleEntrySerialized.serialized,
				serializedPromptRefs: singleEntrySerialized.promptRefs,
				promptBlobs: singleEntrySerialized.promptBlobs,
				takeOwnership: opts?.takeCacheOwnership
			});
			return;
		}
	}
	const persisted = projectSessionStoreForPersistence({
		storePath,
		store
	});
	const promptBlobs = [...persisted.promptBlobs.values()];
	const promptRefs = collectStorePromptRefs(persisted.store);
	const json = JSON.stringify(persisted.store, null, 2);
	const cloneSerialized = persisted.changed ? void 0 : json;
	if (getSerializedSessionStore(storePath) === json) {
		await ensureSessionStorePromptBlobsForPersistence({
			storePath,
			promptBlobs
		});
		updateSessionStoreWriteCaches({
			storePath,
			store,
			serialized: json,
			serializedPromptRefs: promptRefs,
			cloneSerialized,
			takeOwnership: opts?.takeCacheOwnership
		});
		return;
	}
	if (process.platform === "win32") {
		let finalError;
		for (let i = 0; i < 5; i++) try {
			await writeSessionStoreAtomic({
				storePath,
				store,
				serialized: json,
				serializedPromptRefs: promptRefs,
				cloneSerialized,
				promptBlobs,
				takeOwnership: opts?.takeCacheOwnership
			});
			return;
		} catch (err) {
			finalError = err;
			if (getErrorCode(err) === "ENOENT") {
				if (opts?.requireWriteSuccess) throw err;
				return;
			}
			if (i < 4) {
				await new Promise((r) => {
					setTimeout(r, 50 * (i + 1));
				});
				continue;
			}
			log.warn(`atomic write failed after 5 attempts: ${storePath}`);
		}
		if (opts?.requireWriteSuccess) throw finalError;
		return;
	}
	try {
		await writeSessionStoreAtomic({
			storePath,
			store,
			serialized: json,
			serializedPromptRefs: promptRefs,
			cloneSerialized,
			promptBlobs,
			takeOwnership: opts?.takeCacheOwnership
		});
	} catch (err) {
		if (getErrorCode(err) === "ENOENT") {
			try {
				await writeSessionStoreAtomic({
					storePath,
					store,
					serialized: json,
					serializedPromptRefs: promptRefs,
					cloneSerialized,
					promptBlobs,
					takeOwnership: opts?.takeCacheOwnership
				});
			} catch (err2) {
				if (getErrorCode(err2) === "ENOENT") {
					if (opts?.requireWriteSuccess) throw err2;
					return;
				}
				throw err2;
			}
			return;
		}
		throw err;
	}
}
async function saveSessionStore(storePath, store, opts) {
	await runExclusiveSessionStoreWrite(storePath, async () => {
		await saveSessionStoreUnlocked(storePath, store, opts);
	});
}
async function updateSessionStore(storePath, mutator, opts) {
	return await runExclusiveSessionStoreWrite(storePath, async () => {
		const store = loadMutableSessionStoreForWriter(storePath);
		const result = await mutator(store);
		if (opts?.skipSaveWhenResult?.(result)) {
			restoreUnchangedSessionStoreCache(storePath, store);
			return result;
		}
		await saveSessionStoreUnlocked(storePath, store, {
			...opts,
			singleEntryPersistence: opts?.resolveSingleEntryPersistence?.(result) ?? void 0
		});
		return result;
	});
}
function cloneSessionEntryProjectionSnapshot(store) {
	return { entries: Object.entries(store).map(([sessionKey, entry]) => ({
		sessionKey,
		entry: cloneSessionEntry(entry)
	})) };
}
function resolveFreshestProjectedEntry(params) {
	let freshest;
	const keys = /* @__PURE__ */ new Set();
	for (const candidateKey of params.candidateKeys) {
		const trimmed = normalizeOptionalString(candidateKey) ?? "";
		if (!trimmed) continue;
		keys.add(trimmed);
		for (const match of findSessionStoreKeysIgnoreCase(params.store, trimmed)) keys.add(match);
	}
	for (const key of keys) {
		const entry = params.store[key];
		if (!entry) continue;
		if (!freshest || (entry.updatedAt ?? 0) > (freshest.updatedAt ?? 0)) freshest = entry;
	}
	return freshest;
}
function findSessionStoreKeysIgnoreCase(store, targetKey) {
	const lowered = normalizeLowercaseStringOrEmpty(targetKey);
	return Object.keys(store).filter((key) => normalizeLowercaseStringOrEmpty(key) === lowered);
}
function migrateSessionEntryProjectionTarget(params) {
	const candidateKeys = params.target.candidateKeys ?? [params.target.primaryKey];
	const freshest = resolveFreshestProjectedEntry({
		store: params.store,
		candidateKeys
	});
	const currentPrimary = params.store[params.target.primaryKey];
	if (freshest && (!currentPrimary || (freshest.updatedAt ?? 0) > (currentPrimary.updatedAt ?? 0))) params.store[params.target.primaryKey] = freshest;
	const keysToDelete = /* @__PURE__ */ new Set();
	for (const candidateKey of candidateKeys) {
		const trimmed = normalizeOptionalString(candidateKey) ?? "";
		if (!trimmed) continue;
		if (trimmed !== params.target.primaryKey) keysToDelete.add(trimmed);
		for (const match of findSessionStoreKeysIgnoreCase(params.store, trimmed)) if (match !== params.target.primaryKey) keysToDelete.add(match);
	}
	for (const key of keysToDelete) delete params.store[key];
}
/**
* Applies a storage-neutral entry projection inside the session-store writer.
* The projection receives a cloned snapshot and returns the replacement entry;
* it cannot mutate the backing whole store.
*/
async function applySessionEntryPatchProjection(params) {
	return await runExclusiveSessionStoreWrite(params.storePath, async () => {
		const store = loadMutableSessionStoreForWriter(params.storePath);
		const target = params.resolveTarget(cloneSessionEntryProjectionSnapshot(store));
		migrateSessionEntryProjectionTarget({
			store,
			target
		});
		const projected = await params.project({
			...target,
			entries: cloneSessionEntryProjectionSnapshot(store).entries,
			...store[target.primaryKey] ? { existingEntry: cloneSessionEntry(store[target.primaryKey]) } : {}
		});
		if (projected.ok) store[target.primaryKey] = cloneSessionEntry(projected.entry);
		await saveSessionStoreUnlocked(params.storePath, store, { activeSessionKey: target.primaryKey });
		return projected.ok ? {
			...projected,
			entry: cloneSessionEntry(projected.entry)
		} : projected;
	});
}
/** Resets one persisted session entry and rotates its file-backed transcript artifacts. */
async function resetSessionEntryLifecycle(params) {
	return await runExclusiveSessionStoreWrite(params.storePath, async () => {
		const store = loadMutableSessionStoreForWriter(params.storePath);
		const currentEntry = resolveLifecyclePrimaryEntry({
			store,
			target: params.target
		});
		const previousSessionId = currentEntry?.sessionId;
		const previousSessionFile = currentEntry?.sessionFile;
		const nextEntry = await params.buildNextEntry({
			currentEntry: cloneOptionalSessionEntry(currentEntry),
			primaryKey: params.target.canonicalKey
		});
		const nextSessionFile = nextEntry.sessionFile?.trim();
		if (!nextSessionFile) throw new Error("reset session lifecycle requires next entry sessionFile");
		store[params.target.canonicalKey] = nextEntry;
		await saveSessionStoreUnlocked(params.storePath, store);
		const mutation = { nextEntry: cloneSessionEntry(nextEntry) };
		const previousEntry = cloneOptionalSessionEntry(currentEntry);
		if (previousEntry) mutation.previousEntry = previousEntry;
		if (previousSessionFile) mutation.previousSessionFile = previousSessionFile;
		if (previousSessionId) mutation.previousSessionId = previousSessionId;
		await params.afterEntryMutation?.(mutation);
		const archivedTranscripts = await archiveLifecycleSessionTranscripts({
			sessionId: previousSessionId,
			storePath: params.storePath,
			sessionFile: previousSessionFile,
			agentId: params.agentId,
			reason: "reset"
		});
		ensureLifecycleTranscriptHeader({
			sessionFile: nextSessionFile,
			sessionId: nextEntry.sessionId
		});
		return {
			...mutation,
			archivedTranscripts
		};
	});
}
/** Deletes one persisted session entry and archives its file-backed transcript artifacts. */
async function deleteSessionEntryLifecycle(params) {
	return await runExclusiveSessionStoreWrite(params.storePath, async () => {
		const store = loadMutableSessionStoreForWriter(params.storePath);
		const deletedEntry = resolveLifecyclePrimaryEntry({
			store,
			target: params.target
		});
		if (!deletedEntry) {
			restoreUnchangedSessionStoreCache(params.storePath, store);
			return {
				archivedTranscripts: [],
				deleted: false
			};
		}
		const deletedSessionId = deletedEntry.sessionId;
		const deletedSessionFile = deletedEntry.sessionFile;
		delete store[params.target.canonicalKey];
		await saveSessionStoreUnlocked(params.storePath, store);
		const result = {
			archivedTranscripts: params.archiveTranscript ? await archiveLifecycleSessionTranscripts({
				sessionId: deletedSessionId,
				storePath: params.storePath,
				sessionFile: deletedSessionFile,
				agentId: params.agentId,
				reason: "deleted"
			}) : [],
			deleted: true
		};
		result.deletedEntry = cloneSessionEntry(deletedEntry);
		if (deletedSessionFile) result.deletedSessionFile = deletedSessionFile;
		if (deletedSessionId) result.deletedSessionId = deletedSessionId;
		return result;
	});
}
function shouldRemoveSessionEntry(entry, removal) {
	if (!entry) return false;
	if (removal.expectedEntry !== void 0 && JSON.stringify(entry) !== JSON.stringify(removal.expectedEntry)) return false;
	if (removal.expectedSessionId !== void 0 && entry.sessionId !== removal.expectedSessionId) return false;
	if (removal.expectedUpdatedAt !== void 0 && entry.updatedAt !== removal.expectedUpdatedAt) return false;
	return true;
}
/**
* Applies exact entry removals/upserts and lifecycle artifact cleanup as one
* backend-owned operation. Callers choose domain keys; storage owns the final
* referenced-session set used for transcript/artifact cleanup.
*/
async function applySessionEntryLifecycleMutation(params) {
	const storePath = path.resolve(params.storePath);
	const removedSessionFiles = /* @__PURE__ */ new Map();
	const removedSessionKeys = [];
	const archivedTranscriptDirectories = [];
	let unreferencedArtifacts = null;
	let maintenanceReport = null;
	let afterCount = 0;
	let artifactCleanupError;
	await runExclusiveSessionStoreWrite(storePath, async () => {
		const store = loadMutableSessionStoreForWriter(storePath);
		for (const removal of params.removals ?? []) {
			const sessionKey = removal.sessionKey.trim();
			if (!sessionKey) continue;
			const entry = store[sessionKey];
			if (!shouldRemoveSessionEntry(entry, removal)) continue;
			if (removal.archiveRemovedTranscript === true && entry.sessionId) rememberRemovedSessionFile(removedSessionFiles, entry);
			delete store[sessionKey];
			removedSessionKeys.push(sessionKey);
		}
		for (const upsert of params.upserts ?? []) {
			const sessionKey = upsert.sessionKey.trim();
			if (!sessionKey) continue;
			const entry = upsert.buildEntry === void 0 ? upsert.entry : await upsert.buildEntry({
				currentEntry: store[sessionKey] ? cloneSessionEntry(store[sessionKey]) : void 0,
				sessionKey,
				store
			});
			if (!entry) continue;
			store[sessionKey] = cloneSessionEntry(entry);
		}
		await saveSessionStoreUnlocked(storePath, store, {
			activeSessionKey: params.activeSessionKey,
			maintenanceOverride: params.maintenanceOverride,
			skipMaintenance: params.skipMaintenance,
			onMaintenanceApplied: (report) => {
				maintenanceReport = report;
			}
		});
		afterCount = Object.keys(store).length;
		const cleanupArtifacts = async () => {
			const referencedSessionIds = new Set(Object.values(store).map((entry) => entry?.sessionId).filter((sessionId) => Boolean(sessionId)));
			if (removedSessionFiles.size > 0) {
				const archivedDirs = await archiveRemovedSessionTranscripts({
					removedSessionFiles,
					referencedSessionIds,
					storePath,
					reason: params.archiveReason ?? "deleted",
					restrictToStoreDir: params.restrictArchivedTranscriptsToStoreDir
				});
				archivedTranscriptDirectories.push(...[...archivedDirs].toSorted());
				if (archivedDirs.size > 0 && params.cleanupArchivedTranscripts) {
					const { cleanupArchivedSessionTranscripts } = await loadSessionArchiveRuntime();
					await cleanupArchivedSessionTranscripts({
						directories: [...archivedDirs],
						rules: params.cleanupArchivedTranscripts.rules,
						nowMs: params.cleanupArchivedTranscripts.nowMs
					});
				}
			}
			if (params.pruneUnreferencedArtifacts) unreferencedArtifacts = await pruneUnreferencedSessionArtifacts({
				store,
				storePath,
				olderThanMs: params.pruneUnreferencedArtifacts.olderThanMs,
				dryRun: params.pruneUnreferencedArtifacts.dryRun
			});
		};
		try {
			await cleanupArtifacts();
		} catch (err) {
			if (params.captureArtifactCleanupError === true) artifactCleanupError = err;
			else throw err;
		}
	});
	return {
		removedEntries: removedSessionKeys.length,
		removedSessionKeys,
		archivedTranscriptDirectories,
		unreferencedArtifacts,
		maintenanceReport,
		afterCount,
		artifactCleanupError
	};
}
/**
* Purges entries owned by a deleted agent while holding the store writer lock.
* This preserves the old delete-time current-store owner check without
* exposing a mutable whole-store callback to callers.
*/
async function purgeDeletedAgentSessionEntries(params) {
	const storePath = path.resolve(params.storePath);
	const removedSessionKeys = [];
	let maintenanceReport = null;
	let afterCount = 0;
	await runExclusiveSessionStoreWrite(storePath, async () => {
		const store = loadMutableSessionStoreForWriter(storePath);
		for (const sessionKey of Object.keys(store)) if (resolveStoredSessionOwnerAgentId({
			cfg: params.cfg,
			agentId: params.storeAgentId,
			sessionKey
		}) === params.agentId) {
			delete store[sessionKey];
			removedSessionKeys.push(sessionKey);
		}
		await saveSessionStoreUnlocked(storePath, store, { onMaintenanceApplied: (report) => {
			maintenanceReport = report;
		} });
		afterCount = Object.keys(store).length;
	});
	return {
		removedEntries: removedSessionKeys.length,
		removedSessionKeys,
		archivedTranscriptDirectories: [],
		unreferencedArtifacts: null,
		maintenanceReport,
		afterCount
	};
}
async function archiveUnreferencedLifecycleTranscriptArtifacts(params) {
	const sessionsDir = path.dirname(path.resolve(params.storePath));
	return await runExclusiveSessionStoreWrite(params.storePath, async () => {
		const store = loadMutableSessionStoreForWriter(params.storePath);
		const referencedTranscriptPaths = /* @__PURE__ */ new Set();
		for (const entry of Object.values(store)) {
			const transcriptPath = resolveLifecycleTranscriptPath({
				entry,
				sessionsDir
			});
			if (transcriptPath) referencedTranscriptPaths.add(normalizePathForLifecycleComparison(transcriptPath));
		}
		restoreUnchangedSessionStoreCache(params.storePath, store);
		let entries;
		try {
			entries = await fs.promises.readdir(sessionsDir, { withFileTypes: true });
		} catch {
			return 0;
		}
		const { archiveSessionTranscripts } = await loadSessionArchiveRuntime();
		let archived = 0;
		for (const entry of entries) {
			if (!entry.isFile() || !entry.name.endsWith(".jsonl")) continue;
			const transcriptPath = path.join(sessionsDir, entry.name);
			if (referencedTranscriptPaths.has(normalizePathForLifecycleComparison(transcriptPath))) continue;
			let stat;
			try {
				stat = await fs.promises.stat(transcriptPath);
			} catch {
				continue;
			}
			if (params.nowMs - stat.mtimeMs < params.orphanTranscriptMinAgeMs) continue;
			let content;
			try {
				content = await fs.promises.readFile(transcriptPath, "utf-8");
			} catch {
				continue;
			}
			if (!content.includes(params.transcriptContentMarker)) continue;
			const sessionId = entry.name.slice(0, -6);
			archived += archiveSessionTranscripts({
				sessionId,
				storePath: params.storePath,
				sessionFile: transcriptPath,
				reason: "deleted",
				restrictToStoreDir: true
			}).length;
		}
		return archived;
	});
}
/** Cleans scoped session lifecycle entries and their unreferenced transcript artifacts. */
async function cleanupSessionLifecycleArtifacts(params) {
	const sessionKeySegmentPrefix = params.sessionKeySegmentPrefix.trim();
	const transcriptContentMarker = params.transcriptContentMarker;
	if (!sessionKeySegmentPrefix || !transcriptContentMarker) return {
		removedEntries: 0,
		archivedTranscriptArtifacts: 0
	};
	const nowMs = params.nowMs ?? Date.now();
	const storePath = path.resolve(params.storePath);
	const sessionsDir = path.dirname(storePath);
	const removedSessionFiles = /* @__PURE__ */ new Map();
	const removedTranscriptPaths = [];
	let removedEntries = 0;
	let archivedTranscriptArtifacts = 0;
	await runExclusiveSessionStoreWrite(storePath, async () => {
		const store = loadMutableSessionStoreForWriter(storePath);
		for (const [sessionKey, entry] of Object.entries(store)) {
			const transcriptPath = resolveLifecycleTranscriptPath({
				entry,
				sessionsDir
			});
			if (sessionKeySegmentStartsWith(sessionKey, sessionKeySegmentPrefix) && lifecycleTranscriptIsReclaimable({
				transcriptPath,
				nowMs,
				orphanTranscriptMinAgeMs: params.orphanTranscriptMinAgeMs
			})) {
				rememberRemovedSessionFile(removedSessionFiles, entry);
				if (entry.sessionId && transcriptPath && fs.existsSync(transcriptPath)) removedTranscriptPaths.push({
					sessionId: entry.sessionId,
					transcriptPath
				});
				delete store[sessionKey];
				removedEntries += 1;
				continue;
			}
		}
		if (removedEntries === 0) {
			restoreUnchangedSessionStoreCache(storePath, store);
			return;
		}
		const referencedSessionIds = new Set(Object.values(store).map((entry) => entry?.sessionId).filter((sessionId) => Boolean(sessionId)));
		for (const { sessionId: removedSessionId, transcriptPath } of removedTranscriptPaths) {
			if (referencedSessionIds.has(removedSessionId)) continue;
			archivedTranscriptArtifacts += archiveExactLifecycleTranscriptPath({
				sessionsDir,
				transcriptPath
			});
		}
		const { removeRemovedSessionTrajectoryArtifacts } = await loadTrajectoryCleanupRuntime();
		await removeRemovedSessionTrajectoryArtifacts({
			removedSessionFiles,
			referencedSessionIds,
			storePath,
			restrictToStoreDir: true
		});
		await saveSessionStoreUnlocked(storePath, store, { skipMaintenance: true });
	});
	return {
		removedEntries,
		archivedTranscriptArtifacts: archivedTranscriptArtifacts + await archiveUnreferencedLifecycleTranscriptArtifacts({
			storePath,
			transcriptContentMarker,
			orphanTranscriptMinAgeMs: params.orphanTranscriptMinAgeMs,
			nowMs
		})
	};
}
function getErrorCode(error) {
	if (!error || typeof error !== "object" || !("code" in error)) return null;
	return String(error.code);
}
function rememberRemovedSessionFile(removedSessionFiles, entry) {
	if (!removedSessionFiles.has(entry.sessionId) || entry.sessionFile) removedSessionFiles.set(entry.sessionId, entry.sessionFile);
}
async function archiveRemovedSessionTranscripts(params) {
	const { archiveSessionTranscripts } = await loadSessionArchiveRuntime();
	const archivedDirs = /* @__PURE__ */ new Set();
	for (const [sessionId, sessionFile] of params.removedSessionFiles) {
		if (params.referencedSessionIds.has(sessionId)) continue;
		const archived = archiveSessionTranscripts({
			sessionId,
			storePath: params.storePath,
			sessionFile,
			reason: params.reason,
			restrictToStoreDir: params.restrictToStoreDir
		});
		for (const archivedPath of archived) archivedDirs.add(path.dirname(archivedPath));
	}
	return archivedDirs;
}
async function writeSessionStoreAtomic(params) {
	await writeTextAtomic(params.storePath, params.serialized, {
		durable: false,
		mode: 384,
		tempPrefix: path.basename(params.storePath),
		beforeRename: async () => {
			await ensureSessionStorePromptBlobsForPersistence({
				storePath: params.storePath,
				promptBlobs: params.promptBlobs
			});
		}
	});
	updateSessionStoreWriteCaches({
		storePath: params.storePath,
		store: params.store,
		serialized: params.serialized,
		serializedPromptRefs: params.serializedPromptRefs,
		cloneSerialized: params.cloneSerialized,
		takeOwnership: params.takeOwnership
	});
}
async function persistResolvedSessionEntry(params) {
	const entryUnchanged = params.resolved.legacyKeys.length === 0 && sessionEntriesHaveSameSerializedForm(params.resolved.existing, params.next);
	const next = params.takeCacheOwnership ? cloneSessionEntry(params.next) : params.next;
	params.store[params.resolved.normalizedKey] = next;
	for (const legacyKey of params.resolved.legacyKeys) delete params.store[legacyKey];
	await saveSessionStoreUnlocked(params.storePath, params.store, {
		activeSessionKey: params.resolved.normalizedKey,
		skipMaintenance: params.skipMaintenance,
		maintenanceConfig: params.maintenanceConfig,
		skipSerializeForUnchangedStore: entryUnchanged,
		singleEntryPersistence: params.resolved.legacyKeys.length === 0 && params.resolved.existing ? {
			sessionKey: params.resolved.normalizedKey,
			entry: next
		} : void 0,
		takeCacheOwnership: params.takeCacheOwnership,
		requireWriteSuccess: params.requireWriteSuccess
	});
	return entryUnchanged || params.returnDetached ? cloneSessionEntry(next) : next;
}
async function updateSessionStoreEntry(params) {
	const { storePath, sessionKey, update } = params;
	return await runExclusiveSessionStoreWrite(storePath, async () => {
		const store = loadMutableSessionStoreForWriter(storePath);
		const resolved = resolveSessionStoreEntry({
			store,
			sessionKey
		});
		const existing = resolved.existing;
		if (!existing) return null;
		const patch = await update(cloneSessionEntry(existing));
		if (!patch) return existing;
		return await persistResolvedSessionEntry({
			storePath,
			store,
			resolved,
			next: mergeSessionEntry(existing, patch),
			skipMaintenance: params.skipMaintenance,
			takeCacheOwnership: params.takeCacheOwnership ?? true,
			requireWriteSuccess: params.requireWriteSuccess,
			returnDetached: params.takeCacheOwnership !== true
		});
	});
}
async function applySessionStoreEntryPatch(params) {
	const { storePath, sessionKey, patch } = params;
	return await runExclusiveSessionStoreWrite(storePath, async () => {
		const store = loadMutableSessionStoreForWriter(storePath);
		const resolved = resolveSessionStoreEntry({
			store,
			sessionKey
		});
		const existing = resolved.existing;
		if (!existing) return null;
		return await persistResolvedSessionEntry({
			storePath,
			store,
			resolved,
			next: mergeSessionEntry(existing, patch),
			skipMaintenance: params.skipMaintenance,
			takeCacheOwnership: params.takeCacheOwnership ?? true,
			returnDetached: params.takeCacheOwnership !== true
		});
	});
}
async function patchSessionEntry(params) {
	const storePath = resolveSessionWorkflowStorePath(params);
	return await runExclusiveSessionStoreWrite(storePath, async () => {
		const store = loadMutableSessionStoreForWriter(storePath);
		const resolved = resolveSessionStoreEntry({
			store,
			sessionKey: params.sessionKey
		});
		const existing = resolved.existing ?? params.fallbackEntry;
		if (!existing) return null;
		const patch = await params.update(cloneSessionEntry(existing), { existingEntry: resolved.existing ? cloneSessionEntry(resolved.existing) : void 0 });
		if (!patch) return existing;
		return await persistResolvedSessionEntry({
			storePath,
			store,
			resolved,
			next: params.replaceEntry ? cloneSessionEntry(patch) : params.preserveActivity ? mergeSessionEntryPreserveActivity(existing, patch) : mergeSessionEntry(existing, patch),
			maintenanceConfig: params.maintenanceConfig,
			takeCacheOwnership: true,
			returnDetached: true
		});
	});
}
async function recordSessionMetaFromInbound(params) {
	const { storePath, sessionKey, ctx } = params;
	const createIfMissing = params.createIfMissing ?? true;
	return await runExclusiveSessionStoreWrite(storePath, async () => {
		const store = loadMutableSessionStoreForWriter(storePath);
		const resolved = resolveSessionStoreEntry({
			store,
			sessionKey
		});
		const existing = resolved.existing;
		const patch = deriveSessionMetaPatch({
			ctx,
			sessionKey: resolved.normalizedKey,
			existing,
			groupResolution: params.groupResolution
		});
		if (!patch) {
			if (existing && resolved.legacyKeys.length > 0) return await persistResolvedSessionEntry({
				storePath,
				store,
				resolved,
				next: existing,
				takeCacheOwnership: true,
				returnDetached: true
			});
			await saveSessionStoreUnlocked(storePath, store, {
				activeSessionKey: resolved.normalizedKey,
				skipSerializeForUnchangedStore: true
			});
			return existing ? cloneSessionEntry(existing) : null;
		}
		if (!existing && !createIfMissing) {
			await saveSessionStoreUnlocked(storePath, store, {
				activeSessionKey: resolved.normalizedKey,
				skipSerializeForUnchangedStore: true
			});
			return null;
		}
		return await persistResolvedSessionEntry({
			storePath,
			store,
			resolved,
			next: existing ? mergeSessionEntryPreserveActivity(existing, patch) : mergeSessionEntry(existing, patch),
			takeCacheOwnership: true,
			returnDetached: true
		});
	});
}
async function updateLastRoute(params) {
	const { storePath, sessionKey, channel, to, accountId, threadId, ctx } = params;
	const createIfMissing = params.createIfMissing ?? true;
	return await runExclusiveSessionStoreWrite(storePath, async () => {
		const store = loadMutableSessionStoreForWriter(storePath);
		const resolved = resolveSessionStoreEntry({
			store,
			sessionKey
		});
		const existing = resolved.existing;
		if (!existing && !createIfMissing) return null;
		const explicitContext = normalizeDeliveryContext(params.deliveryContext);
		const inlineContext = normalizeDeliveryContext({
			channel,
			to,
			accountId,
			threadId
		});
		const routeContext = deliveryContextFromChannelRoute(params.route);
		const mergedInput = mergeDeliveryContext(routeContext, mergeDeliveryContext(explicitContext, inlineContext));
		const explicitDeliveryContext = params.deliveryContext;
		const explicitThreadValue = (explicitDeliveryContext != null && Object.hasOwn(explicitDeliveryContext, "threadId") ? explicitDeliveryContext.threadId : void 0) ?? (threadId != null && threadId !== "" ? threadId : void 0);
		const merged = mergeDeliveryContext(mergedInput, Boolean(routeContext?.channel || routeContext?.to || explicitContext?.channel || explicitContext?.to || inlineContext?.channel || inlineContext?.to) && explicitThreadValue == null ? removeThreadFromDeliveryContext(deliveryContextFromSession(existing)) : deliveryContextFromSession(existing));
		const normalized = normalizeSessionDeliveryFields({
			route: params.route,
			deliveryContext: {
				channel: merged?.channel,
				to: merged?.to,
				accountId: merged?.accountId,
				threadId: merged?.threadId
			}
		});
		const metaPatch = ctx ? deriveSessionMetaPatch({
			ctx,
			sessionKey: resolved.normalizedKey,
			existing,
			groupResolution: params.groupResolution
		}) : null;
		const basePatch = {
			route: normalized.route,
			deliveryContext: normalized.deliveryContext,
			lastChannel: normalized.lastChannel,
			lastTo: normalized.lastTo,
			lastAccountId: normalized.lastAccountId,
			lastThreadId: normalized.lastThreadId
		};
		return await persistResolvedSessionEntry({
			storePath,
			store,
			resolved,
			next: mergeSessionEntryPreserveActivity(existing, metaPatch ? {
				...basePatch,
				...metaPatch
			} : basePatch),
			takeCacheOwnership: true,
			returnDetached: true
		});
	});
}
//#endregion
export { resolveSessionStoreAgentId as A, buildGroupDisplayName as C, resolveSessionArtifactCanonicalPathsForEntry as D, pruneUnreferencedSessionArtifacts as E, resolveStoredSessionKeyForAgentStore as M, resolveStoredSessionOwnerAgentId as N, canonicalizeSessionKeyForAgent as O, snapshotSessionOrigin as S, enforceSessionDiskBudget as T, updateSessionStoreEntry as _, cleanupSessionLifecycleArtifacts as a, deriveSessionMetaPatch as b, listSessionEntries as c, readSessionUpdatedAt as d, recordSessionMetaFromInbound as f, updateSessionStore as g, updateLastRoute as h, archiveRemovedSessionTranscripts as i, resolveSessionStoreKey as j, canonicalizeSpawnedByForAgent as k, patchSessionEntry as l, saveSessionStore as m, applySessionEntryPatchProjection as n, deleteSessionEntryLifecycle as o, resetSessionEntryLifecycle as p, applySessionStoreEntryPatch as r, getSessionEntry as s, applySessionEntryLifecycleMutation as t, purgeDeletedAgentSessionEntries as u, clearSessionStoreCacheForTest as v, resolveGroupSessionKey as w, deriveSessionOrigin as x, deriveGroupSessionPatch as y };
