"""Verify a named glyph batch against its Git checkpoint, including component donors."""
import argparse
from pathlib import Path
import subprocess
import tempfile

from fgtools import project, source_inventory
from fgtools.diff import sources_at


def files(command, *args):
    output = subprocess.check_output(["git", command, "-z", *args])
    return set(output.decode().split("\0")) - {""}


def records(root, master, design):
    glyphs = source_inventory.load_master(root, master, design)
    donors = {part["base"] for glyph in glyphs.values() for part in glyph["components"]}
    return glyphs, donors


def topology(glyph):
    return glyph["point_types"], [part["base"] for part in glyph["components"]]


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
    removed = sorted(path for path in changed if not (source.root / path).is_file())
    if removed:
        print("A draft cannot delete or rename a source file:", ", ".join(removed))
        return True
    errors = []
    rebuilt = set()
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
                if topology(old[name]) != topology(now[name]):
                    rebuilt.add(name)
                if old[name]["color"]["protected"] or name in old_donors | new_donors:
                    errors.append(f"{master} {name}: protected green glyph or component donor")
                if now[name]["color"]["name"] != "purple":
                    errors.append(f"{master} {name}: draft must be purple")
                for key in ("advance", "anchors", "unicodes"):
                    if old[name][key] != now[name][key]:
                        errors.append(f"{master} {name}: changed {key} outside a drawing assignment")
    if rebuilt:
        structures = {name: [] for name in rebuilt}
        for master in source.masters:
            data = source_inventory.load_master(source.root, master, design)
            for name in rebuilt:
                structures[name].append(topology(data[name]) if name in data else None)
        for name, shapes in structures.items():
            if any(shape != shapes[0] for shape in shapes):
                errors.append(f"{name}: edited topology differs across masters")
    errors.extend(f"Outside assignment: {path}" for path in sorted(changed))
    for error in errors:
        print(error)
    if not errors:
        print("Assignment scope, protected colors, donors and metrics pass.")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
