"""Genera los SVG del perfil (tema claro y oscuro).

Uso: python3 generate-assets.py [carpeta-de-iconos]
Los iconos de tecnologías vienen de skill-icons (MIT) y simple-icons (CC0); se incrustan
en cada SVG porque GitHub no deja que un SVG servido como <img> cargue recursos externos.
"""
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape as esc

ROOT = Path(__file__).parent
OUT = ROOT / "assets"
ICONS = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "icons"
OUT.mkdir(exist_ok=True)
W = 880

# Paleta de GitHub (Primer) para que el perfil se funda con la página en ambos temas.
THEMES = {
    "dark": dict(bg="#0d1117", surface="#151b23", surface2="#212830", border="#3d444d",
                 ink="#f0f6fc", muted="#9198a1", faint="#656c76", glow=".30", tint=".15", wash=".09",
                 violet="#ab7df8", pink="#db61a2", orange="#db6d28", amber="#d29922",
                 green="#3fb950", sky="#4493f8",
                 code_bg="#010409", code_border="#3d444d", code_bar="#151b23", code_ln="#656c76"),
    "light": dict(bg="#ffffff", surface="#f6f8fa", surface2="#eff2f5", border="#d1d9e0",
                  ink="#1f2328", muted="#59636e", faint="#818b98", glow=".22", tint=".12", wash=".07",
                  violet="#8250df", pink="#bf3989", orange="#bc4c00", amber="#9a6700",
                  green="#1a7f37", sky="#0969da",
                  code_bg="#f6f8fa", code_border="#d1d9e0", code_bar="#eff2f5", code_ln="#818b98"),
}
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

BASE_CSS = f""".s{{font-family:{SANS}}} .m{{font-family:{MONO}}}
@media (prefers-reduced-motion: reduce){{ *{{animation:none!important}} }}"""


def doc(w, h, body, css="", defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" role="img">'
            f'<style>{BASE_CSS}{css}</style><defs>{defs}</defs>{body}</svg>')


def text(x, y, s, size, fill, cls="s", weight=400, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}" fill="{fill}" {extra}>{esc(s)}</text>')


def lines(x, y, rows, size, fill, lh, **kw):
    return "".join(text(x, y + i * lh, r, size, fill, **kw) for i, r in enumerate(rows))


def card(x, y, w, h, t, r=6):
    return f'<rect x="{x+.5}" y="{y+.5}" width="{w-1}" height="{h-1}" rx="{r}" fill="{t["surface"]}" stroke="{t["border"]}"/>'


def section_title(n, title, sub, t, color):
    return (text(0, 30, f"{n:02d}", 13, t[color], cls="m", weight=700)
            + text(30, 30, title, 22, t["ink"], weight=700, extra='letter-spacing="-0.4"')
            + text(W, 30, sub, 13, t["faint"], anchor="end"))


# ---------------- ICONOS ----------------
SIMPLE = {  # slug: (color en tema oscuro, color en tema claro)
    "expo": ("#FFFFFF", "#000020"), "stripe": ("#7A73FF", "#635BFF"), "sentry": ("#B4A3F5", "#362D59"),
    "turborepo": ("#FF4F6D", "#EF4444"), "openai": ("#FFFFFF", "#0C0A09"), "playwright": ("#45BA4B", "#2EAD33"),
}
TILE = {"dark": "#212830", "light": "#eaeef2"}
_uid = [0]


