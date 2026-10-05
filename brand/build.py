"""Generates NEXKO logo concept sheet (round 2). Run: python3 brand/build.py"""
import math, os
HERE = os.path.dirname(__file__)

INK = "#0b1220"
GRAD = [("0", "#ffc53d"), ("0.5", "#ff6a1f"), ("1", "#e2283c")]

_uid = [0]
def uid(p):
    _uid[0] += 1
    return f"{p}{_uid[0]}"

def grad(gid, x1=0, y1=0, x2=1, y2=1, units="objectBoundingBox"):
    stops = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in GRAD)
    return f'<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" gradientUnits="{units}">{stops}</linearGradient>'

# ---------- wordmark (cap height 100) ----------
def letter(ch, x, s):
    """returns (svg, width)"""
    cid = uid("c")
    def clip(w): return f'<clipPath id="{cid}"><rect x="{x}" y="0" width="{w}" height="100"/></clipPath>'
    if ch == "N":
        w = 82
        return (f'{clip(w)}<rect x="{x}" y="0" width="{s}" height="100"/><rect x="{x+w-s}" y="0" width="{s}" height="100"/>'
                f'<line x1="{x+s*0.5}" y1="-2" x2="{x+w-s*0.5}" y2="102" stroke="currentColor" stroke-width="{s*1.12}" clip-path="url(#{cid})"/>', w)
    if ch == "E":
        w = 62
        return (f'<rect x="{x}" y="0" width="{s}" height="100"/><rect x="{x}" y="0" width="{w}" height="{s}"/>'
                f'<rect x="{x}" y="{50-s/2}" width="{w-6}" height="{s}"/><rect x="{x}" y="{100-s}" width="{w}" height="{s}"/>', w)
    if ch == "X":
        w = 84
        return (f'{clip(w)}<g clip-path="url(#{cid})" stroke="currentColor" stroke-width="{s*1.12}">'
                f'<line x1="{x+s*0.45}" y1="-3" x2="{x+w-s*0.45}" y2="103"/><line x1="{x+w-s*0.45}" y1="-3" x2="{x+s*0.45}" y2="103"/></g>', w)
    if ch == "K":
        w = 74
        return (f'{clip(w)}<rect x="{x}" y="0" width="{s}" height="100"/><g clip-path="url(#{cid})" stroke="currentColor" stroke-width="{s*1.08}">'
                f'<line x1="{x+s*0.6}" y1="66" x2="{x+w+4}" y2="-6"/><line x1="{x+s+10}" y1="42" x2="{x+w+4}" y2="106"/></g>', w)
    if ch == "O":
        w = 100
        return (f'<circle cx="{x+50}" cy="50" r="{50-s/2+1}" fill="none" stroke="currentColor" stroke-width="{s}"/>', w)
    raise ValueError(ch)

def wordmark(s=12, gap=26):
    out, x = [], 0
    for ch in "NEXKO":
        svg, w = letter(ch, x, s)
        out.append(svg); x += w + gap
    return "".join(out), x - gap

WM, WMW = wordmark()

# ---------- symbols (drawn in a 200x200 box) ----------
SPIN_CSS = ('<style>@keyframes nx-spin{to{transform:rotate(360deg)}}'
            '.nx-rotor{animation:nx-spin 7s linear infinite}'
            '@media (prefers-reduced-motion:reduce){.nx-rotor{animation:none}}</style>')

def sym_flux(spin=True):
    """Rotor blades centred on (100,100). spin=True adds a slow CSS rotation
    (works in <img>, inline SVG and browsers; static in print/design tools)."""
    g = uid("g")
    def pt(r, a):
        a = math.radians(a)
        return f"{r*math.cos(a):.2f} {r*math.sin(a):.2f}"
    N = 28
    outer = [pt(14 + 80*t, -112 + 90*t**0.7) for t in (i/N for i in range(N+1))]
    inner = [pt(14 + 80*t, -30 + 8*t**1.5) for t in (i/N for i in range(N, -1, -1))]
    blade = "M " + " L ".join(outer + inner) + " Z"
    stops = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in GRAD)
    gd = f'<linearGradient id="{g}" x1="10" y1="-90" x2="0" y2="-10" gradientUnits="userSpaceOnUse">{stops}</linearGradient>'
    blades = "".join(f'<path d="{blade}" fill="url(#{g})" transform="rotate({a})"/>' for a in (0, 120, 240))
    # Rotation happens around the inner group's origin, which sits at the hub (100,100).
    rotor = f'<g transform="translate(100 100)"><g class="nx-rotor">{blades}</g></g>'
    return f'<defs>{gd}</defs>{SPIN_CSS if spin else ""}{rotor}'

