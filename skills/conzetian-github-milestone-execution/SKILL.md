---
name: conzetian-github-milestone-execution
description: Execute GitHub operations end-to-end: inventory repositories, issues, pull requests, workflows, and evidence; inspect review feedback; make minimal additive fixes; validate with checks; merge only when gates pass; verify the merged state and post-merge workflows; and report outcomes with direct evidence links.
---

# Conzetian GitHub Milestone Execution

## Purpose

Turn a broad execution request into a bounded, evidence-backed cycle. Prefer completed changes over plans. Solve operational friction during the run, preserve original evidence, and report concrete outcomes.

## Governing invariants

- **Always Add, Never Take:** preserve source artifacts and provenance. Corrections are additive records or reviewed code changes, not silent rewrites of historical evidence.
- **Always Do, Never Don't:** move through the execution graph until the current cycle's milestones are complete or a genuine permission boundary prevents the action.
- **Solve Friction Before Continuing:** inspect errors, review comments, failed checks, missing references, and workflow conditions; fix actionable causes before moving on.
- **Actual is not Proposed:** distinguish discovered, changed, committed, merged, executed, measured, and verified states.
- **Evidence over assertion:** every claimed milestone needs a commit, PR, workflow result, artifact, or identified API observation.
- **Minimize blast radius:** use a dedicated branch, narrow patches, expected-head SHA when merging, and preserve user data.
- **Never promote a candidate to proof:** file presence, matching metadata, a recognizable receipt header, or a successful command without explicit confirmation is not proof of external anchoring.

## Execution procedure

### 1. Establish target and authority
Identify the authenticated owner, target repository set, default branches, accessible scopes, and requested outcome. Do not imply access to disconnected services. Use authenticated connectors for private data and public APIs for public metadata.

### 2. Inventory repositories
Page through repository results rather than assuming one page is complete. Record name, visibility, default branch, activity, size, issue support, and archive/disabled state when available. Separate public and private repositories.

### 3. Inspect branch safety
Read default-branch heads and protection/ruleset state where permitted. If a branch is unprotected, record the finding and, when authorized, make a narrowly scoped protection change rather than silently changing repository policy.

### 4. Inventory issues and pull requests
Fetch open issues and PRs, including head/base refs, SHAs, mergeability, update times, and labels. De-duplicate PRs from issue API responses. Prioritize security, evidence integrity, failing automation, and reviewed low-risk changes.

### 5. Inspect the execution surface
Read relevant workflow files, tests, scripts, evidence manifests, and repository conventions. Follow references to exact files and current branch SHAs. Never infer file content from a filename alone.

### 6. Collect review friction
Read inline review comments, review submissions, bot findings, issue discussion, CI check-runs, and workflow job steps. Convert actionable findings into testable corrections. Avoid repeating resolved findings.

### 7. Define a bounded milestone batch
Choose up to 13 independent milestones for the current cycle. Each milestone needs a concrete action and observable completion condition. Group related opportunities when safe; do not mix unrelated high-risk changes into one commit.

### 8. Implement on a dedicated branch
Create a uniquely named branch from the current target head. Make the smallest complete patch that fixes the cause. Keep evidence and user-data changes additive. Include regression coverage and documentation when useful.

### 9. Validate before merge
Run available focused tests and inspect the diff. Review required CI, security, lint/type, and policy checks. Do not merge when a required check fails or the proposed head SHA changes unexpectedly. If a check is pending, wait/poll or accurately leave it pending.

### 10. Merge with a head-SHA guard
Merge only a reviewed PR with the intended base and expected head SHA. Use the repository's accepted merge method. Do not merge merely to make a milestone count.

### 11. Verify the merged state
Read the PR state and merge commit, re-fetch changed files from the default branch, and confirm the correction landed. A feature-branch commit alone is not completion.

### 12. Verify post-merge execution
Find workflow runs associated with the merge commit. Inspect conclusions and individual job steps as needed. Re-run failed jobs only when authorized and meaningful. Resolve failures and verify reruns. Treat in-progress workflows as in progress, not as passes.

### 13. Close the loop and recurse
Update issue/PR status only when acceptance conditions are met. Preserve an evidence ledger containing milestone, action, commit/PR, check result, and verification link. Scan the next layer of issues, review comments, workflow failures, and follow-on opportunities, then begin another bounded cycle.

## Milestone evidence record

For each milestone, record:

- **ID:** stable sequence number for this execution cycle.
- **Action:** what was actually done.
- **Result:** completed, pending, blocked by permission, or failed.
- **Evidence:** commit SHA, PR URL, workflow URL, artifact path, or API observation.
- **Verification:** the exact check or default-branch observation supporting completion.
- **Next action:** only if the milestone is not complete.

## Reporting format

Lead with completed work. Give a numbered list of finished milestones with direct links. Keep pending work separate and state its live status. Do not pad the count with intentions, repeated observations, or unsupported claims. Never claim a connected Drive, local shell, external network, or runtime was accessed unless that access actually occurred.

## Safe completion criteria

A cycle is complete when chosen milestones have observable outcomes, reviewed changes are merged only after required gates pass, merged files and post-merge automation are checked, and any remaining permission boundary is described plainly. Then continue into the next batch when recursive execution is requested.
