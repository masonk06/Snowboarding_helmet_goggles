"""WIRELESS / BLUETOOTH OPTION: build SnowHUD_Wireless.kicad_pcb (goggle + jacket boards, no tether),
placement, grid maze routing, GND pours."""
import sys, math, heapq, os, re
import pcbnew

# Usage (KiCad 10 bundled Python):
#   kicad-cli sch export netlist --format kicadsexpr -o SnowHUD_Wireless.net ../SnowHUD_Wireless.kicad_sch
#   "C:\Program Files\KiCad\10.0\bin\python.exe" build_pcb.py SnowHUD_Wireless.net
# WARNING: regenerates ../SnowHUD_Wireless.kicad_pcb from scratch, overwriting manual edits.
PRJ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
NETLIST = sys.argv[1]
OUT = os.path.join(PRJ, "SnowHUD_Wireless.kicad_pcb")
STOCK = os.environ.get("KICAD10_FOOTPRINT_DIR", r"C:\Program Files\KiCad\10.0\share\kicad\footprints")
POWER = r"GND|5V|3V3|/VBAT$|BAT_RAW"   # nets routed 0.5 mm
MM = pcbnew.FromMM
V = lambda x, y: pcbnew.VECTOR2I(MM(x), MM(y))

# ---------------- netlist ----------------
def sexp(text):
    tok = re.findall(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()]+', text)
    st = [[]]
    for t in tok:
        if t == "(":
            st.append([])
        elif t == ")":
            x = st.pop(); st[-1].append(x)
        else:
            st[-1].append(t[1:-1].replace('\\"', '"') if t.startswith('"') else t)
    return st[0][0]

def find(node, key):
    return [c for c in node if isinstance(c, list) and c and c[0] == key]

nl = sexp(open(NETLIST, encoding="utf-8").read())
pinnet = {}          # (ref, pin) -> net name
comps = {}           # ref -> (value, footprint, symbol uuid)
for comp in find(find(nl, "components")[0], "comp"):
    ref = find(comp, "ref")[0][1]
    val = find(comp, "value")[0][1]
    fpl = find(comp, "footprint"); fp = fpl[0][1] if fpl else ""
    tst = find(comp, "tstamps")
    dsc = find(comp, "description")
    comps[ref] = (val, fp, tst[0][1] if tst else "", dsc[0][1] if dsc and len(dsc[0]) > 1 else "")
for net in find(find(nl, "nets")[0], "net"):
    name = find(net, "name")[0][1]
    for node in find(net, "node"):
        pinnet[(find(node, "ref")[0][1], find(node, "pin")[0][1])] = name

board = pcbnew.CreateEmptyBoard()
board.SetCopperLayerCount(2)
nets = {}
def NET(name):
    if name not in nets:
        ni = pcbnew.NETINFO_ITEM(board, name); board.Add(ni); nets[name] = ni
    return nets[name]

def libpath(nick):
    return os.path.join(PRJ, "SnowHUD_Wireless.pretty") if nick == "SnowHUD_Wireless" else os.path.join(STOCK, nick + ".pretty")

def place(ref, x, y, rot=0, fpid=None, value=None):
    if ref in comps:
        value, fpid, tstamp, desc = comps[ref]
    nick, name = fpid.split(":")
    fp = pcbnew.FootprintLoad(libpath(nick), name)
    assert fp, fpid
    fp.SetFPID(pcbnew.LIB_ID(nick, name))
    fp.SetReference(ref); fp.SetValue(value)
    board.Add(fp)
    fp.SetPosition(V(x, y))
    if rot: fp.SetOrientationDegrees(rot)
    if ref in comps:
        fp.SetPath(pcbnew.KIID_PATH("/" + comps[ref][2]))
        fp.SetLibDescription(desc)
        try:
            fld = fp.GetField(pcbnew.FIELD_T_DESCRIPTION); fld.SetText(desc); fld.SetVisible(False)
        except Exception as e:
            fp.SetField("Description", desc)
        try:
            fp.SetSheetname("/"); fp.SetSheetfile("SnowHUD_Wireless.kicad_sch")
        except Exception:
            pass
        for p in fp.Pads():
            n = pinnet.get((ref, p.GetNumber()))
            if n: p.SetNet(NET(n))
    else:  # board-only part (mounting holes)
        fp.SetBoardOnly(True); fp.SetExcludedFromBOM(True); fp.SetExcludedFromPosFiles(True)
        fp.Reference().SetVisible(False)
    return fp

