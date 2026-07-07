import { i as OpenClawConfig } from "./types.openclaw-CXiJ86ZN.js";
import { r as ChannelConfigUiHint } from "./types.config-D1pSqbn8.js";
import { t as ChannelPlugin } from "./types.plugin-BLJArf-_.js";
import { $n as PluginRuntime } from "./types-B70zVumi.js";
import { r as buildChannelConfigSchema } from "./config-schema-CIXTfG6L.js";
import { r as parseOptionalDelimitedEntries } from "./helpers-C8Mvx18n.js";
import { L as PluginCommandContext, g as OpenClawPluginApi } from "./plugin-entry-CiFOtnwc.js";
import { t as clearAccountEntryFields } from "./config-helpers-C7OLMTDA.js";
import { c as tryReadSecretFileSync } from "./secret-file-CjbjgOXf.js";
import { a as buildThreadAwareOutboundSessionRoute, c as defineChannelPluginEntry, f as recoverCurrentThreadSessionId, i as buildChannelOutboundSessionRoute, l as defineSetupPluginEntry, m as stripTargetKindPrefix, o as createChannelPluginBase$1, p as stripChannelTargetPrefix, s as createChatChannelPlugin, t as ChannelOutboundSessionRouteParams } from "./core-C3b8PKLj.js";

//#region src/plugin-sdk/channel-core.d.ts
/** Creates a channel plugin base while keeping the public import on this SDK subpath. */
declare const createChannelPluginBase: typeof createChannelPluginBase$1;
//#endregion
export { type ChannelConfigUiHint, type ChannelOutboundSessionRouteParams, type ChannelPlugin, type OpenClawConfig, type OpenClawPluginApi, type PluginCommandContext, type PluginRuntime, buildChannelConfigSchema, buildChannelOutboundSessionRoute, buildThreadAwareOutboundSessionRoute, clearAccountEntryFields, createChannelPluginBase, createChatChannelPlugin, defineChannelPluginEntry, defineSetupPluginEntry, parseOptionalDelimitedEntries, recoverCurrentThreadSessionId, stripChannelTargetPrefix, stripTargetKindPrefix, tryReadSecretFileSync };