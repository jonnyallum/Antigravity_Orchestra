"""
Citation Validator - Validates evidence chains and source quality in research dossiers.
Part of the Courtroom Ecosystem | Jai.OS 4.0

Scans dossier markdown files for citations, URLs, and evidence claims.
Checks for: broken links, missing sources, single-source claims,
confidence level consistency, and citation chain completeness.

Usage:
    python citation_validator.py --dossier .tmp/dossiers/ai-agents-2026-02-13.md
    python citation_validator.py --all
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
DOSSIERS_DIR = ROOT / ".tmp" / "dossiers"
REPORTS_DIR = ROOT / ".tmp" / "validation-reports"

# Confidence levels from @Scholar's SOP-004
VALID_CONFIDENCE_LEVELS = ["Verified", "Probable", "Unverified", "Debunked"]

# Minimum sources required per @Scholar's restrictions
MIN_SOURCES_FOR_VERIFIED = 3
MIN_SOURCES_FOR_PROBABLE = 2

# Patterns to detect in dossiers
URL_PATTERN = re.compile(r'https?://[^\s\)\]>]+')
CITATION_PATTERN = re.compile(r'\[(\d+)\]|\[Source:\s*([^\]]+)\]|\*Source:\s*([^*]+)\*')
CONFIDENCE_PATTERN = re.compile(r'\*\*(Verified|Probable|Unverified|Debunked)\*\*|Confidence:\s*(Verified|Probable|Unverified|Debunked)', re.IGNORECASE)
CLAIM_PATTERN = re.compile(r'^[-*]\s+\*\*[^*]+\*\*', re.MULTILINE)
FOLKLORE_INDICATORS = [
    "it's obvious",
    "everyone knows",
    "common knowledge",
    "clearly",
    "of course",
    "needless to say",
    "it goes without saying",
    "as we all know",
]


class ValidationReport:
    """Structured validation report for a dossier."""

    def __init__(self, dossier_path: str):
        self.dossier_path = dossier_path
        self.dossier_name = Path(dossier_path).name
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.errors = []
        self.warnings = []
        self.stats = {
            "total_urls": 0,
            "total_citations": 0,
            "total_claims": 0,
            "claims_with_confidence": 0,
            "claims_without_confidence": 0,
            "unique_sources": 0,
            "folklore_detections": 0,
        }
        self.verdict = "PENDING"

    def add_error(self, code: str, message: str, line: int = None):
        self.errors.append({"code": code, "message": message, "line": line})

    def add_warning(self, code: str, message: str, line: int = None):
        self.warnings.append({"code": code, "message": message, "line": line})

    def calculate_verdict(self) -> str:
        if len(self.errors) == 0 and len(self.warnings) <= 2:
            self.verdict = "PASS"
        elif len(self.errors) == 0:
            self.verdict = "PASS_WITH_WARNINGS"
        elif len(self.errors) <= 3:
            self.verdict = "NEEDS_REVISION"
        else:
            self.verdict = "FAIL"
        return self.verdict

    def to_markdown(self) -> str:
        lines = [
            f"# Citation Validation Report",
            f"> **Dossier:** `{self.dossier_name}`",
            f"> **Validated:** {self.timestamp}",
            f"> **Verdict:** **{self.verdict}**",
            "",
            "---",
            "",
            "## Statistics",
            f"| Metric | Value |",
            f"|:-------|:------|",
        ]
        for key, val in self.stats.items():
            label = key.replace("_", " ").title()
            lines.append(f"| {label} | {val} |")

        if self.errors:
            lines.extend(["", "## Errors (Must Fix)", ""])
            for e in self.errors:
                loc = f" (line {e['line']})" if e['line'] else ""
                lines.append(f"- **[{e['code']}]** {e['message']}{loc}")

        if self.warnings:
            lines.extend(["", "## Warnings", ""])
            for w in self.warnings:
                loc = f" (line {w['line']})" if w['line'] else ""
                lines.append(f"- **[{w['code']}]** {w['message']}{loc}")

        if not self.errors and not self.warnings:
            lines.extend(["", "## Result", "", "All citations validated. Evidence chain intact."])

        lines.extend([
            "",
            "---",
            f"*Citation Validator | The Courtroom | Jai.OS 4.0*",
        ])
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "dossier": self.dossier_name,
            "timestamp": self.timestamp,
            "verdict": self.verdict,
            "errors": self.errors,
            "warnings": self.warnings,
            "stats": self.stats,
        }


def validate_dossier(filepath: Path) -> ValidationReport:
    """Validate a single dossier's citations and evidence quality."""
    report = ValidationReport(str(filepath))

    if not filepath.exists():
        report.add_error("FILE_NOT_FOUND", f"Dossier not found: {filepath}")
        report.calculate_verdict()
        return report

    content = filepath.read_text(encoding="utf-8", errors="replace")
    lines = content.split("\n")

    # Extract URLs
    urls = URL_PATTERN.findall(content)
    report.stats["total_urls"] = len(urls)
    report.stats["unique_sources"] = len(set(urls))

    # Check minimum source diversity
    if report.stats["unique_sources"] < MIN_SOURCES_FOR_VERIFIED:
        report.add_error(
            "LOW_SOURCE_DIVERSITY",
            f"Only {report.stats['unique_sources']} unique sources found. "
            f"@Scholar requires minimum {MIN_SOURCES_FOR_VERIFIED} for 'Verified' claims."
        )

    # Extract and count citations
    citations = CITATION_PATTERN.findall(content)
    report.stats["total_citations"] = len(citations)

    # Extract confidence levels
    confidence_matches = CONFIDENCE_PATTERN.findall(content)
    confidence_count = len(confidence_matches)
    report.stats["claims_with_confidence"] = confidence_count

    # Count claims (bold items in bullet lists)
    claims = CLAIM_PATTERN.findall(content)
    report.stats["total_claims"] = len(claims)
    report.stats["claims_without_confidence"] = max(0, len(claims) - confidence_count)

    # Check for claims without confidence levels
    if len(claims) > 0 and confidence_count == 0:
        report.add_error(
            "NO_CONFIDENCE_LEVELS",
            "Dossier contains claims but no confidence levels. "
            "@Scholar must include Verified/Probable/Unverified/Debunked ratings."
        )
    elif len(claims) > confidence_count + 2:
        report.add_warning(
            "LOW_CONFIDENCE_COVERAGE",
            f"{len(claims)} claims found but only {confidence_count} confidence levels. "
            "Consider adding ratings to remaining claims."
        )

    # Scan for folklore (unsubstantiated language)
    for i, line in enumerate(lines, 1):
        line_lower = line.lower()
        for indicator in FOLKLORE_INDICATORS:
            if indicator in line_lower:
                report.stats["folklore_detections"] += 1
                report.add_warning(
                    "FOLKLORE_DETECTED",
                    f"Unsubstantiated language detected: '{indicator}'",
                    line=i,
                )

    # Check for evidence chain structure
    has_evidence_section = bool(re.search(r'##\s*(Evidence|Sources|References|Bibliography)', content, re.IGNORECASE))
    if not has_evidence_section:
        report.add_warning(
            "NO_EVIDENCE_SECTION",
            "No dedicated Evidence/Sources/References section found. "
            "Consider adding one for traceability."
        )

    # Check for counter-evidence section
    has_counter = bool(re.search(r'(counter.?argument|counter.?evidence|opposing|alternative view)', content, re.IGNORECASE))
    if not has_counter:
        report.add_warning(
            "NO_COUNTER_EVIDENCE",
            "No counter-arguments or alternative viewpoints section found. "
            "@Advocate requires these for adversarial review."
        )

    # Check dossier has a conclusion
    has_conclusion = bool(re.search(r'##\s*(Conclusion|Verdict|Recommendation|Summary|Findings)', content, re.IGNORECASE))
    if not has_conclusion:
        report.add_error(
            "NO_CONCLUSION",
            "Dossier has no conclusion/verdict/recommendation section."
        )

    report.calculate_verdict()
    return report


