import { As as SpeechVoiceOption, qn as SpeechProviderPlugin } from "../../types-C6Y8zGKi.js";
//#region extensions/microsoft/speech-provider.d.ts
declare function isCjkDominant(text: string): boolean;
declare function listMicrosoftVoices(): Promise<SpeechVoiceOption[]>;
declare function buildMicrosoftSpeechProvider(): SpeechProviderPlugin;
//#endregion
export { buildMicrosoftSpeechProvider, isCjkDominant, listMicrosoftVoices };