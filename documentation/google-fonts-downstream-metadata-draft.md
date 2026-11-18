# Google Fonts Downstream Metadata Draft

This is the current downstream `METADATA.pb` preview for review. The date and source revision identify the upstream package candidate. Google Fonts may assign a later date during onboarding.

```textproto
name: "Blocksync"
designer: "Eli Heuer"
license: "OFL"
category: "DISPLAY"
date_added: "2026-11-18"
fonts {
  name: "Blocksync"
  style: "normal"
  weight: 400
  filename: "Blocksync[wdth,wght].ttf"
  post_script_name: "Blocksync-Regular"
  full_name: "Blocksync Regular"
  copyright: "Copyright 2023 The Blocksyncer Project Authors (https://github.com/eliheuer/blocksync)"
}
subsets: "latin"
subsets: "latin-ext"
subsets: "menu"
subsets: "vietnamese"
axes {
  tag: "wdth"
  min_value: 75.0
  max_value: 125.0
}
axes {
  tag: "wght"
  min_value: 400.0
  max_value: 900.0
}
source {
  repository_url: "https://github.com/eliheuer/blocksync"
  commit: "46cd53e51744630b4f92e2a2e5957b41e6bd9294"
  config_yaml: "sources/config.yaml"
  files {
    source_file: "OFL.txt"
    dest_file: "OFL.txt"
  }
  files {
    source_file: "fonts/variable/Blocksync[wdth,wght].ttf"
    dest_file: "Blocksync[wdth,wght].ttf"
  }
  files {
    source_file: "documentation/DESCRIPTION.en_us.html"
    dest_file: "DESCRIPTION.en_us.html"
  }
  branch: "main"
}
primary_script: "Latn"
stroke: "SANS_SERIF"
classifications: "DISPLAY"
```

## Package source

Packager builds the version 1.000 variable font from the public main branch with `sources/config.yaml`. The OFL and description travel with the font. Latin Extended and Vietnamese both clear the declared subset coverage thresholds.
