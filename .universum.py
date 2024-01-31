#!/usr/bin/env python3
from universum.configuration_support import Configuration, Step
from pathlib import Path
import subprocess


def create_directories_for_output_files(files: list, root_dir: str):
    """
    Create directories for output files.
    There is temporary solution to avoid errors when using universum.analyzers.clang_format
    """
    for file in files:
        Path(root_dir, file).parent.mkdir(parents=True, exist_ok=True)


def get_changed_cpp_c_files():
    # Find the merge-base with master
    merge_base_cmd = "git merge-base HEAD origin/main"
    merge_base_result = subprocess.run(
        merge_base_cmd.split(), capture_output=True, text=True
    )

    if merge_base_result.returncode != 0:
        print("Error in finding merge base")
        return []

    merge_base = merge_base_result.stdout.strip()

    # Get changed files (excluding deleted ones) from the merge base to HEAD
    diff_cmd = f"git diff --diff-filter=d --name-only {merge_base} HEAD"
    diff_result = subprocess.run(diff_cmd.split(), capture_output=True, text=True)

    if diff_result.returncode != 0:
        print("Error in running git diff")
        return []

    # Filter out .cpp and .c files
    files = [
        file for file in diff_result.stdout.split("\n") if file.endswith((".cpp", ".c"))
    ]
    return files


# Get the list of changed .cpp and .c files
changed_cpp_c_files = get_changed_cpp_c_files()
print("\nChanged CPP and C files", changed_cpp_c_files, "\n")
create_directories_for_output_files(changed_cpp_c_files, root_dir=Path("clang_report"))

configs = Configuration(
    [
        Step(
            name="clang-format",
            code_report=True,
            command=[
                "python3",
                "-m",
                "universum.analyzers.clang_format",
                "--executable",
                "clang-format",
                "--files",
                *changed_cpp_c_files,
                "--result-file",
                "${CODE_REPORT_FILE}",
                "--output-directory",
                "clang_report",
            ],
        )
    ]
)

if __name__ == "__main__":
    print(configs.dump())
