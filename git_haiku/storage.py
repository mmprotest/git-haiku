"""Persistent storage helpers for git-haiku poems."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List
import re

_HEADER_PATTERN = re.compile(r"^\[[^\]]+\]\s")


def _is_header(line: str) -> bool:
    """Return True if *line* looks like an entry header."""
    return bool(_HEADER_PATTERN.match(line))


class PoetryStorage:
    """Manages a flat file that stores commit poetry entries."""

    def __init__(self, storage_path: Path | str) -> None:
        self._path = Path(storage_path)

    @property
    def path(self) -> Path:
        return self._path

    def append_entry(self, entry: str) -> None:
        """Append *entry* to the storage file using a blank line separator."""
        text = entry.rstrip("\n") + "\n\n"
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("a", encoding="utf-8") as handle:
            handle.write(text)

    def read_all(self) -> List[str]:
        """Return a list of full poem entries stored in the file."""
        if not self._path.exists():
            return []

        entries: List[str] = []
        current: list[str] = []
        seen_blank = False

        with self._path.open("r", encoding="utf-8") as handle:
            for raw_line in handle:
                line = raw_line.rstrip("\n")

                if _is_header(line) and (not current or seen_blank):
                    if current:
                        entries.append(_coalesce_entry(current))
                    current = [line]
                    seen_blank = False
                    continue

                if not current:
                    # Ignore any leading whitespace before the first header.
                    continue

                if line.strip() == "":
                    seen_blank = True
                    current.append(line)
                    continue

                seen_blank = False
                current.append(line)

        if current:
            entries.append(_coalesce_entry(current))

        return entries

    def read_latest(self) -> str | None:
        entries = self.read_all()
        return entries[-1] if entries else None


def _coalesce_entry(lines: Iterable[str]) -> str:
    material = list(lines)
    while material and material[-1].strip() == "":
        material.pop()
    return "\n".join(material)
