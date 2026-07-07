import { r as createLegacyPrivateNetworkDoctorContract } from "./ssrf-policy-B35YwKq4.js";
import "./ssrf-runtime-CV6TBXbQ.js";
//#region extensions/mattermost/src/doctor-contract.ts
const contract = createLegacyPrivateNetworkDoctorContract({ channelKey: "mattermost" });
const legacyConfigRules = contract.legacyConfigRules;
const normalizeCompatibilityConfig = contract.normalizeCompatibilityConfig;
//#endregion
export { normalizeCompatibilityConfig as n, legacyConfigRules as t };
