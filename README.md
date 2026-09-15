# Cyber-Voxel Nusantara — Voxel Rank Renderer

An interactive 3D voxel character renderer in a single HTML file. Five ranked
characters wearing traditional Malay attire — baju melayu, sarung/samping,
songkok and tanijak — rendered Minecraft-style from `THREE.BoxGeometry`
voxels, with neon green circuitry on the higher ranks.

Open `index.html` in a browser. No build step, no install; Three.js r128 and
OrbitControls load from CDN.

## Plugins

`.claude/settings.json` registers the [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
marketplace and enables its plugin — a searchable local database of UI styles,
palettes, font pairings, charts and per-stack guidelines, plus six sibling
skills (`design`, `design-system`, `ui-styling`, `brand`, `banner-design`,
`slides`).

It is registered as a **plugin**, not copied into `.claude/skills/`, because
its search tool resolves through `${CLAUDE_PLUGIN_ROOT}` — a variable only set
for installed plugins. A copied skills folder would load its instructions but
break every `python .../search.py` call in them. Its scripts need Python 3,
which is available here.

## Files

| File | What it is |
| --- | --- |
| `index.html` | The Three.js renderer — five ranks side by side, orbit and focus |
| `app.html` | The Nusuki app mockup, four screens, with the real voxel avatar |
| `mockup.html` | The same characters built from plain divs in CSS 3D, no WebGL |
| `tools/trace_*.py` | Scripts that sample the concept art for palette and proportions |

### app.html — the avatar inside the app

One `WebGLRenderer` on a single canvas floats above the whole UI with an
alpha clear, and the 3D is drawn only inside scissor rectangles pinned to DOM
slots (`#slot-home`, `#slot-avatar`), each with its own camera. That is how the
avatar sits *inside* a card without the card's opaque background covering it —
the canvas is on top, transparent everywhere except those rects. WebGL
viewports start at the bottom-left, so the y of each slot's
`getBoundingClientRect()` is flipped.

On the Avatar screen the earned badges float beside the figure as chips, two
per side at staggered heights with a short tether pointing inward. They are
ordinary DOM *inside* the slot, sitting under the canvas — which works because
the canvas clears to transparent and paints only the character, so everything
else in the slot shows straight through. A chip that drifts behind the figure
therefore reads correctly as being behind it. They carry `aria-hidden`; the
badge grid below the stats is the real, readable list.

Ticking an amal row moves XP and Nur Amanah, and when XP fills the track the
rank advances and the avatar is rebuilt as the next rank — the app's premise is
that the avatar reflects real deeds, so the mockup demonstrates that loop
rather than describing it.

Every glyph starts as an 8×8 pixel grid, not an emoji: emoji are round, glossy
and come from the system font, which reads as a different concept next to the
voxels. The grids are then built as **real geometry** — each filled pixel
becomes a chamfered cube, the same `chamferBox` the characters are made of,
with the cubes of one colour merged into a single `BufferGeometry` so a badge
costs one or two draw calls instead of thirty. Cubes are cut slightly larger
than the 1-unit lattice they sit on, so neighbours overlap; at list size a
chamfer gap between every cube fragmented each shape into loose dots.

Where that geometry is *live* versus *baked* is a deliberate split:

- **Badges beside the avatar are live 3D**, added straight into the avatar's
  own scene. They cost no extra render pass, are lit by the same rig, and bob
  and swing as real objects. They swing rather than spin because a full turn
  would take each slab edge-on twice a lap, where it all but disappears. Their
  names ride along as DOM labels, positioned each frame by projecting a point
  just under each badge through the slot's camera — the underside rather than
  the centre, so a label clears whatever on-screen height the badge happens to
  have.
- **List icons are the same geometry rendered once and kept as a PNG**, baked
  off-screen at startup at a three-quarter angle. Live 3D per list icon would
  mean a render pass and a `getBoundingClientRect` for each of them every
  frame, inside cards that scroll.
- **Chrome marks stay flat vector** — tab marks, mood faces, the tick. They use
  `currentColor` to pick up their active state, which a baked PNG cannot do,
  and at 11–15px a 3D render is mush anyway.

**One bug worth remembering.** `setSize(w, h, false)` skips writing
`canvas.style.width/height`. A canvas is a *replaced* element, so with
`width:auto` CSS resolves its used width to the **intrinsic** width — the
drawing buffer, which is viewport × `devicePixelRatio` — rather than the
`inset:0` box. On a 2× display the canvas was therefore laid out at 1040×1800
in a 520×900 viewport, everything drew at double scale, and the avatar landed
well outside its slot. Letting `setSize` write the style fixes it; testing at
`deviceScaleFactor: 1` hides it completely.

### mockup.html — CSS-only characters

For app views that cannot host WebGL. Each voxel is a div with six face
children placed by `transform`, shaded by a fixed per-face `brightness()` that
stands in for a key light. One constraint shapes the whole approach: CSS 3D
sorts whole elements, not fragments, so two boxes that pass through each other
flicker as they rotate. The Three.js renderer layers clothing as slightly
larger boxes over a bare body, which cannot work here — so each part is a
single box already coloured as its garment, and trim sits in its own y band or
just outside in z. The page also prints the static markup for the selected
character, so it can be pasted into a template with no JS at all.

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

## Roblox shapes, modern render

The concept art reads as Roblox construction — blocky limbs, simple parts —
with a modern game render laid over it, and the second half is mostly lighting
and material, not geometry:

- **Phong, not Lambert.** Flat diffuse shading is what made the voxels look
  like matte toy bricks. Cloth takes a dim broad highlight; neon trim, the
  keris and the belt plates take a tighter one via `shine: 'hard'`.
- **Two back lights rake the silhouette** — pale neon from behind-right, a warm
  counter from behind-left. Edge light is most of what separates a stylised
  modern render from a flatly lit toy. They are kept low and the rim's green is
  desaturated: at full saturation the light tinted whole figures olive instead
  of just grazing their edges.
- **Bolder extremities.** Hands and boots are oversized relative to the limbs,
  the way stylised game characters exaggerate them.

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

The cubes in the concept art have their **edges cut, not squared off**, and
that chamfer — not polygon count — is most of what keeps the art from reading
as a stack of hard boxes. A scaled unit cube cannot carry it: scaling a baked
bevel stretches it into a wedge. So `chamferBox(w, h, d)` generates the shape
per size and caches it — 6 inset face quads, 12 chamfer quads along the edges,
8 corner triangles, 44 triangles a box. `BEVEL` is an absolute world width, so
a hand and a torso get the same cut.

Winding is settled by testing each triangle's normal against its centroid,
which works because the shape is convex and centred on the origin; that saves
hand-ordering 44 triangles correctly.

**UVs are world-space.** Each vertex's position is projected onto the plane
perpendicular to its face's dominant axis and divided by the tile's world size.
One voxel cell is then the same size on a hand as on a torso, with no per-part
texture repeat to manage — `CELL` sets it directly. The samping's check weave
rides the same UVs, with `repeat` setting its square size.

The other half is shading: `voxelTile()` paints each cell like a slightly
inflated cube, bright at the centre and falling off to a darker rim, with a
crisp seam between cells. Values stay at or below full brightness because a
multiply map can darken but never lift past the material colour.

The haircut earns real extra geometry — a 4×4 grid of chunky columns at varying
heights plus a fringe that drops at the temples — so individual cubes step out
of the silhouette. An earlier 6×5 grid of small cubes read as fuzz rather than
as the art's chunky voxel mass.

The head is the one mesh with two materials: `chamferBox` puts its `+z` face in
its own group, with 0..1 UVs, so the painted portrait rides there alone.

**Still different from the art:** the reference is a true fine voxel model, so
its limbs are built from many small cubes where these are single chamfered
boxes, and it has soft ambient occlusion in the crevices that this renderer has
no equivalent for.

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

## `murabbi.html` — the mentor dashboard

The mentee app is a game surface. This is a reading surface for someone who has
ten minutes before halaqah, so the tokens are the same and the glow is turned
down.

**The thesis: the dashboard's job is to generate conversations, not scores.**
That comes from the app's own copy on the Muhasabah screen — *"Murobbi memantau
untuk taujihat — bukan penilaian luaran semata-mata"* — and it decides every
other choice here.

Deliberately absent: a leaderboard, the raw muhasabah log, any red styling, and
absolute score as the primary sort.

### Triage by change, not by level

The landing list surfaces people for one of four reasons, each with its own
colour *and* its own shape so the four never rest on hue:

| Reason | Trigger |
|---|---|
| `SENYAP` | no entries for ≥3 days — the row is about the person, not the amal |
| `TURUN` | Nur Amanah dropped ≥5 points over two weeks |
| `ISYARAT` | one prayer reported rushed ≥18 of 28 days — a pattern, not a day |
| `NAIK` | up ≥5 points — surfaced to be acknowledged, not corrected |

**The list is capped at five, and the cap is the design.** The first build
surfaced nine of twelve, which is the roster with extra steps. Worse, six rows
read *"Solat Asar dilaporkan tergesa…"* with only the count differing — and
that repetition is itself the finding. A pattern half the group shares is not
ten private problems, so whoever the cap cuts rolls into the halaqah topic
instead of being dropped.

That is why the topic card weighs two different kinds of evidence and says which
one won: the weakest amal (a level, averaged) versus a shared reflection pattern
(a pattern). The pattern wins at half the group.

### The privacy line

The murabbi sees the *pattern*; the mentee owns the *entry*. Muhasabah reaches
this screen only as 28-day tallies per prayer — never the day-by-day text. The
card says so out loud, because a promise the interface doesn't visibly keep is
just trust. (Unprompted suggestion for the mentee app: an *"Apa murabbi nampak"*
screen, so the promise is checkable from the other side.)

### The charts

Colour does exactly one job each, and the colour part is computed rather than
eyeballed — every palette below was run through the data-viz validator.

- **Sequential green ramp** `#215433 #2d7742 #3a9c54 #51c76d #90efa1` — magnitude:
  the 28-day mutabaah heatmap and the rank distribution. Validated as an ordinal
  ramp: monotone lightness, ≥0.06 steps, and the low end clears the card at
  2.06:1 (an earlier `#122a1c` sat at 1.19:1 and vanished into the surface).
- **Categorical** `#286e3c` tenang / `#1e78be` mengantuk / `#c8821e` tergesa —
  identity, for the stacked tendency bars. Blue sits between the two a red-green
  colourblind reader confuses, *and* the green is stepped dark enough that the
  pair separates by lightness on its own: at the brighter `#33a24a` the
  green↔amber pair was ΔE 3.8 under protanopia. It now clears 13.4 protan and
  19.8 normal **on all pairs**, not just adjacent ones — adjacent is the right
  pairlist for a stack, but the legend invites the direct green-vs-amber
  comparison, so all-pairs is the honest gate.
- **Status** amber `#bf8a22` perlu disapa / grey `#6a8b78` senyap / green
  `#51c76d` naik — reserved, never reused as a series colour, and always shipped
  with an icon and a label.

The green's 2.93:1 against the card is a documented WARN, not a pass, and it
obligates relief: every segment is labelled and a full table view exists behind
*Papar jadual*. The segment label picks light or dark ink from the fill's own
luminance rather than assuming one works on all three.

Single-series charts get no legend box — the card title names the series — and
only the last point is direct-labelled. Both line charts carry a crosshair and a
per-week tooltip; heatmap cells and bar rows carry their own.

### Reuse and cost

The voxel engine is lifted verbatim from `app.html`, because the figure the
mentee sees in their own app has to be the figure the murabbi sees or the
dashboard becomes a spreadsheet about strangers. Two tiers:

- The selected mentee's avatar is **live**, in a scissored viewport pinned to
  its slot — one scene, one draw.
- The triage busts are the **same geometry baked once** to five PNGs at boot
  (one per rank). A live pass per list row inside a scrolling card is not
  affordable, and the list never needs one.

### The generated data

Twelve people × 28 days × 5 amal is 1,680 numbers, and inventing them by hand
would make them look invented. Each mutarabbi carries a `consist` (how reliably
they tick) and a `drift` (which way they are heading), and a seeded LCG honours
both — so the trend line, the heatmap and the triage reason for one person all
agree with each other. Silence is literal: a mutarabbi who has not written for
six days has six empty columns, and the charts do not quietly fill them in.
