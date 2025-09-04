# File Tree Concatenator

Concatenate all text/code files in a directory tree into a single file.  
Perfect for LLM context, quick reviews, or project snapshots.

---

## Features
- Recursive directory scan  
- Include/exclude by extension, directory, or filename patterns  
- Clear file separators with relative paths  
- Sensible defaults (skips binaries, caches, assets)  

---

## Quick Start

Run from your project root:

```bash
python3 file_tree_concatenator.py
Output → concatenated_output.txt

Custom Usage

from file_tree_concatenator import concatenate_directory_tree

concatenate_directory_tree(
    root_directory=".",
    output_path="project_source.txt",
    excluded_extensions=["pyc", "log"],
    excluded_directories=[".git", "node_modules"],
    included_files=[".py", ".md"]
)


Example Output

============================================================
File: src/utils/date.ts
============================================================
export function toISO(d: Date): string { ... }
License
MIT © Ori Brook - GPT ;)
