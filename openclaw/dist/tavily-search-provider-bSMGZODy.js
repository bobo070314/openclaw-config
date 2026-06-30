import { g as readPositiveIntegerParam } from "./common-DjVgHKFa.js";
import "./param-readers-BB3Hz7nC.js";
import { i as buildTavilyWebSearchProviderBase, n as TAVILY_GENERIC_SEARCH_DESCRIPTION, r as TAVILY_GENERIC_SEARCH_SCHEMA } from "./web-search-shared-Nc_uzO6c.js";
//#region extensions/tavily/src/tavily-search-provider.ts
let tavilyClientModulePromise;
function loadTavilyClientModule() {
	tavilyClientModulePromise ??= import("./tavily-client-CEQGWgiM.js");
	return tavilyClientModulePromise;
}
function createTavilyWebSearchProvider() {
	return {
		...buildTavilyWebSearchProviderBase(),
		createTool: (ctx) => ({
			description: TAVILY_GENERIC_SEARCH_DESCRIPTION,
			parameters: TAVILY_GENERIC_SEARCH_SCHEMA,
			execute: async (args) => {
				const { runTavilySearch } = await loadTavilyClientModule();
				return await runTavilySearch({
					cfg: ctx.config,
					query: typeof args.query === "string" ? args.query : "",
					maxResults: readPositiveIntegerParam(args, "count", {
						message: "count must be an integer from 1 to 20",
						max: 20
					})
				});
			}
		})
	};
}
//#endregion
export { createTavilyWebSearchProvider as t };
