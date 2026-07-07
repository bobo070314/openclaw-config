import "./media-runtime-CP3Buesq.js";
import "./text-chunking-Dv_a57u3.js";
import { t as createPluginRuntimeStore } from "./runtime-store-uAKGMqTs.js";
import "./channel-outbound-CHb-uDxw.js";
import "./outbound-media-DbqHlRw6.js";
import "./ssrf-runtime-CV6TBXbQ.js";
import "./dangerous-name-runtime-cJriWyuh.js";
import "./channel-status-DMvqj2bH.js";
import "./bundled-channel-config-schema-DhL_IZva.js";
import "./channel-config-primitives-CPllmy5H.js";
import "./channel-actions-Cwo0Wl2P.js";
import "./channel-inbound-Bl4qL4ZS.js";
import "./channel-feedback-CVLJbdV5.js";
import "./channel-pairing-Cr6y6rdp.js";
import "./webhook-request-guards-Dm3cs_53.js";
import "./webhook-ingress-Btd-EgwJ.js";
import "./webhook-targets-k9Oe4zzO.js";
//#region extensions/googlechat/src/runtime.ts
const { setRuntime: setGoogleChatRuntime, getRuntime: getGoogleChatRuntime } = createPluginRuntimeStore({
	pluginId: "googlechat",
	errorMessage: "Google Chat runtime not initialized"
});
//#endregion
export { setGoogleChatRuntime as n, getGoogleChatRuntime as t };
