#!/usr/bin/env python3
"""Verify published Scout artifact hashes and OpenTimestamps proofs.

Hash matches establish byte identity of the published artifacts. A timestamp
is confirmed only when a calendar has attached a Bitcoin block attestation
and that attestation's merkle root matches the block header from a public
explorer. Pending calendar proofs are not treated as confirmed.

GitHub-hosted runners do not have a local Bitcoin Core node, and `ots verify`
exits non-zero for that reason even after calendars have upgraded a proof.
This checker upgrades the proof, then checks the block header itself.

The newest Scout run is often only minutes old, so its proof is still
pending. That pending state does not fail the job when the run is inside
the confirmation window and an older run outside the window does confirm.
The newer stamp is still reported as unconfirmed.
"""
import datetime
import hashlib
import io
import json
import pathlib
import subprocess
import sys
import tempfile
import urllib.request

REF = "origin/evidence/scout"
RUN_ID = None
# Calendars usually attach a Bitcoin attestation within a few hours.
# Eight hours covers the gap between a fresh scout publish and the next check.
BITCOIN_CONFIRMATION_GRACE_SECONDS = 8 * 60 * 60
HEADER_SOURCES = (
    (
        "mempool.space",
        "https://mempool.space/api/block-height/{height}",
        "https://mempool.space/api/block/{block_hash}/header",
    ),
    (
        "blockstream.info",
        "https://blockstream.info/api/block-height/{height}",
        "https://blockstream.info/api/block/{block_hash}/header",
    ),
)


def select_run_id():
    """Use an explicitly requested run, otherwise the newest numeric published run."""
    if len(sys.argv) > 1:
        return sys.argv[1]
    result = subprocess.run(
        ["git", "ls-tree", "--name-only", f"{REF}:runs"],
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"Cannot list published runs on {REF}: {result.stderr.strip()}")
    run_ids = [line.strip().rstrip("/") for line in result.stdout.splitlines()
               if line.strip().rstrip("/").isdigit()]
    if not run_ids:
        raise RuntimeError(f"No numeric run directories found on {REF}")
    return str(max((int(run_id) for run_id in run_ids)))


def list_run_ids():
    result = subprocess.run(
        ["git", "ls-tree", "--name-only", f"{REF}:runs"],
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"Cannot list published runs on {REF}: {result.stderr.strip()}")
    return sorted(
        (int(line.strip().rstrip("/")) for line in result.stdout.splitlines()
         if line.strip().rstrip("/").isdigit())
    )


