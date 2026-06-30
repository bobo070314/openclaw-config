import { y as resolveStateDir } from "./paths-DyelItkH.js";
import { t as loadGlobalRuntimeDotEnvFiles } from "./dotenv-global-DqRDlIDe.js";
import { n as loadWorkspaceDotEnvFile } from "./dotenv-BX2pMYDW.js";
import path from "node:path";
//#region src/cli/dotenv.ts
/** Load `.env` files for normal CLI commands without overriding existing process env. */
function loadCliDotEnv(opts) {
	const quiet = opts?.quiet ?? true;
	loadWorkspaceDotEnvFile(path.join(process.cwd(), ".env"), { quiet });
	if (opts?.loadGlobalEnv === false) return;
	loadGlobalRuntimeDotEnvFiles({
		quiet,
		stateEnvPath: path.join(resolveStateDir(process.env), ".env")
	});
}
//#endregion
export { loadCliDotEnv };
