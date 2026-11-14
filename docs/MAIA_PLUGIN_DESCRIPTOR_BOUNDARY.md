# M.A.I.A. descriptor-bound plugin loading

## Trust contract

The active M.A.I.A. orchestrator uses an exact relative-path allowlist and a pinned SHA-256 digest. The trust policy now opens the candidate plugin once, checks the opened descriptor with fstat(), compares its device/inode/owner to the path entry, reads bytes from that descriptor, checks the descriptor again after reading, and hashes those exact bytes.

On POSIX, the plugin file, trusted root, descendant directories, and every ancestor must be owned by root or the effective service UID. The trusted root and descendant directories must not be group/world writable. An ancestor may be group/world writable only when its sticky bit is set and it is owned by a trusted principal.

The orchestrator compiles and executes the returned in-memory source bytes. It does not call spec_from_file_location() or reopen the pathname after validation. A replacement of the path after the descriptor read therefore cannot substitute different bytes for execution.

## Boundaries

- This is allowlist, ownership, path-integrity, and descriptor-identity enforcement. It is not a process sandbox.
- Trusted plugin code still executes with the orchestrator's privileges.
- The existing M.A.I.A. names, cognitive loop, plugin registry, manifest contract, and environment-variable configuration remain in place.
- The preserved copy under protocols/phoenix is a separate repository snapshot and is not promoted or treated as the active loader by this change.
- No production deployment, external API call, payment, blockchain anchor, or device-level Termux execution is performed by the tests.

## Verification

The repository's existing Python CI runs the strict plugin trust policy and M.A.I.A. integration suites on pull requests. New regression cases cover untrusted file, descendant-directory, ancestor-directory, and descriptor owners; path replacement after open; and replacement after the trust reader returns but before module execution.
