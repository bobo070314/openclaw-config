//#region src/agents/code-mode-json.ts
function toCodeModeJsonSafe(value) {
	if (value === void 0) return null;
	try {
		const serialized = JSON.stringify(value);
		return serialized === void 0 ? null : JSON.parse(serialized);
	} catch {
		if (value instanceof Error) return {
			name: value.name,
			message: value.message
		};
		if (value === null) return null;
		switch (typeof value) {
			case "string":
			case "number":
			case "boolean": return value;
			case "bigint":
			case "symbol":
			case "function": return String(value);
			default: return Object.prototype.toString.call(value);
		}
	}
}
//#endregion
export { toCodeModeJsonSafe as t };