def edge_rect(x0, y0, x1, y1, r=1.5):
    # rounded rectangle outline on Edge.Cuts
    def seg(a, b):
        s = pcbnew.PCB_SHAPE(board); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetLayer(pcbnew.Edge_Cuts)
        s.SetStart(V(*a)); s.SetEnd(V(*b)); s.SetWidth(MM(0.1)); board.Add(s)
    def arc(c, st, mid, en):
        s = pcbnew.PCB_SHAPE(board); s.SetShape(pcbnew.SHAPE_T_ARC); s.SetLayer(pcbnew.Edge_Cuts)
        s.SetArcGeometry(V(*st), V(*mid), V(*en)); s.SetWidth(MM(0.1)); board.Add(s)
    k = r * (1 - math.sqrt(0.5))
    seg((x0 + r, y0), (x1 - r, y0)); seg((x1, y0 + r), (x1, y1 - r))
    seg((x1 - r, y1), (x0 + r, y1)); seg((x0, y1 - r), (x0, y0 + r))
    arc(None, (x1 - r, y0), (x1 - k, y0 + k), (x1, y0 + r))
    arc(None, (x1, y1 - r), (x1 - k, y1 - k), (x1 - r, y1))
    arc(None, (x0 + r, y1), (x0 + k, y1 - k), (x0, y1 - r))
    arc(None, (x0, y0 + r), (x0 + k, y0 + k), (x0 + r, y0))

def text(t, x, y, layer=pcbnew.F_SilkS, size=1.0, rot=0):
    tx = pcbnew.PCB_TEXT(board); tx.SetText(t); tx.SetPosition(V(x, y)); tx.SetLayer(layer)
    tx.SetTextSize(V(size, size)); tx.SetTextThickness(MM(0.15 * size))
    if rot: tx.SetTextAngleDegrees(rot)
    if layer == pcbnew.B_SilkS: tx.SetMirrored(True)
    board.Add(tx)

HOLE = "MountingHole:MountingHole_2.2mm_M2_Pad"

# ================= GOGGLE BOARD =================
def refpos(fp, x, y, visible=True):
    r = fp.Reference(); r.SetPosition(V(x, y)); r.SetVisible(visible)

GB = (101.6, 101.6, 132.08, 134.112)
edge_rect(*GB)
place("U1", 116.84, 111.76)                 # XIAO ESP32S3, USB-C at top edge
refpos(place("DS1", 104.14, 104.14), 104.14, 121.6)   # left OLED header
refpos(place("DS2", 129.54, 104.14), 129.54, 121.6)   # right OLED header
refpos(place("TP1", 113.0, 124.3), 0, 0, False)       # BAT+ wire pad -> XIAO underside
refpos(place("TP2", 120.68, 124.3), 0, 0, False)      # BAT- wire pad -> XIAO underside
refpos(place("R1", 124.46, 123.4), 127.4, 123.4)
refpos(place("R2", 124.46, 125.0), 127.4, 125.0)
refpos(place("C1", 124.46, 126.6), 127.4, 126.6)
refpos(place("J5", 110.0, 129.6), 0, 0, False)        # LiPo connector
refpos(place("SW1", 117.5, 130.0), 0, 0, False)       # power switch
place("H1", 104.4, 131.3, fpid=HOLE, value="M2")
place("H2", 129.28, 131.3, fpid=HOLE, value="M2")
text("OLED L", 106.6, 112.0, size=0.8, rot=90)
text("OLED R", 127.14, 112.0, size=0.8, rot=90)
text("B+", 113.0, 126.3, size=0.8)
text("B-", 120.68, 126.3, size=0.8)
text("LIPO", 108.9, 126.6, size=0.8)
text("PWR", 119.5, 133.2, size=0.8)
for k, t in enumerate(["SnowHUD", "GOGGLE", "WIRELESS", "OPTION W0.1", "B+/B- WIRE TO", "XIAO BAT PADS"]):
    text(t, 116.84, 106.5 + 1.6 * k, pcbnew.B_SilkS, 0.8)

