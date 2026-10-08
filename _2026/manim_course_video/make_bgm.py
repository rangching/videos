"""
Synthesize a calm, royalty-free background track for the course video.

Usage: python make_bgm.py [output.wav] [duration_seconds]
Mix it under the voice at roughly -18 to -22 dB.
"""
import sys
import wave

import numpy as np
from scipy.signal import fftconvolve

SAMPLE_RATE = 44100
BPM = 72
BEAT = 60 / BPM
BAR = 4 * BEAT

# Cmaj7 - Am7 - Fmaj7 - G6, as MIDI notes
PROGRESSION = [
    [60, 64, 67, 71],
    [57, 60, 64, 67],
    [53, 57, 60, 64],
    [55, 59, 62, 64],
]

# Scene boundaries (seconds), matching main.py
INTRO_END = 34
OUTRO_START = 252


def midi_to_freq(note):
    return 440 * 2 ** ((note - 69) / 12)


def get_envelope(n_samples, attack, release):
    env = np.ones(n_samples)
    n_attack = min(int(attack * SAMPLE_RATE), n_samples)
    n_release = min(int(release * SAMPLE_RATE), n_samples - n_attack)
    env[:n_attack] = np.linspace(0, 1, n_attack)
    if n_release > 0:
        env[-n_release:] = np.linspace(1, 0, n_release)
    return env


def get_pad(freq, duration):
    t = np.arange(int(duration * SAMPLE_RATE)) / SAMPLE_RATE
    wave_sum = sum(
        np.sin(2 * np.pi * freq * detune * t + phase)
        for detune, phase in [(1.0, 0), (1.003, 1.3), (0.997, 2.1)]
    )
    wave_sum += 0.15 * np.sin(2 * np.pi * 2 * freq * t)
    return wave_sum * get_envelope(len(t), attack=1.2, release=1.5)


def get_pluck(freq, duration):
    t = np.arange(int(duration * SAMPLE_RATE)) / SAMPLE_RATE
    tone = np.sin(2 * np.pi * freq * t)
    tone += 0.3 * np.sin(2 * np.pi * 2 * freq * t) * np.exp(-6 * t)
    tone += 0.1 * np.sin(2 * np.pi * 3 * freq * t) * np.exp(-10 * t)
    return tone * np.exp(-3.5 * t) * get_envelope(len(t), attack=0.005, release=0.05)


def add_at(track, sound, start):
    i0 = int(start * SAMPLE_RATE)
    i1 = min(i0 + len(sound), len(track))
    if i0 < len(track):
        track[i0:i1] += sound[:i1 - i0]


def get_reverb(signal, decay=2.5, mix=0.35, seed=0):
    rng = np.random.default_rng(seed)
    t = np.arange(int(decay * SAMPLE_RATE)) / SAMPLE_RATE
    impulse = rng.standard_normal(len(t)) * np.exp(-5 * t / decay)
    wet = fftconvolve(signal, impulse)[:len(signal)]
    wet *= np.abs(signal).max() / (np.abs(wet).max() + 1e-9)
    return (1 - mix) * signal + mix * wet


def make_track(duration):
    n = int(duration * SAMPLE_RATE)
    pad = np.zeros(n)
    bass = np.zeros(n)
    arp = np.zeros(n)

    arp_pattern = [0, 2, 1, 3, 2, 1, 3, 2]
    n_bars = int(np.ceil(duration / BAR))
    for bar in range(n_bars):
        start = bar * BAR
        chord = PROGRESSION[bar % len(PROGRESSION)]
        for note in chord:
            add_at(pad, get_pad(midi_to_freq(note), BAR + 1.5), start)

        in_body = INTRO_END - BAR < start < OUTRO_START
        if start >= INTRO_END - 2 * BAR:
            add_at(bass, get_pluck(midi_to_freq(chord[0] - 24), 2 * BEAT), start)
            add_at(bass, get_pluck(midi_to_freq(chord[0] - 24), 2 * BEAT), start + 2.5 * BEAT)
        if in_body:
            for step, index in enumerate(arp_pattern):
                note = chord[index] + 12
                add_at(arp, get_pluck(midi_to_freq(note), 1.5), start + step * BEAT / 2)

    track = 0.5 * pad / 3 + 0.5 * bass + 0.18 * arp
    track = get_reverb(track)

    # Fade in and out
    fade_in = int(4 * SAMPLE_RATE)
    fade_out = int(6 * SAMPLE_RATE)
    track[:fade_in] *= np.linspace(0, 1, fade_in)
    track[-fade_out:] *= np.linspace(1, 0, fade_out)
    return 0.89 * track / np.abs(track).max()


def write_wav(path, track):
    stereo = np.stack([track, np.roll(track, 300)], axis=1)
    data = (stereo * 32767).astype(np.int16)
    with wave.open(path, "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(data.tobytes())


if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else "bgm.wav"
    duration = float(sys.argv[2]) if len(sys.argv) > 2 else 290
    write_wav(out_path, make_track(duration))
    print(f"Wrote {out_path} ({duration:.0f}s)")
