#!/usr/bin/env python3
"""
Spool iPod Engine — read music directly from a connected iPod.

When you plug in your iPod (classic/nano/touch), Windows mounts it as a USB drive.
Apple hides the music behind scrambled filenames in iPod_Control/Music/,
but the real artist/song/album data is inside the ID3 tags.

This scanner:
  1. Finds the iPod drive (D:, E:, etc. or /mnt/d/, /mnt/e/)
  2. Scans iPod_Control/Music/ for all audio files
  3. Extracts real metadata (title, artist, album, artwork) from ID3 tags
  4. Outputs a clean track list that Spool can play

Usage:
  python3 ipod_scanner.py              # Auto-detect iPod drive
  python3 ipod_scanner.py --json       # Output as JSON for web player
  python3 ipod_scanner.py --copy ~/Music/Spool/  # Copy tracks to PC
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

try:
    from mutagen import File as MutagenFile
    from mutagen.easyid3 import EasyID3
    from mutagen.id3 import ID3, APIC
    from mutagen.mp3 import MP3
    from mutagen.flac import FLAC
    HAS_MUTAGEN = True
except ImportError:
    HAS_MUTAGEN = False
    print("[⚠] Install mutagen for full metadata: pip3 install mutagen")


def find_ipod():
    """Auto-detect connected iPod drive."""
    # Windows drive letters (via WSL paths)
    for letter in "DEFGHIJK":
        path = Path(f"/mnt/{letter.lower()}")
        control = path / "iPod_Control" / "Music"
        if control.exists():
            return path
        # Also check root for iPod_Control
        if (path / "iPod_Control").exists():
            return path

    # Try mounting directly
    try:
        import subprocess
        result = subprocess.run(
            ["lsblk", "-o", "NAME,LABEL,MOUNTPOINT", "-l"],
            capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.split('\n'):
            if 'ipod' in line.lower() or 'spool' in line.lower():
                parts = line.split()
                if len(parts) >= 3:
                    return Path(parts[2])
    except Exception:
        pass

    # Ask Windows what drives are connected
    try:
        result = subprocess.run(
            ["powershell.exe", "-Command",
             "Get-WmiObject Win32_LogicalDisk | Where-Object { $_.DriveType -eq 2 } | "
             "Select-Object -ExpandProperty DeviceID"],
            capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.strip().split('\n'):
            drive = line.strip().rstrip(':')
            if drive:
                path = Path(f"/mnt/{drive.lower()}")
                if (path / "iPod_Control").exists():
                    return path
    except Exception:
        pass

    return None


def scan_ipod(ipod_path):
    """Scan the iPod_Control/Music folder for all tracks with metadata."""
    music_path = ipod_path / "iPod_Control" / "Music"
    if not music_path.exists():
        print(f"[✗] No iPod_Control/Music at {music_path}")
        return []

    tracks = []
    audio_exts = {'.mp3', '.m4a', '.m4p', '.m4b', '.aac', '.wav', '.aiff'}

    # Walk all F00-F49 folders
    for root, dirs, files in os.walk(str(music_path)):
        for fname in sorted(files):
            ext = Path(fname).suffix.lower()
            if ext not in audio_exts:
                continue

            full_path = Path(root) / fname
            
            # Extract metadata
            title = fname
            artist = "Unknown Artist"
            album = "Unknown Album"
            track_num = 0
            genre = ""
            year = ""
            has_artwork = False
            duration = 0

            if HAS_MUTAGEN:
                try:
                    audio = MutagenFile(str(full_path))
                    if audio is not None:
                        # MP3 tags
                        if hasattr(audio, 'tags') and audio.tags:
                            title = str(audio.tags.get('TIT2', title))
                            artist = str(audio.tags.get('TPE1', artist))
                            album = str(audio.tags.get('TALB', album))
                            genre = str(audio.tags.get('TCON', ''))
                            year = str(audio.tags.get('TDRC', ''))

                            if hasattr(audio.tags, 'getall'):
                                trck = audio.tags.getall('TRCK')
                                if trck:
                                    track_num = int(str(trck[0]).split('/')[0])

                            # Check for artwork
                            if hasattr(audio, 'info') and hasattr(audio.info, 'length'):
                                duration = audio.info.length
                            has_artwork = any(
                                frame.FrameID.startswith('APIC')
                                for frame in audio.tags.values()
                                if hasattr(frame, 'FrameID')
                            )

                        # M4A tags
                        elif hasattr(audio, 'tags'):
                            tags = dict(audio.tags)
                            title = tags.get('\xa9nam', [title])[0]
                            artist = tags.get('\xa9ART', [artist])[0]
                            album = tags.get('\xa9alb', [album])[0]
                            genre = tags.get('\xa9gen', [''])[0]
                            year = tags.get('\xa9day', [''])[0]
                            if hasattr(audio, 'info') and hasattr(audio.info, 'length'):
                                duration = audio.info.length
                except Exception as e:
                    pass  # Keep defaults for unreadable files

            # Format duration
            mins = int(duration // 60)
            secs = int(duration % 60)
            duration_str = f"{mins}:{secs:02d}"

            tracks.append({
                "title": str(title),
                "artist": str(artist),
                "album": str(album),
                "track": track_num,
                "genre": str(genre),
                "year": str(year),
                "duration": duration,
                "duration_str": duration_str,
                "path": str(full_path),
                "filename": fname,
                "album_folder": Path(root).name,
                "has_artwork": has_artwork,
            })

    # Sort by artist, then album, then track number
    tracks.sort(key=lambda t: (
        t['artist'].lower().lstrip('the '),
        t['album'].lower(),
        t['track']
    ))

    return tracks


def summary(tracks):
    """Print a clean summary of the iPod's contents."""
    artists = set(t['artist'] for t in tracks)
    albums = set((t['artist'], t['album']) for t in tracks)
    total_duration = sum(t['duration'] for t in tracks)
    hours = int(total_duration // 3600)
    mins = int((total_duration % 3600) // 60)

    print(f"\n{'='*50}")
    print(f"  🎵 iPod Music Library")
    print(f"  {len(tracks)} songs · {len(artists)} artists · {len(albums)} albums")
    print(f"  {hours}h {mins}m total")
    print(f"{'='*50}\n")

    current_artist = None
    current_album = None
    for t in tracks:
        if t['artist'] != current_artist:
            current_artist = t['artist']
            print(f"\n  {current_artist}")
        if t['album'] != current_album:
            current_album = t['album']
            print(f"    📀 {current_album}")
        print(f"      {t['track']:02d}. {t['title']} ({t['duration_str']})")


def generate_html_player(tracks, output_path=None):
    """Generate a standalone HTML record player with the iPod track list embedded."""
    import html

    if output_path is None:
        output_path = Path.home() / "Desktop" / "Spool Music" / "ipod_player.html"

    track_json = json.dumps(tracks, indent=2)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Spool — iPod Mode</title>
<style>
  :root {{
    --bg: #0a0a14; --surface: #141428; --text: #e0dcc8;
    --green: #2dd4bf; --cyan: #00d4ff; --brass: #c4a35a;
    --crimson: #e04343; --text-dim: #8888aa;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: var(--bg);
    color: var(--text);
    font-family: 'Segoe UI', system-ui, sans-serif;
    height: 100vh;
    display: flex;
    overflow: hidden;
  }}

  /* Sidebar — track list */
  .sidebar {{
    width: 320px;
    background: var(--surface);
    border-right: 1px solid rgba(255,255,255,0.06);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}
  .sidebar-header {{
    padding: 16px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    flex-shrink: 0;
  }}
  .sidebar-title {{
    font-size: 14px;
    font-weight: 600;
    color: var(--green);
  }}
  .sidebar-count {{
    font-size: 11px;
    color: var(--text-dim);
    margin-top: 4px;
  }}
  .track-list {{
    flex: 1;
    overflow-y: auto;
  }}
  .track-list::-webkit-scrollbar {{ width: 4px; }}
  .track-list::-webkit-scrollbar-track {{ background: transparent; }}
  .track-list::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.1); border-radius: 2px; }}

  .track-item {{
    padding: 10px 16px;
    cursor: pointer;
    border-bottom: 1px solid rgba(255,255,255,0.03);
    transition: 0.15s;
    display: flex;
    gap: 10px;
    align-items: center;
  }}
  .track-item:hover {{ background: rgba(45,212,191,0.05); }}
  .track-item.playing {{
    background: rgba(45,212,191,0.1);
    border-left: 3px solid var(--green);
  }}
  .track-item .index {{ color: var(--text-dim); font-size: 11px; width: 20px; text-align: right; flex-shrink: 0; }}
  .track-item .info {{ flex: 1; min-width: 0; }}
  .track-item .title {{ font-size: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
  .track-item .artist {{ font-size: 10px; color: var(--text-dim); }}
  .track-item .duration {{ font-size: 10px; color: var(--text-dim); flex-shrink: 0; }}

  /* Search */
  .search-box {{
    padding: 10px 16px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    flex-shrink: 0;
  }}
  .search-input {{
    width: 100%;
    background: rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 6px;
    padding: 8px 12px;
    color: var(--text);
    font-size: 12px;
    outline: none;
  }}
  .search-input:focus {{ border-color: var(--green); }}

  /* Now Playing */
  .now-playing {{
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px;
    position: relative;
  }}
  .now-playing-art {{
    width: 300px; height: 300px;
    background: linear-gradient(135deg, #1a1a2e, #2a1a3e);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 80px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    margin-bottom: 30px;
  }}
  .now-playing-info {{
    text-align: center;
  }}
  .np-title {{ font-size: 20px; font-weight: 600; }}
  .np-artist {{ font-size: 14px; color: var(--text-dim); margin-top: 4px; }}
  .np-album {{ font-size: 12px; color: var(--text-dim); margin-top: 2px; }}

  .controls {{
    display: flex;
    gap: 16px;
    align-items: center;
    margin-top: 24px;
  }}
  .ctrl-btn {{
    width: 44px; height: 44px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.1);
    background: var(--surface);
    color: var(--text);
    font-size: 18px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: 0.15s;
  }}
  .ctrl-btn:hover {{ border-color: var(--green); color: var(--green); }}
  .ctrl-btn.play-btn {{
    width: 56px; height: 56px;
    background: var(--green);
    color: var(--bg);
    border: none;
    font-size: 22px;
  }}

  .ipod-badge {{
    position: absolute;
    top: 16px;
    left: 16px;
    padding: 4px 10px;
    background: rgba(45,212,191,0.1);
    border: 1px solid rgba(45,212,191,0.2);
    border-radius: 10px;
    font-size: 10px;
    color: var(--green);
  }}
</style>
</head>
<body>

<div class="sidebar">
  <div class="sidebar-header">
    <div class="sidebar-title">🎵 iPod Library</div>
    <div class="sidebar-count" id="track-count">{len(tracks)} songs · {len(set(t['artist'] for t in tracks))} artists</div>
  </div>
  <div class="search-box">
    <input class="search-input" id="search" placeholder="Search songs or artists..." oninput="filterTracks()">
  </div>
  <div class="track-list" id="track-list">
  </div>
</div>

<div class="now-playing">
  <div class="ipod-badge">📱 iPod Connected</div>
  <div class="now-playing-art" id="now-art">🎵</div>
  <div class="now-playing-info">
    <div class="np-title" id="np-title">Select a song</div>
    <div class="np-artist" id="np-artist"></div>
    <div class="np-album" id="np-album"></div>
  </div>
  <div class="controls">
    <button class="ctrl-btn" onclick="prev()">⏮</button>
    <button class="ctrl-btn play-btn" id="play-btn" onclick="togglePlay()">▶</button>
    <button class="ctrl-btn" onclick="next()">⏭</button>
  </div>
</div>

<script>
  const ALL_TRACKS = {track_json};
  let tracks = [...ALL_TRACKS];
  let currentIndex = -1;
  let isPlaying = false;
  const audio = new Audio();

  // Render track list
  function renderList(list) {{
    const el = document.getElementById('track-list');
    el.innerHTML = list.map((t, i) => `
      <div class="track-item" data-index="${{i}}" onclick="playTrack(${{i}})">
        <span class="index">${{i + 1}}</span>
        <div class="info">
          <div class="title">${{t.title}}</div>
          <div class="artist">${{t.artist}}</div>
        </div>
        <span class="duration">${{t.duration_str}}</span>
      </div>
    `).join('');
  }}

  function filterTracks() {{
    const q = document.getElementById('search').value.toLowerCase();
    if (!q) {{
      tracks = [...ALL_TRACKS];
    }} else {{
      tracks = ALL_TRACKS.filter(t =>
        t.title.toLowerCase().includes(q) ||
        t.artist.toLowerCase().includes(q) ||
        t.album.toLowerCase().includes(q)
      );
    }}
    renderList(tracks);
  }}

  // Playback
  function playTrack(index) {{
    if (index < 0 || index >= tracks.length) return;
    currentIndex = index;
    const t = tracks[index];

    document.querySelectorAll('.track-item').forEach(el => el.classList.remove('playing'));
    document.querySelector(`.track-item[data-index="${{index}}"]`)?.classList.add('playing');

    document.getElementById('np-title').textContent = t.title;
    document.getElementById('np-artist').textContent = t.artist;
    document.getElementById('np-album').textContent = t.album;

    // iPod files are local — use file:// protocol
    audio.src = 'file:///' + t.path.replace(/\\\\/g, '/');
    audio.play().catch(e => {{
      console.error('Playback error:', e);
      document.getElementById('np-title').textContent = '⚠ Cannot play — iPod may be disconnected';
      document.getElementById('np-artist').textContent = 'Plug in your iPod to play';
    }});
    isPlaying = true;
    document.getElementById('play-btn').innerHTML = '⏸';
  }}

  function togglePlay() {{
    if (currentIndex === -1) {{ playTrack(0); return; }}
    if (isPlaying) {{
      audio.pause();
      document.getElementById('play-btn').innerHTML = '▶';
    }} else {{
      audio.play();
      document.getElementById('play-btn').innerHTML = '⏸';
    }}
    isPlaying = !isPlaying;
  }}

  function next() {{
    if (tracks.length === 0) return;
    playTrack((currentIndex + 1) % tracks.length);
  }}

  function prev() {{
    if (tracks.length === 0) return;
    playTrack((currentIndex - 1 + tracks.length) % tracks.length);
  }}

  audio.addEventListener('ended', next);

  // Keyboard shortcuts
  document.addEventListener('keydown', e => {{
    if (e.code === 'Space') {{ e.preventDefault(); togglePlay(); }}
    else if (e.code === 'ArrowDown') {{ e.preventDefault(); playTrack(Math.min(currentIndex + 1, tracks.length - 1)); }}
    else if (e.code === 'ArrowUp') {{ e.preventDefault(); playTrack(Math.max(0, currentIndex - 1)); }}
  }});

  // Init
  renderList(ALL_TRACKS);
</script>
</body>
</html>"""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_content, encoding='utf-8')
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Spool iPod Scanner")
    parser.add_argument("--drive", type=str, help="iPod drive path (e.g., /mnt/d or D:)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--player", action="store_true", help="Generate HTML player file")
    parser.add_argument("--copy", type=str, help="Copy tracks to target folder")
    parser.add_argument("--summary", action="store_true", help="Print track summary")
    args = parser.parse_args()

    # Find iPod
    if args.drive:
        ipod = Path(args.drive)
        if args.drive.endswith(':'):
            ipod = Path(f"/mnt/{args.drive[0].lower()}")
    else:
        ipod = find_ipod()

    if ipod is None:
        print("❌ No iPod detected.")
        print("   Make sure it's plugged in and shows up as a drive in File Explorer.")
        print("   If you know the drive letter, run: python3 ipod_scanner.py --drive D:")
        sys.exit(1)

    print(f"📱 iPod found at: {ipod}")
    print(f"   Scanning iPod_Control/Music/ ...")

    # Scan
    tracks = scan_ipod(ipod)

    if not tracks:
        print("⚠ No music files found on iPod.")
        print("  Is this an iPod classic/nano/touch with music synced via iTunes/Apple Music?")
        sys.exit(1)

    # Output
    if args.json:
        print(json.dumps(tracks, indent=2))
    elif args.player:
        # Generate HTML player on the iPod itself (runs from iPod!)
        output = ipod / "Spool Player.html"
        path = generate_html_player(tracks, output)
        print(f"\n✅ iPod player saved to iPod: {path.name}")
        print(f"   Double-click on iPod drive → {path.name}")
        print(f"   Or open: file://{path}")
    elif args.copy:
        target = Path(args.copy)
        target.mkdir(parents=True, exist_ok=True)
        print(f"\n📦 Copying {len(tracks)} tracks to {target} ...")
        for i, t in enumerate(tracks):
            src = Path(t['path'])
            # Use artist/album/title for filename
            safe_name = f"{t['artist']} - {t['title']}{src.suffix}".replace('/', '-').replace('\\', '-')
            dst = target / safe_name
            shutil.copy2(src, dst)
            print(f"   [{i+1}/{len(tracks)}] {safe_name}")
        print(f"\n✅ {len(tracks)} tracks copied to {target}")
    else:
        summary(tracks)
        print(f"\n💡 Tips:")
        print(f"   View as JSON:  python3 ipod_scanner.py --json")
        print(f"   Copy to PC:    python3 ipod_scanner.py --copy ~/Desktop/Spool\\ Music/")
        print(f"   HTML player:   python3 ipod_scanner.py --player")


if __name__ == "__main__":
    main()