def icon(name, x, y, size, theme):
    _uid[0] += 1
    pre = f"i{_uid[0]}_"
    if name in SIMPLE:
        raw = (ICONS / f"si-{name}.svg").read_text()
        path = re.search(r'<path d="([^"]+)"', raw).group(1)
        col = SIMPLE[name][0 if theme == "dark" else 1]
        inner = (f'<rect width="256" height="256" rx="40" fill="{TILE[theme]}"/>'
                 f'<g transform="translate(56 56) scale(6)"><path d="{path}" fill="{col}"/></g>')
    else:
        raw = (ICONS / f"{name}-{'Dark' if theme == 'dark' else 'Light'}.svg").read_text()
        inner = re.sub(r"^<svg[^>]*>|</svg>\s*$", "", raw.strip())
        inner = inner.replace('fill="#242938"', f'fill="{TILE[theme]}"').replace('fill="#F4F2ED"', f'fill="{TILE[theme]}"').replace('rx="60"', 'rx="40"')
        ids = re.findall(r'id="([^"]+)"', inner)
        for i in ids:
            inner = inner.replace(f'id="{i}"', f'id="{pre}{i}"').replace(f"url(#{i})", f"url(#{pre}{i})") \
                         .replace(f'href="#{i}"', f'href="#{pre}{i}"')
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 256 256">{inner}</svg>'


# ---------------- HERO ----------------
TERMINAL = [  # recorrido de un producto, de la idea a producción
    [("$ ", "faint"), ("discover ", "violet"), ("--client ", "sky"), ('"the real problem"', "green")],
    [("  ✓ ", "green"), ("scope set · risks ranked", "muted")],
    [("$ ", "faint"), ("design ", "violet"), ("--architecture", "sky")],
    [("  ✓ ", "green"), ("api · web · mobile · cloud", "muted")],
    [("$ ", "faint"), ("build ", "violet"), ("&& ", "faint"), ("test", "violet")],
    [("  ✓ ", "green"), ("domain rules covered", "muted")],
    [("$ ", "faint"), ("ship ", "violet"), ("--prod", "sky")],
    [("  ✓ ", "green"), ("live · monitored · v1.0", "orange")],
]


