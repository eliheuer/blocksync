"""Apply the pinned layout rules to Blocksync, retaining its pre-migration archive."""
from collections import Counter
from io import BytesIO
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile

from fgtools import check_repository as layout

BASELINE = "faff21cc6b30bf80a213fb17f81b4ab92b79bae5"


def findings(root, files):
    rows = layout.layout_problems(root, files)
    rows.extend(layout.reference_problems(root, files))
    rows.extend(layout.contents_problems(root, files))
    # A line moving in an existing document is not a new broken reference.
    return Counter(re.sub(r"(?<=\.md):\d+:", ":", row) for row in rows)


def main():
    root = Path(__file__).resolve().parents[1]
    archive = subprocess.check_output(["git", "archive", "--format=tar", BASELINE], cwd=root)
    with tempfile.TemporaryDirectory() as directory, tarfile.open(fileobj=BytesIO(archive)) as tar:
        prior = Path(directory)
        tar.extractall(prior, filter="data")
        files = [entry.name for entry in tar if entry.isfile() or entry.issym()]
        inherited = findings(prior, files)
    # The migration must satisfy every required template path.
    inherited = Counter({row: n for row, n in inherited.items() if "the layout requires it" not in row})
    # The preflight already required this skill. Its directory was ignored by
    # the old global "proof" pattern, so it first enters Git at migration.
    inherited[".agents/skills/proof/SKILL.md: no allowed place in the layout"] = 1
    current = findings(root, layout.tracked(root))
    new = current - inherited
    for problem in sorted(new.elements()):
        print(problem)
    print(f"Layout: {new.total()} new findings, {(current & inherited).total()} inherited.")
    return bool(new)


if __name__ == "__main__":
    raise SystemExit(main())