# ================= JACKET BOARD =================
JB = (96.52, 139.7, 162.56, 203.2)
edge_rect(*JB)
place("U2", 147.32, 172.72)                 # ESP32-S3-DevKitC-1, USB at bottom edge
place("U3", 124.46, 146.05)                 # GPS
place("U4", 124.46, 160.02)                 # MPU6050
place("U5", 124.46, 185.42)                 # BMP280
place("H3", 99.32, 142.5, fpid=HOLE, value="M2")
place("H4", 99.32, 200.4, fpid=HOLE, value="M2")
place("H5", 130.81, 142.5, fpid=HOLE, value="M2")
place("H6", 130.81, 200.4, fpid=HOLE, value="M2")
text("GPS", 121.6, 149.86, size=0.9, rot=90)
text("MPU6050", 121.6, 168.91, size=0.9, rot=90)
text("BMP280", 121.6, 191.77, size=0.9, rot=90)
text("SnowHUD JACKET", 110.0, 163.5, size=1.2)
text("WIRELESS OPTION W0.1", 110.0, 166.0, size=1.2)
text("link = ESP32 BLE / ESP-NOW", 110.0, 168.5, size=0.9)
text("ESP USB this edge", 147.32, 201.9, size=0.8)

# ================= ROUTER =================
G = 0.254
CLR = 0.2
EDGE = 0.5
VIA_D, VIA_DRILL = 0.6, 0.3
LAYERS = [pcbnew.F_Cu, pcbnew.B_Cu]

def width_for(net):
    return 0.5 if re.search(POWER, net) else 0.3

class Obs:
    def __init__(s, kind, net, layers, **k):
        s.kind, s.net, s.layers = kind, net, layers; s.__dict__.update(k)
        if kind == "rect":
            s.bb = (s.x0, s.y0, s.x1, s.y1)
        elif kind == "seg":
            s.bb = (min(s.ax, s.bx) - s.hw, min(s.ay, s.by) - s.hw, max(s.ax, s.bx) + s.hw, max(s.ay, s.by) + s.hw)
        else:
            s.bb = (s.cx - s.r, s.cy - s.r, s.cx + s.r, s.cy + s.r)
    def dist(s, px, py):
        if s.kind == "rect":
            dx = max(s.x0 - px, 0, px - s.x1); dy = max(s.y0 - py, 0, py - s.y1)
            return math.hypot(dx, dy)
        if s.kind == "seg":
            vx, vy = s.bx - s.ax, s.by - s.ay; L2 = vx * vx + vy * vy
            t = 0 if L2 == 0 else max(0, min(1, ((px - s.ax) * vx + (py - s.ay) * vy) / L2))
            return math.hypot(px - s.ax - t * vx, py - s.ay - t * vy) - s.hw
        return math.hypot(px - s.cx, py - s.cy) - s.r

