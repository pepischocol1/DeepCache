import os
import shutil
import argparse
from datetime import datetime
from utils import random_name, load_or_create_key, encrypt_log_entry

def generate_encoded_filename(original_name, category_hint="GEN"):
    date_str = datetime.now().strftime("%m%d")
    random_suffix = random_name(4)
    base, ext = os.path.splitext(original_name)
    return f"Z25_{date_str}_{category_hint}_{random_suffix}{ext}"

def create_decoy_structure(base_dir, min_items=20, max_items=50):
    import random
    print(f"[INFO] Creating decoy structure in base directory: {base_dir}")
    os.makedirs(base_dir, exist_ok=True)
    total_items = random.randint(min_items, max_items)
    print(f"[INFO] Total decoy items to create: {total_items}")
    final_folder = base_dir

    for _ in range(total_items):
        if random.random() < 0.6:
            folder_name = random_name()
            final_folder = os.path.join(final_folder, folder_name)
            os.makedirs(final_folder, exist_ok=True)
            print(f"[FOLDER] Created folder: {final_folder}")
        else:
            file_name = random_name() + ".log"
            file_path = os.path.join(final_folder, file_name)
            with open(file_path, 'w') as f:
                f.write("System log placeholder\n")
            print(f"[FILE] Created decoy file: {file_path}")

    print(f"[INFO] Final folder for file burial: {final_folder}")
    return final_folder

def move_and_rename_file(file_path, decoy_folder, category_hint):
    print(f"[INFO] Preparing to move and rename file: {file_path}")
    if not os.path.isfile(file_path):
        print("❌ ERROR: File not found.")
        return

    original_name = os.path.basename(file_path)
    new_name = generate_encoded_filename(original_name, category_hint)
    destination = os.path.join(decoy_folder, new_name)
    shutil.move(file_path, destination)
    print(f"✅ SUCCESS: File moved to {destination}")

    key = load_or_create_key()
    log_entry = f"{original_name} -> {new_name} @ {destination}"
    encrypt_log_entry(log_entry, key)
    print(f"[LOG] Mapping stored securely in encrypted log.")

def main():
    parser = argparse.ArgumentParser(description="Hide and rename a file in a randomized decoy folder structure with encrypted logging.")
    parser.add_argument("file", help="Path to the file you want to hide")
    parser.add_argument("--base", default="C:\\ProgramData\\SystemCache", help="Base directory for decoy folders")
    parser.add_argument("--min", type=int, default=20, help="Minimum number of decoy items")
    parser.add_argument("--max", type=int, default=50, help="Maximum number of decoy items")
    parser.add_argument("--hint", default="GEN", help="Category hint for filename (e.g., DOC, IMG, FIN)")
    args = parser.parse_args()

    print("[START] Decoy file burial operation initiated.")
    print(f"[CONFIG] File to hide: {args.file}")
    print(f"[CONFIG] Base directory: {args.base}")
    print(f"[CONFIG] Decoy range: {args.min}–{args.max}")
    print(f"[CONFIG] Category hint: {args.hint}")

    decoy_folder = create_decoy_structure(args.base, args.min, args.max)
    move_and_rename_file(args.file, decoy_folder, args.hint)
    print("[COMPLETE] Operation finished.")

if __name__ == "__main__":
    main()
