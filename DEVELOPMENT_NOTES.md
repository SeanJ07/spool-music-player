# Development Notes

## Version 0 Working Rules

- prioritize repository organization and documentation over feature builds
- preserve prior work whenever possible
- move uncertain material into `archive/` or `prototypes/` rather than deleting
- document all file moves and major edits in `CHANGELOG.md` and audit docs

## Folder Intent (Short Reference)

- `src/`: future production app code
- `docs/`: additional structured documentation
- `assets/`: shared images, design references, media assets (non-user library)
- `tests/`: future automated/manual test code and plans
- `tools/`: helper scripts for repository maintenance and workflows
- `prototypes/`: experiments and partial implementations
- `archive/`: historical docs/artifacts not currently canonical
- `legacy/`: reserved for old systems/code that require migration
- `samples/`: sample data policy and placeholders
- `config/`: config templates and environment conventions

## Prototype Preservation Policy

- treat files in `prototypes/` as reference implementations
- avoid silent rewrites of prototype behavior
- if prototype changes are needed, annotate intent in changelog and docs

## Documentation Priority Order

1. `README.md`
2. `PROJECT_VISION.md`
3. `ROADMAP.md`
4. `VERSION_0_AUDIT.md`
5. `ARCHIVE_MANIFEST.md`
6. `CHANGELOG.md`

## Collaboration Guidance

- prefer explicit rationale over implicit assumptions
- keep architecture decisions simple and reversible
- when uncertain, preserve and label instead of deleting
- keep status and ownership visible in docs so onboarding does not rely on chat history

## Version 1 Checkpoint 1 - Local Run Instructions

These steps install only the minimal prototype dependencies from `pyproject.toml`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
# If editable install is not supported in your pip version, use:
# pip install .
python -m spool.main
```

Expected output during Checkpoint 1:

- `[Spool] Checkpoint 1 scaffold is installed.`
- `[Spool] UI startup is planned for Checkpoint 2.`

## Version 1 Checkpoint 2 - Metadata/Import Terminal Test

Checkpoint 2 verifies one thing only:

- local MP3 paths can be parsed into clean in-memory `Track` objects

What Checkpoint 2 does not do:

- no PySide6 UI shell yet
- no file picker yet
- no playback yet
- no copying/moving music files

### Where to put local sample MP3 files

Place local-only files in:

- `samples/media/mp3/`

These are test files only and must not be committed.

### macOS/Linux commands

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .

python tools/dev_scan_mp3.py samples/media/mp3/song1.mp3
python tools/dev_scan_mp3.py samples/media/mp3/song1.mp3 samples/media/mp3/song2.mp3 samples/media/mp3/song3.mp3
```

### Windows PowerShell commands

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
# If editable install is not supported in your pip version, use:
# pip install .

python tools/dev_scan_mp3.py samples/media/mp3/song1.mp3
python tools/dev_scan_mp3.py samples/media/mp3/song1.mp3 samples/media/mp3/song2.mp3 samples/media/mp3/song3.mp3
```

### Successful output should include

- `[Spool][Scan] Imported N track(s):`
- one block per track with `title`, `artist`, `album`, `duration`, and `path`
- fallback values like `Unknown Artist`, `Unknown Album`, or filename-as-title when tags are missing

### Common failure cases

- path does not exist
- path is not a file
- file is not `.mp3` (skipped in Version 1)
- MP3 exists but metadata parsing fails (reported as an error, no crash)