def route_board(bounds, label):
    x0, y0, x1, y1 = bounds
    nx = int(round((x1 - x0) / G)) + 1; ny = int(round((y1 - y0) / G)) + 1; N = nx * ny
    inside = lambda b: b[0] < x1 and b[2] > x0 and b[1] < y1 and b[3] > y0
    obs, pads_by_net = [], {}
    for fp in board.GetFootprints():
        for p in fp.Pads():
            bb = p.GetBoundingBox()
            r = (pcbnew.ToMM(bb.GetX()), pcbnew.ToMM(bb.GetY()),
                 pcbnew.ToMM(bb.GetX() + bb.GetWidth()), pcbnew.ToMM(bb.GetY() + bb.GetHeight()))
            if not inside(r): continue
            lay = [i for i, L in enumerate(LAYERS) if p.IsOnLayer(L)]
            if not lay: lay = [0, 1]   # NPTH
            net = p.GetNetname()
            c = p.GetPosition()
            o = Obs("rect", net, lay, x0=r[0], y0=r[1], x1=r[2], y1=r[3])
            o.center = (pcbnew.ToMM(c.x), pcbnew.ToMM(c.y)); o.pad = True
            obs.append(o)
            if net and not net.startswith("unconnected-"):
                pads_by_net.setdefault(net, []).append(o)

    def cell(x, y):
        return int(round((x - x0) / G)), int(round((y - y0) / G))

    def mark(arr, o, margin):
        bx0, by0, bx1, by1 = o.bb
        i0 = max(0, int(math.floor((bx0 - margin - x0) / G))); i1 = min(nx - 1, int(math.ceil((bx1 + margin - x0) / G)))
        j0 = max(0, int(math.floor((by0 - margin - y0) / G))); j1 = min(ny - 1, int(math.ceil((by1 + margin - y0) / G)))
        for j in range(j0, j1 + 1):
            py = y0 + j * G; base = j * nx
            for i in range(i0, i1 + 1):
                if o.dist(x0 + i * G, py) < margin:
                    arr[base + i] = 1

    def build_block(net, w):
        mt = CLR + w / 2 + 0.03
        mv = CLR + VIA_D / 2 + 0.03
        blk = [bytearray(N), bytearray(N)]; vb = bytearray(N)
        ed = EDGE + w / 2; edv = EDGE + VIA_D / 2
        for j in range(ny):
            py = y0 + j * G
            for i in range(nx):
                px = x0 + i * G
                d = min(px - x0, x1 - px, py - y0, y1 - py)
                if d < ed: blk[0][j * nx + i] = blk[1][j * nx + i] = 1
                if d < edv: vb[j * nx + i] = 1
        for o in obs:
            if getattr(o, "pad", False):
                mark(vb, o, VIA_D / 2 + 0.25)      # no vias on/near any pad
            if o.net == net and o.net != "":
                continue
            for L in o.layers: mark(blk[L], o, mt)
            if not getattr(o, "pad", False): mark(vb, o, mv)
        return blk, vb

    DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    VIA_COST, TURN = 12.0, 0.4

    def astar(sources, target, tlayers, blk, vb):
        ti, tj = target
        def h(i, j):
            dx, dy = abs(i - ti), abs(j - tj)
            return max(dx, dy) + 0.4142 * min(dx, dy)
        openh, g, came = [], {}, {}
        for (i, j, L) in sources:
            st = (i, j, L, 8); g[st] = 0.0; came[st] = None
            heapq.heappush(openh, (h(i, j), 0.0, st))
        while openh:
            f, gc, st = heapq.heappop(openh)
            if gc > g.get(st, 1e18): continue
            i, j, L, d = st
            if i == ti and j == tj and L in tlayers:
                path = []
                while st is not None:
                    path.append(st[:3]); st = came[st]
                return path[::-1]
            for k, (di, dj) in enumerate(DIRS):
                ni, nj = i + di, j + dj
                if not (0 <= ni < nx and 0 <= nj < ny): continue
                if blk[L][nj * nx + ni]: continue
                if di and dj and (blk[L][j * nx + ni] or blk[L][nj * nx + i]): continue
                c = gc + (1.4142 if di and dj else 1.0) + (TURN if d != 8 and d != k else 0)
                ns = (ni, nj, L, k)
                if c < g.get(ns, 1e18):
                    g[ns] = c; came[ns] = st; heapq.heappush(openh, (c + h(ni, nj), c, ns))
            idx = j * nx + i
            if not vb[idx] and not blk[1 - L][idx]:
                ns = (i, j, 1 - L, 8); c = gc + VIA_COST
                if c < g.get(ns, 1e18):
                    g[ns] = c; came[ns] = st; heapq.heappush(openh, (c + h(i, j), c, ns))
        return None

    def commit(path, net, w, padcells):
        ni = NET(net)
        pts = [(x0 + i * G, y0 + j * G, L) for i, j, L in path]
        def add_seg(a, b, L):
            if abs(a[0] - b[0]) < 1e-6 and abs(a[1] - b[1]) < 1e-6: return
            t = pcbnew.PCB_TRACK(board); t.SetStart(V(*a)); t.SetEnd(V(*b)); t.SetWidth(MM(w))
            t.SetLayer(LAYERS[L]); t.SetNet(ni); board.Add(t)
            obs.append(Obs("seg", net, [L], ax=a[0], ay=a[1], bx=b[0], by=b[1], hw=w / 2))
        # pad-centre stubs for off-grid pads
        for end in (path[0], path[-1]):
            pc = padcells.get(end[:2])
            if pc: add_seg((x0 + end[0] * G, y0 + end[1] * G), pc, end[2])
        start = pts[0]; prev = pts[0]; pdir = None
        for p in pts[1:]:
            if p[2] != prev[2]:
                add_seg(start[:2], prev[:2], prev[2])
                v = pcbnew.PCB_VIA(board); v.SetPosition(V(p[0], p[1]))
                try: v.SetWidth(MM(VIA_D))
                except TypeError: v.SetWidth(pcbnew.F_Cu, MM(VIA_D))
                v.SetDrill(MM(VIA_DRILL)); v.SetNet(ni); board.Add(v)
                obs.append(Obs("circ", net, [0, 1], cx=p[0], cy=p[1], r=VIA_D / 2))
                start = p; prev = p; pdir = None; continue
            d = (round((p[0] - prev[0]) / G), round((p[1] - prev[1]) / G))
            if pdir is not None and d != pdir:
                add_seg(start[:2], prev[:2], prev[2]); start = prev
            pdir = d; prev = p
        add_seg(start[:2], prev[:2], prev[2])

    failures = []
    order = sorted(pads_by_net, key=lambda n: (0 if re.search(POWER, n) else 1, len(pads_by_net[n])))
    for net in order:
        pads = pads_by_net[net]
        if len(pads) < 2: continue
        w = width_for(net)
        padcells = {}
        for p in pads:
            c = cell(*p.center)
            if abs(x0 + c[0] * G - p.center[0]) > 1e-4 or abs(y0 + c[1] * G - p.center[1]) > 1e-4:
                padcells[c] = p.center
        tree = set()
        first = pads[0]; c = cell(*first.center)
        for L in first.layers: tree.add((c[0], c[1], L))
        remaining = pads[1:]
        while remaining:
            # nearest remaining pad to the tree
            def dmin(p):
                c = cell(*p.center); return min(abs(c[0] - t[0]) + abs(c[1] - t[1]) for t in tree)
            remaining.sort(key=dmin)
            p = remaining.pop(0)
            for ww in (w, 0.3, 0.25):
                blk, vb = build_block(net, ww)
                path = astar(tree, cell(*p.center), set(p.layers), blk, vb)
                if path: break
            if not path:
                failures.append((net, p.center)); continue
            commit(path, net, ww, padcells)
            for (i, j, L) in path: tree.add((i, j, L))
            for k in range(1, len(path)):
                if path[k][2] != path[k - 1][2]:
                    tree.add((path[k][0], path[k][1], 0)); tree.add((path[k][0], path[k][1], 1))
            c = cell(*p.center)
            for L in p.layers: tree.add((c[0], c[1], L))
        print(f"[{label}] routed {net} ({len(pads)} pads, w={w})", flush=True)
    return failures

