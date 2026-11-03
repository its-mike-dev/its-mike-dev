#!/usr/bin/env python3
"""
Generator for the minimalist CRT / retro-tech GitHub profile banner.
Single-color phosphor green (#a4e3ad), clean terminal aesthetic,
rotating 3D low-poly wireframe figure, zero bulky plastic frames.
"""
import math, random
from pathlib import Path

W, H = 960, 185
BG = "#060907"
BORDER = "#1b281f"
PHOS = "#a4e3ad"
PHOS_DIM = "#5f8f68"
PHOS_DEEP = "#243829"
FONT = "'JetBrains Mono','IBM Plex Mono','DejaVu Sans Mono',Consolas,'Courier New',monospace"

GLYPHS = {
    "P": ["#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "],
    "R": ["#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"],
    "O": [" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    "F": ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "],
    "I": ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "#####"],
    "L": ["#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"],
    "E": ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"],
    " ": ["     "] * 7,
}

rnd = random.Random(42)

def pixel_text(text, x0, y0, px=6.8):
    out = []
    for ci, ch in enumerate(text.upper()):
        for ry, row in enumerate(GLYPHS.get(ch, GLYPHS[" "])):
            for rx, c in enumerate(row):
                if c == "#":
                    x = x0 + (ci * 6 + rx) * px
                    y = y0 + ry * px
                    o = round(rnd.uniform(0.80, 1.0), 2)
                    out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{px-1.4:.1f}" height="{px-1.4:.1f}" opacity="{o}"/>')
    return "\n".join(out)

def wire_frames(cx, cy, r, frames=24):
    t = (1 + 5 ** 0.5) / 2
    v = [(-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0), (0, -1, t), (0, 1, t),
         (0, -1, -t), (0, 1, -t), (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1)]
    edges = sorted({tuple(sorted((i, j))) for i in range(12) for j in range(12)
                    if i != j and abs(sum((a - b) ** 2 for a, b in zip(v[i], v[j])) - 4) < 1e-6})
    n = math.sqrt(1 + t * t)
    paths = []
    for f in range(frames):
        a = 2 * math.pi * f / frames
        b = 0.42
        pts = []
        for x, y, z in v:
            x, y, z = x / n, y / n, z / n
            x, z = x * math.cos(a) + z * math.sin(a), -x * math.sin(a) + z * math.cos(a)
            y, z = y * math.cos(b) - z * math.sin(b), y * math.sin(b) + z * math.cos(b)
            s = 2.4 / (3.0 - z)
            pts.append((round((cx + x * r * s) / 2) * 2, round((cy + y * r * s) / 2) * 2))
        paths.append(" ".join(f"M{pts[i][0]} {pts[i][1]}L{pts[j][0]} {pts[j][1]}" for i, j in edges))
    return paths

def build_header():
    frames = wire_frames(cx=820, cy=86, r=46, frames=24)
    frame_d_str = ";".join(frames)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="PROFILE // its-mike-dev">
<title>PROFILE // its-mike-dev</title>
<defs>
  <radialGradient id="bg_glow" cx="45%" cy="50%" r="65%">
    <stop offset="0" stop-color="#0c150f"/>
    <stop offset="70%" stop-color="#070c08"/>
    <stop offset="100%" stop-color="#040605"/>
  </radialGradient>
  <linearGradient id="scanroll" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{PHOS}" stop-opacity="0"/>
    <stop offset="50%" stop-color="{PHOS}" stop-opacity="0.04"/>
    <stop offset="100%" stop-color="{PHOS}" stop-opacity="0"/>
  </linearGradient>
  <pattern id="scanlines" width="4" height="2" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="#000" opacity="0.42"/>
  </pattern>
  <filter id="bloom" x="-10%" y="-10%" width="120%" height="120%">
    <feGaussianBlur stdDeviation="1.5" result="blur"/>
    <feMerge>
      <feMergeNode in="blur"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
  <clipPath id="inner_clip">
    <rect x="0" y="0" width="{W}" height="{H}" rx="6"/>
  </clipPath>
</defs>

<style>
  text {{
    font-family: {FONT};
    font-size: 13px;
    fill: {PHOS};
    white-space: pre;
  }}
  .cursor {{
    animation: blink 1.1s infinite steps(1);
  }}
  .roll {{
    animation: sweep 6s linear infinite;
  }}
  @keyframes blink {{
    50% {{ opacity: 0; }}
  }}
  @keyframes sweep {{
    from {{ transform: translateY(-80px); }}
    to {{ transform: translateY({H + 50}px); }}
  }}
</style>

<g clip-path="url(#inner_clip)">
  <rect width="{W}" height="{H}" fill="url(#bg_glow)"/>

  <g filter="url(#bloom)" fill="{PHOS}">
    <!-- Pixel Logo: PROFILE -->
    <g transform="translate(42, 28)">
      {pixel_text("PROFILE", 0, 0, px=6.8)}
      <text x="310" y="32" fill="{PHOS_DIM}" font-size="13">// its-mike-dev</text>
    </g>

    <!-- Divider line -->
    <line x1="42" y1="94" x2="690" y2="94" stroke="{PHOS_DEEP}" stroke-width="1" stroke-dasharray="3 3"/>

    <!-- Info Lines (DOMAIN and TERMINAL SESSION ACTIVE removed) -->
    <g transform="translate(42, 122)">
      <text x="0" y="0" fill="{PHOS_DIM}">SYSTEM</text>
      <text x="90" y="0">Arch Linux [zen kernel] · KDE Plasma [Wayland]</text>

      <text x="0" y="24" fill="{PHOS_DIM}">ACCEL</text>
      <text x="90" y="24">NVIDIA GeForce RTX 4060 Ti · CUDA / Tensor <tspan class="cursor" fill="{PHOS}">█</tspan></text>
    </g>

    <!-- 3D Geometric Wireframe with '24f' -->
    <g>
      <line x1="720" y1="20" x2="720" y2="{H-20}" stroke="{PHOS_DEEP}" stroke-width="1" stroke-dasharray="2 4"/>
      <path d="{frames[0]}" fill="none" stroke="{PHOS}" stroke-width="1.3" opacity="0.95">
        <animate attributeName="d" values="{frame_d_str}" dur="3.6s" repeatCount="indefinite" calcMode="discrete"/>
      </path>
      <text x="820" y="156" text-anchor="middle" fill="{PHOS_DIM}" font-size="11">24f</text>
    </g>
  </g>

  <!-- CRT Scanlines & Rolling Beam -->
  <rect class="roll" width="{W}" height="60" fill="url(#scanroll)"/>
  <rect width="{W}" height="{H}" fill="url(#scanlines)" pointer-events="none"/>
</g>

<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="6" fill="none" stroke="{BORDER}" stroke-width="1"/>
</svg>'''

if __name__ == "__main__":
    assets_dir = Path(__file__).parent / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    header_path = assets_dir / "header.svg"
    header_path.write_text(build_header(), encoding="utf-8")
    print(f"Header generated -> {header_path}")
