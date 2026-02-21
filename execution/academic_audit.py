import sys
import io

# Force UTF-8 for stdout/stderr
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import sys
import os

def run_academic_audit(file_path):
    print(f"🎓 INTELLIGENCE AUDIT: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    try:
        content = open(file_path, 'r', encoding='utf-8').read()
        
        # Dictionary of deprecated patterns in Next.js 15 / React 19
        deprecated = {
            "next/head": "Next.js 13+ should use 'Metadata' API (layout.tsx/page.tsx) instead of 'next/head'.",
            "getInitialProps": "Legacy data fetching. Use Server Components and 'fetch'.",
            "getServerSideProps": "Legacy data fetching. Use Server Components and 'fetch' with {cache: 'no-store'}.",
            "forwardRef": "React 19 supports refs directly as props; 'forwardRef()' is no longer required.",
            "useContext": "React 19 promotes 'use()' for consuming contexts."
        }
        
        warnings = []
        for pattern, advice in deprecated.items():
            if pattern in content:
                warnings.append(f"⚠️ DEPRECATED PATTERN: '{pattern}' detected. {advice}")
        
        if not warnings:
            print("✅ Academic Sync: NOMINAL. Code utilizes modern framework patterns.")
        else:
            print("❌ Academic Sync: SYNERGY GAP DETECTED.")
            for w in warnings:
                print(f"  {w}")
                
    except Exception as e:
        print(f"❌ Audit Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python academic_audit.py [file_path]")
        sys.exit(1)
        
    run_academic_audit(sys.argv[1])
