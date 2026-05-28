# Contributing

## Current Project Mode

The repository is currently in Version 0.1 (documentation and onboarding hardening).

### Version 0 / 0.1

Allowed focus:

- repository organization
- preservation of historical work
- documentation clarity
- onboarding and handoff readiness

Not allowed in this phase:

- implementing production app features
- rewriting prototype systems as active app source
- introducing major infrastructure without documented need

### Version 1 (Later)

Version 1 will begin controlled feature work after Version 0 readiness is accepted.

## Collaboration Rules

- preserve first, delete only when explicitly justified
- move uncertain artifacts into `archive/`, `prototypes/`, or `legacy/` as appropriate
- keep `legacy/` for old systems/code that may require migration later
- keep experiments in `prototypes/` or `tools/` before promoting into active `src/`
- document every meaningful move or scope change in `CHANGELOG.md`
- update canonical docs when project direction changes

## Documentation and Traceability

When making changes:

1. update relevant canonical docs (`README.md`, `ROADMAP.md`, decision log)
2. add/adjust entries in `CHANGELOG.md`
3. if moving historical materials, update `ARCHIVE_MANIFEST.md`
4. keep rationale explicit so context survives beyond chat history

## Promotion Path for Experimental Work

- Stage 1: experiment in `prototypes/` or helper in `tools/`
- Stage 2: review for usefulness, maintenance cost, and fit with roadmap
- Stage 3: promote selected patterns into `src/` with explicit documentation

## Commit Hygiene (Recommended)

- use small, reviewable commits
- prefer descriptive commit messages focused on why
- avoid bundling unrelated structural and behavioral changes together
