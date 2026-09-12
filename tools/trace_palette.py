"""Sample the reference lineup: per-rank column bounds, heights and lit palettes."""
import numpy as np
from PIL import Image
from collections import Counter

img = Image.open('/root/.claude/uploads/344e9755-0bdd-50fa-ad54-757ad57e97c2/4cba1fda-image.jpg').convert('RGB')
a = np.asarray(img).astype(int)
H, W, _ = a.shape

mx, mn = a.max(2), a.min(2)
sat = mx - mn
# solid body pixels only: the neon halo is bright and only mildly saturated,
# so a tighter threshold keeps the glow from bridging two characters
solid = (mx < 185) | (sat > 85)
solid[int(H*0.70):, :] = False            # drop the caption band

cols = solid.sum(0)
runs, inside = [], None
for x in range(W):
    if cols[x] > 6 and inside is None:
        inside = x
    elif cols[x] <= 6 and inside is not None:
        if x - inside > 60:
            runs.append((inside, x))
        inside = None
if inside is not None:
    runs.append((inside, W))
print('columns:', len(runs), [(x0, x1, x1-x0) for x0, x1 in runs])

def hexof(c):
    return '0x%02x%02x%02x' % tuple(int(round(v)) for v in c)

def lit(region, mask, frac=0.4):
    """Average of the brightest `frac` of masked pixels — the lit faces,
    which is the tone the material actually reads as."""
    px = region[mask]
    if len(px) < 20:
        return None
    lum = px.sum(1)
    keep = px[lum >= np.quantile(lum, 1 - frac)]
    return keep.mean(0)

BANDS = [('hair', 0.02, 0.11), ('face', 0.14, 0.22), ('torso', 0.28, 0.44),
         ('hip', 0.47, 0.58), ('leg', 0.64, 0.86), ('foot', 0.90, 1.00)]
RANKS = [5, 4, 3, 2, 1]                   # reference runs tallest-first, left to right

out = {}
for i, (x0, x1) in enumerate(runs):
    sub, m = a[:, x0:x1], solid[:, x0:x1]
    rows = np.where(m.any(1))[0]
    top, bot = rows[0], rows[-1]
    h = bot - top + 1
    rank = RANKS[i] if i < len(RANKS) else '?'
    print('\n--- rank %s   x=%d..%d   height=%dpx' % (rank, x0, x1, h))
    out[rank] = {'h': h}
    for name, f0, f1 in BANDS:
        y0, y1 = top + int(h*f0), top + int(h*f1)
        c = lit(sub[y0:y1], m[y0:y1])
        if c is not None:
            print('   %-6s %s' % (name, hexof(c)))
            out[rank][name] = hexof(c)
    g = sub[m]
    isg = (g[:,1] > g[:,0] + 45) & (g[:,1] > g[:,2] + 45)
    if isg.sum() > 60:
        ng = g[isg]
        print('   %-6s %s   core %s   (%d px)' % ('neon', hexof(ng.mean(0)),
              hexof(ng[ng.sum(1).argmax()]), isg.sum()))

hs = [out[r]['h'] for r in RANKS if r in out]
print('\nheights px (rank 5..1):', hs)
print('normalised to rank 5   :', [round(v/hs[0], 3) for v in hs])