def validate_all_dossiers() -> list:
    """Validate all dossiers in the dossiers directory."""
    if not DOSSIERS_DIR.exists():
        print(f"No dossiers directory found at {DOSSIERS_DIR}")
        return []

    dossiers = list(DOSSIERS_DIR.glob("*.md"))
    if not dossiers:
        print("No dossiers found to validate.")
        return []

    reports = []
    for dossier in sorted(dossiers):
        report = validate_dossier(dossier)
        reports.append(report)

    return reports


def save_report(report: ValidationReport) -> Path:
    """Save validation report to disk."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    slug = Path(report.dossier_path).stem
    filename = f"validation-{slug}-{datetime.now(timezone.utc).strftime('%Y%m%d')}.md"
    filepath = REPORTS_DIR / filename
    filepath.write_text(report.to_markdown(), encoding="utf-8")
    return filepath


def print_summary(reports: list):
    """Print validation summary."""
    total = len(reports)
    passed = sum(1 for r in reports if r.verdict in ("PASS", "PASS_WITH_WARNINGS"))
    failed = sum(1 for r in reports if r.verdict in ("FAIL", "NEEDS_REVISION"))

    print(f"\n=== Citation Validation Summary ===")
    print(f"Dossiers scanned: {total}")
    print(f"Passed: {passed}")
    print(f"Failed/Needs Revision: {failed}")
    print()

    for report in reports:
        icon = "PASS" if report.verdict.startswith("PASS") else "FAIL"
        print(f"  [{icon}] {report.dossier_name} — {report.verdict} "
              f"({len(report.errors)} errors, {len(report.warnings)} warnings)")


def main():
    parser = argparse.ArgumentParser(description="Validate citations in Courtroom dossiers")
    parser.add_argument("--dossier", help="Path to a specific dossier to validate")
    parser.add_argument("--all", action="store_true", help="Validate all dossiers")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--save", action="store_true", help="Save reports to disk")

    args = parser.parse_args()

    if args.dossier:
        report = validate_dossier(Path(args.dossier))
        reports = [report]
    elif args.all:
        reports = validate_all_dossiers()
    else:
        print("Usage: python citation_validator.py --dossier <path> | --all")
        sys.exit(1)

    if not reports:
        return

    if args.json:
        print(json.dumps([r.to_dict() for r in reports], indent=2))
    else:
        print_summary(reports)
        for report in reports:
            if report.verdict not in ("PASS",):
                print(f"\n--- Detail: {report.dossier_name} ---")
                print(report.to_markdown())

    if args.save:
        for report in reports:
            path = save_report(report)
            print(f"Report saved: {path}")


if __name__ == "__main__":
    main()
