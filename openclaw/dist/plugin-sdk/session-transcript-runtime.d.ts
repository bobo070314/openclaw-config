import { n as TranscriptMessageAppendResult, r as TranscriptUpdatePayload, t as TranscriptMessageAppendOptions } from "./session-accessor-DAKXqqth.js";
import { a as SessionTranscriptMemoryHitKeyParams, c as parseSessionTranscriptMemoryHitKey, i as SessionTranscriptMemoryHitKey, l as resolveSessionTranscriptMemoryHitKeyToSessionKeys, n as SessionTranscriptIdentity, o as SessionTranscriptReadParams, r as SessionTranscriptMemoryHitIdentity, s as formatSessionTranscriptMemoryHitKey, t as ResolveSessionTranscriptMemoryHitKeyParams } from "./session-transcript-memory-hit-BxQ_JGZh.js";

//#region src/plugin-sdk/session-transcript-runtime.d.ts
type SessionTranscriptEvent = unknown;
type SessionTranscriptTargetParams = SessionTranscriptReadParams & {
  /**
   * @deprecated Prefer `{ agentId, sessionKey, sessionId }`. Pass this only
   * when adapting code that already receives an active transcript artifact and
   * needs each helper to operate on that same artifact.
   */
  sessionFile?: string;
};
type SessionTranscriptTarget = SessionTranscriptIdentity & {
  targetKind: "active-session-file" | "runtime-session";
};
type SessionTranscriptAppendMessageParams<TMessage> = SessionTranscriptTargetParams & TranscriptMessageAppendOptions<TMessage>;
type SessionTranscriptWriteLockParams = SessionTranscriptTargetParams & {
  config?: TranscriptMessageAppendOptions<unknown>["config"];
};
type SessionTranscriptWriteLockContext = {
  appendMessage: <TMessage>(options: Omit<TranscriptMessageAppendOptions<TMessage>, "config">) => Promise<TranscriptMessageAppendResult<TMessage> | undefined>;
  publishUpdate: (update?: TranscriptUpdatePayload) => Promise<void>;
  readEvents: () => Promise<SessionTranscriptEvent[]>;
  target: SessionTranscriptTarget;
};
/**
 * Resolves the public identity for a transcript without returning its file path.
 */
declare function resolveSessionTranscriptIdentity(params: SessionTranscriptReadParams): Promise<SessionTranscriptIdentity>;
/**
 * Resolves the public target for transcript operations without exposing the
 * current storage path as identity.
 */
declare function resolveSessionTranscriptTarget(params: SessionTranscriptTargetParams): Promise<SessionTranscriptTarget>;
/**
 * Reads transcript events by public session identity instead of file path.
 */
declare function readSessionTranscriptEvents(params: SessionTranscriptTargetParams): Promise<SessionTranscriptEvent[]>;
/**
 * Appends a transcript message by scoped transcript target.
 */
declare function appendSessionTranscriptMessageByIdentity<TMessage>(params: SessionTranscriptAppendMessageParams<TMessage>): Promise<TranscriptMessageAppendResult<TMessage> | undefined>;
/**
 * Publishes a transcript update by scoped transcript target.
 */
declare function publishSessionTranscriptUpdateByIdentity(params: SessionTranscriptTargetParams & {
  update?: TranscriptUpdatePayload;
}): Promise<void>;
/**
 * Runs transcript work under the write lock for the resolved scoped target.
 */
declare function withSessionTranscriptWriteLock<T>(params: SessionTranscriptWriteLockParams, run: (context: SessionTranscriptWriteLockContext) => Promise<T> | T): Promise<T>;
//#endregion
export { type ResolveSessionTranscriptMemoryHitKeyParams, SessionTranscriptAppendMessageParams, SessionTranscriptEvent, type SessionTranscriptIdentity, type SessionTranscriptMemoryHitIdentity, type SessionTranscriptMemoryHitKey, type SessionTranscriptMemoryHitKeyParams, type SessionTranscriptReadParams, SessionTranscriptTarget, SessionTranscriptTargetParams, SessionTranscriptWriteLockContext, SessionTranscriptWriteLockParams, appendSessionTranscriptMessageByIdentity, formatSessionTranscriptMemoryHitKey, parseSessionTranscriptMemoryHitKey, publishSessionTranscriptUpdateByIdentity, readSessionTranscriptEvents, resolveSessionTranscriptIdentity, resolveSessionTranscriptMemoryHitKeyToSessionKeys, resolveSessionTranscriptTarget, withSessionTranscriptWriteLock };