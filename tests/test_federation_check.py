"""Visibility-aware regression tests for federation health inventory."""
from scripts import federation_check


def test_public_health_roster_excludes_known_private_nodes():
    public = federation_check.PUBLIC_REPOS
    private = federation_check.PRIVATE_REPOS

    assert len(public) == 21
    assert len(set(public)) == 21
    assert set(private) == {
        "Sovereign-Narrative-Intelligence-SNI-",
        "ZYGROS-PRIME",
        "sovereign-agsi-portal",
        "CONZETIAN-UNIFIED-INTELLIGANCE",
        "CONZETIAN-AI",
    }
    assert set(public).isdisjoint(private)


def test_visibility_inventory_accounts_for_all_26_current_nodes():
    nodes = federation_check.PUBLIC_REPOS + federation_check.PRIVATE_REPOS
    assert len(nodes) == 26
    assert len(set(nodes)) == 26
    assert federation_check.REPOS is federation_check.PUBLIC_REPOS


def test_health_report_does_not_count_private_404s_as_public_failures(
    monkeypatch, capsys,
):
    private = set(federation_check.PRIVATE_REPOS)

    def fake_check(repo):
        if repo in private:
            return "NOT_FOUND_OR_PRIVATE", 404
        return "LIVE", 200

    monkeypatch.setattr(federation_check, "check", fake_check)
    federation_check.main()
    output = capsys.readouterr().out

    assert "21/21 public repository URLs responded successfully." in output
    assert "ZYGROS-PRIME" not in output
    assert "CONZETIAN-UNIFIED-INTELLIGANCE" not in output
