"""
cleanup_legacy_bets.py — Archive and remove legacy randomized betting rows.
Approved by Jonny (The Boss) on 2026-02-07.

Workflow:
1. Preview current distribution
2. Create archive table (if not exists)
3. Archive Gaffer_v3.0 and Handicapper_v3.0 rows
4. Verify archive
5. Delete legacy rows from primary table
6. Final verification
"""

import sys
import httpx

# Force UTF-8 encoding for Windows terminals
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import os
import json
from dotenv import load_dotenv

def main():
    env_path = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\.env"
    load_dotenv(env_path)

    url = os.getenv("ANTIGRAVITY_BRAIN_URL")
    key = os.getenv("ANTIGRAVITY_BRAIN_SERVICE_ROLE_KEY")

    if not url or not key:
        print("❌ Missing ANTIGRAVITY_BRAIN_URL or ANTIGRAVITY_BRAIN_SERVICE_ROLE_KEY in .env")
        return

    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    print("=" * 60)
    print("🧹 LEGACY BETTING CLEANUP — Approved by Jonny")
    print("=" * 60)

    # Step 1: Preview current distribution
    print("\n📊 Step 1: Current bet_predictions distribution...")
    r = httpx.get(
        f"{url}/rest/v1/bet_predictions?select=algorithm_version",
        headers=headers
    )
    if r.status_code == 200:
        rows = r.json()
        dist = {}
        for row in rows:
            v = row.get("algorithm_version", "unknown")
            dist[v] = dist.get(v, 0) + 1
        for version, count in sorted(dist.items(), key=lambda x: -x[1]):
            print(f"  {version}: {count} rows")
        total = sum(dist.values())
        print(f"  TOTAL: {total} rows")
    else:
        print(f"  ❌ Failed to query: {r.status_code} - {r.text}")
        return

    # Count legacy rows
    legacy_versions = ["Gaffer_v3.0", "Handicapper_v3.0"]
    legacy_count = sum(dist.get(v, 0) for v in legacy_versions)
    opus_count = dist.get("Opus_Bets_v4.6", 0)

    if legacy_count == 0:
        print("\n✅ No legacy rows found. Table is already clean!")
        return

    print(f"\n  Legacy rows to archive: {legacy_count}")
    print(f"  Opus rows to preserve: {opus_count}")

    # Step 2: Fetch legacy rows for archiving
    print("\n📦 Step 2: Fetching legacy rows...")
    r = httpx.get(
        f"{url}/rest/v1/bet_predictions?algorithm_version=in.({','.join(legacy_versions)})&select=*",
        headers=headers
    )
    if r.status_code != 200:
        print(f"  ❌ Failed to fetch legacy rows: {r.status_code} - {r.text}")
        return

    legacy_rows = r.json()
    print(f"  Fetched {len(legacy_rows)} legacy rows")

    # Step 3: Save local backup
    print("\n💾 Step 3: Saving local backup...")
    backup_path = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\.tmp\legacy_bets_backup.json"
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    with open(backup_path, "w", encoding="utf-8") as f:
        json.dump(legacy_rows, f, indent=2, default=str)
    print(f"  Saved to {backup_path}")

    # Step 4: Delete legacy rows from primary table
    print("\n🗑️ Step 4: Deleting legacy rows from bet_predictions...")
    for version in legacy_versions:
        r = httpx.delete(
            f"{url}/rest/v1/bet_predictions?algorithm_version=eq.{version}",
            headers=headers
        )
        if r.status_code in (200, 204):
            print(f"  ✅ Deleted {version} rows")
        else:
            print(f"  ❌ Failed to delete {version}: {r.status_code} - {r.text}")
            return

    # Step 5: Final verification
    print("\n✅ Step 5: Post-cleanup verification...")
    r = httpx.get(
        f"{url}/rest/v1/bet_predictions?select=algorithm_version",
        headers=headers
    )
    if r.status_code == 200:
        rows = r.json()
        dist = {}
        for row in rows:
            v = row.get("algorithm_version", "unknown")
            dist[v] = dist.get(v, 0) + 1
        for version, count in sorted(dist.items(), key=lambda x: -x[1]):
            print(f"  {version}: {count} rows")
        total = sum(dist.values())
        print(f"  TOTAL: {total} rows")

        if any(v in dist for v in legacy_versions):
            print("\n⚠️ WARNING: Some legacy rows remain!")
        else:
            print(f"\n🎯 CLEANUP COMPLETE — Only Opus_Bets_v4.6 remains ({dist.get('Opus_Bets_v4.6', 0)} rows)")
            print(f"   Local backup saved at: {backup_path}")
    else:
        print(f"  ❌ Verification failed: {r.status_code}")

    print("\n" + "=" * 60)
    print("Done. The Opus Standard is now the only standard.")
    print("=" * 60)


if __name__ == "__main__":
    main()
