import { n as zalouserSetupAdapter } from "./setup-core-DM7ynsGr.js";
import { t as createZalouserPluginBase } from "./shared-BhZG-gQl.js";
import { t as zalouserSetupWizard } from "./setup-surface-DT1I32fb.js";
//#region extensions/zalouser/src/channel.setup.ts
const zalouserSetupPlugin = { ...createZalouserPluginBase({
	setupWizard: zalouserSetupWizard,
	setup: zalouserSetupAdapter
}) };
//#endregion
export { zalouserSetupPlugin as t };
