"""Regression tests for strict OpenTimestamps confirmation parsing."""
from types import SimpleNamespace

from scripts import ots_verify


def test_pending_message_containing_confirmed_is_not_accepted(tmp_path, monkeypatch):
    proof = tmp_path / "pending.ots"
    proof.write_bytes(b"fixture")
    monkeypatch.setattr(
        ots_verify.subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(
            stdout="Timestamp not yet confirmed on Bitcoin",
            stderr="",
            returncode=0,
        ),
    )
    result = ots_verify.verify(proof)
    assert result["ok"] is True
    assert result["confirmed"] is False
    assert result["bitcoin_block"] is None


def test_explicit_bitcoin_block_is_accepted(tmp_path, monkeypatch):
    proof = tmp_path / "confirmed.ots"
    proof.write_bytes(b"fixture")
    monkeypatch.setattr(
        ots_verify.subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(
            stdout="Success! Bitcoin block 912345",
            stderr="",
            returncode=0,
        ),
    )
    result = ots_verify.verify(proof)
    assert result["ok"] is True
    assert result["confirmed"] is True
    assert result["bitcoin_block"] == 912345
