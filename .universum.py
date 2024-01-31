#!/usr/bin/env python3
from universum.configuration_support import Configuration, Step
from pathlib import Path
import os
import shutil


def create_directories_for_output_files(files: list, root_dir: str, clear = True):
    """
    Create directories for output files.
    There is temporary solution to avoid errors when using universum.analyzers.clang_format
    """
    # Remove root dir if exists
    if clear:
        shutil.rmtree(root_dir, ignore_errors=True)

    for file in files:
        Path(root_dir, file).parent.mkdir(parents=True, exist_ok=True)

def get_all_files_in_dir(path: str, extensions: list):
    """
    Returns a list of all files in the given directory and its subdirectories
    that match the specified extensions.
    """
    return [file for ext in extensions for file in Path(path).rglob(f"*.{ext}")]


# print $PROJECT_ROOT env


found_files = get_all_files_in_dir(".", ["cpp", "c"])


if found_files:
    root_dir = ""
    # temp solution
    root_dir += "tmp" + "/clang_report"

    # if "PROJECT_ROOT" not in os.environ:
    #     root_dir = "clang_report"
    # else:
    #     root_dir = os.environ["PROJECT_ROOT"] + "/clang_report"
    create_directories_for_output_files(found_files, root_dir=root_dir)
    os.environ["ENABLE_CLANG_FORMAT"] = "1"

configs = Configuration(
    [
        Step(name="Print Hello world", command=["echo", "Hello world"]),
        Step(
            name="clang-format",
            code_report=True,
            if_env_set="ENABLE_CLANG_FORMAT == 1",
            command=[
                "python3",
                "-m",
                "universum.analyzers.clang_format",
                "--executable",
                "clang-format",
                "--files",
                *[str(file) for file in found_files],
                "--result-file",
                "${CODE_REPORT_FILE}",
                "--output-directory",
                "clang_report",
            ],
        ),
    ]
)


if __name__ == "__main__":
    print(configs.dump())
