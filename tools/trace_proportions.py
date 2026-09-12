"""Split the merged rank 4/5 columns and measure ground->forehead, a landmark
that is comparable across ranks because it excludes headwear."""
import numpy as np
from PIL import Image

a = np.asarray(Image.open('/root/.claude/uploads/344e9755-0bdd-50fa-ad54-757ad57e97c2/4cba1fda-image.jpg')
                .convert('RGB')).astype(int)
H, W, _ = a.shape
mx, mn = a.max(2), a.min(2)
solid = (mx < 185) | (mx - mn > 85)
solid[int(H*0.70):, :] = False
cols = solid.sum(0)

# the merged run holds ranks 5 and 4; cut it at the sparsest interior column
m0, m1 = 94, 610
mid = m0 + 180 + int(np.argmin(cols[m0+180:m0+300]))
print('rank5/rank4 split at x =', mid, ' (density', cols[mid], ')')
runs = [(m0, mid), (mid, m1), (626, 842), (883, 1100), (1158, 1341)]
RANKS = [5, 4, 3, 2, 1]

r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]
skin = (r > 150) & (r > g + 18) & (g > b + 12) & (r - b > 45) & solid

print('\nrank  x0..x1   ground  forehead  h(px)  ratio')
ground = 715.0
res = {}
for rank, (x0, x1) in zip(RANKS, runs):
    sm = skin[:, x0:x1]
    rows = np.where(sm.sum(1) > 3)[0]
    fore = rows[0]
    h = ground - fore
    res[rank] = h
    print('  %d   %4d..%-4d  %5.0f   %5d    %5.0f' % (rank, x0, x1, ground, fore, h))

base = res[5]
print('\nground->forehead, normalised to rank 5:')
for rank in [1,2,3,4,5]:
    print('  rank %d  %.3f' % (rank, res[rank]/base))
