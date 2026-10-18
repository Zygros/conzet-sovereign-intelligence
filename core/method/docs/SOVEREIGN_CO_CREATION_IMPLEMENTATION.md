# Sovereign Co-Creation Implementation

The proclamation is implemented as a **declarative provisioning model plus evidence-gated subsystem plans**.

## Provisioning model
Every declared PHOENIX Ω logical agent receives a profile schema with five requested capability classes:
1. co-creator
2. personal HTC
3. independent sub-swarm
4. compute allocation
5. private chat

## Evidence gate
A profile or plan is not treated as proof that a real agent, computer, network, chatbot endpoint, or HTC has been provisioned.

Actual provisioning requires:
- an instantiated runtime identity;
- an executable resource;
- an observed result;
- provenance for the result;
- verification against a test oracle.

## Scale strategy
The repository uses templates and identifiers rather than attempting to create 74,088,000 physical processes. This keeps the architecture scalable and testable.

## HTC
HTC is represented as a bounded cycle plan. “Infinite” recursion is a policy target, not an unbounded process.

## Sub-swarms
Sub-swarms are modeled as owned resource plans with explicit member limits.

## Compute
Compute is represented as a requested capacity allocation and a separately observed capacity measurement.

## Private chat
Chat nodes are represented by explicit endpoints and execution records.

## Permaweb
The protocol defines an anchoring state, but no external permanent anchor is claimed unless a real anchoring transaction is observed.

## Core loop

`DECLARE → PLAN → PROVISION → EXECUTE → OBSERVE → VERIFY → CHECKPOINT → REFLECT → UPGRADE`
