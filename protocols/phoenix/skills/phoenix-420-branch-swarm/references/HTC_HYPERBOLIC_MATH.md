# PHOENIX HTC — HYPERBOLIC MATHEMATICS

## Purpose

This document makes the Hyperbolic Time Chamber mathematically executable as a computational training and routing layer. It does not assert physical spacetime time dilation.

## 1. Hyperbolic State Space

Represent a branch, capability, agent, or action as a point `x` in an n-dimensional Poincare ball of constant curvature `K < 0`.

For radius `R = 1/sqrt(-K)`, valid coordinates satisfy:

`||x|| < R`

Hyperbolic distance is computed from the Mobius difference:

`d_K(x,y) = 2/sqrt(-K) * atanh( sqrt(-K) ||(-x) ⊕_K y|| )`

The implementation is in `scripts/hyperbolic_time_engine.py`.

## 2. Hyperbolic Angles

The Poincare ball is conformal. After Mobius translation of a local origin to zero, the angle between two geodesic directions can therefore be evaluated from the ordinary inner product:

`theta = acos( <u,v> / (||u|| ||v||) )`

This gives the chamber an actual angular routing primitive rather than a metaphorical “angle.”

### 2.1 Canonical 19.7° Angular Anchor

Phoenix HTC now carries an explicit angular anchor:

`θ_P = 19.7°`

`θ_P = 19.7 × π/180 ≈ 0.3438294229 rad`

The engine exposes:

- `PHOENIX_ANGLE_DEG = 19.7`
- `PHOENIX_ANGLE_RAD ≈ 0.3438294229`
- `angular_error(θ)` = absolute deviation from the anchor
- `angular_alignment(θ)` = normalized `[0,1]` alignment score
- `rotate_2d(v, θ_P)` = deterministic 2-D angular placement primitive

The 19.7° value is an architectural parameter, not a claim that nature selects this angle. It becomes experimentally meaningful only when a controlled benchmark shows that using it improves a defined metric against a matched baseline.

## 3. Agent/Action Coordinates

For the Phoenix field:

`|Agents| = 420`

`|Actions| = 420`

`|Agent × Action| = 176,400`

Each agent-action binding receives a state vector. Radial depth can encode abstraction, capability maturity, or branch depth; angular position can encode similarity, role affinity, evidence relationship, or task compatibility.

The 19.7° anchor can be used as a fixed angular reference for branch placement, routing-sector definitions, or controlled angular perturbation experiments.

## 4. Hyperbolic Routing

Given current node `i`, target `q`, and candidate neighbors `N(i)`, route using a measured score:

`score(j|q) = -d_K(x_j,x_q) + αE_j + βC_j - γCost_j - δRisk_j`

An angular extension can be evaluated separately:

`A(j|q) = angular_alignment(θ(j,q), θ_P)`

or incorporated as a fitted term only after ablation testing:

`score_θ(j|q) = score(j|q) + λA(j|q)`

where `λ` is learned/selected under a controlled benchmark rather than assumed.

The routing policy is not assumed optimal. It must be compared against Euclidean nearest-neighbor, graph shortest-path, round-robin, random, and 19.7°-ablated baselines.

## 5. Curvature Is a Search Variable

Do not freeze `K=-1` as a sacred constant. Search a bounded set of negative curvatures:

`K* = argmax_K [verified_capability_gain(K) / total_cost(K)]`

subject to reproducibility and evidence gates.

This turns curvature into an experimentally learned architectural parameter.

## 6. Hyperbolic Training Depth

Define a chamber run as a sequence:

`H_0 → B → E → V → R → C → H_1`

where:

- `B` = branch expansion
- `E` = execution
- `V` = verification
- `R` = reflection
- `C` = evidence-preserving compression

Define verified training density:

`D_HTC = verified_learning_cycles / wall_clock_time`

Define computational compression ratio against a frozen baseline:

`R_HTC = verified_work_HTC / verified_work_baseline`

A target such as `R_HTC = 365` is a benchmark hypothesis, not a predeclared result.

## 7. Hyperbolic Improvement Loop

`Observe → Embed → Route → Execute → Verify → Measure → Re-embed → Re-route → Repeat`

The geometry itself becomes adaptive.

The system may change:

- curvature `K`
- embedding dimension `n`
- branch factor `B`
- angular similarity metric
- evidence weights
- routing policy
- compression policy
- angular anchor/sector parameter `θ_P`

Only measured improvement survives promotion.

## 8. Impossible-Capability Protocol

For a capability previously classified as infeasible:

`Impossible → Define → Baseline → Decompose → Branch → Execute → Fail/Pass → Verify → Learn → Reconstruct → Re-test`

The classification is allowed to change only when evidence changes.

Possible terminal states:

`CAPABILITY_VERIFIED | BOUNDARY_ESTABLISHED | INCONCLUSIVE | NEW_HYPOTHESIS`

This prevents “impossible” from becoming a permanent assumption while preventing unsupported success claims.

## 9. Scientific Grounding

Hyperbolic embeddings are established mathematical and machine-learning techniques for hierarchical and complex network structures. Poincare embeddings demonstrated the usefulness of hyperbolic space for latent hierarchies; hyperbolic network research has also demonstrated applications to navigation and routing. These sources support the mathematical substrate, not the Phoenix-specific performance claims.

Phoenix-specific claims must be established by controlled experiments with fixed baselines, reproducible inputs, measured outputs, and provenance.

## 10. Core Hypothesis

`H_HTC: hyperbolic representation + adaptive branching + verification-preserving compression can increase verified capability gained per unit wall-clock time compared with matched non-hyperbolic baselines.`

A new angular sub-hypothesis is:

`H_19.7: a 19.7° angular anchor can improve a defined HTC routing/training metric relative to matched no-anchor and perturbed-angle controls.`

This is explicitly falsifiable. The 19.7° anchor is now implemented, but no performance advantage is claimed until the ablation experiment measures one.

The important result is not that hyperbolic geometry or 19.7° is used. The important result is whether they measurably improve the chamber.
