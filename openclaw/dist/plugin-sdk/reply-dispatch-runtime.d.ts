import { a as CommandTurnContext } from "./templating-Bx-yYzyQ.js";
import { v as resolveChunkMode } from "./outbound.types-D8j53lhL.js";
import { Gr as DispatchReplyWithBufferedBlockDispatcher, Kr as DispatchReplyWithDispatcher, Ur as finalizeInboundContext } from "./types-B70zVumi.js";
import { r as ReplyPayload } from "./reply-payload-cBVog_19.js";
import { n as generateConversationLabel } from "./conversation-label-generator-DQqK0buF.js";

//#region src/plugin-sdk/reply-dispatch-runtime.d.ts
/** Dispatches a reply with buffered block support after lazy-loading the runtime dispatcher. */
declare const dispatchReplyWithBufferedBlockDispatcher: DispatchReplyWithBufferedBlockDispatcher;
/** Dispatches a reply through the provider dispatcher after lazy-loading runtime code. */
declare const dispatchReplyWithDispatcher: DispatchReplyWithDispatcher;
//#endregion
export { type CommandTurnContext, type DispatchReplyWithBufferedBlockDispatcher, type DispatchReplyWithDispatcher, type ReplyPayload, dispatchReplyWithBufferedBlockDispatcher, dispatchReplyWithDispatcher, finalizeInboundContext, generateConversationLabel, resolveChunkMode };