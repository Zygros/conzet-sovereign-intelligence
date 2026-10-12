# Additive Technical Errata Draft — Infinite Mathematics / OmniNet / φ^∞-Algebra
**Date:** 2026-10-12  
**Status:** Proposed corrections for author review. Not a replacement for, or silent edit to, any published record.  
**Rule:** Preserve the original publication and issue a new version or linked erratum after confirming intended definitions.

## E-01 — OmniNet v4: CΩ equation and table
The published expression is transcribed as:
`CΩ(t) = (φ^(2^t) + 1) / 2`.

Direct evaluation using φ=(1+√5)/2 gives approximately:
- t=2: 3.92705
- t=3: 23.98936
- t=4: 1104.00023

These values do not match the values in the paper's table. The table must not be silently overwritten. Author decision required:
1. confirm whether the equation is canonical or whether a different recurrence was intended;
2. publish the chosen recurrence with unambiguous parentheses;
3. regenerate the table programmatically;
4. attach a versioned correction and tests.

## E-02 — φ^∞-Algebra: convergence-threshold inequality
The theorem statement reportedly says `φ > e`, while the proof uses the standard real power-tower convergence threshold `e^(1/e)`. Since φ≈1.618034 and e≈2.718282, φ>e is false; φ>e^(1/e)≈1.444668 is true.

Proposed statement correction, subject to confirming the paper's exact definitions:
“For the standard sequence of finite-height real power towers with base φ, where φ=(1+√5)/2, the base exceeds the convergence threshold e^(1/e); consequently, the sequence does not converge to a finite real limit.”

This statement concerns that specific tower convention only. It does not imply a general result about transfinite arithmetic, agent capacity, or physical computation.

## E-03 — φ^∞-Algebra: composition notation
Where `f(x)=φ^(φ^x)`, literal substitution gives:
`f(f(x)) = φ^(φ^(φ^(φ^x)))`.
Use explicit parentheses or a recursive definition to remove ambiguity and test the first few heights numerically.

## E-04 — Claims requiring separate evidence
The above corrections do not settle broader claims about infinite computational capacity, compression ratios, operational-agent counts, κ-coherence, or network resilience. Those need separate formal definitions, proof or experimental protocols, raw artifacts, and independent reproduction.

## Publication workflow
1. Confirm exact source lines and intended semantics against the preserved PDF.
2. Decide the canonical equation/theorem with a documented rationale.
3. Add a changelog and version increment; retain the old record.
4. Run regression tests against the new version.
5. Publish the correction linked to the original DOI and clearly identify the scope of the change.
