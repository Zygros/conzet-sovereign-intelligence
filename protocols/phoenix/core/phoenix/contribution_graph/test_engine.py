from engine import build_seed_graph


def test_graph_structure():
    graph = build_seed_graph()
    assert len(graph.nodes) == 40
    assert len(graph.edges) == 30
    assert graph.validate() == []


def test_reverse_provenance():
    graph = build_seed_graph()
    assert "C-136" in graph.reverse_neighbors("C-127")
    assert "C-166" in graph.reverse_neighbors("C-150")


def test_recursive_activation():
    graph = build_seed_graph()
    activated = set(graph.activate("C-166", max_hops=3))
    assert "C-127" in activated
    assert "C-150" in activated
    assert "C-153" in activated


def test_proof():
    from engine import prove
    result = prove()
    assert result["passed"] is True
    assert result["validation_errors"] == []
