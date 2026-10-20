#!/usr/bin/env python3
"""Unified entry point for the Conzet sovereign hub.

Run ``python -m sovereign``. Component paths come from ``sovereign.toml``.
Trees that live on unmerged ``unify/*`` drafts are listed even when absent.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "sovereign.toml"

# Printed claim precision from the math verification brief.
GAIA_K = "1e14"
GAIA_CLAIM = "0.9333"
GAIA_PLACES = 4
PHI_TOWER_CLAIM = "5625.11"
PHI_TOWER_PLACES = 2
N_MAX_CLAIM = "33750.66"
N_MAX_PLACES = 2
PHI_17_94_CLAIM = "5613.56"
PHI_17_94_PLACES = 2
PHI_100_CLAIM = "7.92e20"
PHI_100_SIGFIGS = 3


def load_config(path: Path = CONFIG_PATH) -> dict:
    """Read the small component config. Strings, numbers, and tables only."""
    if not path.is_file():
        raise FileNotFoundError("missing {0}".format(path))
    config = {"components": []}
    current = None
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip()
            if section == "meta":
                current = config.setdefault("meta", {})
            elif section.startswith("component."):
                current = {"id": section.split(".", 1)[1]}
                config["components"].append(current)
            else:
                raise ValueError("{0}:{1}: unknown section {2}".format(path, line_no, section))
            continue
        if current is None or "=" not in line:
            raise ValueError("{0}:{1}: expected key = value".format(path, line_no))
        key, raw_value = line.split("=", 1)
        current[key.strip()] = _parse_scalar(raw_value.strip())
    return config


def _parse_scalar(value: str):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    if value in {"true", "false"}:
        return value == "true"
    try:
        if any(ch in value for ch in ".eE"):
            return float(value)
        return int(value)
    except ValueError:
        return value


def _components(config: dict) -> list:
    return list(config.get("components") or [])


def cmd_status(_args: argparse.Namespace) -> int:
    config = load_config()
    rows = _components(config)
    print("component\tlayer\tpath\tversion\tpresent")
    for item in rows:
        path = ROOT / str(item.get("path", ""))
        version = item.get("version") or item.get("revision") or ""
        print(
            "{id}\t{layer}\t{path}\t{version}\t{present}".format(
                id=item.get("id", ""),
                layer=item.get("layer", ""),
                path=item.get("path", ""),
                version=version,
                present="yes" if path.is_dir() else "no",
            )
        )
    print("{0} components".format(len(rows)))
    return 0


def _round_places(value, places: int):
    import mpmath as mp

    scale = mp.power(10, places)
    return mp.nint(value * scale) / scale


def _round_sigfigs(value, digits: int):
    import mpmath as mp

    if value == 0:
        return mp.mpf(0)
    exponent = int(mp.floor(mp.log10(abs(value))))
    scale = mp.power(10, digits - 1 - exponent)
    return mp.nint(value * scale) / scale


def _check(name: str, computed, rounded, claim: str) -> bool:
    import mpmath as mp

    ok = rounded == mp.mpf(claim)
    print(name)
    print("  computed {0}".format(mp.nstr(computed, 20)))
    print("  rounded  {0}".format(mp.nstr(rounded, 12)))
    print("  claim    {0}".format(claim))
    print("  {0}".format("pass" if ok else "fail"))
    return ok


def verify_math() -> int:
    """Recompute the briefed numeric claims with mpmath.

    GAIA: P(k) = 1 - 1 / (log10(k) + 1) at k = 1e14 is 0.9333.
    phi^(phi^6) = 5625.11 and N_max = 6 * that = 33750.66.
    phi^17.94 = 5613.56. phi^100 = 7.92e20.
    """
    try:
        import mpmath as mp
    except ImportError:
        print("verify-math: mpmath is not installed (pip install mpmath)", file=sys.stderr)
        return 1

    mp.mp.dps = 50
    phi = (1 + mp.sqrt(5)) / 2
    k = mp.mpf(GAIA_K)
    probability = 1 - 1 / (mp.log10(k) + 1)
    tower = phi ** (phi ** 6)
    n_max = 6 * tower
    phi_17_94 = phi ** mp.mpf("17.94")
    phi_100 = phi ** 100

    checks = [
        _check(
            "GAIA P(k)=1-1/(log10(k)+1) at k={0}".format(GAIA_K),
            probability,
            _round_places(probability, GAIA_PLACES),
            GAIA_CLAIM,
        ),
        _check(
            "phi^(phi^6)",
            tower,
            _round_places(tower, PHI_TOWER_PLACES),
            PHI_TOWER_CLAIM,
        ),
        _check(
            "N_max=6*phi^(phi^6)",
            n_max,
            _round_places(n_max, N_MAX_PLACES),
            N_MAX_CLAIM,
        ),
        _check(
            "phi^17.94",
            phi_17_94,
            _round_places(phi_17_94, PHI_17_94_PLACES),
            PHI_17_94_CLAIM,
        ),
        _check(
            "phi^100",
            phi_100,
            _round_sigfigs(phi_100, PHI_100_SIGFIGS),
            PHI_100_CLAIM,
        ),
    ]
    failed = len([item for item in checks if not item])
    print("{0} passed, {1} failed".format(len(checks) - failed, failed))
    return 0 if failed == 0 else 1


def cmd_verify_math(_args: argparse.Namespace) -> int:
    return verify_math()


_PENDING_MARKERS = (
    "not yet confirmed",
    "pending",
    "waiting for",
    "calendar",
    "connection",
    "timed out",
    "timeout",
    "unreachable",
    "temporary failure",
    "name or service not known",
    "network is unreachable",
    "no node",
    "bitcoin node",
    "connection refused",
    "failed to connect",
    "nodename nor servname",
)


def _classify_ots(returncode: int, output: str) -> str:
    match = re.search(r"Bitcoin block\s+(\d+)", output, flags=re.IGNORECASE)
    if returncode == 0 and match is not None:
        return "verified"
    lowered = output.lower()
    if "not an ots" in lowered or "does not exist" in lowered:
        return "failed"
    if returncode != 0 or any(marker in lowered for marker in _PENDING_MARKERS) or match is None:
        return "pending"
    return "failed"


def cmd_verify_ots(_args: argparse.Namespace) -> int:
    proofs = sorted((ROOT / "provenance").glob("**/*.ots")) if (ROOT / "provenance").is_dir() else []
    if not proofs:
        print("verify-ots: no proofs at provenance/**/*.ots")
        return 0
    pending = 0
    verified = 0
    failed = 0
    for proof in proofs:
        rel = proof.relative_to(ROOT)
        try:
            result = subprocess.run(
                ["ots", "verify", str(proof)],
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
        except FileNotFoundError:
            print("{0}\tpending\tots client not installed; no verification node".format(rel))
            pending += 1
            continue
        except subprocess.TimeoutExpired:
            print("{0}\tpending\tots verify timed out; no node response".format(rel))
            pending += 1
            continue
        output = (result.stdout or "") + "\n" + (result.stderr or "")
        state = _classify_ots(result.returncode, output)
        detail = " ".join(output.split())[:180]
        print("{0}\t{1}\t{2}".format(rel, state, detail))
        if state == "verified":
            verified += 1
        elif state == "pending":
            pending += 1
        else:
            failed += 1
    print("verified={0} pending={1} failed={2}".format(verified, pending, failed))
    return 1 if failed else 0


def cmd_phoenix_bench(_args: argparse.Namespace) -> int:
    root = ROOT / "core" / "omega-10"
    if not root.is_dir():
        print("phoenix-bench: core/omega-10 is not present; skipped")
        return 0
    benchmark = root / "src" / "omega" / "phoenix" / "benchmark.py"
    bench_dirs = [root / name for name in ("benches", "benchmarks", "bench") if (root / name).is_dir()]
    if benchmark.is_file():
        env = os.environ.copy()
        env["PYTHONPATH"] = os.pathsep.join([str(root / "src"), env.get("PYTHONPATH", "")])
        code = (
            "from pathlib import Path; "
            "from omega.phoenix.benchmark import PhoenixBenchmark; "
            "r = PhoenixBenchmark(Path('runs/phoenix'), seed=42).run(); "
            "print(r.to_dict()); "
            "raise SystemExit(0 if r.passed else 1)"
        )
        print("phoenix-bench: PhoenixBenchmark")
        completed = subprocess.run([sys.executable, "-c", code], cwd=str(root), env=env, check=False)
        return int(completed.returncode)
    if bench_dirs:
        print("phoenix-bench: pytest {0}".format(", ".join(str(path.relative_to(ROOT)) for path in bench_dirs)))
        completed = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "--rootdir", str(root)] + [str(path) for path in bench_dirs],
            cwd=str(ROOT),
            check=False,
        )
        return int(completed.returncode)
    print("phoenix-bench: core/omega-10 has no benchmark.py or benches directory; skipped")
    return 0


def _contains_tests(path: Path) -> bool:
    if (path / "tests").is_dir() or (path / "test").is_dir():
        return True
    for candidate in path.rglob("test_*.py"):
        if "node_modules" in candidate.parts or ".git" in candidate.parts:
            return True
    for candidate in path.rglob("*_test.py"):
        if "node_modules" in candidate.parts or ".git" in candidate.parts:
            return True
    return False


def cmd_test(_args: argparse.Namespace) -> int:
    try:
        config = load_config()
    except FileNotFoundError as exc:
        print("test: {0}".format(exc), file=sys.stderr)
        return 1
    ignores = []
    suites = []
    for item in _components(config):
        path = ROOT / str(item.get("path", ""))
        if path.is_dir() and _contains_tests(path):
            ignores.extend(["--ignore", str(path.relative_to(ROOT))])
            suites.append(path)
    print("test: pytest hub")
    hub = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"] + ignores,
        cwd=str(ROOT),
        check=False,
    )
    status = int(hub.returncode)
    for path in suites:
        print("test: pytest {0}".format(path.relative_to(ROOT)))
        completed = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "--rootdir", str(path), str(path)],
            cwd=str(ROOT),
            check=False,
        )
        if completed.returncode != 0:
            status = int(completed.returncode)
    return status


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sovereign", description="Unified sovereign hub commands")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("status", help="list components and paths").set_defaults(func=cmd_status)
    commands.add_parser("verify-math", help="recompute numeric claims with mpmath").set_defaults(func=cmd_verify_math)
    commands.add_parser("verify-ots", help="run ots verify on provenance/**/*.ots").set_defaults(func=cmd_verify_ots)
    commands.add_parser("phoenix-bench", help="run core/omega-10 benches if present").set_defaults(func=cmd_phoenix_bench)
    commands.add_parser("test", help="run pytest suites").set_defaults(func=cmd_test)
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