def sym_horizon():
    g, c = uid("g"), uid("c")
    bands, y = [], 104
    for h, gap in [(12, 8), (10, 9), (8, 10), (6, 11), (4, 12)]:
        bands.append(f'<rect x="0" y="{y}" width="200" height="{h}"/>'); y += h + gap
    return (f'<defs>{grad(g, 0, 0, 0, 1)}<clipPath id="{c}"><circle cx="100" cy="100" r="86"/></clipPath></defs>'
            f'<g clip-path="url(#{c})"><path d="M14 100 A86 86 0 0 1 186 100 Z" fill="url(#{g})" transform="translate(0 -4)"/>'
            f'<g fill="currentColor">{"".join(bands)}</g></g>')

def sym_stream():
    g, c = uid("g"), uid("c")
    L, R, T, B, W, H = 22, 178, 28, 172, 34, 50
    x0, x1 = L + W, R - W
    ang = math.degrees(math.atan2((B - H/2) - (T + H/2), x1 - x0))
    offs = (0, 13.5, 27)
    up = "".join(f'<rect x="{x+o}" y="{T}" width="7" height="{B-T}"/>' for x in (L, R - W) for o in offs)
    ln = math.hypot(B - T, x1 - x0) + 40
    diag = "".join(f'<rect x="-20" y="{o-17}" width="{ln}" height="7"/>' for o in offs)
    band = f'<clipPath id="{c}"><path d="M{x0-1} {T} L{x1+1} {B-H} V{B} L{x0-1} {T+H} Z"/></clipPath>'
    return (f'<defs>{grad(g, 20, 30, 180, 170, "userSpaceOnUse")}{band}</defs><g fill="url(#{g})">{up}'
            f'<g clip-path="url(#{c})"><g transform="translate({x0} {T + H/2}) rotate({ang:.2f})">{diag}</g></g></g>')

SYMS = {
    "flux": ("Flux", "Three swept blades turning around an open centre, like a rotor caught in motion. It's clearly wind energy without drawing a turbine, and the sunrise gradient adds heat and power. Best suited to a flagship brand.", sym_flux),
    "horizon": ("Horizon", "A rising sun over layered lines that suggest wind currents, power lines and roads. It sums up what the company does, energy above and infrastructure below, in one calm, premium emblem.", sym_horizon),
    "stream": ("Current", "An N drawn as four parallel lines of current, like conductors on a 33kV line or streams of wind. It's the most technical and corporate of the three, and the letter is built into it.", sym_stream),
}

def lockup(sym_fn, color, tag_color):
    # symbol 200 box scaled to 1.3x cap height, wordmark at cap 100
    return (f'<svg viewBox="-10 -40 {280+WMW+10} 190" xmlns="http://www.w3.org/2000/svg" style="color:{color}">'
            f'<g transform="translate(0 -35) scale(0.85)">{sym_fn()}</g>'
            f'<g transform="translate(220 0)" fill="currentColor">{WM}</g>'
            f'<text x="221" y="142" fill="{tag_color}" font-family="Inter, Helvetica, Arial, sans-serif" font-size="19" font-weight="500" letter-spacing="10.6">RENEWABLE SOLUTIONS</text>'
            f'</svg>')

def mark(sym_fn, color):
    return f'<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" style="color:{color}">{sym_fn()}</svg>'

