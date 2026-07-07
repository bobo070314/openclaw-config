import { i as resolveAgentModelPrimaryValue } from "./model-input-CIqVjBTV.js";
import { r as logConfigUpdated } from "./logging-BVA6CZPz.js";
import { t as applyDefaultModelPrimaryUpdate, u as updateConfig } from "./shared-BSu_bkyn.js";
//#region src/commands/models/set-image.ts
/** Command for setting the default image model. */
/** Sets agents.defaults.imageModel.primary after resolving aliases/catalog provider aliases. */
async function modelsSetImageCommand(modelRaw, runtime) {
	const updated = await updateConfig((cfg) => {
		return applyDefaultModelPrimaryUpdate({
			cfg,
			modelRaw,
			field: "imageModel"
		});
	});
	logConfigUpdated(runtime);
	runtime.log(`Image model: ${resolveAgentModelPrimaryValue(updated.agents?.defaults?.imageModel) ?? modelRaw}`);
}
//#endregion
export { modelsSetImageCommand };
