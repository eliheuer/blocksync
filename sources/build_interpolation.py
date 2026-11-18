"""Build Blocksync with compiler-only Bold and Black masters at normal width.

The seven editable sources define the width endpoints. At the default width,
varLib also needs explicit weight deltas, or its center line stays Regular.
"""
from pathlib import Path
import plistlib
import subprocess
import sys
import tempfile

from fontTools.designspaceLib import (
    AxisDescriptor, DesignSpaceDocument, InstanceDescriptor, SourceDescriptor,
)
from ufo2ft.instantiator import Instantiator
import yaml


def add_width_midpoint(design, style, folder):
    widths = DesignSpaceDocument()
    axis = design.getAxis("Width")
    widths.addAxis(AxisDescriptor(name=axis.name, tag=axis.tag, minimum=axis.minimum,
                                  default=axis.minimum, maximum=axis.maximum))
    masters = {source.styleName: source for source in design.sources}
    for side in ("Condensed", "Expanded"):
        source = masters[f"{side} {style}"]
        widths.addSource(SourceDescriptor(path=source.path, name=side,
                                          designLocation={"Width": source.location["Width"]}))
    instance = InstanceDescriptor(familyName="Blocksync", styleName=style,
                                  designLocation={"Width": axis.default})
    font = Instantiator.from_designspace(widths, round_geometry=False).generate_instance(instance)
    default = Path(design.findDefault().path)
    with (default / "lib.plist").open("rb") as stream:
        font.lib["public.glyphOrder"] = plistlib.load(stream)["public.glyphOrder"]
    path = folder / f"Blocksync-{style}.ufo"
    font.save(path)
    # Inherit the default's complete family metadata, as for the editable
    # normal-width Regular. Geometry, anchors and kerning are interpolated.
    with (default / "fontinfo.plist").open("rb") as stream:
        info = plistlib.load(stream)
    info["styleName"] = style
    with (path / "fontinfo.plist").open("wb") as stream:
        plistlib.dump(info, stream)
    weight = masters[f"Condensed {style}"].location["Weight"]
    design.addSource(SourceDescriptor(path=str(path), familyName="Blocksync", styleName=style,
                                      name=f"Blocksync {style}",
                                      designLocation={"Width": axis.default, "Weight": weight}))


def main():
    source_dir = Path(__file__).resolve().parent
    config = yaml.safe_load((source_dir / "config.yaml").read_text())
    config.pop("recipe")  # The inner build uses the standard Google Fonts recipe.
    config["outputDir"] = str((source_dir / config["outputDir"]).resolve())
    designspace, = config["sources"]
    with tempfile.TemporaryDirectory(prefix="blocksync-interpolation-") as temporary:
        folder = Path(temporary).resolve()
        design = DesignSpaceDocument.fromfile(source_dir / designspace)
        for source in design.sources:
            local_master = folder / source.filename
            local_master.symlink_to(source.path, target_is_directory=True)
            source.path = str(local_master)
        for style in ("Bold", "Black"):
            add_width_midpoint(design, style, folder)
        design.write(folder / designspace)
        recipe = folder / "config.yaml"
        recipe.write_text(yaml.safe_dump(config, sort_keys=False))
        subprocess.run([sys.executable, "-m", "gftools.builder", str(recipe)], check=True)


if __name__ == "__main__":
    main()
