import { h as readResponseTextLimited } from "./provider-http-errors-eOZDQ0A5.js";
import { t as resolveFetch } from "./fetch-C13FzR_K.js";
import "./fetch-runtime-C_C_UhEb.js";
import "./provider-http-b4uHLlJ1.js";
//#region extensions/discord/src/pluralkit.ts
const PLURALKIT_API_BASE = "https://api.pluralkit.me/v2";
const PLURALKIT_ERROR_BODY_LIMIT_BYTES = 8 * 1024;
async function fetchPluralKitMessageInfo(params) {
	if (!params.config?.enabled) return null;
	const fetchImpl = resolveFetch(params.fetcher);
	if (!fetchImpl) return null;
	const headers = {};
	if (params.config.token?.trim()) headers.Authorization = params.config.token.trim();
	const res = await fetchImpl(`${PLURALKIT_API_BASE}/messages/${params.messageId}`, { headers });
	if (res.status === 404) return null;
	if (!res.ok) {
		const text = await readResponseTextLimited(res, PLURALKIT_ERROR_BODY_LIMIT_BYTES).catch(() => "");
		const detail = text.trim() ? `: ${text.trim()}` : "";
		throw new Error(`PluralKit API failed (${res.status})${detail}`);
	}
	return await res.json();
}
//#endregion
export { fetchPluralKitMessageInfo as t };
