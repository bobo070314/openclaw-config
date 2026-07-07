import { S as findModelInCatalog } from "./model-selection-shared-DXdzMPOG.js";
import { c as resolveDefaultModelForAgent } from "./model-selection-60FiczuZ.js";
import { i as modelSupportsVision, n as loadModelCatalog } from "./model-catalog-C5hjklw2.js";
import "./agent-runtime-Dq0mxT36.js";
//#region extensions/telegram/src/sticker-vision.runtime.ts
async function resolveStickerVisionSupportRuntime(params) {
	const catalog = await loadModelCatalog({ config: params.cfg });
	const defaultModel = resolveDefaultModelForAgent({
		cfg: params.cfg,
		agentId: params.agentId
	});
	const entry = findModelInCatalog(catalog, defaultModel.provider, defaultModel.model);
	if (!entry) return false;
	return modelSupportsVision(entry);
}
//#endregion
export { resolveStickerVisionSupportRuntime };
