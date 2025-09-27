import io

from git_haiku.cli import _display_latest_poem, _display_random_poem
from git_haiku.storage import PoetryStorage


def _sample_entries() -> tuple[str, str]:
    first = """[2024-05-01 12:00] chore: hydrate branches
Repository rain
Leaves in the staging forest

 /\\_/\\
( o.o )
 > ^ <"""

    second = '''[2024-05-01 12:05] feat: blossom refs
Petals of commit
Merge winds hum through the history

  |\\_/|
 (=^.^=)
  (")_(")'''

    return first, second


class _FirstEntryChooser:
    def choice(self, sequence):
        return sequence[0]


def test_random_and_show_commands_preserve_ascii_art(tmp_path):
    storage = PoetryStorage(tmp_path / "haiku.log")
    first, second = _sample_entries()
    storage.append_entry(first)
    storage.append_entry(second)

    latest_stream = io.StringIO()
    _display_latest_poem(storage, stream=latest_stream)
    latest_output = latest_stream.getvalue().rstrip("\n")
    assert latest_output == second
    assert '  |\\_/|\n (=^.^=)\n  (")_(")' in latest_output

    random_stream = io.StringIO()
    _display_random_poem(storage, stream=random_stream, rng=_FirstEntryChooser())
    random_output = random_stream.getvalue().rstrip("\n")
    assert random_output == first
    assert " /\\_/\\\n( o.o )\n > ^ <" in random_output
