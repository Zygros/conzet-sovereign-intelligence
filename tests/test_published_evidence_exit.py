"""Exit policy for published evidence verification.

These cases do not contact calendars or Bitcoin. They lock the rule that a
pending proof is not reported as confirmed, while a fresh pending run can
still pass when an older run has a real confirmation.
"""
from scripts.verify_published_evidence import (
    BITCOIN_CONFIRMATION_GRACE_SECONDS,
    decide_exit,
)


def _summary(run_id, state, hashes_match=True, age_seconds=60, bitcoin_block=None, detail=None):
    return {
        "run_id": run_id,
        "published_at": "2026-10-17T15:41:04Z",
        "age_seconds": age_seconds,
        "hashes_match": hashes_match,
        "state": state,
        "bitcoin_block": bitcoin_block,
        "detail": detail,
    }


def test_hash_mismatch_fails_even_when_timestamp_is_confirmed():
    code, reason = decide_exit(
        _summary("1", "confirmed", hashes_match=False, bitcoin_block=1),
        None,
        BITCOIN_CONFIRMATION_GRACE_SECONDS,
    )
    assert code == 1
    assert "manifest hashes" in reason


def test_confirmed_newest_run_passes():
    code, reason = decide_exit(
        _summary("9", "confirmed", bitcoin_block=971845),
        None,
        BITCOIN_CONFIRMATION_GRACE_SECONDS,
    )
    assert code == 0
    assert "971845" in reason
    assert "not confirmed" not in reason


def test_young_pending_run_passes_only_when_older_run_is_confirmed():
    code, reason = decide_exit(
        _summary("10", "pending", age_seconds=120),
        _summary("4", "confirmed", age_seconds=90000, bitcoin_block=971800),
        BITCOIN_CONFIRMATION_GRACE_SECONDS,
    )
    assert code == 0
    assert "not confirmed" in reason
    assert "971800" in reason


def test_young_pending_run_fails_when_older_run_is_not_confirmed():
    code, _reason = decide_exit(
        _summary("10", "pending", age_seconds=120),
        _summary("4", "pending", age_seconds=90000),
        BITCOIN_CONFIRMATION_GRACE_SECONDS,
    )
    assert code == 2


def test_old_pending_run_fails_without_using_the_grace_exception():
    code, _reason = decide_exit(
        _summary("10", "pending", age_seconds=BITCOIN_CONFIRMATION_GRACE_SECONDS + 1),
        _summary("4", "confirmed", bitcoin_block=1),
        BITCOIN_CONFIRMATION_GRACE_SECONDS,
    )
    assert code == 2


def test_merkleroot_mismatch_fails_even_when_the_run_is_young():
    code, reason = decide_exit(
        _summary("10", "mismatch", age_seconds=30),
        _summary("4", "confirmed", bitcoin_block=1),
        BITCOIN_CONFIRMATION_GRACE_SECONDS,
    )
    assert code == 2
    assert "does not match" in reason


def test_missing_public_header_fails_closed():
    code, reason = decide_exit(
        _summary("10", "unavailable", age_seconds=30, detail="explorers unreachable"),
        None,
        BITCOIN_CONFIRMATION_GRACE_SECONDS,
    )
    assert code == 2
    assert "explorers unreachable" in reason
