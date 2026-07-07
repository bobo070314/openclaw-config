import "./undici-runtime-BfllGx-h.js";
import "./ssrf-DmSIVBht.js";
import "./node-proxy-agent-CWnkEd0Y.js";
import "./proxy-fetch-Cs4HXql4.js";
import "./fetch-C13FzR_K.js";
//#region src/plugin-sdk/fetch-runtime.ts
/** Apply the trusted-env-proxy guarded fetch preset without exposing raw mode strings to plugins. */
function withTrustedEnvProxyGuardedFetchMode(params) {
	return {
		...params,
		mode: "trusted_env_proxy"
	};
}
//#endregion
export { withTrustedEnvProxyGuardedFetchMode as t };
