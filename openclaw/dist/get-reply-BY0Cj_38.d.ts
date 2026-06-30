import { i as OpenClawConfig } from "./types.openclaw-BhmF31_h.js";
import { f as ReplyPayload, n as GetReplyOptions } from "./types-Iy-uj5hQ.js";
import { i as MsgContext } from "./templating-C0ehoyWm.js";

//#region src/auto-reply/reply/get-reply.d.ts
declare function getReplyFromConfig(ctx: MsgContext, opts?: GetReplyOptions, configOverride?: OpenClawConfig): Promise<ReplyPayload | ReplyPayload[] | undefined>;
//#endregion
export { getReplyFromConfig as t };