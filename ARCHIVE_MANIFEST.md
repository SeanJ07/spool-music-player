# Archive Manifest

This manifest records historical files moved out of active root usage during Version 0 cleanup.

## Purpose

- preserve historical context
- keep active root documentation focused
- provide traceable old-to-new path mapping

## Historical Planning Docs Moved to `archive/docs/`

| Original Path | Current Path | Reason |
|------|------|------|
| `AI-DJ.md` | `archive/docs/AI-DJ.md` | Historical concept/design exploration; not canonical Version 0 direction |
| `PROPOSAL.md` | `archive/docs/PROPOSAL.md` | Earlier proposal artifact preserved for reference |
| `SPOOL-HARDWARE.md` | `archive/docs/SPOOL-HARDWARE.md` | Future hardware planning, out of current Version 0 scope |
| `sprint-2-plan.md` | `archive/docs/sprint-2-plan.md` | Legacy sprint record from prototype phase |

## Prototype Code and UI Moved to `prototypes/`

| Original Path | Current Path | Reason |
|------|------|------|
| `ipod_scanner.py` | `prototypes/python/ipod_scanner.py` | Experimental script, preserved as reference implementation |
| `spool_launcher.py` | `prototypes/python/spool_launcher.py` | Experimental launcher logic, preserved without rewrite |
| `spool.html` | `prototypes/web/spool.html` | Composite web prototype, not production application structure |
| `record-player.html` | `prototypes/web/record-player.html` | Standalone visual experiment preserved for UX reference |
| `coverflow.html` | `prototypes/web/coverflow.html` | Standalone Cover Flow experiment preserved for UX reference |

## Notes

- No archive content was deleted during this reorganization pass.
- `legacy/` remains intentionally empty and reserved for old code/systems requiring migration work later.

## Canonical Doc Rewrite Recoverability

`README.md` and `ROADMAP.md` were rewritten for Version 0 clarity. Earlier versions remain recoverable from Git history.

- Example history check command: `git log --oneline -- README.md ROADMAP.md`
- Recovery option: `git show <commit>:README.md` or `git show <commit>:ROADMAP.md`

Current observed commit references containing prior content:

- `7df9bc0` - Add README with features and usage
- `771d9c8` - Initial commit: Spool iPod-inspired music player
