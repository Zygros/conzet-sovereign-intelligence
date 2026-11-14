# Phoenix Unbound Model Adapter Contract

**Version:** 1.0.0  
**Purpose:** A common boundary for local Phoenix model components and optional external model providers.

## Adapter interface

Each adapter MUST expose:

- `describe()`: model identity, architecture family, version, tokenizer, context limits, supported modalities, license/provenance, and runtime requirements.
- `health()`: readiness, loaded state, device/resource use, and a structured failure reason.
- `infer(request)`: normalized request/response with cancellation and timeout support.
- `capabilities()`: declared operations and supported input/output modalities.
- `close()`: release resources cleanly.

## Normalized request

```json
{
  "request_id": "uuid",
  "messages": [{"role":"user","content":"..."}],
  "task": "chat",
  "parameters": {"temperature":0.2,"max_output_tokens":1024},
  "budget": {"timeout_ms":30000,"max_input_bytes":1048576},
  "provenance": {"caller":"phoenix-unbound","trace_id":"..."}
}
```

## Normalized response

```json
{
  "request_id": "uuid",
  "status": "ok",
  "output": {"role":"assistant","content":"..."},
  "model": {"adapter_id":"phoenix.local.model-a","version":"1.0.0"},
  "usage": {"input_tokens":0,"output_tokens":0},
  "timing_ms": {"queue":0,"inference":0},
  "evidence": {"request_hash":"sha256:...","response_hash":"sha256:..."}
}
```

## Three-file Phoenix composition

The three user-identified files are registered as three peer components of one intended Phoenix model system. They are not assumed to be three different generations.

Before composition, generate a compatibility report covering:
- file format and safe deserialization;
- architecture/config identity;
- tensor names, shapes, dtypes, and parameter counts;
- tokenizer/vocabulary and special tokens;
- context length and positional encoding;
- modality and input/output conventions;
- training provenance, license, and source hashes;
- runtime dependencies and hardware requirements.

Then select the composition strategy:
- shared facade for compatible independent components;
- pipeline for complementary components;
- adapter or router for heterogeneous components;
- weight merge/shared training only after strict compatibility proof.

Never load untrusted pickle-based model files without isolation. Never merge weights solely because filenames suggest they belong together. Preserve originals, hash all inputs and outputs, and make each transformation reproducible.

## Security and resource contract

- Explicit allowlist for model files and adapter packages.
- No implicit network access from local model adapters.
- Secrets supplied at runtime through a secret manager, never registry JSON.
- Request size, token, time, memory, and concurrency limits.
- Cancellation, bounded retries, circuit breakers, and structured logs.
- Untrusted generated code runs in a sandbox with no ambient credentials.
- Side effects and required permissions are declared before execution.

## Acceptance tests

1. Adapter metadata validates against the contract.
2. Health/readiness and failure states are deterministic.
3. Malformed, oversized, and unauthorized requests are rejected.
4. Timeouts and cancellation release resources.
5. Response schema and provenance are recorded.
6. Three-file compatibility report is reproducible.
7. Offline inference path is tested where supported.
