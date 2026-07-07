import { i as MsgContext } from "./templating-Bx-yYzyQ.js";
import { n as GroupKeyResolution } from "./types-CUUb7tbP.js";
import { t as InboundLastRouteUpdate } from "./session.types-o_o2gWOV.js";

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