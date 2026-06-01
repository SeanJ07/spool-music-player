#!/usr/bin/env python3
"""
Spool Music Player — Launcher

Scans ~/Desktop/Spool Music (or any folder), injects all audio files
into the record player HTML, and opens it in your browser.

Usage:
  python3 spool_launcher.py                    # Scans Desktop/Spool Music
  python3 spool_launcher.py /path/to/music     # Scans custom folder

Double-click this file on Windows to launch.
"""

import http.server
import json
import os
import socketserver
import sys
import tempfile
import webbrowser
from pathlib import Path

PORT = 8765
RECORD_PLAYER = Path(__file__).parent / "record-player.html"


def find_spool_folder():
    """Find the Spool Music folder on the desktop."""
    # Windows desktop
    candidates = [
        Path.home() / "Desktop" / "Spool Music",
        Path("/mnt/c/Users/seanj/Desktop/Spool Music"),
        Path("/mnt/c/Users") / os.environ.get("USER", "seanj") / "Desktop" / "Spool Music",
    ]
    # Also check Windows user profile
    try:
        import subprocess
        result = subprocess.run(
            ["powershell.exe", "-Command", "[Environment]::GetFolderPath('Desktop')"],
            capture_output=True, text=True, timeout=5
        )
        win_desktop = Path(result.stdout.strip())
        candidates.insert(0, win_desktop / "Spool Music")
    except Exception:
        pass

    for c in candidates:
        if c.exists() and c.is_dir():
            return c
    return None


def scan_folder(folder_path):
    """Find all audio files in the given folder."""
    folder = Path(folder_path)
    if not folder.exists():
        return []

    audio_exts = {'.mp3', '.wav', '.flac', '.ogg', '.m4a', '.aac', '.wma', '.wav', '.opus'}
    tracks = []

    for f in sorted(folder.iterdir()):
        if f.suffix.lower() in audio_exts:
            tracks.append({
                "name": f.stem,
                "path": str(f.resolve()),
                "size_mb": round(f.stat().st_size / (1024 * 1024), 1),
                "ext": f.suffix.lower(),
            })

    return tracks


def inject_tracks(html_path, tracks):
    """Inject track data into the HTML file's JavaScript."""
    html = Path(html_path).read_text()

    # Find the <script> tag and inject track data before the closing tag
    tracks_json = json.dumps(tracks)
    injection = f"""
<script>
  // AUTO-INJECTED by Spool Launcher
  window.SPOOL_TRACKS = {tracks_json};
  window.SPOOL_FOLDER = "{str(find_spool_folder() or '')}";
  window.SPOOL_AUTO_LOAD = true;
</script>
"""

    # Insert after the <body> tag
    html = html.replace("<body>", f"<body>\n{injection}")

    # Also add an auto-load block in the existing script
    auto_load_js = """
  // Auto-load from Spool Music folder
  if (window.SPOOL_TRACKS && window.SPOOL_TRACKS.length > 0 && window.SPOOL_AUTO_LOAD) {
    console.log(`[Spool] Auto-loading ${window.SPOOL_TRACKS.length} tracks from Spool Music folder`);
    window.SPOOL_TRACKS.forEach(t => {
      tracks.push({
        name: t.name,
        artist: 'Spool Music',
        url: 'file://' + t.path,
        file: null,
        size: t.size_mb
      });
    });
    if (tracks.length > 0 && currentIndex === -1) {
      currentIndex = 0;
      loadTrack(0);
      // Update display
      trackTitle.textContent = tracks.length + ' tracks loaded from Spool Music';
      trackArtist.textContent = 'Drop more files to add';
    }
  }
"""
    # Insert auto-load after the DOMContentLoaded logic
    html = html.replace(
        "// Init",
        auto_load_js + "\n\n  // Init"
    )

    return html


def main():
    # Determine folder
    if len(sys.argv) > 1:
        folder = Path(sys.argv[1])
    else:
        folder = find_spool_folder()
        if folder is None:
            print("⚠ No Spool Music folder found on Desktop.")
            print("  Creating one now...")
            try:
                desktop = Path.home() / "Desktop" / "Spool Music"
                desktop.mkdir(parents=True, exist_ok=True)
                folder = desktop
                print(f"  Created: {folder}")
            except Exception:
                print("  Couldn't create folder. Drag files into the player instead.")
                folder = None

    # Scan for tracks
    tracks = []
    if folder and folder.exists():
        tracks = scan_folder(folder)
        print(f"🎵 Found {len(tracks)} tracks in {folder}")
        for t in tracks:
            print(f"   {t['name']}{t['ext']} ({t['size_mb']} MB)")
    else:
        print("🎵 No folder — player will start empty. Drag files to play.")

    # Prepare HTML
    if tracks:
        html_content = inject_tracks(RECORD_PLAYER, tracks)
    else:
        html_content = RECORD_PLAYER.read_text()

    # Write to temp file
    tmp = tempfile.NamedTemporaryFile(
        mode='w', suffix='.html', delete=False,
        encoding='utf-8', dir=Path(__file__).parent
    )
    tmp_path = Path(tmp.name)
    tmp.write(html_content)
    tmp.close()

    # Start server
    os.chdir(tmp_path.parent)

    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass  # quiet

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}/{tmp_path.name}"
        print(f"\n🎧 Opening Spool Record Player → {url}")
        webbrowser.open(url)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Spool closed.")


if __name__ == "__main__":
    main()
