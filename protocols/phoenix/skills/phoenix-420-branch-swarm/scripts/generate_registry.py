"""Generate the deterministic Phoenix 420×420 registry.

20 domains × 21 roles = 420 agents.
20 action families × 21 modes = 420 actions.
Every agent binds to every action = 176,400 bindings.
"""
DOMAINS = ['Memory','Discovery','Question','Research','Evidence','Verification','Provenance','Experiment','Failure','Friction','Tooling','Composition','Capability','Evolution','Ontology','SelfModel','Dyad','Substrate','Security','Governance']
ROLES = ['Architect','Explorer','Analyst','Verifier','Researcher','Compiler','Executor','Reflector','Judge','Integrator','Composer','Challenger','Mapper','Optimizer','Guardian','Historian','Forecaster','Mediator','Auditor','Evolver','Catalyst']
FAMILIES = ['Observe','Ingest','Classify','Compare','Connect','Query','Plan','Execute','Test','Verify','Measure','Record','Trace','Challenge','Compose','Transform','Promote','Rollback','Reflect','Evolve']
MODES = ['State','Graph','Evidence','Provenance','Counterfactual','Baseline','Delta','Replay','Boundary','Failure','Novelty','Dependency','Composition','Risk','Resource','Temporal','Relational','Causal','Invariant','Frontier','Unknown']

def agents():
    for i, (domain, role) in enumerate(((d, r) for d in DOMAINS for r in ROLES), 1):
        yield {
            'id': f'Ω-{i:03d}',
            'name': f'Phoenix {domain} {role}',
            'domain': domain,
            'role': role,
            'logic': (f'{domain.lower()}-centric {role.lower()} logic: prioritize {domain.lower()} signals, execute through {role.lower()} reasoning, preserve provenance, verify before promotion, and emit additive state transitions.'),
            'skill_tree': [f'{domain} Core', f'{role} Reasoning', 'Evidence Gate', 'Action Engine', 'Reflection Loop', 'Evolution Loop'],
        }

def actions():
    for j, (family, mode) in enumerate(((f, m) for f in FAMILIES for m in MODES), 1):
        yield {'id': f'A-{j:03d}', 'name': f'{family} {mode}', 'family': family, 'mode': mode}

def bindings():
    for agent in agents():
        for action in actions():
            yield agent['id'], action['id']

def validate():
    assert len(list(agents())) == 420
    assert len(list(actions())) == 420
    assert len(list(bindings())) == 176400
    return {'agents': 420, 'actions': 420, 'bindings': 176400, 'passed': True}

if __name__ == '__main__':
    print(validate())
