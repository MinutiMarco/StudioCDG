"""Parsing dei blocchi ```schema``` nei riassunti e rendering come immagini per il Word."""
import json, re, os, textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon, Circle

# ---- palette sobria, leggibile in stampa ----
INK      = "#1c2733"
MUTED    = "#5b6b7c"
LINE     = "#c3ced9"
BG       = "#ffffff"
FILL     = ["#e8eef5", "#e4efe8", "#f6ece2", "#efe8f2", "#e6f0f2", "#f2ece5"]
EDGE     = ["#7d9bbd", "#6fa383", "#c89a6d", "#9b83ad", "#6fa0aa", "#b39a7d"]
ACCENT   = "#2c4a6b"

def parse_schemi(md_text):
    out = []
    for m in re.finditer(r"```schema\s*\n(.*?)\n```", md_text, re.S):
        try:
            out.append(json.loads(m.group(1)))
        except json.JSONDecodeError as e:
            print("  ! schema non valido:", e)
    return out

def strip_schemi(md_text):
    return re.sub(r"```schema\s*\n.*?\n```\s*", "", md_text, flags=re.S)

def _wrap(s, w):
    return "\n".join("\n".join(textwrap.wrap(l, w)) or "" for l in str(s).split("\n"))

def _fig(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    ax.axis("off"); fig.patch.set_facecolor(BG)
    return fig, ax

def _title(ax, t):
    ax.text(50, 97, t, ha="center", va="top", fontsize=11.5, weight="bold", color=INK)

def _note(ax, s, y=2.5):
    if s:
        ax.text(50, y, _wrap(s, 110), ha="center", va="bottom", fontsize=7.5,
                color=MUTED, style="italic")

def _box(ax, x, y, w, h, label, detail=None, i=0, fs=9):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.6",
                                linewidth=1.1, edgecolor=EDGE[i % len(EDGE)],
                                facecolor=FILL[i % len(FILL)]))
    cw = max(int(w / 1.05), 12)
    if detail:
        ax.text(x + w/2, y + h*0.68, _wrap(label, cw), ha="center", va="center",
                fontsize=fs, weight="bold", color=INK)
        ax.text(x + w/2, y + h*0.28, _wrap(detail, cw + 4), ha="center", va="center",
                fontsize=fs - 1.7, color=MUTED)
    else:
        ax.text(x + w/2, y + h/2, _wrap(label, cw), ha="center", va="center",
                fontsize=fs, weight="bold", color=INK)

def _arrow(ax, x1, y1, x2, y2, style="-|>"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                                 mutation_scale=13, linewidth=1.2, color=ACCENT))

# ---------------- tipi di schema ----------------

def draw_flow(s, path):
    steps = s["steps"]; n = len(steps)
    cols = 1 if n <= 4 else 2
    rows = (n + cols - 1) // cols
    fig, ax = _fig(9, max(2.4, 1.15 * rows + 1.1))
    _title(ax, s["title"])
    top, bot = 88, (14 if s.get("note") else 8)
    hgt = (top - bot) / rows
    bh = hgt * 0.72
    for k, st in enumerate(steps):
        r, c = k // cols, k % cols
        w = 40 if cols == 2 else 74
        x = (6 + c * 50) if cols == 2 else 13
        y = top - (r + 1) * hgt + (hgt - bh) / 2
        _box(ax, x, y, w, bh, st["label"], st.get("detail"), k)
        if k < n - 1:
            if (k + 1) % cols == 0 and cols == 2:
                _arrow(ax, x + w/2, y, x + w/2 - 44, y - (hgt - bh))
            elif cols == 2:
                _arrow(ax, x + w, y + bh/2, x + w + 10, y + bh/2)
            else:
                _arrow(ax, x + w/2, y, x + w/2, y - (hgt - bh))
    _note(ax, s.get("note"))
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor=BG); plt.close(fig)

def draw_cycle(s, path):
    nodes = s["nodes"]; n = len(nodes)
    import math
    fig, ax = _fig(8, 6.4)
    _title(ax, s["title"])
    cx, cy, R = 50, 50, 27
    pts = []
    for k in range(n):
        a = math.pi/2 - 2*math.pi*k/n
        pts.append((cx + R*math.cos(a)*1.35, cy + R*math.sin(a)))
    for k, (x, y) in enumerate(pts):
        w, h = 34, 15
        _box(ax, x - w/2, y - h/2, w, h, nodes[k].split("\n")[0],
             "\n".join(nodes[k].split("\n")[1:]) or None, k, fs=8.5)
    for k in range(n):
        x1, y1 = pts[k]; x2, y2 = pts[(k+1) % n]
        dx, dy = x2-x1, y2-y1
        L = (dx*dx+dy*dy) ** .5 or 1
        pad = 11
        _arrow(ax, x1+dx/L*pad, y1+dy/L*pad, x2-dx/L*pad, y2-dy/L*pad)
    _note(ax, s.get("note"))
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor=BG); plt.close(fig)

