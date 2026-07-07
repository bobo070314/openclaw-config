import { r as ChannelSetupWizardAdapter } from "./setup-wizard-types-CAT_klok.js";
import { H as ChannelSetupAdapter } from "./types.adapters-DvwGUDck.js";
//#region extensions/matrix/src/setup-core.d.ts
type MatrixSetupWizardModule = {
  matrixSetupWizard: ChannelSetupWizardAdapter;
};
declare function createMatrixSetupWizardProxy(loadWizardModule: () => Promise<MatrixSetupWizardModule>): ChannelSetupWizardAdapter;
declare const matrixSetupAdapter: ChannelSetupAdapter;
//#endregion
//#region extensions/matrix/src/onboarding.d.ts
declare const matrixOnboardingAdapter: ChannelSetupWizardAdapter;
//#endregion
export { createMatrixSetupWizardProxy as n, matrixSetupAdapter as r, matrixOnboardingAdapter as t };