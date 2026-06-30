import { i as OpenClawConfig } from "./types.openclaw-BhmF31_h.js";
//#region src/sessions/transcript-events.d.ts
/** Normalized transcript update emitted after a session transcript changes. */
type SessionTranscriptUpdate = {
  sessionFile: string;
  sessionKey?: string;
  agentId?: string;
  message?: unknown;
  messageId?: string;
  messageSeq?: number;
};
type SessionTranscriptListener = (update: SessionTranscriptUpdate) => void;
/** Registers a listener for normalized session transcript updates. */
declare function onSessionTranscriptUpdate(listener: SessionTranscriptListener): () => void;
/** Emits a normalized transcript update to all registered listeners. */
declare function emitSessionTranscriptUpdate(update: string | SessionTranscriptUpdate): void;
//#endregion
//#region src/config/sessions/session-accessor.d.ts
type TranscriptMessageAppendOptions<TMessage> = {
  /** Runtime config used for message redaction and transcript header metadata. */config?: OpenClawConfig; /** Working directory recorded in a newly created transcript header. */
  cwd?: string; /** How duplicate message idempotency keys are detected before append. */
  idempotencyLookup?: "scan" | "caller-checked"; /** Provider/channel message payload to persist. */
  message: TMessage; /** Testable timestamp override for the generated transcript entry. */
  now?: number; /** Optional finalizer that runs after duplicate detection but before persistence. */
  prepareMessageAfterIdempotencyCheck?: (message: TMessage) => TMessage | undefined; /** Allow append without parent-link migration for large legacy linear transcripts. */
  useRawWhenLinear?: boolean;
};
type TranscriptMessageAppendResult<TMessage> = {
  /** False when idempotency lookup found an existing transcript message. */appended: boolean; /** Redacted message payload as persisted or replayed from the transcript. */
  message: TMessage; /** Existing or newly generated transcript message id. */
  messageId: string;
};
/** Transcript update fields supplied by callers; sessionFile is resolved here. */
type TranscriptUpdatePayload = Omit<SessionTranscriptUpdate, "sessionFile">;
//#endregion
export { onSessionTranscriptUpdate as a, emitSessionTranscriptUpdate as i, TranscriptMessageAppendResult as n, TranscriptUpdatePayload as r, TranscriptMessageAppendOptions as t };