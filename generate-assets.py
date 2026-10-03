"""Genera los SVG del perfil (tema claro y oscuro) con estética de plano de arquitectura."""
from pathlib import Path
from xml.sax.saxutils import escape as esc

OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)
W = 880

THEMES = {
    "dark": dict(bg="#0B1220", panel="#0F192C", grid="#132036", grid2="#1A2B47", line="#24385A",
                 ink="#E6EDF7", muted="#8A9BB5", faint="#5B6E8C", cyan="#00C2D1", blue="#3B82F6"),
    "light": dict(bg="#F7F9FC", panel="#FFFFFF", grid="#E8EEF6", grid2="#D6E0EE", line="#C3D0E3",
                  ink="#0B1220", muted="#4A5B75", faint="#8394AE", cyan="#0E8FA0", blue="#2563EB"),
}
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"


def svg(h, body, t, extra_css=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img">
<style>
.s{{font-family:{SANS}}} .m{{font-family:{MONO}}}
{extra_css}
@media (prefers-reduced-motion: reduce){{ .anim{{animation:none!important}} .pk{{display:none}} }}
</style>
<defs>
<pattern id="g1" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="{t['grid']}" stroke-width="1"/></pattern>
<pattern id="g2" width="100" height="100" patternUnits="userSpaceOnUse"><rect width="100" height="100" fill="url(#g1)"/><path d="M100 0H0V100" fill="none" stroke="{t['grid2']}" stroke-width="1"/></pattern>
</defs>
<rect width="{W}" height="{h}" rx="14" fill="{t['bg']}"/>
<rect x="1" y="1" width="{W-2}" height="{h-2}" rx="13" fill="url(#g2)" stroke="{t['line']}"/>
{body}
</svg>"""


def crop_marks(h, t, inset=14, s=12):
    c = t["cyan"]
    pts = [(inset, inset, 1, 1), (W - inset, inset, -1, 1), (inset, h - inset, 1, -1), (W - inset, h - inset, -1, -1)]
    return "".join(f'<path d="M{x} {y+dy*s}V{y}H{x+dx*s}" fill="none" stroke="{c}" stroke-width="1.5"/>' for x, y, dx, dy in pts)


def sheet_header(n, title, sub, t, y=44):
    return (f'<text x="36" y="{y}" class="m" font-size="12" letter-spacing="2" fill="{t["cyan"]}">SHEET {n:02d}</text>'
            f'<text x="112" y="{y}" class="m" font-size="12" letter-spacing="2" fill="{t["faint"]}">/</text>'
            f'<text x="128" y="{y}" class="m" font-size="12" letter-spacing="2" fill="{t["ink"]}">{esc(title)}</text>'
            f'<text x="{W-36}" y="{y}" text-anchor="end" class="m" font-size="11" fill="{t["faint"]}">{esc(sub)}</text>'
            f'<line x1="36" y1="{y+14}" x2="{W-36}" y2="{y+14}" stroke="{t["line"]}" stroke-dasharray="2 4"/>')


def lines(x, y, txt_lines, size, fill, lh, cls="s", weight=400):
    return "".join(f'<text x="{x}" y="{y+i*lh}" class="{cls}" font-size="{size}" font-weight="{weight}" fill="{fill}">{esc(l)}</text>'
                   for i, l in enumerate(txt_lines))


# ---------- HERO ----------
def hero(t):
    h = 340
    b = crop_marks(h, t)
    b += f'<text x="44" y="62" class="m" font-size="12" letter-spacing="2.5" fill="{t["cyan"]}">PROFILE.SPEC  ·  REV 2026.10</text>'
    b += f'<text x="42" y="118" class="s" font-size="46" font-weight="700" fill="{t["ink"]}" letter-spacing="-1">Yeltsin López</text>'
    b += f'<text x="44" y="152" class="s" font-size="20" font-weight="500" fill="{t["blue"]}">Full-Stack Product Engineer</text>'
    b += lines(44, 192, ["I design and ship SaaS end to end — from the client's",
                         "problem to the Postgres policy that enforces it."], 15.5, t["muted"], 24)
    # meta chips
    x = 44
    for c in ["7 YRS", "API", "WEB", "MOBILE", "CLOUD", "MX"]:
        w = 14 + len(c) * 8
        b += f'<rect x="{x}" y="250" width="{w}" height="24" rx="4" fill="none" stroke="{t["line"]}"/>'
        b += f'<text x="{x+w/2}" y="266" text-anchor="middle" class="m" font-size="11" letter-spacing="1" fill="{t["muted"]}">{c}</text>'
        x += w + 8
    # diagram (right)
    bx = 560
    nodes = [(bx, 70, "client", "web · mobile"), (bx, 150, "api", "auth · rules"), (bx, 230, "postgres", "rls · tx")]
    for i, (nx, ny, a, s) in enumerate(nodes):
        b += f'<rect x="{nx}" y="{ny}" width="150" height="50" rx="8" fill="{t["panel"]}" stroke="{t["cyan"] if i==2 else t["line"]}"/>'
        b += f'<text x="{nx+14}" y="{ny+22}" class="m" font-size="13" font-weight="600" fill="{t["ink"]}">{a}</text>'
        b += f'<text x="{nx+14}" y="{ny+38}" class="m" font-size="11" fill="{t["faint"]}">{s}</text>'
        if i < 2:
            b += f'<line x1="{nx+75}" y1="{ny+50}" x2="{nx+75}" y2="{ny+80}" stroke="{t["faint"]}" stroke-width="1.3" stroke-dasharray="3 3"/>'
            b += f'<circle class="pk anim" cx="{nx+75}" cy="{ny+50}" r="3" fill="{t["cyan"]}" style="animation:down 2.4s {i*1.2}s linear infinite"/>'
    # side annotation
    b += f'<line x1="722" y1="95" x2="760" y2="95" stroke="{t["faint"]}"/><line x1="760" y1="95" x2="760" y2="255" stroke="{t["faint"]}"/><line x1="722" y1="255" x2="760" y2="255" stroke="{t["faint"]}"/>'
    b += f'<text x="772" y="170" class="m" font-size="10.5" fill="{t["faint"]}">rules live</text><text x="772" y="185" class="m" font-size="10.5" fill="{t["faint"]}">in the data</text>'
    # title block
    tb_x, tb_y = 560, 296
    b += f'<rect x="{tb_x}" y="{tb_y}" width="284" height="26" fill="{t["panel"]}" stroke="{t["line"]}"/>'
    for i, (k, v) in enumerate([("DRAWN", "Y.LÓPEZ"), ("SCALE", "1:1"), ("SHEET", "01/06")]):
        cx = tb_x + i * 95
        if i: b += f'<line x1="{cx}" y1="{tb_y}" x2="{cx}" y2="{tb_y+26}" stroke="{t["line"]}"/>'
        b += f'<text x="{cx+8}" y="{tb_y+17}" class="m" font-size="9.5" fill="{t["faint"]}">{k}</text>'
        b += f'<text x="{cx+88}" y="{tb_y+17}" text-anchor="end" class="m" font-size="10" fill="{t["ink"]}">{v}</text>'
    css = "@keyframes down{0%{transform:translateY(0);opacity:0}15%{opacity:1}85%{opacity:1}100%{transform:translateY(30px);opacity:0}}"
    return svg(h, b, t, css)


# ---------- PRINCIPLES ----------
PRINCIPLES = [
    ("Let the database enforce it", ["Row-Level Security with FORCE,", "serializable bookings, advisory locks,", "prices computed in SQL."]),
    ("Kill the riskiest assumption first", ["Spike what can sink the project", "before any UI. Phase 0 proves it;", "panels come last."]),
    ("Constraints choose the stack", ["Shared hosting, LAN-only, Win32", "interop — the hard constraint picks", "the tools, not the hype."]),
    ("Audit against the code", ["Docs drift. I verify specs against", "the code and pin every rule with a", "regression test."]),
    ("Money is never a float", ["Integer cents, price snapshots and", "idempotency keys. A retry never", "charges twice."]),
    ("Every incident leaves a lesson", ["Root cause, timeline, prevention —", "written down, not remembered."]),
]


def detail_bubble(cx, cy, n, ref, t, r=21):
    """Marcador de detalle de plano: círculo partido, número arriba y hoja abajo."""
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{t["bg"]}" stroke="{t["cyan"]}" stroke-width="1.3"/>'
            f'<line x1="{cx-r}" y1="{cy}" x2="{cx+r}" y2="{cy}" stroke="{t["cyan"]}" stroke-width="1.3"/>'
            f'<text x="{cx}" y="{cy-6}" text-anchor="middle" class="m" font-size="11" font-weight="700" fill="{t["ink"]}">{n}</text>'
            f'<text x="{cx}" y="{cy+14}" text-anchor="middle" class="m" font-size="9" fill="{t["faint"]}">{ref}</text>')


def principles(t):
    cols, cw, ch, gx, gy = 2, 396, 118, 16, 16
    rows = (len(PRINCIPLES) + 1) // 2
    h = 84 + rows * (ch + gy) + 20
    b = sheet_header(2, "PRINCIPLES", "how I make decisions", t)
    for i, (title, body) in enumerate(PRINCIPLES):
        x = 36 + (i % cols) * (cw + gx)
        y = 80 + (i // cols) * (ch + gy)
        b += f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="10" fill="{t["panel"]}" stroke="{t["line"]}"/>'
        b += detail_bubble(x + 40, y + 42, f"{i+1:02d}", "S-02", t)
        b += f'<line x1="{x+40}" y1="{y+63}" x2="{x+40}" y2="{y+ch-18}" stroke="{t["line"]}" stroke-dasharray="2 3"/>'
        b += f'<text x="{x+78}" y="{y+38}" class="s" font-size="16" font-weight="600" fill="{t["ink"]}">{esc(title)}</text>'
        b += lines(x + 78, y + 62, body, 13.5, t["muted"], 20)
    return svg(h, b, t)


# ---------- OSS CARDS ----------
OSS = {
    "dueo": ("DUEO", "Subscriptions, as progress rings.",
             ["Self-hosted tracker with reminders on web,", "Telegram and email. Multi-user, ships as", "a single binary with the UI embedded."],
             ["Rust", "Axum", "SQLite", "Svelte 5", "SSE"]),
    "lscrib": ("LSCRIB", "Transcription that stays local.",
               ["Drop audio or video, get an editable", "transcript + SRT/VTT/TXT/MD. Whisper runs", "on your machine — no cloud, no account."],
               ["Python", "FastAPI", "faster-whisper", "React"]),
}


def oss_card(key, t):
    cw, h = 430, 236
    name, tag, body, stack = OSS[key]
    b = f'<rect width="{cw}" height="{h}" rx="14" fill="{t["bg"]}"/>'
    b += f'<rect x="1" y="1" width="{cw-2}" height="{h-2}" rx="13" fill="url(#g2)" stroke="{t["line"]}"/>'
    b += f'<circle cx="34" cy="38" r="5" fill="{t["cyan"]}"/>'
    b += f'<text x="48" y="43" class="m" font-size="13" font-weight="700" letter-spacing="2.5" fill="{t["ink"]}">{name}</text>'
    b += f'<text x="{cw-28}" y="43" text-anchor="end" class="m" font-size="11" fill="{t["faint"]}">open source ↗</text>'
    b += f'<text x="28" y="84" class="s" font-size="19" font-weight="600" fill="{t["ink"]}">{esc(tag)}</text>'
    b += lines(28, 114, body, 13.5, t["muted"], 21)
    x = 28
    for s in stack:
        w = 16 + len(s) * 7.4
        b += f'<rect x="{x}" y="186" width="{w}" height="24" rx="12" fill="none" stroke="{t["cyan"]}" stroke-opacity=".6"/>'
        b += f'<text x="{x+w/2}" y="202" text-anchor="middle" class="m" font-size="11" fill="{t["cyan"]}">{esc(s)}</text>'
        x += w + 8
    return svg(h, b, t).replace(f'width="{W}"', f'width="{cw}"', 1).replace(f'viewBox="0 0 {W} {h}"', f'viewBox="0 0 {cw} {h}"', 1) \
        .replace(f'<rect width="{W}" height="{h}" rx="14" fill="{t["bg"]}"/>\n<rect x="1" y="1" width="{W-2}" height="{h-2}" rx="13" fill="url(#g2)" stroke="{t["line"]}"/>\n', "")


def oss_header(t):
    h = 76
    return svg(h, sheet_header(3, "OPEN SOURCE", "public repos · MIT", t), t)


# ---------- SELECTED WORK ----------
WORK = [
    ("Booking SaaS", "beauty & wellness", ["Serializable tx against double-booking,", "advisory locks, incident postmortems."], "Next.js · Postgres"),
    ("Hospital EHR", "multi-tenant", ["RLS with FORCE, append-only audit log,", "clinical-record compliance mapping."], "NestJS · Angular"),
    ("Retail POS", "multi-tenant", ["Inventory ledger, immutable sales,", "67 ADRs, rules pinned by tests."], "Laravel · Angular"),
    ("Restaurant ordering", "free-tier first", ["Order state machine in Postgres,", "idempotency keys, encrypted bank data."], "Next.js · Supabase"),
    ("Real-estate leads", "wallet + scoring", ["Versioned, explainable lead scoring;", "money in cents with ISO-4217."], "Go · sqlc · Next.js"),
    ("PC lab control", "LAN · in production", ["Threat-modeled kiosk lock, fail-closed", "agent, Win32 interop, append-only clock."], ".NET 10 · Avalonia"),
    ("Logistics ops", "offline-first", ["Mobile outbox, event-sourced trip status,", "conflicts kept, never dropped."], "Expo · NestJS"),
    ("ERP for retail chain", "multi-branch", ["Branch-scoped access against BOLA,", "e-invoicing, face-recognition attendance."], "Laravel · Angular"),
]


def work(t):
    cols, cw, ch, gx, gy = 2, 396, 128, 16, 16
    rows = (len(WORK) + 1) // 2
    h = 84 + rows * (ch + gy) + 36
    b = sheet_header(4, "SELECTED WORK", "client & partner systems · names withheld", t)
    for i, (name, tag, body, stack) in enumerate(WORK):
        x = 36 + (i % cols) * (cw + gx)
        y = 80 + (i // cols) * (ch + gy)
        b += f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="10" fill="{t["panel"]}" stroke="{t["line"]}"/>'
        b += f'<text x="{x+20}" y="{y+32}" class="s" font-size="16" font-weight="600" fill="{t["ink"]}">{esc(name)}</text>'
        b += f'<text x="{x+cw-20}" y="{y+32}" text-anchor="end" class="m" font-size="10.5" fill="{t["cyan"]}">{esc(tag.upper())}</text>'
        b += lines(x + 20, y + 58, body, 13, t["muted"], 20)
        b += f'<line x1="{x+20}" y1="{y+ch-32}" x2="{x+cw-20}" y2="{y+ch-32}" stroke="{t["line"]}" stroke-dasharray="2 4"/>'
        b += f'<text x="{x+20}" y="{y+ch-13}" class="m" font-size="11" fill="{t["faint"]}">{esc(stack)}</text>'
    b += f'<text x="{W/2}" y="{h-22}" text-anchor="middle" class="m" font-size="11" fill="{t["faint"]}">code is private — architecture notes available on request</text>'
    return svg(h, b, t)


# ---------- STACK (layered diagram) ----------
LAYERS = [
    ("CLIENT", ["TypeScript", "React", "Next.js", "Angular", "Vue · micro-frontends", "Svelte 5", "Astro", "Tailwind"]),
    ("MOBILE", ["Expo", "React Native", "Flutter"]),
    ("SERVICES", ["NestJS", ".NET / C#", "Laravel", "Go", "Rust · Axum", "FastAPI", "GraphQL"]),
    ("DATA", ["PostgreSQL · RLS", "Supabase", "MySQL", "SQLite", "Redis · BullMQ", "Prisma", "Drizzle"]),
    ("PLATFORM", ["AWS", "Docker", "GitHub Actions", "Vercel", "Hetzner", "Cloudflare R2", "Nginx"]),
    ("PRODUCT", ["Stripe", "OpenAI API", "Whisper · local", "Sentry", "Playwright", "Turborepo"]),
]


def stack(t):
    rh, gy = 46, 10
    h = 84 + len(LAYERS) * (rh + gy) + 16
    b = sheet_header(5, "STACK", "by layer, not by logo", t)
    for i, (layer, items) in enumerate(LAYERS):
        y = 78 + i * (rh + gy)
        b += f'<rect x="36" y="{y}" width="{W-72}" height="{rh}" rx="8" fill="{t["panel"]}" stroke="{t["line"]}"/>'
        b += f'<text x="54" y="{y+28}" class="m" font-size="11" letter-spacing="2" fill="{t["cyan"]}">{layer}</text>'
        x = 160
        for it in items:
            w = 14 + len(it) * 7.0
            b += f'<rect x="{x}" y="{y+11}" width="{w}" height="24" rx="5" fill="{t["bg"]}" stroke="{t["line"]}"/>'
            b += f'<text x="{x+w/2}" y="{y+27}" text-anchor="middle" class="m" font-size="11" fill="{t["ink"]}">{esc(it)}</text>'
            x += w + 7
    return svg(h, b, t)


def footer(t):
    h = 76
    b = sheet_header(6, "CONTACT", "open to senior & architecture roles", t)
    return svg(h, b, t)


def button(label, value, t):
    bw, h = 300, 56
    b = f'<rect x=".5" y=".5" width="{bw-1}" height="{h-1}" rx="10" fill="{t["panel"]}" stroke="{t["line"]}"/>'
    b += f'<circle cx="26" cy="28" r="6" fill="none" stroke="{t["cyan"]}" stroke-width="1.3"/><circle cx="26" cy="28" r="2" fill="{t["cyan"]}"/>'
    b += f'<text x="44" y="24" class="m" font-size="10" letter-spacing="2" fill="{t["cyan"]}">{label}</text>'
    b += f'<text x="44" y="42" class="m" font-size="13" fill="{t["ink"]}">{esc(value)}</text>'
    b += f'<text x="{bw-18}" y="35" text-anchor="end" class="m" font-size="14" fill="{t["faint"]}">↗</text>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{bw}" height="{h}" viewBox="0 0 {bw} {h}" role="img">'
            f'<style>.m{{font-family:{MONO}}}</style>{b}</svg>')


for name, t in THEMES.items():
    (OUT / f"hero-{name}.svg").write_text(hero(t))
    (OUT / f"principles-{name}.svg").write_text(principles(t))
    (OUT / f"oss-{name}.svg").write_text(oss_header(t))
    for k in OSS:
        (OUT / f"{k}-{name}.svg").write_text(oss_card(k, t))
    (OUT / f"work-{name}.svg").write_text(work(t))
    (OUT / f"stack-{name}.svg").write_text(stack(t))
    (OUT / f"contact-{name}.svg").write_text(footer(t))
    (OUT / f"btn-linkedin-{name}.svg").write_text(button("LINKEDIN", "in/yeltsinlopezv", t))
    (OUT / f"btn-email-{name}.svg").write_text(button("EMAIL", "yeltsin.lopez94@gmail.com", t))
print(sorted(p.name for p in OUT.iterdir()))
