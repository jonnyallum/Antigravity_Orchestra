"""
Dossier Indexer - Indexes and catalogues all research dossiers in The Courtroom.
Part of the Courtroom Ecosystem | Jai.OS 4.0

Scans the dossiers directory, extracts metadata (topic, date, confidence,
verdict status), and produces a searchable index. Prevents duplicate research
and enables @Scholar to check prior work before starting new investigations.

Usage:
    python dossier_indexer.py                    # Rebuild full index
    python dossier_indexer.py --search "AI"      # Search existing dossiers
    python dossier_indexer.py --stats            # Show research statistics
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
BRIEFS_DIR = ROOT / ".tmp" / "briefs"
VERDICTS_DIR = ROOT / ".tmp" / "verdicts"
INDEX_FILE = ROOT / ".tmp" / "dossier-index.json"

# Metadata extraction patterns
TITLE_PATTERN = re.compile(r'^#\s+(.+)', re.MULTILINE)
DATE_PATTERN = re.compile(r'(\d{4}-\d{2}-\d{2})')
CONFIDENCE_PATTERN = re.compile(r'\*\*(Verified|Probable|Unverified|Debunked)\*\*', re.IGNORECASE)
VERDICT_PATTERN = re.compile(r'(Courtroom Verdict|Strong Finding|Preliminary|Insufficient)', re.IGNORECASE)
AGENT_PATTERN = re.compile(r'@(\w+)')
TOPIC_FROM_FILENAME = re.compile(r'^(.+?)-\d{4}-\d{2}-\d{2}')


class DossierEntry:
    """Metadata entry for a single dossier."""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.filename = filepath.name
        self.file_size = filepath.stat().st_size
        self.modified = datetime.fromtimestamp(filepath.stat().st_mtime, tz=timezone.utc).isoformat()
        self.title = ""
        self.topic = ""
        self.date = ""
        self.confidence_levels = []
        self.verdict = None
        self.agents_mentioned = []
        self.word_count = 0
        self.has_evidence_section = False
        self.has_counter_arguments = False

    def extract_metadata(self):
        """Extract metadata from the dossier content."""
        content = self.filepath.read_text(encoding="utf-8", errors="replace")
        self.word_count = len(content.split())

        # Title
        title_match = TITLE_PATTERN.search(content)
        if title_match:
            self.title = title_match.group(1).strip()

        # Topic from filename
        topic_match = TOPIC_FROM_FILENAME.match(self.filepath.stem)
        if topic_match:
            self.topic = topic_match.group(1).replace("-", " ").title()
        elif self.title:
            self.topic = self.title

        # Date
        date_match = DATE_PATTERN.search(self.filename)
        if date_match:
            self.date = date_match.group(1)

        # Confidence levels used
        self.confidence_levels = list(set(
            m.lower() for m in CONFIDENCE_PATTERN.findall(content)
        ))

        # Verdict classification
        verdict_match = VERDICT_PATTERN.search(content)
        if verdict_match:
            self.verdict = verdict_match.group(1)

        # Agents mentioned
        self.agents_mentioned = list(set(AGENT_PATTERN.findall(content)))

        # Structure checks
        self.has_evidence_section = bool(re.search(
            r'##\s*(Evidence|Sources|References|Bibliography)', content, re.IGNORECASE
        ))
        self.has_counter_arguments = bool(re.search(
            r'(counter.?argument|counter.?evidence|opposing|alternative view)', content, re.IGNORECASE
        ))

    def to_dict(self) -> dict:
        return {
            "filename": self.filename,
            "filepath": str(self.filepath),
            "title": self.title,
            "topic": self.topic,
            "date": self.date,
            "modified": self.modified,
            "word_count": self.word_count,
            "file_size": self.file_size,
            "confidence_levels": self.confidence_levels,
            "verdict": self.verdict,
            "agents_mentioned": self.agents_mentioned,
            "has_evidence_section": self.has_evidence_section,
            "has_counter_arguments": self.has_counter_arguments,
        }


def build_index() -> list:
    """Scan all dossiers and build the index."""
    entries = []

    for directory in [DOSSIERS_DIR, BRIEFS_DIR, VERDICTS_DIR]:
        if not directory.exists():
            continue
        for md_file in sorted(directory.glob("*.md")):
            entry = DossierEntry(md_file)
            entry.extract_metadata()
            entries.append(entry)

    return entries


def save_index(entries: list):
    """Save the index to disk."""
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    index_data = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "total_dossiers": len(entries),
        "entries": [e.to_dict() for e in entries],
    }
    INDEX_FILE.write_text(json.dumps(index_data, indent=2), encoding="utf-8")
    return INDEX_FILE


def search_index(query: str, entries: list) -> list:
    """Search the index by topic, title, or content keywords."""
    query_lower = query.lower()
    results = []
    for entry in entries:
        searchable = f"{entry.title} {entry.topic} {entry.filename}".lower()
        if query_lower in searchable:
            results.append(entry)
    return results


def print_index(entries: list):
    """Print the dossier index as a formatted table."""
    if not entries:
        print("No dossiers found.")
        return

    print(f"\n=== Courtroom Dossier Index ({len(entries)} documents) ===\n")
    print(f"{'#':<4} {'Topic':<35} {'Date':<12} {'Words':<7} {'Verdict':<20} {'Evidence':<9}")
    print("-" * 90)

    for i, entry in enumerate(entries, 1):
        verdict = entry.verdict or "—"
        evidence = "Yes" if entry.has_evidence_section else "No"
        topic = (entry.topic or entry.filename)[:33]
        print(f"{i:<4} {topic:<35} {entry.date:<12} {entry.word_count:<7} {verdict:<20} {evidence:<9}")

    print()


def print_stats(entries: list):
    """Print aggregate research statistics."""
    if not entries:
        print("No dossiers to analyse.")
        return

    total_words = sum(e.word_count for e in entries)
    verdicts = [e for e in entries if e.verdict]
    with_evidence = sum(1 for e in entries if e.has_evidence_section)
    with_counter = sum(1 for e in entries if e.has_counter_arguments)

    all_agents = []
    for e in entries:
        all_agents.extend(e.agents_mentioned)

    agent_counts = {}
    for a in all_agents:
        agent_counts[a] = agent_counts.get(a, 0) + 1

    all_confidence = []
    for e in entries:
        all_confidence.extend(e.confidence_levels)

    conf_counts = {}
    for c in all_confidence:
        conf_counts[c] = conf_counts.get(c, 0) + 1

    print(f"\n=== Courtroom Research Statistics ===\n")
    print(f"Total Documents:      {len(entries)}")
    print(f"Total Word Count:     {total_words:,}")
    print(f"Avg Words/Dossier:    {total_words // max(1, len(entries)):,}")
    print(f"With Evidence Section: {with_evidence}/{len(entries)}")
    print(f"With Counter-Args:    {with_counter}/{len(entries)}")
    print(f"With Verdicts:        {len(verdicts)}/{len(entries)}")

    if conf_counts:
        print(f"\nConfidence Level Distribution:")
        for level, count in sorted(conf_counts.items(), key=lambda x: -x[1]):
            print(f"  {level.title()}: {count}")

    if agent_counts:
        print(f"\nMost Referenced Agents:")
        for agent, count in sorted(agent_counts.items(), key=lambda x: -x[1])[:10]:
            print(f"  @{agent}: {count} mentions")

    print()


def main():
    parser = argparse.ArgumentParser(description="Index and search Courtroom dossiers")
    parser.add_argument("--search", help="Search dossiers by keyword")
    parser.add_argument("--stats", action="store_true", help="Show research statistics")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    entries = build_index()
    save_index(entries)

    if args.search:
        results = search_index(args.search, entries)
        if args.json:
            print(json.dumps([e.to_dict() for e in results], indent=2))
        else:
            print(f"\nSearch results for '{args.search}':")
            print_index(results)
    elif args.stats:
        print_stats(entries)
    elif args.json:
        print(json.dumps([e.to_dict() for e in entries], indent=2))
    else:
        print_index(entries)

    print(f"Index saved to: {INDEX_FILE}")


if __name__ == "__main__":
    main()
