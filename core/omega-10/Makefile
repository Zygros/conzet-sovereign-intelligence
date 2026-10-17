.PHONY: bootstrap lint test phoenix redteam htc demo

PYTHON ?= python3
export PYTHONPATH := src:$(PYTHONPATH)

bootstrap:
	$(PYTHON) -m pip install -e ".[dev]"

lint:
	ruff check src tests || true

test:
	$(PYTHON) -m pytest tests -v --tb=short

phoenix:
	$(PYTHON) -c "from pathlib import Path; from omega.phoenix.benchmark import PhoenixBenchmark; r=PhoenixBenchmark(Path('runs/phoenix'), seed=42).run(); print(r.to_dict()); raise SystemExit(0 if r.passed else 1)"

redteam:
	$(PYTHON) -c "from pathlib import Path; from omega.redteam.fixtures import run_all_fixtures; rs=run_all_fixtures(Path('runs/redteam')); print([(x.id,x.test_result) for x in rs]); raise SystemExit(0 if sum(1 for x in rs if x.test_result=='PASS')>=18 else 1)"

htc:
	$(PYTHON) -c "from pathlib import Path; from omega.htc.chamber import HTCBounded; r=HTCBounded(Path('/tmp/htc'), seed=42, max_cycles=50).run(); print(r.to_dict()); raise SystemExit(0 if r.passed else 1)"

demo:
	$(PYTHON) -c "from pathlib import Path; from omega.demonstrator.demo import run_demo; r=run_demo(Path('/tmp/demo')); print('overall_local_ok', r.get('overall_local_ok')); raise SystemExit(0 if r.get('overall_local_ok') else 1)"
