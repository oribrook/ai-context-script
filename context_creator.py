#!/usr/bin/env python3
"""
File Tree Concatenator

A utility to concatenate all text files from a directory tree into a single output file.
Useful for creating context files for LLMs, code reviews, or documentation.

Repository: https://github.com/yourusername/file-tree-concatenator
License: MIT
"""

import os
from typing import List, Optional


def concatenate_directory_tree(
    root_directory: str = ".",
    output_path: str = "concatenated_output.txt",
    excluded_extensions: Optional[List[str]] = None,
    excluded_directories: Optional[List[str]] = None,
    included_directories: Optional[List[str]] = None,
    included_files: Optional[List[str]] = None,
    excluded_file_patterns: Optional[List[str]] = None,
) -> None:
    """
    Recursively concatenate all matching files from a directory tree into a single text file.
    
    Args:
        root_directory: Base directory to scan (default: current directory)
        output_path: Path for the output file (default: "concatenated_output.txt")
        excluded_extensions: File extensions to skip (without dot)
        excluded_directories: Directory names to skip entirely
        included_directories: If specified, only process directories containing these substrings
        included_files: If specified, only process files containing these substrings
        excluded_file_patterns: File name patterns to exclude
    
    Example:
        concatenate_directory_tree(
            root_directory="/path/to/project",
            output_path="project_source.txt",
            excluded_extensions=["pyc", "log", "tmp"],
            excluded_directories=["__pycache__", ".git", "node_modules"],
            included_directories=["src", "lib"],
            included_files=["test_", "main"],
            excluded_file_patterns=["deprecated", "backup"]
        )
    """
    # Initialize default values
    excluded_extensions = excluded_extensions or []
    excluded_directories = excluded_directories or []
    included_directories = included_directories or []
    included_files = included_files or []
    excluded_file_patterns = excluded_file_patterns or []
    
    files_processed = 0
    files_skipped = 0
    
    with open(output_path, "w", encoding="utf-8") as output:
        for current_dir, subdirs, files in os.walk(root_directory):
            # Remove excluded directories from traversal
            subdirs[:] = [d for d in subdirs if d not in excluded_directories]
            
            # Skip if directory doesn't match inclusion criteria
            if included_directories:
                dir_name = os.path.basename(current_dir)
                if not any(pattern in dir_name for pattern in included_directories):
                    continue
            
            for filename in files:
                # Check extension exclusion
                if any(filename.endswith(f".{ext}") for ext in excluded_extensions):
                    files_skipped += 1
                    continue
                
                # Check file pattern exclusion
                if any(pattern in filename for pattern in excluded_file_patterns):
                    files_skipped += 1
                    continue
                
                # Check file inclusion criteria
                if included_files:
                    if not any(pattern in filename for pattern in included_files):
                        files_skipped += 1
                        continue
                
                file_path = os.path.join(current_dir, filename)
                relative_path = os.path.relpath(file_path, root_directory)
                
                print(f"Processing: {relative_path}")
                
                # Write file separator and path
                output.write(f"{'=' * 60}\n")
                output.write(f"File: {relative_path}\n")
                output.write(f"{'=' * 60}\n")
                
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as input_file:
                        output.write(input_file.read())
                    files_processed += 1
                except Exception as error:
                    output.write(f"[ERROR: Could not read file - {error}]\n")
                    files_skipped += 1
                
                output.write("\n\n")
    
    print(f"\nComplete! Processed {files_processed} files, skipped {files_skipped}")
    print(f"Output saved to: {output_path}")


# Usage Examples:
# ----------------

# Example 1: Process a Python project
# concatenate_directory_tree(
#     root_directory="/home/user/my_python_project",
#     output_path="python_project_source.txt",
#     excluded_extensions=["pyc", "pyo", "pyd", "so", "egg-info"],
#     excluded_directories=["__pycache__", ".git", "venv", ".pytest_cache"],
#     included_files=[".py"]
# )

# Example 2: Process a web project
# concatenate_directory_tree(
#     root_directory="/home/user/my_web_app",
#     output_path="web_app_source.txt",
#     excluded_extensions=["jpg", "png", "gif", "ico", "woff", "woff2", "ttf"],
#     excluded_directories=["node_modules", "dist", "build", ".git"],
#     included_directories=["src", "components", "pages"],
# )

# Example 3: Process only test files
# concatenate_directory_tree(
#     root_directory="/home/user/project",
#     output_path="test_files.txt",
#     included_files=["test_", "_test.py", "spec.js"],
#     excluded_directories=["node_modules", ".git"]
# )


if __name__ == "__main__":
    # Default execution with common development exclusions
    concatenate_directory_tree(
        root_directory=r".",
        output_path="concatenated_output.txt",
        excluded_extensions=[
            "pyc", "pyo", "pyd", "so",  # Python compiled
            "class", "jar",              # Java compiled
            "exe", "dll", "obj",         # Binary files
            "log", "tmp", "cache",       # Temporary files
            "jpg", "jpeg", "png", "gif", "svg", "ico",  # Images
            "woff", "woff2", "ttf", "eot",  # Fonts
            "mp3", "mp4", "avi", "mov",  # Media
            "zip", "tar", "gz", "rar",   # Archives
            "pdf", "doc", "docx",         # Documents
        ],
        excluded_directories=[
            "__pycache__", ".git", ".svn", ".hg",  # Version control
            "node_modules", "venv", "env", ".env",  # Dependencies
            "dist", "build", "target",              # Build outputs
            ".idea", ".vscode", ".vs",              # IDE folders
            "migrations", "static", "media",        # Django specific
        ],
        excluded_file_patterns=["requirements", ".min.js", ".min.css"]
    )
