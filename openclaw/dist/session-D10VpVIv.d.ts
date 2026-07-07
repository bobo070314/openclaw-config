import { i as MsgContext } from "./templating-C0ehoyWm.js";
import { n as GroupKeyResolution } from "./types-CznwT7G6.js";
import { t as InboundLastRouteUpdate } from "./session.types-CJv8Z18t.js";

//#region src/channels/session.d.ts
declare function recordInboundSession(params: {
  storePath: string;
  sessionKey: string;
  ctx: MsgContext;
  groupResolution?: GroupKeyResolution | null;
  createIfMissing?: boolean;
  updateLastRoute?: InboundLastRouteUpdate;
  onRecordError: (err: unknown) => void;
  trackSessionMetaTask?: (task: Promise<unknown>) => void;
}): Promise<void>;
//#endregion
export { recordInboundSession as t };