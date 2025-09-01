import os
import argparse
import shutil
from utils import load_or_create_key, decrypt_log

def search_entries(entries, query):
    results = [e for e in entries if query.lower() in e.lower()]
    if not results:
        print("❌ No matches found.")
    else:
        print(f"[INFO] Found {len(results)} match(es):")
        for r in results:
            print("   ", r)
    return results

def restore_file(entry):
    try:
        original, rest = entry.split(" -> ")
        renamed, path = rest.split(" @ ")
        current_path = path.strip()
        if not os.path.exists(current_path):
            print("❌ File not found at stored path.")
            return
        restore_path = os.path.join(os.path.dirname(current_path), original)
        shutil.move(current_path, restore_path)
        print(f"✅ Restored {renamed} to original name: {restore_path}")
    except Exception as e:
        print("❌ ERROR restoring file:", e)

def main():
    parser = argparse.ArgumentParser(description="Retrieve and optionally restore hidden files from encrypted log.")
    parser.add_argument("--search", help="Search term (original name, renamed name, or category hint)")
    parser.add_argument("--restore", action="store_true", help="Restore the first matching file to its original name")
    args = parser.parse_args()

    print("[START] Retrieval operation initiated.")
    key = load_or_create_key()
    entries = decrypt_log(key)
    if not entries:
        return

    if args.search:
        matches = search_entries(entries, args.search)
        if args.restore and matches:
            restore_file(matches[0])
    else:
        print("[INFO] Full log contents:")
        for e in entries:
            print("   ", e)

    print("[COMPLETE] Retrieval operation finished.")

if __name__ == "__main__":
    main()
