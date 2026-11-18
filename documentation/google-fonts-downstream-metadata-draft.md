# Google Fonts Downstream Metadata Draft

This is the current downstream `METADATA.pb` preview for review. Replace the
pending date and commit before applying it in a local `google/fonts` checkout.

```textproto
name: "Blocksync"
designer: "Eli Heuer"
license: "OFL"
category: "DISPLAY"
date_added: "PENDING-YYYY-MM-DD"
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
  commit: "PENDING_FINAL_40_CHARACTER_COMMIT"
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

## Open Values

- `date_added`: final Google Fonts date.
- `source.commit`: final source commit hash after the release tree is reviewed.
- `source.branch`: confirm the public default branch name before applying.
- `source.files`: decide whether the first PR ships generated variable TTFs
  from a release/archive or uses the reproducible `sources/config.yaml` build
  path. Keep `config_yaml` because this repo is being prepared around
  designspace/UFO sources.
- `subsets`: current draft includes `latin-ext` and `vietnamese` because the
  font already encodes many Latin Extended and Vietnamese-related codepoints.
  Package-context probing now shows both declared broad subsets clear the local
  Google Fonts support thresholds.