def draw_hierarchy(s, path):
    br = s["branches"]; n = len(br)
    maxch = max(len(b.get("children", [])) for b in br)
    fig, ax = _fig(10.5, max(3.2, 0.62 * maxch + 2.2))
    _title(ax, s["title"])
    _box(ax, 33, 80, 34, 11, s.get("root", ""), None, 0, fs=10.5)
    lows = []
    colw = 96 / n
    for i, b in enumerate(br):
        x = 2 + i * colw
        w = colw - 3
        _box(ax, x, 64, w, 11, b["label"], None, i + 1, fs=8.8)
        _arrow(ax, 50, 80, x + w/2, 75.5)
        y = 60
        lows.append(y)
        for ch in b.get("children", []):
            lines = _wrap(ch, max(int(w/1.0), 14))
            nl = lines.count("\n") + 1
            h = 3.6 + 2.6 * nl
            y -= h + 1.6
            ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1",
                                        linewidth=0.8, edgecolor=LINE, facecolor="#fbfcfd"))
            ax.text(x + w/2, y + h/2, lines, ha="center", va="center", fontsize=7.4, color=INK)
            lows[-1] = y
    _note(ax, s.get("note"), max(1, min(lows) - 6))
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor=BG); plt.close(fig)

def draw_matrix(s, path):
    q = {d["pos"]: d for d in s["quadrants"]}
    fig, ax = _fig(8.6, 6.6)
    _title(ax, s["title"])
    L, B, W, H = 16, 16, 74, 68
    for j, pos in enumerate(["tl", "tr", "bl", "br"]):
        d = q.get(pos)
        if not d: continue
        x = L if pos[1] == "l" else L + W/2
        y = B + H/2 if pos[0] == "t" else B
        _box(ax, x + .6, y + .6, W/2 - 1.2, H/2 - 1.2, d["label"], d.get("detail"), j, fs=9)
    ax.plot([L, L+W], [B, B], color=INK, lw=1.1)
    ax.plot([L, L], [B, B+H], color=INK, lw=1.1)
    xa, ya = s.get("xaxis", ["", ""]), s.get("yaxis", ["", ""])
    ax.text(L + W/4, B - 3.5, _wrap(xa[0], 26), ha="center", va="top", fontsize=8, color=MUTED)
    ax.text(L + 3*W/4, B - 3.5, _wrap(xa[1], 26), ha="center", va="top", fontsize=8, color=MUTED)
    ax.text(L - 3, B + H/4, _wrap(ya[0], 24), ha="right", va="center", fontsize=8,
            color=MUTED, rotation=90)
    ax.text(L - 3, B + 3*H/4, _wrap(ya[1], 24), ha="right", va="center", fontsize=8,
            color=MUTED, rotation=90)
    _note(ax, s.get("note"))
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor=BG); plt.close(fig)

def draw_pyramid(s, path):
    lv = s["levels"]; n = len(lv)
    fig, ax = _fig(8.6, max(2.6, 0.95 * n + 1.4))
    _title(ax, s["title"])
    top, bot = 87, (16 if s.get("note") else 10)
    hgt = (top - bot) / n
    for k, t in enumerate(lv):
        frac = 0.42 + 0.58 * (k + 1) / n
        w = 86 * frac
        y = top - (k + 1) * hgt
        _box(ax, 50 - w/2, y + 1.2, w, hgt - 2.4, t, None, k, fs=8.8)
    _note(ax, s.get("note"))
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor=BG); plt.close(fig)

def draw_tradeoff(s, path):
    ax_list = s["axes"]; n = len(ax_list)
    fig, ax = _fig(9.5, max(2.6, 0.62 * n + 1.2))
    _title(ax, s["title"])
    top, bot = 88, 8
    hgt = (top - bot) / n
    for k, (lab, a, b) in enumerate(ax_list):
        y = top - (k + 0.5) * hgt
        ax.text(1, y, _wrap(lab, 34), ha="left", va="center", fontsize=7.8, color=INK, weight="bold")
        x0, x1 = 37, 97
        ax.plot([x0, x1], [y, y], color=LINE, lw=1.1, zorder=1)
        for xx in (x0, x1):
            ax.add_patch(Circle((xx, y), 0.9, color=ACCENT, zorder=2))
        ax.text(x0 - 1.5, y, a, ha="right", va="center", fontsize=7.2, color=MUTED)
        ax.text(x1 + 1.5, y, b, ha="left", va="center", fontsize=7.2, color=MUTED)
    _note(ax, s.get("note"))
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor=BG); plt.close(fig)

DRAW = {"flow": draw_flow, "cycle": draw_cycle, "hierarchy": draw_hierarchy,
        "matrix": draw_matrix, "pyramid": draw_pyramid, "tradeoff": draw_tradeoff}

def render(schema, path):
    """Ritorna True se lo schema è stato reso come immagine, False se va reso come tabella."""
    fn = DRAW.get(schema["type"])
    if not fn:
        return False
    fn(schema, path)
    return True
