import { t as DEFAULT_ACCOUNT_ID } from "../../account-id-5IgE9UKY.js";
import { r as buildChannelConfigSchema } from "../../config-schema-CFVaMM-z.js";
import { p as formatTrimmedAllowFromEntries } from "../../channel-config-helpers-5wam5y3m.js";
import { a as resolveChannelMediaMaxBytes } from "../../media-runtime-CP3Buesq.js";
import { t as chunkTextForOutbound } from "../../text-chunking-Dv_a57u3.js";
import { c as getChatChannelMeta } from "../../core-DSBgt6Pg.js";
import { t as PAIRING_APPROVED_MESSAGE } from "../../pairing-message-DNhqI-OE.js";
import { c as collectStatusIssuesFromLastError, r as buildComputedAccountStatusSnapshot } from "../../status-helpers-CMNeqAe_.js";
import "../../channel-status-DMvqj2bH.js";
import { i as IMessageConfigSchema } from "../../bundled-channel-config-schema-DhL_IZva.js";
import { a as resolveIMessageAccount } from "../../accounts-BOMzFUbH.js";
import { f as setIMessageRuntime } from "../../monitor-reply-cache-MpvSgrUj.js";
import { o as probeIMessage } from "../../sanitize-outbound-CToPBvEI.js";
import { n as resolveIMessageGroupToolPolicy, r as imessageMessageActions, t as resolveIMessageGroupRequireMention } from "../../group-policy-D073BZWc.js";
import { n as normalizeIMessageMessagingTarget, t as looksLikeIMessageTargetId } from "../../normalize-brecK3tj.js";
import "../../config-api-CqnPyyFP.js";
import { t as monitorIMessageProvider } from "../../monitor-yIqYLwyY.js";
import { t as sendMessageIMessage } from "../../send-CTGVU9X6.js";
//#region extensions/imessage/src/config-accessors.ts
function resolveIMessageConfigAllowFrom(params) {
	return (resolveIMessageAccount(params).config.allowFrom ?? []).map((entry) => String(entry));
}
function resolveIMessageConfigDefaultTo(params) {
	const defaultTo = resolveIMessageAccount(params).config.defaultTo;
	if (defaultTo == null) return;
	return defaultTo.trim() || void 0;
}
//#endregion
export { DEFAULT_ACCOUNT_ID, IMessageConfigSchema, PAIRING_APPROVED_MESSAGE, buildChannelConfigSchema, buildComputedAccountStatusSnapshot, chunkTextForOutbound, collectStatusIssuesFromLastError, formatTrimmedAllowFromEntries, getChatChannelMeta, imessageMessageActions, looksLikeIMessageTargetId, monitorIMessageProvider, normalizeIMessageMessagingTarget, probeIMessage, resolveChannelMediaMaxBytes, resolveIMessageConfigAllowFrom, resolveIMessageConfigDefaultTo, resolveIMessageGroupRequireMention, resolveIMessageGroupToolPolicy, sendMessageIMessage, setIMessageRuntime };
