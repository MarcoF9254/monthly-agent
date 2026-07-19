# System-Level Adversarial Architecture & Governance Review

Date: 2026-07-19
Reviewer: Claude (claude-fable-5), acting as independent senior systems architect and governance reviewer
Scope: entire repository state at branch point from `main` (post PR #33)
Status: advisory review artifact only. This document confers no authority, changes no policy, and activates nothing.

Reviewer correlation disclosure: this review is produced by an Anthropic model. A majority of the historical independent-review perspectives in this repository (Claude, Fable) were also Anthropic models. Under the repository's own correlated-failure standards, this review should be treated as one perspective, not a substitute for Owner judgment or for a genuinely independent second perspective.

Evidence limits: this review is based on repository contents, git history, and the live PR #32 record. Off-repository orchestration conversations (ChatGPT, Hermes, DeepSeek sessions), full PR comment threads for all 33 PRs, and actual labor cost per PR were not inspected. Statements about process cost are inferred from the artifact trail and are labeled as such.

---

## 1. Executive assessment

**Classification: governance-heavy with material architectural debt — where the debt is concentrated almost entirely in the control plane, not the product code.**

Blunt summary:

- The product code is small, clean, deterministic, well-tested, and essentially frozen. The extraction/validation pipeline has not materially advanced since PR #10 (D2B) and BR-005.
- The governance system has become the de facto primary workload. Of the last 11 merged PRs (#23–#33): 3 are governance policy publications, 5 are post-merge reconciliation PRs that exist only to update the governance system's own records of the other PRs, 2 are packaging/interface work on a fictional-only verifier, and 1 (#32) is a test-only pilot validator explicitly outside the runtime registry. Zero advanced the monthly-newsletter product.
- The governance policy is ~590 lines of prose plus an ~60-field per-PR classification record, and **none of it is machine-enforced**. CI runs pytest, a lock check, and a wheel build. Every control the policy treats as safety-critical — exact-head binding, path allowlists, true-merge proof, landed-scope proof — is enforced by LLM interpretation and Owner diligence, which is precisely the enforcement mechanism the policy itself distrusts.
- The state-management design (the same merge facts hand-copied into `decisions.md`, `current-status.md`, and `roadmap.md`) mechanically generates the reconciliation PRs, which themselves require governance ceremony, which generates more state. This is a self-sustaining loop, and it is the single largest source of systemic friction.

The individual controls are mostly well-reasoned. The accumulation is not. The system is coherent in intent, over-governed in procedure, and under-governed in mechanism.

---

## 2. System map (what actually exists)

Five distinguishable subsystems live in one repository:

**A. Domain product (monthly-agent proper)** — the only part with production intent.
- Prompts (`prompts/`), activity schema (`schemas/activity.schema.json`), six business rules (`rules/`, `validators/business_rules/` — BR-001..005 active, BR-006 implemented but activation held), two validator CLIs (`tools/validate_schema.py`, `tools/validate_business_rules.py`), findings JSON emission, run evidence (`data/runs/2026-06-r01..r03`), workflow docs. R03 closed `partially_approved` (32/45 approved). **No pipeline runner exists**; the "pipeline" is a documented convention executed manually.

**B. Owner Authority Resolution (OAR) / bounded authority chain** — a cryptographic delegation system: RFC 8785 canonicalization, SHA-256 subject digests, typed non-transferable authority purposes, external trust anchor, closed-world registry snapshots, revocation-first lifecycle. ~960 LOC verifier (`tools/oar_verifier/`) + ~1,000 LOC tests. Entirely fictional (year-2099 fixtures), all schemas inactive Draft 0.x, architecture frozen at v0. Phase 1B.1/1B.2 (packaging, result contract) complete; Phase 2 deferred.

**C. Governance control plane** — `docs/governance.md` (OD-REVIEW-POLICY-001, OD-REVIEW-EVIDENCE-002, OD-REVIEW-QUALIFICATION-001): tiering, dual review, substantive-initiator analysis, exact-head binding, stale-state search, evidence submission modes, transcription protocol, stop rules, the ~60-field classification record, true-merge and post-merge proof requirements. Enforced entirely in prose.

**D. State/records layer** — `docs/decisions.md` (ADRs + Owner Decisions), `docs/current-status.md` (agent handoff dashboard), `docs/roadmap.md`. These three hold overlapping copies of the same facts (verified: PR #26/#28/#30/#32 merge SHAs, parents, tree hashes, and landed-path lists each appear in all three files). 63 instances of negative-authorization boilerplate ("does not authorize… remains deferred…") across docs; the phrase "downstream activation" appears 23 times.

**E. Multi-AI execution layer** (visible only through records, not code) — Owner/Marco: final approval, merge, trust anchor, qualification confirmer. ChatGPT: substantive initiator and "governance facilitator" (drafts the governance itself). Codex: implementation author. DeepSeek: planning initiator (PR #32). Hermes: orchestration shell. Claude/Fable/Qwen3-Max: independent review perspectives. Greptile: mentioned only as never-qualified.

**Coupling assessment:** A and B are cleanly separated in code (the OAR verifier imports nothing from the domain validators and vice versa). B, C, and D are heavily interleaved in documentation: `architecture.md`, `governance.md`, and `docs/contracts/README.md` each open with OAR boundary disclaimers; every Owner Decision re-enumerates the full deferred-boundary list. The control plane and the domain share the same three status files, so every change to either forces reconciliation of both.

---

## 3. Top systemic findings

### Critical

**SF-1 — The governance system's primary output is now maintenance of the governance system.**
- *Observation:* PRs #25, #27, #29, #31, #33 exist solely to reconcile `current-status.md` / `decisions.md` / `roadmap.md` after PRs #24, #26, #28, #30, #32. That is a 1:1 reconciliation PR per substantive PR. PR #33 itself needed a second commit ("Resolve PR #32 stale status reference") — reconciliation of the reconciliation. Meanwhile no product-pipeline capability has landed since PR #10.
- *Why it matters:* governance cost is superlinear in activity. Each substantive PR triggers a follow-up PR, which triggers classification, review, stale-state search, and new state to keep consistent. At current ratios, activating real work (shadow evidence, real data) would roughly double the reconciliation load exactly when correctness matters most.
- *Evidence:* git log #23–#33; diffs of the five reconciliation merges (each touches only the three status docs ± an index).
- *Layer:* workflow lifecycle / state management.
- *Direction:* eliminate the reconciliation stage as a PR class. Merge facts (SHAs, parents, trees, landed paths, timestamps) are already immutably recorded by GitHub; the repository should either derive them mechanically into one machine-readable ledger or stop copying them into prose at all. Update status *in the same PR* that changes it, or not at all.
- *Action required before further activation:* **yes.**

**SF-2 — Every safety-critical control is prose interpreted by LLMs; none is machine-enforced.**
- *Observation:* `.github/workflows/tests.yml` enforces pytest + `uv lock --check` + wheel build. Nothing enforces: exact-head binding, changed-path allowlists, true-merge method (repo merge settings are not even asserted), merge-parent proof, landed-scope proof, classification-record presence or completeness, stale-SHA detection, or the activation registry boundary. All of these are deterministic checks — the policy itself lists them as objective — yet each is re-derived by hand/LLM per PR and transcribed into PR bodies.
- *Why it matters:* the architecture's stated core risk is `workflow execution → model interpretation → de facto governance decision`. The current design maximizes that risk surface: the models that execute the workflow are also the ones attesting that the deterministic gates passed. A model that mis-copies a SHA or silently skips a checklist line produces a record indistinguishable from a passed gate. The elaborate record format increases the attestation surface without increasing verification.
- *Evidence:* PR #32 body — a ~60-field hand-assembled record including commit-chain SHAs and CI run IDs, none validated by any tooling; `governance.md` §"Merge method and post-merge proof" has no corresponding check anywhere in the repo.
- *Layer:* governance / control plane.
- *Direction:* move the deterministic subset into CI and branch protection (see §6). Prose should then only cover what genuinely needs judgment.
- *Action required before further activation:* **yes.** This is the highest-leverage change available.

### Major

**SF-3 — Triplicated human-readable state is the root cause of SF-1.**
- *Observation:* the same merge facts are hand-maintained in `decisions.md`, `current-status.md`, and `roadmap.md` (verified for PRs #24, #26, #28, #30, #32). `current-status.md` already concedes the problem for one field ("The latest commit hash is intentionally not tracked in this file because it can become stale") while tracking a dozen other equally stale-prone facts.
- *Why it matters:* every fact copied N times creates N−1 reconciliation obligations and N−1 opportunities for the "stale-state" defects the governance system then needs stale-state searches to catch. The stale-state search gate is a compensating control for a self-inflicted problem.
- *Layer:* documentation/state management.
- *Direction:* one source of truth per fact class. Decisions: append-only in `decisions.md` only. Merge/verification facts: GitHub + (optionally) one machine-readable ledger file. `current-status.md` shrinks to pointers; `roadmap.md` records only forward intent, never completed-milestone forensics.
- *Action before activation:* yes (bundled with SF-1).

**SF-4 — OAR solves a multi-party trust problem in a single-party system: proportionality inversion.**
- *Observation:* the authority chain (trust anchor → registry snapshot → typed envelopes → revocation-first resolution) is a delegation-verification architecture. In this system, the Owner is simultaneously the trust anchor authority, registry publisher, authority issuer, eligibility decider, selection decider, final approver, and merge authority. Every link in the cryptographic chain begins and ends with the same person. Meanwhile the risk the product actually faces today — a wrong fee or date reaching elderly participants — is governed by six business rules, QA prompts, and human review, and the pipeline that would carry that risk has no runner.
- *Why it matters:* this is not wasted work — the verifier is well-built and fail-closed discipline is genuinely good — but it is mis-sequenced capital. Roughly half the repository's code, tests, contracts (15+ contract docs, 12 draft schemas), and review cycles protect a boundary (downstream field-level authority) that no consumer yet crosses, while the near-term boundary (real extraction correctness at scale) is comparatively under-invested (no runner, no QA engine, corpus untested end-to-end).
- *Evidence:* file inventory §2; roadmap "No pipeline runner exists"; Milestones 4 (QA Engine) and 5 (Newsletter) untouched.
- *Layer:* architecture / roadmap allocation.
- *Direction:* freeze OAR exactly where it is (it is already frozen — honor that). No Phase 2, no further OAR interface polish, until a real second party (a consumer, an external publisher, or a second human) exists. Redirect capacity to the vertical slice that exercises the domain pipeline.
- *Action before activation:* no code change required; a sequencing decision is required.

**SF-5 — Hidden authority concentration in the orchestration layer.**
- *Observation:* ChatGPT is recorded as "substantive initiator and governance facilitator" for the governance policies themselves (OD-REVIEW-EVIDENCE-002 roles; OD-REVIEW-QUALIFICATION-001 draft). The same orchestration layer that runs the workflow drafts the rules that govern the workflow, proposes tier classifications, and assembles the evidence records the Owner ratifies. The designed check — independent review — was satisfied for both governance-policy PRs (#24, #30) by Fable + Claude: two models from one provider. The policy's own model-diversity rule did not apply because governance changes are not in the non-waivable category, but the correlated-failure risk the rule targets is at least as real for the rules of the game as for production changes. Separately, in PR #32 the Owner qualified Qwen3-Max-via-Hermes as Perspective 2 by discretionarily accepting a shared operator context — i.e., in the one hard case, the independence gate resolved by Owner waiver.
- *Why it matters:* this is exactly the `execution → interpretation → de facto governance` path the system fears, one level up. Nothing improper is evidenced; the structure is simply load-bearing on the Owner reading everything, and the Owner is also the busiest node.
- *Layer:* authority model.
- *Direction:* (a) extend the model-diversity requirement (or a human-perspective requirement) to changes of `docs/governance.md` itself; (b) record the orchestrator (ChatGPT/Hermes) as a standing role with explicitly *no* review or classification authority, so its outputs are always inputs to a gate, never gate outcomes; (c) shrink what must be interpreted (SF-2) so the Owner's ratification is over less surface.
- *Action before activation:* yes for (a)/(b) — cheap, one governance edit; (c) tracks SF-2.

**SF-6 — Negative-authorization boilerplate grows O(n²) and buries the actual state.**
- *Observation:* 63 occurrences of "does not authorize / remains deferred / grants no…" phrases; each new Owner Decision re-enumerates the full list of everything it does not activate (BR-006, D3, Phase 2, projection, manifest, trust-anchor delivery, Greptile…). Each newly deferred item must then be appended to every future decision's denial list.
- *Why it matters:* agents must hold the entire denial corpus in context to know what is active; the honest answer ("active = BR-001..005 + two validator CLIs, everything else inactive") is one short whitelist. The blacklist style also produced dangling references: **GOV-DEBT-001 and GOV-DEBT-002 are listed as deferred/unauthorized but are defined nowhere in the repository** — a governance record that cannot be audited.
- *Layer:* documentation / agent context burden.
- *Direction:* maintain one authoritative activation registry (what IS active/authorized, with everything else inactive by default rule). Decisions then state their positive grant plus "no other activation" in one sentence. Define or delete GOV-DEBT-001/002.
- *Action before activation:* yes — the whitelist must exist before activation decisions start flipping entries.

### Moderate

**SF-7 — The new-head rule imposes flat re-review cost regardless of delta risk.**
PR #32 went through three heads; each new commit invalidated all review and required full base-to-head dual Tier 2 re-review — for a one-commit, three-file correction to a test-only artifact. The rule's intent (no review inheritance across heads) is correct; its cost is flat because nothing can mechanically attest "delta from reviewed head touches only paths X,Y,Z with these diffs." A deterministic delta-scope check would let policy define a bounded re-review (full re-review remains the default for semantic changes). *Layer:* review policy. *Action before activation:* no, but do it before activity volume rises.

**SF-8 — The qualification policy demands evidence that is frequently unverifiable, then resolves by discretion.**
Model provider/family, operator separation, and session provenance are largely unattestable claims for hosted models (the policy admits this: "producing-session provenance unavailable"). The stop rules correctly fail closed on paper, but the observed resolution path is Owner discretion (PR #32). A deterministic rule pretending to solve a semantic/unverifiable problem is the exact anti-pattern the review brief names. *Direction:* be honest in the policy: provenance claims are declarations weighted by the Owner, and the hard requirement should be the one thing verifiable in-repo — separately produced artifacts with materially different content — plus human perspective for the non-waivable class. *Action before activation:* no.

**SF-9 — Single-human governance with organizational-scale ceremony.**
The policy models an organization (Owner, merge authority, classification reviewer, qualification confirmer, transcriber, auditors); all human roles resolve to one person, who is also a substantive initiator on most governance content. As ceremony grows, the realistic failure mode is not malice but ratification fatigue — approving 60-field records without full verification, which converts every control into theater. Machine-enforcing the mechanical fields (SF-2) is the mitigation; so is honest role-collapse: the policy should say what it means for one Owner to hold all these hats rather than simulating separation that doesn't exist. *Action before activation:* partially (via SF-2).

**SF-10 — Domain docs have drifted from operational reality.**
`README.md` still shows "Business Rule Engine: In progress / QA Engine: Planned" and a ChatGPT→Codex→Claude→pytest workflow that omits DeepSeek, Hermes, Qwen, Fable, the Owner gates, and the entire tier system. A newcomer reading README + AGENTS.md would have no idea the governance layer exists. Minor per-file, systemic in aggregate: the human-facing docs describe system A, the effective system is A+C+D+E. *Action before activation:* no.

### Minor

**SF-11 — Example corpus hygiene.** `examples/architecture-review/` carries ~7 months of real .docx/.xlsm/.pdf binaries with staff names in filenames, in a public-facing git history. Weight and privacy are both worth an Owner look (observational evidence per the repo's own hierarchy — flag, not verdict).

**SF-12 — Repo metadata.** GitHub repo description is "testing", branch protection state is not asserted anywhere; the true-merge rule depends on unrecorded platform settings.

---

## 4. What should remain unchanged

These controls address real failure modes and earned their keep in the historical record:

1. **Exact-head binding of review and CI** (as a concept). The #32 multi-head history shows drive-by commits after review are a real pattern.
2. **Author-external independent review with substantive-initiator analysis.** The D3-M01 catch (scope creep into bare-field recognition) was found by review and genuinely corrected — the control demonstrably works.
3. **Fail-closed defaults** throughout (validators, OAR, activation).
4. **Activation-hold discipline** — implemented ≠ active (BR-006, D3, draft schemas). This is the repository's best idea and the seed of the whitelist registry in SF-6.
5. **Immutable run evidence** under `data/runs/` and append-only decision records.
6. **True-merge + landed-scope verification** as *checks* (their enforcement should move to machines; the requirement itself stays).
7. **Uncertainty preservation over inference** in extraction; deterministic per-record business rules; the schema/business/QA/human validation boundary.
8. **Prospective, non-retroactive effect** of policy changes.
9. The OAR verifier codebase itself — small, deterministic, well-tested. Keep frozen; do not delete, do not extend.

## 5. What should be simplified

1. **The reconciliation PR class** — abolish (SF-1/SF-3). Status changes ride in the causing PR or are machine-derived.
2. **The classification record** — from ~60 flat fields to a tiered schema: mechanical tier ≈ 8–10 fields (all machine-fillable), standard ≈ +reviewer fields, high-assurance = current full record. `not required` padding disappears.
3. **Negative-authorization boilerplate** → one activation registry + one-line denial (SF-6).
4. **Triplicated merge forensics** → single ledger (SF-3). `roadmap.md` loses all backward-looking SHA content.
5. **Stale-state search** — shrinks automatically once facts stop being duplicated; retain it only for genuine semantic supersession (policy wording), not SHA bookkeeping.
6. **Per-decision re-narration** of the full OAR/boundary history at the top of `architecture.md`, `governance.md`, `contracts/README.md` — state it once, link to it.

## 6. What should become machine-enforced

All are currently prose/LLM-interpreted; all are deterministic:

| Control | Mechanism |
|---|---|
| True-merge only (no squash/rebase) | GitHub branch-protection settings, asserted in a recorded settings snapshot |
| Merge-parent + landed-scope proof | Post-merge CI job on `main`: verify 2 parents, first parent = prior main, merge tree = head tree, diff paths = declared allowlist |
| Changed-path allowlist per PR | CI job reading a small `pr-scope` file in the PR (declared allowlist vs `git diff --name-only base..head`) |
| Exact-head CI binding | Already inherent in GitHub checks; stop transcribing run IDs into prose |
| Classification record completeness | Record as YAML/JSON in the PR (file or body block), schema-validated by CI |
| Stale-SHA / stale-status lint | CI grep of docs for SHAs/status strings not present in the ledger |
| Activation boundary | Single machine-readable activation registry; test asserts runtime registry (`validators/business_rules/__init__.py`) ⊆ activation registry; D3/BR-006 stay excluded until the registry says otherwise |
| Draft-schema inactivity | Test asserting no runtime tool loads anything under `schemas/drafts/` |

What must **stay** judgment-based (do not fake determinism): tier edge cases beyond path triggers, contract semantics, correlated-reviewer assessment, evidence sufficiency for ambiguous cases, policy exceptions, and reviewer capability. Conversely, the one currently-deterministic rule pretending to solve a semantic problem is the provider/family diversity attestation (SF-8) — keep the intent, reword as declared-evidence-weighed-by-Owner plus the human-perspective option.

## 7. Reusable governance kernel assessment

**Counterfactual:** strip everything elderly-centre/calendar/extraction-specific. What remains is (a) the three governance policies — already ~90% domain-agnostic prose; (b) the OAR authority-verification pattern — generic envelope design but with calendar-typed purposes baked into subjects, schemas, and fixtures; (c) the lifecycle conventions (activation holds, exact-head binding, evidence records). That is a real, coherent kernel-shaped asset — on paper.

**Is extraction justified now? No.**

- n=1. There is no second project to falsify the abstractions, so extraction now would enshrine monthly-agent's accidents (three-status-file layout, reconciliation PRs, the 60-field record) as the "kernel" — including the very debt this review flags.
- The kernel's deterministic gates don't exist yet (SF-2). Extracting a prose-only governance kernel exports the enforcement gap.
- The proposed `core/profiles/adapters/projects` tree is platform-building ahead of demand. Model-specific "adapters" (codex/hermes/claude/qwen) are especially premature: the qualification policy deliberately removed named-model coupling; an adapter layer would reintroduce it structurally.

**What would belong in a kernel later:** review policy + evidence procedures + qualification policy (as templates), the classification-record schema, the deterministic CI gate scripts from §6, the activation-registry pattern, and the authority-envelope concept (purposes parameterized, not calendar-typed). **Must remain project-specific:** business rules, schemas, prompts, run layout, tier triggers tied to concrete paths, and all activation decisions. **Do not introduce yet:** profiles-as-code, adapter layer, any packaging of the kernel as an installable artifact.

The cheap, no-regret move: once §6 gates exist as scripts, keep them in a clearly separable directory (e.g., `governance/`) with no imports from domain code. That preserves the extraction option at near-zero cost without committing to it.

## 8. Governance profiles

One governance model is currently applied to everything: a docs-typo-level reconciliation and a policy rewrite both pass through classification records, stale-state searches, and independent confirmation. The Tier 1/Tier 2 split exists but Tier 1 is itself heavyweight ("Tier 1 is neither review exemption nor reduced-quality review" — correct in spirit, but in practice Tier 1 carries most of the ceremony).

Minimum viable profile model — three levels, triggered by system properties:

- **Mechanical** — changes fully characterized by deterministic checks (status-ledger updates, index files, comment-only edits, additions of inactive draft artifacts within a declared allowlist). Gates: CI + allowlist check + one reviewer sanity pass. No classification record beyond the machine-generated one.
- **Standard** (≈ current Tier 1) — code/doc changes without authority, contract-semantic, or activation impact. One qualified independent reviewer + machine gates.
- **High-assurance** (≈ current Tier 2) — governance changes, contract/schema semantics, any activation, authority/security surfaces, real-data or production effects. Dual perspectives, diversity/human requirement, full record.

Profile selection should be machine-proposed from changed paths + activation-registry deltas, with escalation always allowed and de-escalation requiring the author-external reviewer, as today. Do not build more taxonomy than this.

## 9. Failure-mode analysis (from the historical record)

- **D3-M01** (validator silently acquired a field-name vocabulary → scope/authority creep): *model capability + spec-precision failure*, caught by independent review. Lesson: review works; also, semantic authority boundaries need executable negative tests (which the correction added — good pattern to standardize).
- **Repeated stale-state incidents** (dedicated reconciliation PRs; a reconciliation PR itself needing a stale-reference fix in #33): *architectural failure*, not an execution mistake — duplicated state guarantees staleness regardless of agent quality. The recurring pattern with the strongest signal.
- **Exact-head invalidation churn** (PR #32, three heads, full dual re-review each time): *policy cost defect*, not a safety defect — the rule is right, its flat cost is not (SF-7).
- **Reviewer qualification hard cases resolved by Owner discretion** (Qwen-via-Hermes; shared operator context accepted): *policy defect* — the policy demands unverifiable evidence, so the gate's rigor becomes discretionary exactly when it binds (SF-8).
- **Orchestration/model-role blur** (ChatGPT drafting governance it facilitates; Hermes classified post-hoc as "execution/orchestration shell"): *authority-model gap* (SF-5). No incident evidenced, but the structure invites one.
- **Tier-classification correctness**: the record shows careful classification with no evidenced misclassification incident — but also no deterministic backstop, so this remains an unfalsifiable success claim (insufficient evidence either way; noted explicitly).
- **Isolated execution mistakes** (early duplicate-looking commits, spec/impl alignment fixes in Milestone 3.x): normal engineering noise, no structural response needed.

## 10. Readiness for the next stage

**Recommendation: B — pause and simplify/refactor governance first, as a short, bounded refactor (roughly the size of two of the existing governance PRs), then resume the monthly-agent roadmap. Defer C (kernel extraction) with a cheap option preserved.**

Reasoning: the next roadmap stages (real vertical-slice evidence, BR-006 activation, shadow processing, activation decisions) are exactly the stages where per-PR governance load and stale-state risk multiply. Entering them with hand-enforced gates and triplicated state means either escalating overhead (SF-1 curve) or eroding compliance (SF-9 ratification fatigue). Both are worse than a two-step pause. A (continue first) burns the cheapest moment to fix the loop; C (extract kernel now) doubles the abstraction surface at n=1; D adds nothing A–C lack.

---

## Recommended target architecture (minimal, incremental)

Keep the current repository shape. Add/change only:

1. `governance/ledger` — one machine-readable append-only record of merges, decisions, and activation state (the facts currently triplicated in prose). `decisions.md` remains the human narrative; SHAs/trees/paths live only in the ledger.
2. `governance/activation-registry` — the single whitelist of active rules/contracts/schemas; runtime registry and tests assert against it.
3. `governance/checks/` — the deterministic gate scripts from §6, wired into CI + a post-merge verification job; branch protection configured and its snapshot recorded.
4. `docs/governance.md` — reduced to: authority model (honest about single-Owner role collapse), the three profiles and their triggers, the judgment-only gates, stop rules, and pointers to the machine checks that replaced prose enforcement. Target: well under half its current length with no assurance loss.
5. Status docs: `current-status.md` becomes a one-screen pointer page; `roadmap.md` forward-looking only.
6. Domain layer, OAR verifier, contracts, schemas: unchanged. OAR stays frozen.

## Transition plan

| # | Step | Purpose | Risk | Depends on | Governance change? | Blocks next milestone? |
|---|------|---------|------|------------|--------------------|------------------------|
| 1 | No-regret cleanup: define/delete GOV-DEBT-001/002; fix README drift; create activation registry (initially just documenting current truth); stop adding backward-looking SHAs to roadmap | Remove dangling refs, establish whitelist | Minimal — factual only | — | No (factual reconciliation under existing rules) | No |
| 2 | Deterministic gate extraction: ledger + CI checks + branch-protection assertion + record-as-schema (§6) | Convert attestation into verification; kill the reconciliation loop | Low; checks are additive and can run non-blocking first, then flip to required | 1 | Yes — Tier 2 once, amending evidence procedures to recognize machine gates | **Yes — do before activation work** |
| 3 | Authority-boundary clarification: orchestrator role defined with no gate authority; diversity/human rule extended to governance.md changes; qualification policy reworded per SF-8 | Close the execution→interpretation→decision path | Low | — (parallelizable with 2) | Yes — Tier 2, small | Partially (should land before activation decisions) |
| 4 | Governance profiles: introduce Mechanical profile; re-scope Tier 1/Tier 2 as Standard/High-assurance; tiered record schema | Proportional cost; make light work light | Medium — de-escalation errors; mitigated by machine-proposed classification and upward-only overrides | 2 | Yes — Tier 2 | No, but strongly recommended first |
| 5 | (Optional, deferred) kernel separation: keep `governance/` import-free from domain code; extract only when a second project exists | Preserve reuse option at zero abstraction cost | Low if deferred; high if forced now | 2–4 | No (structural only) | No |
| 6 | Resume roadmap: vertical-slice evidence → BR-006 activation decision → QA engine → shadow processing, under the new profiles | The actual product | Normal | 2 (hard), 3–4 (soft) | Activation decisions per existing policy | — |

## Final verdict

1. **Should the system proceed beyond the current bounded D4A/shadow-contract stage before this review is acted on?** No. Complete transition steps 1–2 (and ideally 3) first. They are small, and every activation-stage control gets cheaper and more trustworthy after them. Nothing else needs to stop; this is a weeks-scale pause, not a freeze.
2. **Is governance under-built, proportionate, or over-built?** Both mis-built directions at once: **over-built in procedure** (prose volume, record size, reconciliation lifecycle, ceremony applied uniformly) and **under-built in mechanism** (zero machine enforcement of its own deterministic gates). Net classification: over-governed relative to delivered assurance.
3. **Should `monthly-agent` remain the primary product or become a reference implementation for a reusable governance system?** Remain the primary product for now — while acknowledging what the evidence shows: since PR #23 the governance system has received nearly all investment and is the more developed asset. If the Owner's real ambition is the governance system, that should be decided explicitly rather than continuing to fund it implicitly through a newsletter project. Until that decision is made deliberately, treat monthly-agent as the product and the governance layer as its (slimmed) control plane, with the §7 option preserved.
4. **Single highest-leverage decision for the Owner:** authorize the deterministic control plane — one machine-readable state ledger plus CI-enforced gates (transition step 2) — and simultaneously abolish the post-merge reconciliation PR class. This one decision removes the largest recurring cost (SF-1/SF-3), closes the largest assurance gap (SF-2), shrinks the Owner's own ratification burden (SF-9), and is a precondition for safe activation work.
