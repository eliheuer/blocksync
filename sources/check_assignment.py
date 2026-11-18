"""Verify a named glyph batch against its Git checkpoint, including component donors."""
import argparse
from pathlib import Path
import subprocess
import tempfile

from fgtools import project, source_inventory
from fgtools.diff import sources_at


def files(*args):
    output = subprocess.check_output(["git", *args, "-z"])
    return set(output.decode().split("\0")) - {""}


def records(root, master, design):
    glyphs = source_inventory.load_master(root, master, design)
    donors = {part["base"] for glyph in glyphs.values() for part in glyph["components"]}
    return glyphs, donors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True)
    parser.add_argument("--glyphs", required=True, help="space-separated existing glyph names")
    parser.add_argument("--masters", required=True, help="comma-separated designspace style names")
    args = parser.parse_args()
    source = project.load()
    glyphs = set(args.glyphs.split())
    masters = {m.strip() for m in args.masters.split(",") if m.strip()}
    if not glyphs or not masters or masters - set(source.masters):
        parser.error("Set GLYPHS and MASTERS (comma-separated exact master names).")
    changed = files("diff", "--no-renames", "--name-only", args.base, "--")
    changed |= files("ls-files", "--others", "--exclude-standard")
    errors = []
    with tempfile.TemporaryDirectory() as directory:
        base = Path(directory)
        sources_at(args.base, source.root, base)
        design = source.design()
        for master in sorted(masters):
            old, old_donors = records(base, master, design)
            now, new_donors = records(source.root, master, design)
            for name in sorted(glyphs):
                if name not in old or name not in now:
                    errors.append(f"{master} {name}: batch must name an existing glyph")
                    continue
                path = now[name]["path"]
                if path not in changed:
                    continue
                changed.remove(path)
                if old[name]["color"]["protected"] or name in old_donors | new_donors:
                    errors.append(f"{master} {name}: protected green glyph or component donor")
                if now[name]["color"]["name"] != "purple":
                    errors.append(f"{master} {name}: draft must be purple")
                for key in ("advance", "anchors", "unicodes"):
                    if old[name][key] != now[name][key]:
                        errors.append(f"{master} {name}: changed {key} outside a drawing assignment")
    errors.extend(f"Outside assignment: {path}" for path in sorted(changed))
    for error in errors:
        print(error)
    if not errors:
        print("Assignment scope, protected colors, donors and metrics pass.")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
