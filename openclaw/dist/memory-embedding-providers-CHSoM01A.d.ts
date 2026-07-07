import { i as OpenClawConfig } from "./types.openclaw-BhmF31_h.js";
import { d as SecretInput } from "./types.secrets-C15Z_eLX.js";

//#region src/memory-host-sdk/host/embedding-inputs.d.ts
/** Plain text segment accepted by embedding providers. */
type EmbeddingInputTextPart = {
  type: "text";
  text: string;
};
/** Base64 inline payload segment for multimodal embedding providers. */
type EmbeddingInputInlineDataPart = {
  type: "inline-data";
  mimeType: string;
  data: string;
};
/** Provider-neutral embedding input part. */
type EmbeddingInputPart = EmbeddingInputTextPart | EmbeddingInputInlineDataPart;
/** Embedding input preserving legacy text plus optional structured parts. */
type EmbeddingInput = {
  text: string;
  parts?: EmbeddingInputPart[];
};
//#endregion
//#region src/plugins/memory-embedding-providers.d.ts
/** Chunk submitted to memory embedding batch processing. */
type MemoryEmbeddingBatchChunk = {
  text: string;
  embeddingInput?: EmbeddingInput;
};
/** Options for batch memory embedding work. */
type MemoryEmbeddingBatchOptions = {
  agentId: string;
  chunks: MemoryEmbeddingBatchChunk[];
  wait: boolean;
  concurrency: number;
  pollIntervalMs: number;
  timeoutMs: number;
  debug: (message: string, data?: Record<string, unknown>) => void;
};
/** Per-call options for memory embedding providers. */
type MemoryEmbeddingProviderCallOptions = {
  signal?: AbortSignal;
};
/** Runtime metadata returned with memory embedding providers. */
type MemoryEmbeddingProviderRuntime = {
  id: string;
  cacheKeyData?: Record<string, unknown>; /** Prior persisted model/cache identities that are equivalent to the current identity. */
  indexIdentityAliases?: Array<{
    model: string;
    cacheKeyData: Record<string, unknown>;
  }>;
  inlineQueryTimeoutMs?: number;
  inlineBatchTimeoutMs?: number;
  sourceWideBatchEmbed?: boolean;
  batchEmbed?: (options: MemoryEmbeddingBatchOptions) => Promise<number[][] | null>;
};
/** Provider-owned canonical identity and exact aliases for persisted indexes. */
type MemoryEmbeddingProviderIndexIdentity = {
  model: string;
  cacheKeyData: Record<string, unknown>;
  aliases?: Array<{
    model: string;
    cacheKeyData: Record<string, unknown>;
  }>;
};
/** Created memory embedding provider instance. */
type MemoryEmbeddingProvider = {
  id: string;
  model: string;
  maxInputTokens?: number;
  embedQuery: (text: string, options?: MemoryEmbeddingProviderCallOptions) => Promise<number[]>;
  embedBatch: (texts: string[], options?: MemoryEmbeddingProviderCallOptions) => Promise<number[][]>;
  embedBatchInputs?: (inputs: EmbeddingInput[], options?: MemoryEmbeddingProviderCallOptions) => Promise<number[][]>;
  close?: () => Promise<void> | void;
};
/** Options passed to memory embedding provider adapters. */
type MemoryEmbeddingProviderCreateOptions = {
  config: OpenClawConfig;
  agentDir?: string;
  provider?: string;
  fallback?: string;
  remote?: {
    baseUrl?: string;
    apiKey?: SecretInput;
    headers?: Record<string, string>;
  };
  model: string;
  inputType?: string;
  queryInputType?: string;
  documentInputType?: string;
  local?: {
    modelPath?: string;
    modelCacheDir?: string;
    contextSize?: number | "auto";
  };
  outputDimensionality?: number;
  taskType?: "RETRIEVAL_QUERY" | "RETRIEVAL_DOCUMENT" | "SEMANTIC_SIMILARITY" | "CLASSIFICATION" | "CLUSTERING" | "QUESTION_ANSWERING" | "FACT_VERIFICATION";
};
/** Result returned by a memory embedding provider adapter. */
type MemoryEmbeddingProviderCreateResult = {
  provider: MemoryEmbeddingProvider | null;
  runtime?: MemoryEmbeddingProviderRuntime;
};
/** Adapter contract for registered memory embedding providers. */
type MemoryEmbeddingProviderAdapter = {
  id: string;
  defaultModel?: string;
  transport?: "local" | "remote";
  authProviderId?: string;
  autoSelectPriority?: number;
  allowExplicitWhenConfiguredAuto?: boolean;
  supportsMultimodalEmbeddings?: (params: {
    model: string;
  }) => boolean;
  resolveIndexIdentity?: (options: MemoryEmbeddingProviderCreateOptions) => MemoryEmbeddingProviderIndexIdentity;
  create: (options: MemoryEmbeddingProviderCreateOptions) => Promise<MemoryEmbeddingProviderCreateResult>;
  formatSetupError?: (err: unknown) => string;
  shouldContinueAutoSelection?: (err: unknown) => boolean;
};
/** Registered memory embedding provider with optional owning plugin metadata. */
type RegisteredMemoryEmbeddingProvider = {
  adapter: MemoryEmbeddingProviderAdapter;
  ownerPluginId?: string;
};
/** Registers a memory embedding provider adapter for the current process. */
declare function registerMemoryEmbeddingProvider(adapter: MemoryEmbeddingProviderAdapter, options?: {
  ownerPluginId?: string;
}): void;
/** Lists registered memory embedding provider entries. */
declare function listRegisteredMemoryEmbeddingProviders(): RegisteredMemoryEmbeddingProvider[];
/** Clears registered memory embedding providers. */
declare function clearMemoryEmbeddingProviders(): void;
//#endregion
export { MemoryEmbeddingProviderCallOptions as a, MemoryEmbeddingProviderIndexIdentity as c, listRegisteredMemoryEmbeddingProviders as d, registerMemoryEmbeddingProvider as f, MemoryEmbeddingProviderAdapter as i, MemoryEmbeddingProviderRuntime as l, MemoryEmbeddingBatchOptions as n, MemoryEmbeddingProviderCreateOptions as o, MemoryEmbeddingProvider as r, MemoryEmbeddingProviderCreateResult as s, MemoryEmbeddingBatchChunk as t, clearMemoryEmbeddingProviders as u };