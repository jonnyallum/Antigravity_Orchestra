# Memory Hygiene Protocol — Anti-Pollution Safeguards
> Jai.OS 4.0 | Effective: 2026-02-09

## Purpose
Prevent memory pollution as the system scales. Based on research into parallel learning degradation patterns and the Feb 9 system audit findings.

---

## The 4 Safeguards

### 1. Selective Memory Addition (Confidence Gate)
**Rule:** Only learnings with confidence >= 0.7 enter permanent memory.

- **Verified Pool** (confidence >= 0.9): Production-validated learnings. Used for agent decisions.
- **Experimental Pool** (0.7 <= confidence < 0.9): PLR results, untested techniques. Used for training only.
- **Rejected** (confidence < 0.7): Not stored. Log reason in chatroom.

**Tool:** `python execution/memory_quality_gate.py validate --learning "..." --source "T0XX" --confidence 0.9`

### 2. Novelty Check (Deduplication Gate)
**Rule:** New learnings must be sufficiently different from existing ones.

- Similarity > 0.5 with any existing learning = REJECTED (duplicate)
- If similar but higher confidence: REPLACE the existing entry
- If similar from multiple PLR branches: MERGE with combined confidence

**Tool:** Built into `memory_quality_gate.py validate`

### 3. Temporal Decay (Freshness Gate)
**Rule:** Older learnings lose weight over time.

- Formula: `weight = original_weight * e^(-0.1 * age_in_days)`
- Run weekly: `python execution/memory_quality_gate.py decay`
- Learnings below weight 0.3 are candidates for pruning

**Tool:** `python execution/memory_quality_gate.py decay`

### 4. Inference vs Training Separation
**Rule:** Don't let experimental learnings contaminate production decisions.

- **For agent decisions:** Only use Verified Pool learnings
- **For PLR runs:** Can reference Experimental Pool
- **For Training Day:** Review both pools, promote experimentals that proved out

---

## Weekly Maintenance Cycle

Every Sunday (or at start of new week):

```bash
# 1. Apply temporal decay
python execution/memory_quality_gate.py decay

# 2. Prune low-weight memories
python execution/memory_quality_gate.py prune --threshold 0.3

# 3. Generate health report
python execution/memory_quality_gate.py report

# 4. Run full brain sync
python execution/brain_sync_protocol.py
```

---

## When to Add Learnings

| Trigger | Action | Confidence |
|:--------|:-------|:-----------|
| Production bug fixed | Add learning | 0.95 |
| Deployment succeeded | Add learning | 0.9 |
| PLR run completed | Add winner's insight | 0.85 |
| PLR observer session | Add techniques | 0.8 |
| Research completed | Add key findings | 0.75 |
| Hypothesis untested | Do NOT add | < 0.7 |

---

## Red Flags (Memory Pollution Indicators)

Watch for these signs that memory is degrading:

1. **Contradictory learnings** — Two entries that say opposite things
2. **Duplicate clusters** — 3+ entries saying the same thing differently
3. **Stale dominance** — Old learnings with high weight blocking new patterns
4. **Confidence inflation** — Everything rated 1.0 (no discrimination)
5. **Orphan learnings** — No source task ID (unverifiable)

If any detected: Run `memory_quality_gate.py report` and escalate to @Marcus.

---

*Directive created: 2026-02-09 | Source: Full System Audit (AUDIT-001) + Parallel Learning Research*
