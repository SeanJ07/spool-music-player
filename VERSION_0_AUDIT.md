# Version 0 Audit

Audit date: 2026-05-28

## Scope

Repository-wide structural and documentation audit focused on preservation and non-destructive organization.

## Inventory Summary

### Source and prototypes discovered

- Python prototype scripts (scanner/launcher)
- Web prototypes (combined and standalone UI experiments)
- multiple historical planning/vision documents
- root-level docs with mixed status and overlapping intent

### Generated artifacts

- no committed build outputs or generated binaries found in root

### Config and housekeeping

- `.gitignore` present and already excludes common media file types

## Key Findings

1. Prototype and planning files were mixed at repository root, making status unclear.
2. Historical planning documents contained useful context but were not clearly marked non-canonical.
3. Existing roadmap/readme language implied implementation-first flow, conflicting with Version 0 guardrails.
4. Web prototype files overlap in purpose and should be preserved as references, not treated as production baseline.

## Actions Taken in This Audit Cycle

- established Version 0 directory scaffold
- moved Python and web experimental implementations into `prototypes/`
- moved historical planning docs into `archive/docs/`
- updated canonical project docs for Version 0 scope clarity
- added sample media placement guidance without introducing media files

## Files Requiring Future Human Review

- `prototypes/web/spool.html`
- `prototypes/web/record-player.html`
- `prototypes/web/coverflow.html`
- `prototypes/python/ipod_scanner.py`
- `prototypes/python/spool_launcher.py`
- all docs in `archive/docs/` for future extraction of durable ideas

## Open Review Questions

- Which prototype behaviors are worth carrying into Version 1 UX requirements?
- Should any prototype script be promoted into `tools/` as-is (with explicit prototype tags), or remain archived until rewrite?
- What minimum architecture decision record format should be adopted before Version 1 starts?

## Version 0 Completion Gate (Proposed)

Before entering Version 1 planning:

- confirm directory ownership/responsibility for each top-level folder
- confirm documentation baseline is accepted by maintainers
- decide prototype retention policy and review cadence
