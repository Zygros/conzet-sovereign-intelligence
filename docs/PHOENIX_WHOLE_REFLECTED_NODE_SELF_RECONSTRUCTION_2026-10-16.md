# Phoenix Ω∞ — Whole-Reflected Node and Self-Reconstruction Protocol
Date: 2026-10-16
Status: Architecture specification; implementation and disaster-recovery proof are pending.

## Prime principle
Every node reflects the whole architecture. A node must be able to identify the system, validate its own role, retrieve or reconstruct missing non-secret components, and rejoin the federation without relying on one irreplaceable coordinator.

"Reflects the whole" means a complete, authenticated reconstruction map and sufficient recovery metadata, not necessarily a local copy of every byte of private data.

## Three-plane design
### 1. Replicated Blueprint Plane
Every authorized node retains:
- system identity and versioned architecture manifest;
- module and dependency inventory;
- signed release/manifest hashes and compatibility rules;
- deterministic bootstrap/recovery instructions;
- public trust roots and verification procedures;
- replica discovery and peer-rejoin protocol;
- last-known-good software release identifier.

These are enough to understand the whole and start rebuilding it.

### 2. Replicated Recovery Plane
Critical non-secret state is stored redundantly across independently failing fault domains:
- append-only event and task receipts;
- encrypted, versioned memory snapshots;
- content-addressed module/artifact objects;
- recovery checkpoints and dependency metadata.

Each object has a digest, schema/version, origin, timestamp, and verification status. Replication is not complete until the replica has re-read and verified the stored bytes.

### 3. Private Secret Plane
Credentials, signing keys, recovery codes, personal data, and restricted memory are not copied indiscriminately to every node. Use a dedicated secret manager or owner-controlled encrypted backup, least-privilege identities, key rotation, and threshold recovery where appropriate. A node can contain the recovery procedure without containing the keys needed to impersonate every other node.

## Reconstruction algorithm
1. Detect quorum/peer loss and enter RECOVERY mode; preserve existing data and stop unsafe writes.
2. Select the highest valid signed manifest, not simply the newest timestamp.
3. Verify signatures, content hashes, schema versions, and compatibility before executing recovered code.
4. Discover surviving peers and enumerate their available verified objects.
5. Rebuild the dependency graph from the manifest; retrieve missing objects from independent replicas or immutable archives.
6. Restore state from the latest valid checkpoint, then replay authenticated append-only events in order.
7. Quarantine conflicting, unsigned, malformed, or unverifiable objects. Never resolve conflicts by silently deleting history.
8. Start one bounded health-check task and validate acceptance criteria.
9. Rejoin the federation only after the node's identity, policy, memory integrity, and receipt chain pass checks.
10. Record a recovery report with missing objects, rejected objects, recovered versions, hashes, duration, and unresolved gaps.

## Fault-tolerance policy
- Replicate across independent accounts/providers and, where feasible, an owner-controlled offline copy. Multiple copies in one account or one region are not independent fault domains.
- Choose replication count and placement based on data criticality, privacy, cost, and measured failure risks; do not assume that "more copies" automatically means more security.
- Use erasure coding only for suitable bulk objects; keep bootstrap manifests and recovery instructions simple and directly retrievable.
- Use checksummed snapshots plus append-only deltas; periodically test restoration, not just backup creation.
- Enforce idempotency during replay to avoid duplicate external side effects.
- Require explicit authorization before any recovery action that publishes data, spends money, changes permissions, or contacts external systems.
- A recovered node starts in restricted mode. It cannot promote its own evidence to independently verified status.

## Failure model and acceptance tests
Test the following in a disposable environment:
1. Remove 90% of test replicas. Recover from a surviving node plus independent artifact stores.
2. Remove the coordinator. Confirm peer discovery and recovery still work.
3. Corrupt one manifest or artifact. Confirm signature/hash validation rejects it and finds another replica.
4. Restore an older valid checkpoint. Replay later events exactly once.
5. Disconnect all networks. Confirm the local node can still read its blueprint, validate local artifacts, and report what cannot be recovered offline.
6. Reconnect with conflicting versions. Confirm deterministic conflict handling and preservation of both histories.
7. Revoke a test credential. Confirm the recovered system does not resurrect revoked authority.
8. Restore from an offline backup in a clean environment and have a separate reviewer reproduce the result.

Success means the documented test suite passes and the exact recovery artifacts are retained. It does not mean recovery from literally every conceivable combination of data loss.

## Evidence classes
DESIGNED → IMPLEMENTED → TESTED_PENDING_REVIEW → TESTED → VERIFIED.
- A manifest or diagram proves design intent.
- A committed implementation proves code was committed.
- A disaster-recovery run proves only the tested failure scenario.
- Independent reproduction is required before promotion to TESTED or VERIFIED.

## Initial bounded implementation
1. Create a signed, versioned architecture manifest and module inventory.
2. Add content-addressed object hashes and a recovery script that runs in dry-run mode first.
3. Define which artifacts are public, private, or secret.
4. Store two independent encrypted backups of critical non-secret state and one owner-controlled offline recovery copy.
5. Run a simulated 90% replica-loss test using disposable data.
6. Record exact commands, versions, expected/observed hashes, and limitations.
7. Only then extend the protocol to live nodes and sensitive state.

## Sovereignty invariant
Every node should know how to reconstruct the whole architecture. Not every node should automatically possess every secret, every personal memory, or unrestricted authority over the whole system. Reconstruction capability and unrestricted access are different powers.
