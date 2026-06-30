import { mn as errorShape, pn as ErrorCodes } from "./schema-BrDi0lZs.js";
import "./src-BNueln22.js";
import { t as formatForLog } from "./ws-log-CWfbQxL_.js";
import { i as setVoiceWakeTriggers, n as normalizeVoiceWakeTriggers, r as loadVoiceWakeConfig } from "./server-utils-DGEd_1Oo.js";
//#region src/gateway/server-methods/voicewake.ts
/** Gateway request handlers for reading and updating voice wake triggers. */
const voicewakeHandlers = {
	"voicewake.get": async ({ respond }) => {
		try {
			respond(true, { triggers: (await loadVoiceWakeConfig()).triggers });
		} catch (err) {
			respond(false, void 0, errorShape(ErrorCodes.UNAVAILABLE, formatForLog(err)));
		}
	},
	"voicewake.set": async ({ params, respond, context }) => {
		if (!Array.isArray(params.triggers)) {
			respond(false, void 0, errorShape(ErrorCodes.INVALID_REQUEST, "voicewake.set requires triggers: string[]"));
			return;
		}
		try {
			const cfg = await setVoiceWakeTriggers(normalizeVoiceWakeTriggers(params.triggers));
			context.broadcastVoiceWakeChanged(cfg.triggers);
			respond(true, { triggers: cfg.triggers });
		} catch (err) {
			respond(false, void 0, errorShape(ErrorCodes.UNAVAILABLE, formatForLog(err)));
		}
	}
};
//#endregion
export { voicewakeHandlers };
