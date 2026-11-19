"""Findet die lautesten/aufregendsten Momente eines Stream-Videos und schneidet sie als Clips."""
import glob
import os
import subprocess
import sys

import numpy as np

URL = os.environ["VOD_URL"].strip()
COUNT = max(1, min(10, int(os.environ.get("CLIP_COUNT", "5"))))
LENGTH = max(15, min(120, int(os.environ.get("CLIP_LEN", "45"))))
VERTICAL = os.environ.get("VERTICAL", "false").lower() == "true"
SR = 8000

if not URL.startswith(("http://", "https://")):
    sys.exit("Ungültiger Link: er muss mit http:// oder https:// beginnen.")

os.makedirs("out", exist_ok=True)


def run(cmd, **kw):
    print("+", " ".join(cmd), flush=True)
    return subprocess.run(cmd, check=True, **kw)


# 1) Nur die Tonspur laden (klein und schnell) und als Lautstärke pro Sekunde auslesen
run(["yt-dlp", "-f", "audio_only/bestaudio/worst", "-o", "audio.%(ext)s", "--", URL])
audio = glob.glob("audio.*")[0]
pcm = run(
    ["ffmpeg", "-v", "error", "-i", audio, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
    capture_output=True,
).stdout
x = np.frombuffer(pcm, dtype=np.int16).astype(np.float32)
secs = len(x) // SR
if secs < LENGTH:
    sys.exit("Das Video ist kürzer als ein Clip.")
rms = np.sqrt((x[: secs * SR].reshape(secs, SR) ** 2).mean(axis=1))


# 2) Score = Lautstärke der letzten Sekunden im Vergleich zur normalen Stimmung des Streams
def smooth(a, w):
    return np.convolve(a, np.ones(w) / w, mode="same")


score = smooth(rms, 8) - smooth(rms, 120)
score = (score - score.mean()) / (score.std() + 1e-9)

# 3) Die besten Momente wählen, mindestens eine Clip-Länge auseinander
picked = []
for i in np.argsort(score)[::-1]:
    if all(abs(int(i) - p) >= LENGTH for p in picked):
        picked.append(int(i))
    if len(picked) == COUNT:
        break

# 4) Nur diese Abschnitte laden und schneiden
for n, peak in enumerate(sorted(picked), 1):
    start = max(0, min(peak - int(LENGTH * 0.6), secs - LENGTH))
    end = start + LENGTH
    name = f"raw{n}"
    run([
        "yt-dlp", "-f", "best[height<=720]/best",
        "--download-sections", f"*{start}-{end}", "--force-keyframes-at-cuts",
        "-o", name + ".%(ext)s", "--", URL,
    ])
    src = glob.glob(name + ".*")[0]
    vf = "crop=ih*9/16:ih,scale=1080:1920" if VERTICAL else "scale=-2:720"
    stamp = f"{start // 3600:02d}h{start % 3600 // 60:02d}m{start % 60:02d}s"
    run([
        "ffmpeg", "-y", "-v", "error", "-i", src, "-vf", vf,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
        "-c:a", "aac", "-movflags", "+faststart",
        f"out/clip_{n:02d}_{stamp}.mp4",
    ])
print("Fertig:", sorted(os.listdir("out")))
