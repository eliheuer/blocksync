# Blocksync

[![][Fontspector]](https://eliheuer.github.io/blocksync/fontspector/fontspector-report.html)
[![][Universal]](https://eliheuer.github.io/blocksync/fontspector/fontspector-report.html)
[![][Font File Checks]](https://eliheuer.github.io/blocksync/fontspector/fontspector-report.html)
[![][Outline Checks]](https://eliheuer.github.io/blocksync/fontspector/fontspector-report.html)
[![][Shaping]](https://eliheuer.github.io/blocksync/fontspector/fontspector-report.html)

[Fontspector]: https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Feliheuer%2Fblocksync%2Fgh-pages%2Fbadges%2Foverall.json
[Font File Checks]: https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Feliheuer%2Fblocksync%2Fgh-pages%2Fbadges%2FFontFileChecks.json
[Outline Checks]: https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Feliheuer%2Fblocksync%2Fgh-pages%2Fbadges%2FOutlineChecks.json
[Shaping]: https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Feliheuer%2Fblocksync%2Fgh-pages%2Fbadges%2FShapingChecks.json
[Universal]: https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Feliheuer%2Fblocksync%2Fgh-pages%2Fbadges%2FUniversalProfileChecks.json

![Sample Image](documentation/archive/drawbot/image-005.png)

## About

A block-like variable font designed and engineered by Eli Heuer. In-development, not ready for use.

## Building

Install Python 3.13, Rust/Cargo and the system fontconfig headers (Linux). From the repository root run:

```sh
make setup
make build
make test
make proof
```

The pinned Font.Garden tools build the variable font and 18 static proofs from the existing designspace. Blocksync uses the fontmake compiler with its original metadata step. The default fontc recipe produces only the variable font for this config. The family design and its inherited QA findings are in [CONTEXT.md](CONTEXT.md).

Open the [print proof](https://eliheuer.github.io/blocksync/proof/proof.pdf) or the [two-axis specimen](https://eliheuer.github.io/blocksync/proof/widths.html). The [design review](https://eliheuer.github.io/blocksync/proof/design.html) shows the spacing, weight and character-shape issues holding the Google Fonts submission. Local copies are in `output/proof/`. CI updates the existing GitHub Pages branch after the checks pass on main. Release events attach the built fonts and reports to the tagged release.

Use `make runebender` to open the designspace in the native Runebender checkout at `~/GH/repos/runebender`. Set `RUNEBENDER_REPO` for another checkout location. Use `make queue` for draft candidates and `make status` for the source grade inventory. The [agent workflow](AGENTS.md) covers assignments, protected donors and independent review. The [Font.Garden guide](https://font.garden/docs/start/) describes the shared workflow.

## Google Fonts Release Work

The active release source path is designspace/UFO:

* `sources/config.yaml`
* `sources/Blocksync.designspace`
* active UFOs listed in `sources/README.md`

Historical `.glyphs` files live in `sources/archive/` and are not active build
inputs. Agent-oriented release notes and reusable Google Fonts workflow guidance
live in `AGENTS.md`, `GF_READINESS.md`, and `.agents/`.

Start future low-token Google Fonts release passes with:

* `.agents/README.md`
* `.agents/google-fonts-onboarding-checklists.md`
* `.agents/google-fonts-official-reference-map.md`

## Changelog

**26 September 2022. Version 0.1**
- Hello World

## License

This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: https://openfontlicense.org

## Repository Layout

This font repository structure is inspired by [Unified Font Repository v0.3](https://github.com/unified-font-repository/Unified-Font-Repository), modified for the [Google Fonts workflow](https://github.com/googlefonts/googlefonts-project-template).
