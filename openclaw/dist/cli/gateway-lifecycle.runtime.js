import { s as normalizeOptionalLowercaseString } from "../string-coerce-DW4mBlAt.js";
import { i as formatErrorMessage } from "../errors-DNvW4XW_.js";
import { t as isContainerEnvironment } from "../container-environment-CNsJSTpY.js";
import { i as getRuntimeConfig } from "../io-CwmOK6NP.js";
import "../config-CxwD7EO_.js";
import { a as consumeGatewaySigusr1RestartIntent, c as isGatewaySigusr1RestartExternallyAllowed, d as resetGatewayRestartStateForInProcessRestart, f as resolveGatewayRestartDeferralTimeoutMs, g as triggerOpenClawRestart, i as consumeGatewaySigusr1RestartAuthorization, l as markGatewaySigusr1RestartHandled, n as consumeGatewayRestartIntentPayloadSync, p as scheduleGatewaySigusr1Restart, r as consumeGatewayRestartIntentSync, u as peekGatewaySigusr1RestartReason } from "../restart-BHEJqkjr.js";
import { r as writeGatewayRestartHandoffSync } from "../restart-handoff-CsqPFHER.js";
import { _ as rotateAgentEventLifecycleGeneration } from "../agent-events-7y1r8HOP.js";
import { C as reloadTaskRegistryFromStore, K as retireActiveCronTaskRunTracking, W as abortActiveCronTaskRuns, Y as waitForActiveCronTaskRuns } from "../task-registry-z-EZ6Ymu.js";
import "../runtime-internal-BU7f0iz1.js";
import { d as listActiveEmbeddedRunSessionKeys, l as getActiveEmbeddedRunCount, u as listActiveEmbeddedRunSessionIds } from "../run-state-B31lb2Ak.js";
import { p as writeDiagnosticStabilityBundleForFailureSync } from "../diagnostic-stability-bundle-_pGUa2hn.js";
import { n as abortEmbeddedAgentRun, x as waitForActiveEmbeddedRuns } from "../runs-pVtbFfgt.js";
import { t as markRestartAbortedMainSessions } from "../main-session-restart-recovery-C2pmznnh.js";
import { n as detectRespawnSupervisor } from "../supervisor-markers-BnpKGoUs.js";
import { a as markUpdateRestartSentinelFailure } from "../restart-sentinel-DZIvtr_-.js";
import { c as resetCronActiveJobs, l as waitForActiveCronJobs, t as advanceCronActiveJobGeneration } from "../active-jobs-DCucn-SJ.js";
import { _ as waitForActiveTasks, a as getActiveTaskCount, m as resetAllLanes, p as markGatewayDraining } from "../command-queue-Cn3ZuyZZ.js";
import { n as getInspectableActiveTaskRestartBlockers } from "../task-registry.maintenance-B-EpwDZm.js";
import { spawn } from "node:child_process";
//#region src/infra/process-respawn.ts
function isTruthy(value) {
	const normalized = normalizeOptionalLowercaseString(value);
	return normalized === "1" || normalized === "true" || normalized === "yes" || normalized === "on";
}
const PNPM_VERSIONED_OPENCLAW_ENTRY_PATTERN = /^(.*?)([\\/])node_modules\2\.pnpm\2openclaw@[^\\/]+\2node_modules\2openclaw\2.+$/;
function rewritePnpmVersionedOpenClawEntryPath(entryPath) {
	return entryPath.replace(PNPM_VERSIONED_OPENCLAW_ENTRY_PATTERN, "$1$2node_modules$2openclaw$2openclaw.mjs");
}
function spawnDetachedGatewayProcess(opts = {}) {
	const [entryArg, ...entryArgs] = process.argv.slice(1);
	const args = [
		...process.execArgv,
		...entryArg ? [rewritePnpmVersionedOpenClawEntryPath(entryArg)] : [],
		...entryArgs
	];
	const child = spawn(process.execPath, args, {
		env: opts.env ? {
			...process.env,
			...opts.env
		} : process.env,
		detached: true,
		stdio: "inherit"
	});
	child.unref();
	return {
		child,
		pid: child.pid ?? void 0
	};
}
/**
* Attempt to restart this process with a fresh PID.
* - supervised environments (launchd/systemd/schtasks): caller should exit and let supervisor restart
* - OPENCLAW_NO_RESPAWN=1: caller should keep in-process restart behavior (tests/dev)
* - unmanaged environments: caller should keep in-process restart behavior so
*   custom supervisors keep tracking the same gateway PID
*/
function restartGatewayProcessWithFreshPid(_opts = {}) {
	if (isTruthy(process.env.OPENCLAW_NO_RESPAWN)) return { mode: "disabled" };
	const supervisor = detectRespawnSupervisor(process.env);
	if (supervisor) {
		if (supervisor === "schtasks") {
			const restart = triggerOpenClawRestart();
			if (!restart.ok) return {
				mode: "failed",
				detail: restart.detail ?? `${restart.method} restart failed`
			};
		}
		return { mode: "supervised" };
	}
	if (process.platform === "win32") return {
		mode: "disabled",
		detail: "win32: detached respawn unsupported without Scheduled Task markers"
	};
	if (isContainerEnvironment()) return {
		mode: "disabled",
		detail: "container: use in-process restart to keep PID 1 alive"
	};
	return {
		mode: "disabled",
		detail: "unmanaged: use in-process restart to keep custom supervisor PID tracking stable"
	};
}
/**
* Update restarts must replace the OS process so the new code runs from a
* fresh module graph after package files have changed on disk.
*
* Unlike the generic restart path, update mode allows detached respawn on
* unmanaged Windows installs because there is no safe in-process fallback once
* the installed package contents have been replaced.
*/
function respawnGatewayProcessForUpdate(opts = {}) {
	if (isTruthy(process.env.OPENCLAW_NO_RESPAWN)) return {
		mode: "disabled",
		detail: "OPENCLAW_NO_RESPAWN"
	};
	const supervisor = detectRespawnSupervisor(process.env, process.platform, { includeLinuxOpenClawGatewayServiceMarker: true });
	if (supervisor) {
		if (supervisor === "schtasks") {
			const restart = triggerOpenClawRestart();
			if (!restart.ok) return {
				mode: "failed",
				detail: restart.detail ?? `${restart.method} restart failed`
			};
		}
		return { mode: "supervised" };
	}
	try {
		const { child, pid } = spawnDetachedGatewayProcess(opts);
		return {
			mode: "spawned",
			pid,
			child
		};
	} catch (err) {
		return {
			mode: "failed",
			detail: formatErrorMessage(err)
		};
	}
}
//#endregion
export { abortActiveCronTaskRuns, abortEmbeddedAgentRun, advanceCronActiveJobGeneration, consumeGatewayRestartIntentPayloadSync, consumeGatewayRestartIntentSync, consumeGatewaySigusr1RestartAuthorization, consumeGatewaySigusr1RestartIntent, detectRespawnSupervisor, getActiveEmbeddedRunCount, getActiveTaskCount, getInspectableActiveTaskRestartBlockers, getRuntimeConfig, isGatewaySigusr1RestartExternallyAllowed, listActiveEmbeddedRunSessionIds, listActiveEmbeddedRunSessionKeys, markGatewayDraining, markGatewaySigusr1RestartHandled, markRestartAbortedMainSessions, markUpdateRestartSentinelFailure, peekGatewaySigusr1RestartReason, reloadTaskRegistryFromStore, resetAllLanes, resetCronActiveJobs, resetGatewayRestartStateForInProcessRestart, resolveGatewayRestartDeferralTimeoutMs, respawnGatewayProcessForUpdate, restartGatewayProcessWithFreshPid, retireActiveCronTaskRunTracking, rotateAgentEventLifecycleGeneration, scheduleGatewaySigusr1Restart, waitForActiveCronJobs, waitForActiveCronTaskRuns, waitForActiveEmbeddedRuns, waitForActiveTasks, writeDiagnosticStabilityBundleForFailureSync, writeGatewayRestartHandoffSync };
