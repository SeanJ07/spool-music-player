# Architecture Decisions

This file records durable project decisions and boundaries.

## ADR-0001 - Primary Desktop Platforms

- Date: 2026-05-28
- Decision: Prioritize Windows and macOS first.
- Rationale: Matches near-term user goals and keeps early scope manageable.

## ADR-0002 - Main Prototype Language Direction

- Date: 2026-05-28
- Decision: Use Python as the primary prototype direction.
- Rationale: Fast iteration for early desktop prototype development.

## ADR-0003 - GUI Framework Direction

- Date: 2026-05-28
- Decision: PySide6 (Qt for Python) is the likely GUI path for Version 1.
- Rationale: Cross-platform desktop fit with mature UI toolkit capabilities.

## ADR-0004 - C++ Scope Boundary

- Date: 2026-05-28
- Decision: Reserve C++ for possible future lower-level/device components.
- Rationale: Avoid premature complexity while preserving a path for performance/device work later.

## ADR-0005 - Feature Prioritization Order

- Date: 2026-05-28
- Decision: Build local MP3/local-first prototype capabilities before Apple Music or XML integration.
- Rationale: Local-first is lower-risk, testable offline, and aligned with immediate Version 1 goals.

## ADR-0006 - Version 0 Constraints

- Date: 2026-05-28
- Decision: Version 0 is organization/documentation/preservation only.
- Rationale: Establish a clean foundation before application implementation begins.
