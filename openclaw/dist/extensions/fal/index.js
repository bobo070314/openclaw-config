import { t as definePluginEntry } from "../../plugin-entry-BZpzqykQ.js";
import { t as buildFalImageGenerationProvider } from "../../image-generation-provider-BkKVMOGK.js";
import { t as buildFalMusicGenerationProvider } from "../../music-generation-provider-DhLP1VVa.js";
import { t as createFalProvider } from "../../provider-registration-Cs0C2vts.js";
import { t as buildFalVideoGenerationProvider } from "../../video-generation-provider-Da_p3ekP.js";
var fal_default = definePluginEntry({
	id: "fal",
	name: "fal Provider",
	description: "Bundled fal image, video, and music generation provider",
	register(api) {
		api.registerProvider(createFalProvider());
		api.registerImageGenerationProvider(buildFalImageGenerationProvider());
		api.registerMusicGenerationProvider(buildFalMusicGenerationProvider());
		api.registerVideoGenerationProvider(buildFalVideoGenerationProvider());
	}
});
//#endregion
export { fal_default as default };