sections = []
for i, (key, (name, desc, fn)) in enumerate(SYMS.items()):
    sections.append(f'''
<section class="concept">
  <h2><b>{i+1}</b>{name}</h2><p>{desc}</p>
  <div class="grid">
    <div class="tile light wide">{lockup(fn, INK, "#6b7280")}</div>
    <div class="tile dark wide">{lockup(fn, "#fff", "rgba(255,255,255,.6)")}</div>
    <div class="tile photo">{lockup(fn, "#fff", "rgba(255,255,255,.75)")}</div>
    <div class="tile icons">
      <div class="app dark">{mark(fn, "#fff")}</div>
      <div class="app light">{mark(fn, INK)}</div>
      <div class="fav">{mark(fn, INK)}</div>
    </div>
  </div>
</section>''')

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>NEXKO Logo Concepts II</title>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@500&family=Inter:wght@400;500&display=swap" rel="stylesheet"/>
<style>
:root{{--ink:{INK};--paper:#f4f3ef;--muted:#6b7280;--line:#e4e2dc}}
*{{box-sizing:border-box}} body{{margin:0;font-family:Inter,system-ui,sans-serif;background:var(--paper);color:var(--ink)}}
header,.concept{{max-width:1280px;margin:auto;padding:0 48px}} header{{padding-top:64px}}
h1{{font:500 44px/1 "Inter Tight";letter-spacing:-.03em;margin:0 0 12px}} header p{{color:var(--muted);margin:0}}
.concept{{margin-top:64px}} .concept h2{{font:500 28px/1 "Inter Tight";letter-spacing:-.02em;margin:0 0 8px;display:flex;gap:14px;align-items:baseline}}
.concept h2 b{{font:500 14px/1 Inter;color:#ff6a1f}} .concept>p{{color:var(--muted);margin:0 0 22px;max-width:680px;line-height:1.55}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.tile{{border-radius:8px;display:grid;place-items:center;min-height:280px;padding:48px;overflow:hidden;position:relative}}
.tile>svg{{width:100%;max-width:470px;height:auto}}
.light{{background:#fff;border:1px solid var(--line)}} .dark{{background:var(--ink)}}
.photo{{background:linear-gradient(0deg,rgba(11,18,32,.55),rgba(11,18,32,.25)),url(../assets/img/hero-windfarm.jpg) center 70%/cover}}
.icons{{background:#e9e7e1;grid-auto-flow:column;gap:28px;align-items:center;justify-content:center}}
.app{{width:132px;height:132px;border-radius:30px;display:grid;place-items:center;box-shadow:0 12px 30px rgba(11,18,32,.18)}}
.app svg{{width:92px}} .app.light{{background:#fff}}
.fav{{width:40px;height:40px;background:#fff;border-radius:8px;display:grid;place-items:center}} .fav svg{{width:28px}}
@media(max-width:860px){{.grid{{grid-template-columns:1fr}} header,.concept{{padding:0 16px}}}}
</style></head><body>
<header><h1>NEXKO logo concepts, round two</h1><p>Abstract, premium and built around energy. Each concept is shown on white, on dark, over a photo, and as an app icon and favicon.</p></header>
{"".join(sections)}
<div style="height:80px"></div></body></html>'''

open(os.path.join(HERE, "concepts.html"), "w").write(html)
print("ok", WMW)

# ---------- production files ----------
OUT = os.path.join(HERE, "..", "assets", "brand")
os.makedirs(OUT, exist_ok=True)
NS = 'xmlns="http://www.w3.org/2000/svg"'
SYM_T = 'transform="translate(0 -35) scale(0.85)"'

def write(name, svg):
    open(os.path.join(OUT, name), "w").write(svg)

for suffix, color, tag in (("", INK, "#6b7280"), ("-white", "#ffffff", "#ffffffb3")):
    write(f"nexko-logo{suffix}.svg",
          f'<svg {NS} viewBox="0 -32 730 164" color="{color}"><title>NEXKO</title>'
          f'<g {SYM_T}>{sym_flux()}</g><g transform="translate(220 0)" fill="{color}">{WM}</g></svg>')
    write(f"nexko-logo-tagline{suffix}.svg",
          f'<svg {NS} viewBox="0 -32 730 184" color="{color}"><title>NEXKO Renewable Solutions</title>'
          f'<g {SYM_T}>{sym_flux()}</g><g transform="translate(220 0)" fill="{color}">{WM}</g>'
          f'<text x="221" y="142" fill="{tag}" font-family="Inter, Helvetica, Arial, sans-serif" font-size="19" font-weight="500" letter-spacing="10.6">RENEWABLE SOLUTIONS</text></svg>')
write("nexko-mark.svg", f'<svg {NS} viewBox="0 0 200 200"><title>NEXKO</title>{sym_flux()}</svg>')
write("nexko-icon.svg", f'<svg {NS} viewBox="0 0 200 200"><title>NEXKO</title><rect width="200" height="200" rx="44" fill="{INK}"/>'
      f'<g transform="translate(100 100) scale(.78) translate(-100 -100)">{sym_flux(spin=False)}</g></svg>')
print("production files written")
