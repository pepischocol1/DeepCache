# DeepCache

DeepCache is a Python utility for stealthily hiding files inside randomized, deep folder structures with optional renaming and encrypted logging. It also includes a retrieval tool to locate and restore hidden files.

## ✨ Features
- Creates randomized decoy folder structures (20–50 items deep)
- Renames files using a personal encoding scheme: Z25_MMDD_HINT_RANDOM.ext
- Stores original → renamed mapping in an **encrypted log**
- Retrieval script to search and restore files
- Verbose output for full transparency of operations

## 📦 Requirements
- Python 3.8+
- `cryptography` library

## Install dependencies:
pip install -r requirements.txt

## 🚀 Usage

## Hide a File
python src/bury.py "path/to/file.txt" --base "C:\\ProgramData\\SystemCache" --min 20 --max 50 --hint DOC

## Retrieve a File
python src/retrieve.py --search "file.txt"

## Restore the first match:
python src/retrieve.py --search "file.txt" --restore