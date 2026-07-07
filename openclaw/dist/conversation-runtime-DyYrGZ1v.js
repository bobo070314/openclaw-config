import "./session-binding-service-Dz0wDjnb.js";
import "./thread-bindings-policy-zb2mAAVM.js";
import "./channel-access-compat-CmuaCPIx.js";
import "./conversation-binding-CPR7Zjnd.js";
import "./binding-registry-B8xIHILn.js";
import "./session-Dm5l-CcD.js";
import "./pairing-store-Bgc-ubwP.js";
import "./binding-targets-BVJTxlyr.js";
import "./binding-routing-DlasBIGx.js";
import "./pairing-labels-CCGQfyzb.js";
//#region src/channels/session-meta.ts
let inboundSessionRuntimePromise = null;
function loadInboundSessionRuntime() {
	inboundSessionRuntimePromise ??= import("./inbound.runtime.js");
	return inboundSessionRuntimePromise;
}
/**
* Best-effort inbound session metadata recorder for channel plugin command handlers.
*/
async function recordInboundSessionMetaSafe(params) {
	const runtime = await loadInboundSessionRuntime();
	const storePath = runtime.resolveStorePath(params.cfg.session?.store, { agentId: params.agentId });
	try {
		await runtime.recordSessionMetaFromInbound({
			storePath,
			sessionKey: params.sessionKey,
			ctx: params.ctx
		});
	} catch (err) {
		params.onError?.(err);
	}
}
//#endregion
export { recordInboundSessionMetaSafe as t };