def hero(t, theme):
    h = 400
    defs = (f'<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>'
            f'<linearGradient id="role" x1="0" x2="1" spreadMethod="reflect"><stop offset="0" stop-color="{t["violet"]}"/>'
            f'<stop offset=".5" stop-color="{t["pink"]}"/><stop offset="1" stop-color="{t["orange"]}"/>'
            f'<animateTransform attributeName="gradientTransform" type="translate" values="0 0;1 0;0 0" dur="8s" repeatCount="indefinite"/></linearGradient>'
            f'<clipPath id="clip"><rect width="{W}" height="{h}" rx="6"/></clipPath>')
    css = ("@keyframes a{0%,100%{transform:translate(0,0)}50%{transform:translate(40px,-25px)}}"
           "@keyframes b{0%,100%{transform:translate(0,0)}50%{transform:translate(-50px,30px)}}"
           "@keyframes c{0%,100%{transform:translate(0,0)}50%{transform:translate(30px,35px)}}"
           ".b1{animation:a 14s ease-in-out infinite}.b2{animation:b 17s ease-in-out infinite}.b3{animation:c 20s ease-in-out infinite}"
           "@keyframes blink{50%{opacity:0}}.cur{animation:blink 1.1s steps(1) infinite}"
           "@keyframes pulse{0%{r:4;opacity:.8}100%{r:11;opacity:0}}.pl{animation:pulse 1.8s ease-out infinite}")
    b = f'<g clip-path="url(#clip)"><rect width="{W}" height="{h}" fill="{t["bg"]}"/>'
    b += f'<g filter="url(#blur)" opacity="{t["glow"]}">'
    b += f'<circle class="b1" cx="180" cy="80" r="150" fill="{t["violet"]}"/>'
    b += f'<circle class="b2" cx="520" cy="360" r="140" fill="{t["pink"]}"/>'
    b += f'<circle class="b3" cx="800" cy="60" r="130" fill="{t["orange"]}"/></g>'
    b += f'<rect x=".5" y=".5" width="{W-1}" height="{h-1}" rx="6" stroke="{t["border"]}"/></g>'
    # estado
    b += f'<rect x="44" y="44" width="226" height="30" rx="15" fill="{t["surface"]}" fill-opacity=".8" stroke="{t["border"]}"/>'
    b += f'<circle class="pl" cx="62" cy="59" r="4" fill="{t["green"]}"/><circle cx="62" cy="59" r="4" fill="{t["green"]}"/>'
    b += text(76, 63.5, "Shipping from first principles", 12.5, t["ink"], weight=500)
    b += text(42, 140, "Yeltsin López", 54, t["ink"], weight=800, extra='letter-spacing="-1.8"')
    b += text(44, 182, "Senior Software Engineer & Architect", 24, "url(#role)", weight=700, extra='letter-spacing="-0.4"')
    b += lines(44, 222, ["I build products end to end — from the", "client's real problem to architecture,", "code, cloud and launch."], 16, t["muted"], 25)
    # métricas
    for i, (num, lab, col) in enumerate([("7+", "years shipping", "violet"), ("15+", "products built", "pink"), ("3", "open-source projects", "orange")]):
        x = 44 + i * 132
        b += text(x, 336, num, 28, t[col], weight=800, extra='letter-spacing="-1"')
        b += text(x, 358, lab, 12.5, t["faint"])
    # ventana de código
    wx, wy, ww, wh = 492, 66, 350, 262
    b += f'<rect x="{wx+.5}" y="{wy+.5}" width="{ww-1}" height="{wh-1}" rx="6" fill="{t["code_bg"]}" stroke="{t["code_border"]}"/>'
    b += f'<path d="M{wx+.5} {wy+42}V{wy+6}a5.5 5.5 0 0 1 5.5-5.5h{ww-12}a5.5 5.5 0 0 1 5.5 5.5V{wy+42}z" fill="{t["code_bar"]}"/>'
    for i, c in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        b += f'<circle cx="{wx+22+i*18}" cy="{wy+22}" r="5.5" fill="{c}"/>'
    b += text(wx + ww / 2, wy + 26, "~/products — zsh", 11.5, t["muted"], cls="m", anchor="middle")
    b += f'<line x1="{wx}" y1="{wy+42}" x2="{wx+ww}" y2="{wy+42}" stroke="{t["code_border"]}"/>'
    dark = t
    # máquina de escribir: cada línea se revela con un clip cuyo ancho crece (SMIL, funciona en <img>)
    cwid, per_char, gap, start, total = 6.93, .035, .22, .6, 15.0
    x0, tline, cur_x, cur_y, kt = wx + 42, start, [], [], []
    for r, row in enumerate(TERMINAL):
        y = wy + 70 + r * 22
        n = sum(len(sp) for sp, _ in row)
        t0, t1 = tline, tline + n * per_char
        tline = t1 + gap
        k0, k1, w_full = t0 / total, t1 / total, n * cwid + 2
        b += text(wx + 18, y, str(r + 1), 11.5, t["code_ln"], cls="m")
        b += (f'<clipPath id="ln{r}"><rect x="{x0}" y="{y-13}" width="0" height="18">'
              f'<animate attributeName="width" values="0;0;{w_full:.1f};{w_full:.1f};0" '
              f'keyTimes="0;{k0:.4f};{k1:.4f};{(total-.4)/total:.4f};1" dur="{total}s" repeatCount="indefinite"/></rect></clipPath>')
        spans = "".join(f'<tspan fill="{dark[c]}">{esc(sp)}</tspan>' for sp, c in row)
        b += f'<text x="{x0}" y="{y}" class="m" font-size="11.5" xml:space="preserve" clip-path="url(#ln{r})">{spans}</text>'
        if n:
            kt += [k0, k1]; cur_x += [x0 + 2, x0 + n * cwid + 3]; cur_y += [y - 11, y - 11]
    kt = [0] + kt + [1]
    cur_x = [x0] + cur_x + [cur_x[-1]]
    cur_y = [wy + 61] + cur_y + [cur_y[-1]]
    ks = ";".join(f"{k:.4f}" for k in kt)
    b += (f'<rect class="cur" x="{x0}" y="{wy+61}" width="7" height="14" fill="{dark["ink"]}">'
          f'<animate attributeName="x" values="{";".join(f"{v:.1f}" for v in cur_x)}" keyTimes="{ks}" dur="{total}s" repeatCount="indefinite"/>'
          f'<animate attributeName="y" values="{";".join(f"{v:.1f}" for v in cur_y)}" keyTimes="{ks}" dur="{total}s" calcMode="discrete" repeatCount="indefinite"/></rect>')
    return doc(W, h, b, css, defs)


