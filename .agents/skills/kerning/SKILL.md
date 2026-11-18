# /kerning

Review or edit Blocksync kerning in UFO sources.

## Usage

`/kerning [audit|proof|edit]`

Default: `audit`

## Audit

1. Parse `sources/Blocksync.designspace` to list active UFO masters.
2. For each UFO, check for `groups.plist` and `kerning.plist`.
3. Report:
   - whether kerning is present;
   - pair count;
   - group count;
   - masters missing kerning that related masters have.
4. If kerning is absent or intentionally deferred, record that in
   `GF_READINESS.md` or the relevant package checklist before claiming release
   readiness.

## Proof

Run:

```bash
make proof
```

Review `out/proof/index.html` and the generated diffenator2 pages for spacing,
pair behavior, interpolation, and width-axis changes.

## Edit

When adding or changing kerning:

- prefer UFO group kerning when classes are stable;
- keep group names and membership aligned across active masters;
- use integer kerning values;
- rerun `make proof` and `make test`;
- record whether the generated variable font contains expected GPOS `kern`
  data.
