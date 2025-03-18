import shutil
import sys
from collections.abc import Sequence
from pathlib import Path


def _copy_files(src_dir: Path, dest_dir: Path, files: Sequence[str]) -> Sequence[Path]:
    file_paths: list[Path] = []

    for file in files:
        src_path = src_dir / file
        dest_path = dest_dir / file

        max_version = (3, 12)
        min_version = (3, 6)
        if sys.version_info > max_version:
            current_version = max_version
        elif sys.version_info < min_version:
            current_version = min_version
        else:
            current_version = (sys.version_info.major, sys.version_info.minor)

        for minor in range(current_version[1], min_version[1] - 1, -1):
            version_path = src_dir / f"Python{current_version[0]}{minor}" / file
            if version_path.exists():
                src_path = version_path
                break

        shutil.copyfile(src_path, dest_path)
        file_paths.append(dest_path)

    return file_paths