# ---------------- PRINCIPIOS ----------------
def glyph(kind, cx, cy, c):
    s = f'stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"'
    g = {
        "db": f'<ellipse cx="{cx}" cy="{cy-7}" rx="10" ry="4" {s}/><path d="M{cx-10} {cy-7}v14c0 2.2 4.5 4 10 4s10-1.8 10-4v-14M{cx-10} {cy}c0 2.2 4.5 4 10 4s10-1.8 10-4" {s}/>',
        "target": f'<circle cx="{cx}" cy="{cy}" r="10" {s}/><circle cx="{cx}" cy="{cy}" r="5" {s}/><circle cx="{cx}" cy="{cy}" r="1.2" fill="{c}"/>',
        "frame": f'<path d="M{cx-11} {cy-5}v-6h6M{cx+11} {cy-5}v-6h-6M{cx-11} {cy+5}v6h6M{cx+11} {cy+5}v6h-6" {s}/><rect x="{cx-4}" y="{cy-4}" width="8" height="8" rx="2" {s}/>',
        "search": f'<circle cx="{cx-2}" cy="{cy-2}" r="7.5" {s}/><path d="M{cx+3.5} {cy+3.5}l6 6M{cx-5} {cy-2}h6" {s}/>',
        "coin": f'<circle cx="{cx}" cy="{cy}" r="10.5" {s}/><path d="M{cx+3.5} {cy-4}a4.5 4.5 0 1 0 0 8M{cx} {cy-8}v16" {s}/>',
        "person": f'<circle cx="{cx}" cy="{cy-5}" r="4.5" {s}/><path d="M{cx-9} {cy+10}c1-5 4.5-7.5 9-7.5s8 2.5 9 7.5" {s}/>',
        "layers": f'<path d="M{cx} {cy-10}l11 5.5-11 5.5-11-5.5z" {s}/><path d="M{cx-11} {cy+1}l11 5.5 11-5.5M{cx-11} {cy+6.5}l11 5.5 11-5.5" {s}/>',
        "shield": f'<path d="M{cx} {cy-11}l9 3.5v6c0 6-4 10-9 12-5-2-9-6-9-12v-6z" {s}/><path d="M{cx-4} {cy}l3 3 5.5-6" {s}/>',
        "doc": f'<path d="M{cx-8} {cy-11}h11l5 5v17h-16z" {s}/><path d="M{cx+3} {cy-11}v5h5M{cx-4} {cy+1}h8M{cx-4} {cy+6}h6" {s}/>',
        "spark": f'<path d="M{cx} {cy-11}l2.6 7.4 7.4 2.6-7.4 2.6-2.6 7.4-2.6-7.4-7.4-2.6 7.4-2.6z" {s}/>',
    }
    return g[kind]


PRINCIPLES = [
    ("db", "violet", "Make invalid states impossible", ["Rules live where they can't be", "bypassed: constraints, state", "machines, server-side pricing."]),
    ("target", "pink", "Kill the riskiest assumption first", ["Spike what can sink the project", "before any UI. Phase 0 proves it;", "panels come last."]),
    ("frame", "orange", "Constraints choose the stack", ["Shared hosting, LAN-only, Win32", "interop — the hard constraint", "picks the tools, not the hype."]),
    ("search", "sky", "Audit against the code", ["Docs drift. I verify specs against", "the code and pin every rule with", "a regression test."]),
    ("coin", "green", "Every cent adds up", ["Amounts in integer cents. Each sale", "keeps the price it was sold at; a", "retried payment never charges twice."]),
    ("spark", "amber", "Every incident leaves a lesson", ["Root cause, timeline, prevention", "— written down, not remembered."]),
    ("person", "sky", "Start from the real problem", ["Understand what hurts, what already", "exists and what isn't worth building", "— before writing a line of code."]),
    ("layers", "violet", "Fewer parts, fewer failures", ["The simplest thing that works wins:", "one binary over five services, a", "modular monolith over microservices."]),
    ("shield", "green", "Secure by default", ["Fail closed. Hashed tokens, rotating", "sessions, and someone else's data", "answers \"not found\", not \"forbidden\"."]),
    ("doc", "orange", "Decide in writing", ["Every key decision leaves a record:", "context, alternatives, and why", "the others were rejected."]),
]


