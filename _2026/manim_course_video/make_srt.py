"""
Build a draft subtitle file from the narration in script.md.

Each scene's narration is spread over that scene's time window, in proportion
to the length of each line. Replace with STT timings once the voice-over exists.

Usage: python make_srt.py [output.srt]
"""
import re
import sys
from pathlib import Path

# Scene lengths in seconds, as rendered from main.py at 30fps
SCENE_DURATIONS = {
    "Intro": 34.0,
    "Pipeline": 45.0,
    "DivisionOfLabor": 49.2,
    "ParallelAgents": 39.03,
    "IterationLoop": 43.0,
    "Pitfalls": 42.0,
    "Outro": 36.5,
}
LEAD_IN = 1.0
TAIL = 1.5
MAX_CHARS = 18
GAP = 0.1


def get_narration(script_path):
    narration = {}
    current = None
    for line in Path(script_path).read_text(encoding="utf-8").splitlines():
        header = re.match(r"### \d+\. (\w+)", line)
        if header:
            current = header.group(1)
            narration[current] = []
        elif current and line.startswith("> ") and line[2:].strip():
            narration[current].append(line[2:].strip())
    return narration


def split_line(text):
    # Break at Chinese punctuation, then pack pieces into lines of at most MAX_CHARS
    pieces = [p for p in re.split(r"(?<=[，。？！：；、])", text) if p]
    lines = []
    for piece in pieces:
        piece = piece.rstrip("，。；、：")
        if lines and len(lines[-1]) + len(piece) + 1 <= MAX_CHARS:
            lines[-1] += " " + piece
        else:
            lines.append(piece)
    return lines


def format_time(seconds):
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_srt(narration):
    entries = []
    scene_start = 0.0
    for scene, duration in SCENE_DURATIONS.items():
        lines = [sub for para in narration.get(scene, []) for sub in split_line(para)]
        window = duration - LEAD_IN - TAIL
        total_chars = sum(len(line) for line in lines)
        t = scene_start + LEAD_IN
        for line in lines:
            length = window * len(line) / total_chars
            entries.append((t, t + length - GAP, line))
            t += length
        scene_start += duration

    return "\n".join(
        f"{n}\n{format_time(start)} --> {format_time(end)}\n{text}\n"
        for n, (start, end, text) in enumerate(entries, start=1)
    )


if __name__ == "__main__":
    here = Path(__file__).parent
    out_path = sys.argv[1] if len(sys.argv) > 1 else here / "subtitles_draft.srt"
    srt = build_srt(get_narration(here / "script.md"))
    Path(out_path).write_text(srt, encoding="utf-8")
    print(f"Wrote {out_path} ({srt.count(' --> ')} cues)")
