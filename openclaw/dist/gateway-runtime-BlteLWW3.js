import "./net-DQvRbvSK.js";
import "./auth-BDsIZbhK.js";
import "./client-3vtaGf-F.js";
import "./src-BNueln22.js";
import "./operator-approvals-client-XaFrnmEE.js";
import "./gateway-rpc-F1VG-cTS.js";
import "./hosted-plugin-surface-url-DIYZ_g74.js";
import "./plugin-node-capability-CQtFV9Fn.js";
import "./node-command-policy-i3oM6xGs.js";
import "./nodes.helpers-CmLaCjBA.js";
import "./startup-auth-dtNWepEF.js";
//#region src/gateway/channel-status-patches.ts
/** Creates a connected-channel status patch with matching connection/event timestamps. */
function createConnectedChannelStatusPatch(at = Date.now()) {
	return {
		connected: true,
		lastConnectedAt: at,
		lastEventAt: at
	};
}
/** Creates a transport-activity patch for health/activity monitors. */
function createTransportActivityStatusPatch(at = Date.now()) {
	return { lastTransportActivityAt: at };
}
//#endregion
export { createTransportActivityStatusPatch as n, createConnectedChannelStatusPatch as t };
