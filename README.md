# Cyber-Voxel Nusantara — Voxel Rank Renderer

An interactive 3D voxel character renderer in a single HTML file. Five ranked
characters wearing traditional Malay attire — baju melayu, sarung/samping,
songkok and tanijak — rendered Minecraft-style from `THREE.BoxGeometry`
voxels, with neon green circuitry on the higher ranks.

Open `index.html` in a browser. No build step, no install; Three.js r128 and
OrbitControls load from CDN.

## The cast

| Rank | Name | Look |
| --- | --- | --- |
| 1 | Anak Dagang | Brown baju melayu, white sarung, sandals, no glow |
| 2 | Perantau | Blue baju melayu, dark trousers, backpack |
| 3 | Pendekar Muda | Black baju melayu, songkok, checked samping, wooden training stick |
| 4 | Pahlawan Siber | Black baju melayu with subtle neon traces, black tanijak with a faint glow, dim keris |
| 5 | Adiguru | Full black with bright pulsing circuitry, glowing tanijak and crystal node, neon keris |

## Controls

- **Drag** — orbit the scene
- **Scroll** — zoom
- **Click a character** — ease the camera in and slowly orbit them
- **1–5** — jump to a rank; **Esc** or **OVERVIEW** — back out
- **T** or **MOD** — switch presentation preset
- Bottom dock buttons do the same as clicking

## Two presentation presets

**SIBER** is the neon scene: near-black ground, green grid, drifting motes,
glowing ground rings, additive bloom sprites and a green HUD.

**STUDIO** reproduces the concept sheet's white product shot. It drops the
floor plane entirely so no horizon cuts the frame, puts a soft elliptical
contact shadow under each figure, swaps the captions for plain black type on
a white card, dims the per-character lamps and hides the additive glow —
which would be invisible over white anyway. Exposure is set so the sum of
ambient, hemisphere and key contributions stays under 1.0 on the brightest
face; the earlier values clipped and turned the brown baju yellow.

## Traced from the concept art

`tools/trace_palette.py` and `tools/trace_proportions.py` sample the concept
lineup instead of eyeballing it:

- **Proportions.** Each figure's ground-to-forehead height is measured in
  pixels — a landmark that ignores headwear, so the tanijak doesn't inflate
  the ratio. Normalised to rank 4 this gives the `scale` values the renderer
  uses: 0.77 / 0.88 / 0.92 / 1.00 / 1.18. Rank 1 really is only about
  two-thirds the height of rank 5 in the art.
- **Cloth colours.** For each garment band the scripts average the brightest
  40% of pixels (the lit faces, which is the tone a material reads as) rather
  than the most common colour, which would return the shadow side.
- **Neon hue.** The art's circuitry averages around `#2e982a` with a
  `#d1ffa9` bloom core — a yellower green than the HUD's `#39ff6a`. The
  renderer keeps `#39ff6a` for interface chrome and uses `#4dff52` on the
  characters.
- **Build.** Measured from the silhouette rather than from colour, because a
  skin-tone mask catches hands and bare feet and drags the "chin" down to the
  toes. The neck is the narrowest scanline in the upper body, which gives a
  reliable head/shoulder split: in the art, shoulder span is only **1.28×**
  the head width and the head is **0.278** of total height. Classic Minecraft
  proportions sit near 2.10 and 0.20, which is why the first pass read
  stocky. The leg ratio is *not* measurable here — the sarung hides the gap
  between the legs, so the crotch detector returns nonsense — and legs are
  matched by eye instead.

The columns for ranks 4 and 5 need splitting by hand because their neon glow
bridges the gap between them; `trace_proportions.py` cuts the merged run at
its sparsest interior column.

## How a character is built

Each figure is assembled in four passes inside `buildCharacter()`:

1. **Body** — head, neck, torso, upper/lower arms, hands, pelvis, thighs,
   shins and feet, all boxes positioned in absolute world-y so parts can be
   authored independently. The **face is painted, not modelled**: each eye in
   the art is an L — a horizontal brow bar with a short descender on its inner
   edge — and the smile is a smooth curve, neither of which can be built from
   boxes. `faceTexture()` draws them on a 16×16 canvas which is mapped to the
   head's `+z` face alone, via `BoxGeometry`'s six-material array
   (`[+x, -x, +y, -y, +z, -z]`). Ears are real geometry, standing proud of the
   head as they do in the art.
2. **Clothing** — separate box layers inflated by `PAD` (0.5 units) over the
   body: sleeves, baju torso with collar, placket and pesak panels, then the
   sarung or samping over the hips, knee-length on the barefoot ranks. Ranks 1
   and 3 get the small placket buttons the art shows, gold and neon green.
3. **Headwear** — `buildSongkok()` and `buildTanijak()` add boxes above the
   head. The tanijak is a crown band plus flat plates fanned upward at rising
   angles, finished with the upswept "Dendam Tak Sudah" peak.
4. **Circuitry** — `addCircuits()` authors traces in face-local 2D (u across,
   v up) and extrudes them as thin boxes just outside the clothing surface, so
   they hug the voxels. A deterministic LCG keeps the layout stable between
   reloads.

Arms hang from their own pivot groups at the shoulder, so props (the stick and
the keris) attach to the arm and sway with it. Rank 1 stands with its hands
clasped, swung forward rather than inward so they rest in front of the sarung
instead of intersecting it.

## Why it stops looking blocky

Close-ups of the concept art show every surface broken into small cubes, each
with a light chamfer along its top and left edge and a darker seam along the
bottom and right. That bevel, not the polygon count, is most of what separates
the art from a model made of a few big boxes — so `voxelTile()` paints it.
Cells sit below the base tone so the chamfer has room to lift to full, since a
multiply map can darken but never brighten past the material colour.

`voxMap(repeat)` caches one texture object per repeat value, which keeps a
roughly 1-unit cell across parts of very different sizes without needing a
texture per box: `VOX_BODY` for the torso, head and sarung, `VOX_LIMB` for arms,
shins, feet and small trim.

The haircut is the one place that earns real extra geometry — a 6×5 grid of
columns at varying heights, plus a fringe that drops lower at the temples — so
individual cubes step out of the silhouette the way they do in the art.

**Still different from the art:** the reference is a true fine voxel model, so
its limb edges step where these big boxes stay straight, and it has soft
ambient occlusion in the crevices that this renderer has no equivalent for.

## Animation

- All five characters bob gently and turn slightly on an offset phase.
- Arms breathe, heads glance around.
- Rank 5 pulses hard (emissive intensity, glow-sprite scale and the ground
  ring all ride one sine); rank 4 only shimmers.
- The Adiguru's crystal node turns slowly overhead.
- Unfocused characters dim so the selected rank reads clearly.

## Performance notes

One shared `BoxGeometry` scaled per part, one shared grain texture, no shadow
maps and no post-processing — the glow is emissive materials plus additive
radial sprites. The whole scene renders at roughly 7.7k triangles.
