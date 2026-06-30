import { n as ChannelSetupWizard } from "../../setup-wizard-types-CAT_klok.js";
import { H as ChannelSetupAdapter } from "../../types.adapters-DvwGUDck.js";
import { a as resolveDefaultIrcAccountId, i as listIrcAccountIds, n as ResolvedIrcAccount, o as resolveIrcAccount, r as listEnabledIrcAccounts, t as ircPlugin } from "../../channel-DWMVVc8Y.js";
import { t as setIrcRuntime } from "../../runtime-DXCUe9gt.js";
//#region extensions/irc/src/setup-core.d.ts
declare const ircSetupAdapter: ChannelSetupAdapter;
//#endregion
//#region extensions/irc/src/setup-surface.d.ts
declare const ircSetupWizard: ChannelSetupWizard;
//#endregion
export { type ResolvedIrcAccount, ircPlugin, ircSetupAdapter, ircSetupWizard, listEnabledIrcAccounts, listIrcAccountIds, resolveDefaultIrcAccountId, resolveIrcAccount, setIrcRuntime };