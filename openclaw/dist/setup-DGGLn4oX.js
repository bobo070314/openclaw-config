import "./utils-BmpsSbZo.js";
import "./types.secrets-BHLVnd7g.js";
import "./setup-helpers-CPWoWqOy.js";
import "./detect-binary-DadXAZmP.js";
import "./setup-wizard-helpers-BbMLtT3s.js";
import "./setup-wizard-proxy-DVTokaGk.js";
//#region src/plugin-sdk/resolution-notes.ts
/** Format a short note that separates successfully resolved targets from unresolved passthrough values. */
function formatResolvedUnresolvedNote(params) {
	if (params.resolved.length === 0 && params.unresolved.length === 0) return;
	return [params.resolved.length > 0 ? `Resolved: ${params.resolved.join(", ")}` : void 0, params.unresolved.length > 0 ? `Unresolved (kept as typed): ${params.unresolved.join(", ")}` : void 0].filter(Boolean).join("\n");
}
//#endregion
export { formatResolvedUnresolvedNote as t };
