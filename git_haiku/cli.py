"""Command helpers for displaying stored git-haiku poems."""

from __future__ import annotations

import random
import sys
from typing import Optional, Sequence, TextIO

from .storage import PoetryStorage


def _write_entry(entry: str, stream: TextIO) -> None:
    stream.write(entry)
    if not entry.endswith("\n"):
        stream.write("\n")


def _pick_random(entries: Sequence[str], rng: Optional[random.Random]) -> str:
    if rng is None:
        return random.choice(entries)
    return rng.choice(entries)


def _display_random_poem(
    storage: PoetryStorage,
    *,
    stream: Optional[TextIO] = None,
    rng: Optional[random.Random] = None,
) -> Optional[str]:
    """Select a random poem from *storage* and write it to *stream*."""
    entries = storage.read_all()
    if not entries:
        if stream is None:
            stream = sys.stdout
        stream.write("No stored poems.\n")
        return None

    if stream is None:
        stream = sys.stdout

    selection = _pick_random(entries, rng)
    _write_entry(selection, stream)
    return selection


def _display_latest_poem(
    storage: PoetryStorage,
    *,
    stream: Optional[TextIO] = None,
) -> Optional[str]:
    """Write the most recently stored poem to *stream*."""
    latest = storage.read_latest()
    if latest is None:
        if stream is None:
            stream = sys.stdout
        stream.write("No stored poems.\n")
        return None

    if stream is None:
        stream = sys.stdout

    _write_entry(latest, stream)
    return latest


__all__ = ["_display_random_poem", "_display_latest_poem", "PoetryStorage"]
