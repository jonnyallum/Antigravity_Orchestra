"""
Truth Score Calculator - Computes aggregate truth scores for Courtroom verdicts.
Part of the Courtroom Ecosystem | Jai.OS 4.0

Takes a dossier through the full Courtroom pipeline scoring:
  - Source Quality (weighted by primary/secondary/tertiary)
  - Logic Integrity (@Counsel stress test score)
  - Adversarial Survival (@Advocate cross-examination result)
  - Confidence Calibration (are confidence levels honest?)

Produces a final Truth Score (0-100) that determines if a conclusion
can be stamped as a Courtroom Verdict.

Usage:
    python truth_score_calculator.py --dossier .tmp/dossiers/topic-2026-02-13.md
    python truth_score_calculator.py --interactive
    python truth_score_calculator.py --score-card input.json
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
VERDICTS_DIR = ROOT / ".tmp" / "verdicts"
TASK_HISTORY = ROOT / ".agent" / "memory" / "task-history.json"

# Scoring weights — reflects the Courtroom pipeline priorities
WEIGHTS = {
    "source_quality": 0.25,       # @Scholar — how good are the sources?
    "source_diversity": 0.10,     # @Scholar — how many independent sources?
    "data_integrity": 0.10,       # @Parser — is the extracted data clean?
    "logic_integrity": 0.20,      # @Counsel — is the argument structurally sound?
    "adversarial_survival": 0.25, # @Advocate — did it survive cross-examination?
    "confidence_calibration": 0.10, # @Vigil — are confidence levels honest?
}

# Thresholds for verdict classification
THRESHOLDS = {
    "verdict": 80,          # >= 80: Courtroom Verdict (stamped truth)
    "strong_finding": 65,   # >= 65: Strong finding (high confidence)
    "preliminary": 50,      # >= 50: Preliminary finding (needs more work)
    "insufficient": 0,      # < 50: Insufficient evidence (cannot conclude)
}

# Source quality scores by type
SOURCE_QUALITY_MAP = {
    "primary": 100,          # Peer-reviewed, official docs, direct data
    "secondary": 70,         # Industry reports, expert analysis
    "tertiary": 40,          # Wikipedia, blog posts, social media
    "unverified": 10,        # Unknown provenance
}

# @Counsel logic ratings to scores
LOGIC_RATING_MAP = {
    "bulletproof": 100,
    "strong": 80,
    "weak": 40,
    "broken": 0,
}

# @Advocate verdict to scores
ADVERSARIAL_VERDICT_MAP = {
    "survives": 100,
    "wounded": 60,
    "killed": 0,
}


class TruthScoreCard:
    """A score card for computing the final truth score."""

    def __init__(self, topic: str, dossier_path: str = None):
        self.topic = topic
        self.dossier_path = dossier_path
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.scores = {}
        self.notes = {}
        self.final_score = 0
        self.classification = "PENDING"

    def set_score(self, dimension: str, score: int, note: str = ""):
        """Set a score for a dimension (0-100)."""
        if dimension not in WEIGHTS:
            raise ValueError(f"Unknown dimension: {dimension}. Valid: {list(WEIGHTS.keys())}")
        self.scores[dimension] = max(0, min(100, score))
        if note:
            self.notes[dimension] = note

    def calculate(self) -> float:
        """Calculate the weighted final truth score."""
        if not self.scores:
            return 0

        total = 0
        weight_sum = 0
        for dim, weight in WEIGHTS.items():
            if dim in self.scores:
                total += self.scores[dim] * weight
                weight_sum += weight

        # Normalize if not all dimensions are scored
        if weight_sum > 0:
            self.final_score = round(total / weight_sum, 1)
        else:
            self.final_score = 0

        # Classify
        for classification, threshold in sorted(THRESHOLDS.items(), key=lambda x: -x[1]):
            if self.final_score >= threshold:
                self.classification = classification.upper().replace("_", " ")
                break

        return self.final_score

    def to_markdown(self) -> str:
        """Generate a markdown truth score report."""
        lines = [
            f"# Truth Score Report: {self.topic}",
            f"> **Computed:** {self.timestamp}",
            f"> **Final Score:** **{self.final_score}/100**",
            f"> **Classification:** **{self.classification}**",
            "",
            "---",
            "",
            "## Dimension Scores",
            "",
            "| Dimension | Weight | Score | Weighted | Notes |",
            "|:----------|:-------|:------|:---------|:------|",
        ]

        for dim, weight in WEIGHTS.items():
            score = self.scores.get(dim, "N/A")
            note = self.notes.get(dim, "")
            if isinstance(score, (int, float)):
                weighted = round(score * weight, 1)
                bar = "=" * (score // 10) + "-" * (10 - score // 10)
                lines.append(f"| {dim.replace('_', ' ').title()} | {weight:.0%} | {score} [{bar}] | {weighted} | {note} |")
            else:
                lines.append(f"| {dim.replace('_', ' ').title()} | {weight:.0%} | N/A | — | Not scored |")

        lines.extend([
            "",
            "## Classification",
            "",
            f"| Threshold | Classification |",
            f"|:----------|:---------------|",
            f"| >= 80 | VERDICT (Stamped truth, Courtroom-approved) |",
            f"| >= 65 | STRONG FINDING (High confidence, minor gaps) |",
            f"| >= 50 | PRELIMINARY (Needs further investigation) |",
            f"| < 50 | INSUFFICIENT (Cannot draw conclusions) |",
            "",
            f"**This conclusion scores {self.final_score}/100 = {self.classification}**",
            "",
        ])

        if self.final_score >= THRESHOLDS["verdict"]:
            lines.append("This conclusion has been approved as a **Courtroom Verdict**. "
                         "It has survived source verification, logic stress testing, and adversarial review.")
        elif self.final_score >= THRESHOLDS["strong_finding"]:
            lines.append("This is a **Strong Finding** but has not achieved Verdict status. "
                         "Review the lowest-scoring dimensions for improvement opportunities.")
        elif self.final_score >= THRESHOLDS["preliminary"]:
            lines.append("This is a **Preliminary Finding**. Significant gaps remain. "
                         "Route back through the Courtroom pipeline for additional evidence and testing.")
        else:
            lines.append("**Insufficient Evidence.** This conclusion cannot be supported by the current evidence. "
                         "Major rework required before re-submission.")

        lines.extend([
            "",
            "---",
            f"*Truth Score Calculator | The Courtroom | Jai.OS 4.0*",
        ])
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "topic": self.topic,
            "dossier": self.dossier_path,
            "timestamp": self.timestamp,
            "scores": self.scores,
            "notes": self.notes,
            "final_score": self.final_score,
            "classification": self.classification,
        }


def interactive_scoring() -> TruthScoreCard:
    """Guide user through scoring each dimension interactively."""
    print("\n=== The Courtroom | Truth Score Calculator ===\n")

    topic = input("Topic/Conclusion being scored: ").strip()
    dossier = input("Dossier path (optional): ").strip() or None

    card = TruthScoreCard(topic, dossier)

    print("\nScore each dimension (0-100). Press Enter to skip.\n")

    # Source Quality
    print("--- Source Quality (@Scholar) ---")
    print("  primary=100, secondary=70, tertiary=40, unverified=10")
    sq = input("  Average source quality score [0-100]: ").strip()
    if sq:
        card.set_score("source_quality", int(sq), input("  Note: ").strip())

    # Source Diversity
    print("\n--- Source Diversity (@Scholar) ---")
    sd = input("  Number of independent sources (score: sources*20, max 100): ").strip()
    if sd:
        score = min(100, int(sd) * 20)
        card.set_score("source_diversity", score, f"{sd} independent sources")

    # Data Integrity
    print("\n--- Data Integrity (@Parser) ---")
    di = input("  Schema validation pass rate [0-100]: ").strip()
    if di:
        card.set_score("data_integrity", int(di), input("  Note: ").strip())

    # Logic Integrity
    print("\n--- Logic Integrity (@Counsel) ---")
    print("  bulletproof=100, strong=80, weak=40, broken=0")
    rating = input("  @Counsel rating [bulletproof/strong/weak/broken]: ").strip().lower()
    if rating in LOGIC_RATING_MAP:
        card.set_score("logic_integrity", LOGIC_RATING_MAP[rating], f"Rated: {rating}")

    # Adversarial Survival
    print("\n--- Adversarial Survival (@Advocate) ---")
    print("  survives=100, wounded=60, killed=0")
    verdict = input("  @Advocate verdict [survives/wounded/killed]: ").strip().lower()
    if verdict in ADVERSARIAL_VERDICT_MAP:
        card.set_score("adversarial_survival", ADVERSARIAL_VERDICT_MAP[verdict], f"Verdict: {verdict}")

    # Confidence Calibration
    print("\n--- Confidence Calibration (@Vigil) ---")
    cc = input("  Are confidence levels accurately calibrated? [0-100]: ").strip()
    if cc:
        card.set_score("confidence_calibration", int(cc), input("  Note: ").strip())

    card.calculate()
    return card


def score_from_json(filepath: Path) -> TruthScoreCard:
    """Load scores from a JSON score card file."""
    data = json.loads(filepath.read_text(encoding="utf-8"))
    card = TruthScoreCard(data["topic"], data.get("dossier"))

    for dim, score in data.get("scores", {}).items():
        note = data.get("notes", {}).get(dim, "")
        card.set_score(dim, score, note)

    card.calculate()
    return card


def save_verdict(card: TruthScoreCard) -> Path:
    """Save the truth score verdict."""
    VERDICTS_DIR.mkdir(parents=True, exist_ok=True)
    slug = card.topic.lower().replace(" ", "-")[:40]
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    filepath = VERDICTS_DIR / f"verdict-{slug}-{date}.md"
    filepath.write_text(card.to_markdown(), encoding="utf-8")
    return filepath


def main():
    parser = argparse.ArgumentParser(description="Calculate truth scores for Courtroom verdicts")
    parser.add_argument("--interactive", action="store_true", help="Interactive scoring mode")
    parser.add_argument("--score-card", help="Path to JSON score card")
    parser.add_argument("--save", action="store_true", help="Save verdict report")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.interactive:
        card = interactive_scoring()
    elif args.score_card:
        card = score_from_json(Path(args.score_card))
    else:
        print("Usage: python truth_score_calculator.py --interactive | --score-card <path>")
        sys.exit(1)

    if args.json:
        print(json.dumps(card.to_dict(), indent=2))
    else:
        print(card.to_markdown())

    if args.save:
        path = save_verdict(card)
        print(f"\nVerdict saved: {path}")


if __name__ == "__main__":
    main()