def git_bytes(run_id, path):
    result = subprocess.run(
        ["git", "show", f"{REF}:runs/{run_id}/{path}"],
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(
            f"Cannot read {REF}:runs/{run_id}/{path}: {result.stderr.decode(errors='replace')}"
        )
    return result.stdout


def parse_published_at(run_id):
    try:
        text = git_bytes(run_id, "RUN_META.yaml").decode("utf-8", errors="replace")
    except RuntimeError:
        return None
    for line in text.splitlines():
        if line.startswith("published_at:"):
            raw = line.split(":", 1)[1].strip()
            try:
                return datetime.datetime.strptime(raw, "%Y-%m-%dT%H:%M:%SZ").replace(
                    tzinfo=datetime.timezone.utc
                )
            except ValueError:
                return None
    return None


def _fetch_text(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "conzet-published-evidence-verifier"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8").strip()


def fetch_block_header(height):
    """Return (source_name, header_bytes) for a mainnet block height."""
    errors = []
    for name, height_url, header_url in HEADER_SOURCES:
        try:
            block_hash = _fetch_text(height_url.format(height=height))
            header_hex = _fetch_text(header_url.format(block_hash=block_hash))
            return name, bytes.fromhex(header_hex)
        except Exception as exc:  # noqa: BLE001 - try the next public explorer
            errors.append(f"{name}: {exc}")
    raise RuntimeError("; ".join(errors))


def confirm_proof(proof_bytes, target_bytes, proof_name, target_name):
    """Upgrade one .ots proof and confirm any Bitcoin attestation.

    Returns a report dict. `state` is confirmed, pending, mismatch, or unavailable.
    Confirmation never follows from the mere presence of a .ots file.
    """
    base = {
        "file": proof_name,
        "target_file": target_name,
        "present": True,
        "confirmed": False,
        "state": "unavailable",
        "bitcoin_block": None,
        "header_source": None,
        "confirmation_method": None,
        "client_exit_code": None,
        "output_tail": [],
    }
    with tempfile.TemporaryDirectory() as directory:
        proof_path = pathlib.Path(directory) / proof_name
        target_path = pathlib.Path(directory) / target_name
        proof_path.write_bytes(proof_bytes)
        target_path.write_bytes(target_bytes)
        try:
            result = subprocess.run(
                ["ots", "upgrade", str(proof_path)],
                capture_output=True, text=True, timeout=90, check=False,
            )
        except FileNotFoundError:
            base["error"] = "ots client not installed"
            return base
        except subprocess.TimeoutExpired:
            base["error"] = "ots upgrade timed out"
            return base
        output = (result.stdout + "\n" + result.stderr).strip()
        base["client_exit_code"] = result.returncode
        base["output_tail"] = output.splitlines()[-8:]
        try:
            bound = _bitcoin_attestations(proof_path, target_bytes)
        except Exception as exc:  # noqa: BLE001 - report the proof as unreadable
            base["error"] = f"could not read upgraded timestamp: {exc}"
            return base
    if not bound["bound"]:
        base["state"] = "mismatch"
        base["error"] = "OpenTimestamps proof does not commit to the published file bytes"
        return base
    if not bound["attestations"]:
        base["state"] = "pending"
        base["error"] = "calendar has not attached a Bitcoin block attestation yet"
        return base

    import bitcoin
    from bitcoin.core import CBlockHeader
    from opentimestamps.core.notary import BitcoinBlockHeaderAttestation, VerificationError

    bitcoin.SelectParams("mainnet")
    fetch_errors = []
    mismatches = []
    for height, digest in bound["attestations"]:
        try:
            source, header_bytes = fetch_block_header(height)
            header = CBlockHeader.deserialize(header_bytes)
        except Exception as exc:  # noqa: BLE001 - another attestation may still verify
            fetch_errors.append(f"block {height}: {exc}")
            continue
        attestation = BitcoinBlockHeaderAttestation(height)
        try:
            attested_time = attestation.verify_against_blockheader(digest, header)
        except VerificationError as exc:
            mismatches.append(f"block {height}: {exc}")
            continue
        base.update({
            "confirmed": True,
            "state": "confirmed",
            "bitcoin_block": height,
            "header_source": source,
            "confirmation_method": "public-block-header",
            "attested_unix_time": int(attested_time),
            "error": None,
        })
        return base
    if mismatches:
        base["state"] = "mismatch"
        base["error"] = "Bitcoin attestation did not match the public block header: " + "; ".join(mismatches)
        return base
    base["state"] = "unavailable"
    base["error"] = (
        "Could not read a public Bitcoin block header, and no local Bitcoin node is configured. "
        + "; ".join(fetch_errors)
    )
    return base


def _bitcoin_attestations(proof_path, target_bytes):
    from opentimestamps.core.notary import BitcoinBlockHeaderAttestation
    from opentimestamps.core.serialize import StreamDeserializationContext
    from opentimestamps.core.timestamp import DetachedTimestampFile

    with proof_path.open("rb") as handle:
        detached = DetachedTimestampFile.deserialize(StreamDeserializationContext(handle))
    actual = detached.file_hash_op.hash_fd(io.BytesIO(target_bytes))
    if actual != detached.file_digest:
        return {"bound": False, "attestations": []}
    found = []
    for digest, attestation in detached.timestamp.all_attestations():
        if isinstance(attestation, BitcoinBlockHeaderAttestation):
            found.append((int(attestation.height), digest))
    found.sort()
    return {"bound": True, "attestations": found}


def verify_run(run_id):
    """Hash-check one published run and inspect its two timestamp proofs."""
    manifest = git_bytes(run_id, "manifest.sha256").decode("utf-8")
    entries = []
    payloads = {}
    for line in manifest.splitlines():
        if not line.strip():
            continue
        expected, filename = line.split(None, 1)
        filename = filename.strip().lstrip("*")
        payload = git_bytes(run_id, filename)
        payloads[filename] = payload
        actual = hashlib.sha256(payload).hexdigest()
        entries.append({
            "file": filename,
            "expected_sha256": expected,
            "actual_sha256": actual,
            "match": actual == expected,
            "bytes": len(payload),
        })
    proofs = []
    for proof_name, target_name in (
        ("manifest.sha256.ots", "manifest.sha256"),
        ("verification-receipts.json.ots", "verification-receipts.json"),
    ):
        try:
            proof = git_bytes(run_id, proof_name)
            if target_name in payloads:
                target = payloads[target_name]
            else:
                target = git_bytes(run_id, target_name)
        except RuntimeError as exc:
            proofs.append({
                "file": proof_name,
                "target_file": target_name,
                "present": False,
                "confirmed": False,
                "state": "pending",
                "bitcoin_block": None,
                "error": str(exc),
                "output_tail": [],
            })
            continue
        proofs.append(confirm_proof(proof, target, proof_name, target_name))
    published_at = parse_published_at(run_id)
    return {
        "run_id": str(run_id),
        "published_at": published_at,
        "artifact_hashes_match": all(item["match"] for item in entries) if entries else False,
        "artifacts": entries,
        "timestamp_proofs": proofs,
    }


def summarize(verified, now):
    proofs = verified["timestamp_proofs"]
    states = [proof.get("state") for proof in proofs]
    if any(state == "mismatch" for state in states):
        state = "mismatch"
    elif any(state == "unavailable" for state in states):
        state = "unavailable"
    elif not proofs or any(state != "confirmed" for state in states):
        state = "pending"
    else:
        state = "confirmed"
    blocks = [proof.get("bitcoin_block") for proof in proofs if proof.get("bitcoin_block")]
    published_at = verified["published_at"]
    age_seconds = None
    if published_at is not None:
        age_seconds = int((now - published_at).total_seconds())
    details = [proof.get("error") for proof in proofs if proof.get("error")]
    return {
        "run_id": verified["run_id"],
        "published_at": published_at.strftime("%Y-%m-%dT%H:%M:%SZ") if published_at else None,
        "age_seconds": age_seconds,
        "hashes_match": verified["artifact_hashes_match"],
        "state": state,
        "bitcoin_block": min(blocks) if blocks else None,
        "detail": "; ".join(details) if details else None,
    }


def decide_exit(newest, anchor, grace_seconds):
    """Choose the job result without treating a pending proof as confirmed.

    `newest` and `anchor` are summaries from `summarize`. `anchor` may be None.
    """
    if not newest["hashes_match"]:
        return 1, f"Newest published run {newest['run_id']} does not match its manifest hashes."
    state = newest["state"]
    if state == "confirmed":
        return 0, (
            f"Newest run {newest['run_id']} hashes match and Bitcoin block {newest.get('bitcoin_block')} "
            "attests the timestamp. The block header was read from a public explorer because this "
            "runner has no local Bitcoin node."
        )
    if state == "mismatch":
        return 2, (
            f"Newest run {newest['run_id']} has a timestamp proof that does not match the published "
            "file or the Bitcoin block header."
        )
    if state == "unavailable":
        detail = newest.get("detail") or "verification data was unavailable"
        return 2, f"Newest run {newest['run_id']} could not be timestamp-verified: {detail}."
    age = newest.get("age_seconds")
    if age is None or age > grace_seconds:
        return 2, (
            f"Newest run {newest['run_id']} is still waiting on Bitcoin confirmation and is outside "
            "the confirmation window, or its publish time is unknown."
        )
    if anchor is None:
        return 2, (
            f"Newest run {newest['run_id']} is still awaiting Bitcoin confirmation, and there is no "
            "older published run outside the confirmation window."
        )
    if not anchor["hashes_match"]:
        return 1, f"Older run {anchor['run_id']} does not match its manifest hashes."
    if anchor["state"] == "confirmed":
        return 0, (
            f"Newest run {newest['run_id']} hashes match, but its OpenTimestamps proof is still "
            f"pending Bitcoin confirmation (published {newest.get('published_at')}). That newest "
            f"stamp is not confirmed. Older run {anchor['run_id']} is confirmed by Bitcoin block "
            f"{anchor.get('bitcoin_block')}."
        )
    if anchor["state"] == "mismatch":
        return 2, (
            f"Older run {anchor['run_id']} has a timestamp proof that does not match the published "
            "file or the Bitcoin block header."
        )
    return 2, (
        f"Newest run {newest['run_id']} is still pending Bitcoin confirmation, and older run "
        f"{anchor['run_id']} is not confirmed either ({anchor['state']}: {anchor.get('detail')})."
    )


def _jsonable_run(verified, summary):
    published_at = verified["published_at"]
    return {
        "run_id": verified["run_id"],
        "published_at": published_at.strftime("%Y-%m-%dT%H:%M:%SZ") if published_at else None,
        "artifact_hashes_match": verified["artifact_hashes_match"],
        "artifacts": verified["artifacts"],
        "timestamp_proofs": verified["timestamp_proofs"],
        "timestamp_confirmation_complete": summary["state"] == "confirmed",
        "summary": summary,
    }


def main():
    global RUN_ID
    now = datetime.datetime.now(datetime.timezone.utc)
    explicit = len(sys.argv) > 1
    RUN_ID = select_run_id()
    print(f"Verifying published Scout run {RUN_ID} from {REF}")
    newest_verified = verify_run(RUN_ID)
    newest = summarize(newest_verified, now)
    anchor_verified = None
    anchor = None
    # An explicit run id stays strict: the caller asked about that run alone.
    if (
        not explicit
        and newest["hashes_match"]
        and newest["state"] == "pending"
        and newest["age_seconds"] is not None
    ):
        if newest["age_seconds"] <= BITCOIN_CONFIRMATION_GRACE_SECONDS:
            cutoff = now - datetime.timedelta(seconds=BITCOIN_CONFIRMATION_GRACE_SECONDS)
            candidates = []
            for run_id in list_run_ids():
                if str(run_id) == str(RUN_ID):
                    continue
                published_at = parse_published_at(run_id)
                if published_at is not None and published_at <= cutoff:
                    candidates.append((published_at, run_id))
            if candidates:
                _published_at, anchor_id = max(candidates)
                print(f"Newest proof is still pending; checking older run {anchor_id}")
                anchor_verified = verify_run(anchor_id)
                anchor = summarize(anchor_verified, now)
    code, reason = decide_exit(newest, anchor, BITCOIN_CONFIRMATION_GRACE_SECONDS)
    report = {
        "run_id": str(RUN_ID),
        "source_ref": REF,
        "artifact_hashes_match": newest_verified["artifact_hashes_match"],
        "artifacts": newest_verified["artifacts"],
        "timestamp_proofs": newest_verified["timestamp_proofs"],
        "timestamp_confirmation_complete": newest["state"] == "confirmed",
        "bitcoin_node": "not configured; block headers are read from public explorers",
        "confirmation_grace_seconds": BITCOIN_CONFIRMATION_GRACE_SECONDS,
        "anchor_run": _jsonable_run(anchor_verified, anchor) if anchor_verified else None,
        "result": "pass" if code == 0 else "fail",
        "exit_code": code,
        "reason": reason,
        "interpretation": (
            "Hash matches establish byte identity only. A timestamp is confirmed only when its "
            "Bitcoin block attestation matches a public block header. A pending newest proof is "
            "not counted as confirmed."
        ),
    }
    rendered = json.dumps(report, indent=2) + "\n"
    pathlib.Path("published-evidence-verification.json").write_text(rendered, encoding="utf-8")
    print(reason)
    print(rendered, end="")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