fails = route_board(GB, "goggle") + route_board(JB, "jacket")

# ================= GND POURS =================
def pour(bounds, netname):
    x0, y0, x1, y1 = bounds
    for L in LAYERS:
        z = pcbnew.ZONE(board); z.SetLayer(L); z.SetNet(NET(netname))
        o = z.Outline(); o.NewOutline()
        for (x, y) in [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]:
            o.Append(MM(x), MM(y))
        z.SetMinThickness(MM(0.25)); z.SetThermalReliefGap(MM(0.5)); z.SetThermalReliefSpokeWidth(MM(0.5))
        z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
        try: z.SetLocalClearance(MM(0.3))
        except Exception: pass
        z.SetZoneName(netname + "_" + board.GetLayerName(L))
        board.Add(z)
pour(GB, "/GND_HUD")
pour(JB, "/GND")
pcbnew.ZONE_FILLER(board).Fill(board.Zones())

tb = board.GetTitleBlock()
tb.SetTitle("Snowboarding Helmet Goggles HUD - WIRELESS / BLUETOOTH OPTION carrier PCBs"); tb.SetRevision("W0.1"); tb.SetDate("2026-11-19")
tb.SetComment(0, "Two boards: GOGGLE (top, XIAO ESP32S3 + LiPo) and JACKET (bottom). No cable - radio link (ESP-NOW / BLE)")
pcbnew.SaveBoard(OUT, board, True)
print("saved", OUT)
print("FAILED connections:", fails)