def principles(t, theme):
    cw, ch, g = 432, 136, 16
    h = 56 + ((len(PRINCIPLES) + 1) // 2) * (ch + g) - g
    defs = ""
    b = section_title(2, "Principles", "how I make decisions", t, "violet")
    for i, (gl, col, title, body) in enumerate(PRINCIPLES):
        x, y = (i % 2) * (cw + g), 56 + (i // 2) * (ch + g)
        defs += (f'<radialGradient id="pg{i}" cx="1" cy="0" r="1"><stop offset="0" stop-color="{t[col]}" stop-opacity="{t["wash"]}"/>'
                 f'<stop offset="1" stop-color="{t[col]}" stop-opacity="0"/></radialGradient>')
        b += card(x, y, cw, ch, t)
        b += f'<rect x="{x+1}" y="{y+1}" width="{cw-2}" height="{ch-2}" rx="5" fill="url(#pg{i})"/>'
        b += f'<rect x="{x+22}" y="{y+22}" width="44" height="44" rx="6" fill="{t[col]}" fill-opacity="{t["tint"]}"/>'
        b += glyph(gl, x + 44, y + 44, t[col])
        b += text(x + 84, y + 42, title, 16.5, t["ink"], weight=700, extra='letter-spacing="-0.2"')
        b += lines(x + 84, y + 66, body, 13.5, t["muted"], 20)
    return doc(W, h, b, defs=defs)


# ---------------- OPEN SOURCE ----------------
def oss_title(t, theme):
    return doc(W, 44, section_title(3, "Open source", "public · MIT licensed", t, "pink"))


def dueo(t, theme):
    w, h = 432, 300
    defs = (f'<linearGradient id="dg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["violet"]}" stop-opacity=".13"/>'
            f'<stop offset="1" stop-color="{t["violet"]}" stop-opacity="0"/></linearGradient>')
    css = "@keyframes fill{from{stroke-dashoffset:var(--c)}}"
    b = card(0, 0, w, h, t, r=6) + f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="5" fill="url(#dg)"/>'
    b += text(26, 44, "Dueo", 24, t["ink"], weight=800, extra='letter-spacing="-0.6"')
    b += f'<rect x="{w-104}" y="26" width="80" height="24" rx="12" fill="{t["violet"]}" fill-opacity=".16"/>'
    b += text(w - 64, 42, "Rust · Svelte", 11, t["violet"], weight=600, anchor="middle")
    b += lines(26, 72, ["Self-hosted subscription tracker. Each service", "is a ring that fills until it renews."], 13.5, t["muted"], 20)
    rings = [("Hosting", .82, "violet"), ("Domain", .46, "pink"), ("Music", .64, "orange")]
    for i, (lab, p, col) in enumerate(rings):
        cx, cy, r = 80 + i * 136, 168, 40
        c = 2 * 3.14159 * r
        b += f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{t["border"]}" stroke-width="9"/>'
        b += (f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{t[col]}" stroke-width="9" stroke-linecap="round" '
              f'stroke-dasharray="{c:.1f}" stroke-dashoffset="{c*(1-p):.1f}" transform="rotate(-90 {cx} {cy})" '
              f'style="--c:{c:.1f};animation:fill 2.2s {i*.25}s cubic-bezier(.2,.8,.2,1) both"/>')
        b += text(cx, cy + 6, f"{int(p*30)}d", 17, t["ink"], weight=800, anchor="middle")
        b += text(cx, cy + 62, lab, 12, t["faint"], anchor="middle")
    for j, ic in enumerate(["Rust", "Svelte", "SQLite", "Docker"]):
        b += icon(ic, 26 + j * 34, h - 50, 26, theme)
    b += text(w - 26, h - 31, "github.com/Yelt-dev/dueo ↗", 12, t["muted"], anchor="end", cls="m")
    return doc(w, h, b, css, defs)


def lscrib(t, theme):
    w, h = 432, 300
    defs = (f'<linearGradient id="lg" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["green"]}" stop-opacity=".13"/>'
            f'<stop offset="1" stop-color="{t["green"]}" stop-opacity="0"/></linearGradient>')
    css = ("@keyframes wave{0%,100%{transform:scaleY(.35)}50%{transform:scaleY(1)}}"
           ".bar{transform-box:fill-box;transform-origin:center;animation:wave 1.4s ease-in-out infinite}")
    b = card(0, 0, w, h, t, r=6) + f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="5" fill="url(#lg)"/>'
    b += text(26, 44, "lscrib", 24, t["ink"], weight=800, extra='letter-spacing="-0.6"')
    b += f'<rect x="{w-112}" y="26" width="88" height="24" rx="12" fill="{t["green"]}" fill-opacity=".16"/>'
    b += text(w - 68, 42, "Python · AI", 11, t["green"], weight=600, anchor="middle")
    b += lines(26, 72, ["Local-first transcription with Whisper. Your", "audio never leaves your machine."], 13.5, t["muted"], 20)
    heights = [14, 26, 40, 22, 34, 48, 30, 18, 38, 52, 28, 16, 36, 44, 24, 12, 30, 42, 20, 34, 46, 26, 14, 32, 40, 22, 30, 18]
    for i, bh in enumerate(heights):
        x = 26 + i * 13.6
        b += f'<rect class="bar" x="{x:.1f}" y="{142-bh/2}" width="6" height="{bh}" rx="3" fill="{t["green"]}" style="animation-delay:{(i%7)*.12:.2f}s"/>'
    for k, (ts, line) in enumerate([("00:01", "Welcome back to the show."), ("00:04", "Today we talk about local AI…")]):
        y = 196 + k * 24
        b += text(26, y, ts, 11.5, t["green"], cls="m", weight=600)
        b += text(76, y, line, 13, t["ink"])
    for j, ic in enumerate(["Python", "FastAPI", "React", "Docker"]):
        b += icon(ic, 26 + j * 34, h - 50, 26, theme)
    b += text(w - 26, h - 31, "github.com/Yelt-dev/lscrib ↗", 12, t["muted"], anchor="end", cls="m")
    return doc(w, h, b, css, defs)


def markedit(t, theme):
    h = 112
    defs = (f'<linearGradient id="mg" x1="0" x2="1"><stop offset="0" stop-color="{t["orange"]}" stop-opacity=".10"/>'
            f'<stop offset=".6" stop-color="{t["orange"]}" stop-opacity="0"/></linearGradient>')
    b = card(0, 0, W, h, t, r=6) + f'<rect x="1" y="1" width="{W-2}" height="{h-2}" rx="5" fill="url(#mg)"/>'
    b += icon("Swift", 26, 30, 52, theme)
    b += text(98, 48, "MarkEdit Plus", 20, t["ink"], weight=800, extra='letter-spacing="-0.4"')
    b += f'<rect x="246" y="32" width="98" height="22" rx="11" fill="{t["orange"]}" fill-opacity="{t["tint"]}"/>'
    b += text(295, 47, "Fork · macOS", 11, t["orange"], weight=600, anchor="middle")
    b += lines(98, 74, ["Native Markdown editor I extended: live preview, HTML/PDF export, templates,",
                        "outline and inspector — 15 PRs, shipped as signed .dmg releases."], 13.5, t["muted"], 20)
    b += text(W - 26, 48, "github.com/Yelt-dev/MarkEditPlus ↗", 12, t["muted"], anchor="end", cls="m")
    return doc(W, h, b, defs=defs)


# ---------------- TRABAJO SELECCIONADO ----------------
WORK = [
    ("Booking SaaS", "Beauty & wellness", "violet", ["Serializable transactions against", "double-booking; advisory locks."], ["NextJS", "PostgreSQL", "Vercel"]),
    ("Hospital EHR", "Healthcare", "pink", ["RLS with FORCE, append-only audit", "log, clinical-record compliance."], ["NestJS", "Angular", "PostgreSQL"]),
    ("Medical media platform", "Pharma & doctors", "sky", ["Doctor directory, medical talks, ads", "engine, AI assistant, S3 library."], ["NestJS", "Angular", "NextJS"]),
    ("Pet-care marketplace", "Two-sided", "green", ["Verified hosts, bookings, payouts;", "API + two mobile apps, one monorepo."], ["NestJS", "expo", "PostgreSQL"]),
    ("Retail POS", "Commerce", "orange", ["Inventory ledger, immutable sales,", "67 ADRs, rules pinned by tests."], ["Laravel", "Angular", "MySQL"]),
    ("Restaurant ordering", "Food & delivery", "amber", ["Order state machine in Postgres,", "idempotency keys, encrypted data."], ["NextJS", "Supabase", "PostgreSQL"]),
    ("Real-estate leads", "Marketplace", "sky", ["Versioned, explainable lead", "scoring; wallet in integer cents."], ["GoLang", "NextJS", "PostgreSQL"]),
    ("PC lab control", "On-premise", "green", ["Threat-modeled kiosk lock,", "fail-closed agent, Win32 interop."], ["DotNet", "CS", "Svelte"]),
    ("Logistics ops", "Transport", "violet", ["Offline-first driver app, mobile", "outbox, event-sourced trips."], ["expo", "NestJS", "PostgreSQL"]),
    ("Retail ERP", "Multi-branch", "pink", ["Branch-scoped access, e-invoicing,", "face-recognition attendance."], ["Laravel", "Angular", "MySQL"]),
]


def work(t, theme):
    cw, ch, g = 432, 150, 16
    h = 56 + ((len(WORK) + 1) // 2) * (ch + g) - g + 40
    b = section_title(4, "Selected work", "client & partner systems · names withheld", t, "orange")
    for i, (name, dom, col, body, icons) in enumerate(WORK):
        x, y = (i % 2) * (cw + g), 56 + (i // 2) * (ch + g)
        b += card(x, y, cw, ch, t)
        b += f'<circle cx="{x+30}" cy="{y+33}" r="5" fill="{t[col]}"/>'
        b += text(x + 44, y + 38, name, 17, t["ink"], weight=700, extra='letter-spacing="-0.3"')
        pw = 18 + len(dom) * 6.6
        b += f'<rect x="{x+cw-22-pw}" y="{y+22}" width="{pw}" height="22" rx="11" fill="{t[col]}" fill-opacity="{t["tint"]}"/>'
        b += text(x + cw - 22 - pw / 2, y + 37, dom, 11, t[col], weight=600, anchor="middle")
        b += lines(x + 24, y + 70, body, 13.5, t["muted"], 20)
        for j, ic in enumerate(icons):
            b += icon(ic, x + 24 + j * 34, y + ch - 44, 26, theme)
    b += text(W / 2, h - 10, "Code is private — architecture notes available on request.", 12.5, t["faint"], anchor="middle")
    return doc(W, h, b)


# ---------------- STACK ----------------
STACK = [
    ("Frontend", "violet", [("TypeScript", "TS"), ("React", "React"), ("NextJS", "Next"), ("Angular", "Angular"), ("VueJS", "Vue"), ("Svelte", "Svelte"), ("Astro", "Astro"), ("TailwindCSS", "Tailwind")]),
    ("Backend", "pink", [("NestJS", "NestJS"), ("DotNet", ".NET"), ("Laravel", "Laravel"), ("GoLang", "Go"), ("Rust", "Rust"), ("Python", "Python"), ("FastAPI", "FastAPI"), ("GraphQL", "GraphQL")]),
    ("Data", "orange", [("PostgreSQL", "Postgres"), ("Supabase", "Supabase"), ("MySQL", "MySQL"), ("SQLite", "SQLite"), ("Redis", "Redis"), ("Prisma", "Prisma")]),
    ("Cloud & DevOps", "sky", [("AWS", "AWS"), ("Docker", "Docker"), ("GithubActions", "Actions"), ("Vercel", "Vercel"), ("Cloudflare", "Cloudflare"), ("Nginx", "Nginx"), ("Linux", "Linux")]),
    ("Mobile & desktop", "green", [("React", "RN"), ("expo", "Expo"), ("Flutter", "Flutter"), ("Swift", "Swift")]),
    ("AI & product", "amber", [("openai", "OpenAI"), ("stripe", "Stripe"), ("sentry", "Sentry"), ("playwright", "Playwright"), ("turborepo", "Turbo")]),
]


def stack(t, theme):
    cw, g, size, step = 432, 16, 38, 50
    hs = []
    for _, _, items in STACK:
        rows = (len(items) + 7) // 8
        hs.append(64 + rows * 70)
    row_h = [max(hs[i], hs[i + 1]) for i in range(0, len(hs), 2)]
    h = 56 + sum(row_h) + g * (len(row_h) - 1)
    b = section_title(5, "Stack", "what I reach for, by layer", t, "sky")
    y = 56
    for r in range(len(row_h)):
        for c in range(2):
            label, col, items = STACK[r * 2 + c]
            x = c * (cw + g)
            b += card(x, y, cw, row_h[r], t)
            b += f'<circle cx="{x+28}" cy="{y+29}" r="4" fill="{t[col]}"/>'
            b += text(x + 40, y + 34, label, 14, t["ink"], weight=700)
            for k, (ic, lab) in enumerate(items):
                ix = x + 24 + (k % 8) * step
                iy = y + 52 + (k // 8) * 70
                b += icon(ic, ix, iy, size, theme)
                b += text(ix + size / 2, iy + size + 15, lab, 9.5, t["faint"], anchor="middle")
        y += row_h[r] + g
    return doc(W, h, b)


# ---------------- CONTACTO ----------------
def contact_title(t, theme):
    return doc(W, 44, section_title(6, "Let's talk", "replies within a day", t, "green"))


def button(kind, t, theme):
    w, h = 300, 64
    col, lab, val = {"linkedin": ("sky", "LinkedIn", "in/yeltsinlopezv"),
                     "email": ("pink", "Email", "yeltsin.lopez94@gmail.com")}[kind]
    defs = (f'<linearGradient id="bg" x1="0" x2="1"><stop offset="0" stop-color="{t[col]}" stop-opacity=".10"/>'
            f'<stop offset="1" stop-color="{t[col]}" stop-opacity="0"/></linearGradient>')
    b = card(0, 0, w, h, t, r=6) + f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="5" fill="url(#bg)"/>'
    b += f'<rect x="14" y="14" width="36" height="36" rx="6" fill="{t[col]}"/>'
    if kind == "linkedin":
        b += text(32, 38.5, "in", 17, "#fff", weight=800, anchor="middle")
    else:
        b += '<rect x="23" y="24" width="18" height="14" rx="2.5" stroke="#fff" stroke-width="2"/><path d="M23.5 25.5l8.5 6.5 8.5-6.5" stroke="#fff" stroke-width="2" stroke-linejoin="round"/>'
    b += text(64, 28, lab, 12, t["faint"], weight=600)
    b += text(64, 47, val, 14, t["ink"], weight=600)
    b += text(w - 18, 39, "↗", 16, t["muted"], anchor="end")
    return doc(w, h, b, defs=defs)


if __name__ == "__main__":
    for theme, t in THEMES.items():
        files = {
            "hero": hero, "principles": principles, "oss": oss_title, "dueo": dueo, "lscrib": lscrib,
            "markedit": markedit, "work": work, "stack": stack, "contact": contact_title,
        }
        for name, fn in files.items():
            (OUT / f"{name}-{theme}.svg").write_text(fn(t, theme))
        for k in ("linkedin", "email"):
            (OUT / f"btn-{k}-{theme}.svg").write_text(button(k, t, theme))
    print("ok:", len(list(OUT.glob("*.svg"))), "svg")
