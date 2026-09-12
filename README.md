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
- Bottom dock buttons do the same as clicking

## How a character is built

Each figure is assembled in four passes inside `buildCharacter()`:

1. **Body** — head, neck, torso, upper/lower arms, hands, pelvis, thighs,
   shins and feet, all boxes positioned in absolute world-y so parts can be
   authored independently.
2. **Clothing** — separate box layers inflated by `PAD` (0.5 units) over the
   body: sleeves, baju torso with collar, placket and pesak panels, then the
   sarung or samping over the hips.
3. **Headwear** — `buildSongkok()` and `buildTanijak()` add boxes above the
   head. The tanijak is a crown band plus flat plates fanned upward at rising
   angles, finished with the upswept "Dendam Tak Sudah" peak.
4. **Circuitry** — `addCircuits()` authors traces in face-local 2D (u across,
   v up) and extrudes them as thin boxes just outside the clothing surface, so
   they hug the voxels. A deterministic LCG keeps the layout stable between
   reloads.

Arms hang from their own pivot groups at the shoulder, so props (the stick and
the keris) attach to the arm and sway with it.

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
