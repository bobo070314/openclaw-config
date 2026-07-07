import { i as OpenClawConfig } from "../../types.openclaw-BhmF31_h.js";
import { v as ChannelMessageActionAdapter } from "../../types.core-CrBFyVDB.js";
import { g as chunkText } from "../../outbound.types-BbYrqFJk.js";
import { t as ChannelPlugin } from "../../types.plugin-CTcdBrrg.js";
import { $n as PluginRuntime } from "../../types-C6Y8zGKi.js";
import { n as normalizeAccountId, t as DEFAULT_ACCOUNT_ID } from "../../account-id-Dh6XMgGH.js";
import { l as normalizeE164 } from "../../utils-CR2kVvQb.js";
import { r as emptyPluginConfigSchema } from "../../config-schema-uTQb_Bsf.js";
import { g as OpenClawPluginApi } from "../../plugin-entry-BHVCZwwo.js";
import { r as buildChannelConfigSchema } from "../../config-schema-jXAeMqcd.js";
import { s as migrateBaseNameToDefaultAccount, t as applyAccountNameToChannelSection } from "../../setup-helpers-Dja7_qv5.js";
import { n as deleteAccountFromConfigSection, r as setAccountEnabledInConfigSection } from "../../config-helpers-D44btbUM.js";
import { n as formatPairingApproveHint } from "../../helpers-D9b5-14o.js";
import { d as getChatChannelMeta } from "../../core-ClgaYPGw.js";
import { t as formatCliCommand } from "../../command-format-CUz7-yqH.js";
import { D as resolveChannelMediaMaxBytes } from "../../media-runtime-D3D13UcJ.js";
import { t as detectBinary } from "../../detect-binary-Drm6r9o4.js";
import { t as formatDocsLink } from "../../links-DFOTZJs1.js";
import { n as resolveAllowlistProviderRuntimeGroupPolicy, r as resolveDefaultGroupPolicy } from "../../runtime-group-policy-DdHaj_YI.js";
import { t as PAIRING_APPROVED_MESSAGE } from "../../pairing-message-CFjlYpMw.js";
import { c as collectStatusIssuesFromLastError, d as createDefaultChannelRuntimeState, n as buildBaseChannelStatusSummary, t as buildBaseAccountStatusSnapshot } from "../../status-helpers-Bkne4fzS.js";
import { o as SignalConfigSchema } from "../../bundled-channel-config-schema-Xdx3eboZ.js";
import { a as resolveSignalAccount, c as probeSignal, i as resolveDefaultSignalAccountId, n as listEnabledSignalAccounts, o as SignalAccountConfig, r as listSignalAccountIds, t as ResolvedSignalAccount } from "../../accounts-zvMJjd23.js";
import { a as sendMessageSignal, f as monitorSignalProvider, p as signalMessageActions, u as resolveSignalReactionLevel } from "../../send-wtpPY3UX.js";
import { c as installSignalCli, n as normalizeSignalMessagingTarget, t as looksLikeSignalTargetId } from "../../normalize-BtYM5FLJ.js";
import { i as sendReactionSignal, r as removeReactionSignal } from "../../send-reactions-uXebi4Un.js";

//#region extensions/signal/src/runtime.d.ts
declare const setSignalRuntime: (next: PluginRuntime) => void, getSignalRuntime: () => PluginRuntime, getOptionalSignalRuntime: () => PluginRuntime | null, clearSignalRuntime: () => void;
//#endregion
export { type ChannelMessageActionAdapter, type ChannelPlugin, DEFAULT_ACCOUNT_ID, type OpenClawConfig, type OpenClawPluginApi, PAIRING_APPROVED_MESSAGE, type PluginRuntime, type ResolvedSignalAccount, type SignalAccountConfig, SignalConfigSchema, applyAccountNameToChannelSection, buildBaseAccountStatusSnapshot, buildBaseChannelStatusSummary, buildChannelConfigSchema, chunkText, collectStatusIssuesFromLastError, createDefaultChannelRuntimeState, deleteAccountFromConfigSection, detectBinary, emptyPluginConfigSchema, formatCliCommand, formatDocsLink, formatPairingApproveHint, getChatChannelMeta, installSignalCli, listEnabledSignalAccounts, listSignalAccountIds, looksLikeSignalTargetId, migrateBaseNameToDefaultAccount, monitorSignalProvider, normalizeAccountId, normalizeE164, normalizeSignalMessagingTarget, probeSignal, removeReactionSignal, resolveAllowlistProviderRuntimeGroupPolicy, resolveChannelMediaMaxBytes, resolveDefaultGroupPolicy, resolveDefaultSignalAccountId, resolveSignalAccount, resolveSignalReactionLevel, sendMessageSignal, sendReactionSignal, setAccountEnabledInConfigSection, setSignalRuntime, signalMessageActions };