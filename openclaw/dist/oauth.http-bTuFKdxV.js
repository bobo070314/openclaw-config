import { c as shouldUseEnvHttpProxyForUrl } from "./proxy-env-B9aW4MXJ.js";
import { r as fetchWithSsrFGuard } from "./fetch-guard-DOG_pqmj.js";
import { t as withTrustedEnvProxyGuardedFetchMode } from "./fetch-runtime-C_C_UhEb.js";
import "./ssrf-runtime-CV6TBXbQ.js";
import { a as DEFAULT_FETCH_TIMEOUT_MS } from "./oauth.shared-BD6M390i.js";
//#region extensions/google/oauth.http.ts
async function fetchWithTimeout(url, init, timeoutMs = DEFAULT_FETCH_TIMEOUT_MS) {
	const guardedOptions = {
		url,
		init,
		timeoutMs
	};
	const { response, release } = await fetchWithSsrFGuard(shouldUseEnvHttpProxyForUrl(url) ? withTrustedEnvProxyGuardedFetchMode(guardedOptions) : guardedOptions);
	try {
		const body = await response.arrayBuffer();
		return new Response(body, {
			status: response.status,
			statusText: response.statusText,
			headers: response.headers
		});
	} finally {
		await release();
	}
}
//#endregion
export { fetchWithTimeout as t };
