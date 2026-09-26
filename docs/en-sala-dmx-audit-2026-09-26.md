# "En sala" items judged from the engine's DMX output (2026-09-26)

## Method

- Engine: QLC+ 5.2.2 (`qlcplus-qml`), headless web mode on port 9996, loading an I/O-free copy of `QLC+ Setups/Vibra.qxw` made with `qlctool.offline_workspace`. Own instance pid 9876, stopped by exact pid; relaunched once as pid 56684 for the haze test, stopped the same way. Port 9996 confirmed free at the end.
- Driven over `ws://127.0.0.1:9996/qlcplusWS`: `<widget>|255/0`, `QLC+API|setFunctionStatus`, `getFunctionStatus`, `getChannelsValues|1|1|390`.
- Every channel was decoded against the patch in the workspace and the fixture definitions (`QLC+ Fixtures/*.qxf`, and the bundled `Stairville-LED-BAR-240-8-RGB.qxf`, `Generic-Generic-Smoke.qxf`). The sampling scripts, the address map and the raw samples were throwaway scratch work; they are not kept in the repository.
- Each run starts with `PARAR TODO` (widget 20) and a 1.6 s settle. Chasers and EFX were sampled repeatedly, at 30-500 ms depending on the test.

Things to know when reading the evidence:

1. **A web toggle follows its value.** `id|255` turns a Toggle button on and `id|0` turns it off (measured: AUTO 807 went Running on 255 and Stopped on 0). A Flash button is held while at 255. "Press again" in the tests means `id|0`.
2. **About 1.2 % of reads are torn.** `getChannelsValues` sometimes returns a frame with some channels at 0, or at the 127 pan/tilt default. In steady state (AUTO plus Rig Cyan, 734 reads at 20 ms) 9 reads were partly zero, and the channel sum varied from 8169 to 44022. The zeros hit random channels and are gone on the next read, so this is the web thread reading the universe while it is being rebuilt, not the output. Every verdict below rests on repeated samples, and single-frame zeros or 127s are discarded.
3. **The stage plot matters.** `vibra-stage-plot.json` marks the four CromoWash (fx 0, 1, 13, 14), both MiN Wash (15, 16) and both Mini Led (18, 19) as "Spare, not rigged". The rigged heads are the four 7R beams (20-23) and the two MAC WASH (33, 34). Several findings depend on this.

## Verdict summary

| # | Item | Verdict |
|---|---|---|
| 1 | Ver en sala los cuatro modos de color automáticos | **REFUTED** (Pastel tenue loses its white on RGB-only fixtures) |
| 2 | Ver en sala los movimientos nuevos | **REFUTED** (`Alternado` is identical to the default on every rigged head) |
| 3 | Golpes de color del mismo color en toda la sala | NEEDS EYES (DMX side verified) |
| 4 | Decidir en sala la matriz de dos colores sobre Cabezas | NEEDS EYES (owner decision; DMX facts below) |
| 5 | "Quitar y poner un color no apaga las beam": probar la hipótesis | **VERIFIED** (the hypothesis is right: the beams stay lit) |
| 6 | Confirmar en sala los bancos y los picks mantenidos | VERIFIED (banks, mixes, beam colour; part of the text is stale) |
| 7 | Confirmar STROBO / STROBO SUAVE mantenidos | **REFUTED** (the MiN Wash never strobe; the fog LEDs are left out) |
| 8 | `<ExcludeFade>` en las ruedas | VERIFIED |
| 9 | Los blancos usan ahora el emisor White | **REFUTED** (the split also strips the white from fixtures that have no White emitter) |
| 10 | `HUMO VERT` saca la columna del color de la sala | VERIFIED |
| 11 | Confirm JUGAR on site | VERIFIED |
| 12 | Ver en sala lo que cambió la rejilla | **REFUTED** for Cabezas (PAR and Lyres verified) |
| 13 | Humo, las dos cosas nuevas | VERIFIED (DMX side) |
| 14 | Montaje: las 4 máquinas de humo vertical LED | **REFUTED** on "subir/bajar con los niveles"; the rest NEEDS EYES |
| 15 | Probar con el rig el contenido nuevo del 2026-08-28 | NEEDS EYES (one stale claim, two concerns) |
| 16 | Probar en casa los flashes recuperados | **REFUTED** in part (the MiN Wash never strobe on a flash) |
| 17 | Momento Locura ya no abre como pared blanca plana | VERIFIED |
| 18 | Recuperado lo que el show viejo hacía (2026-08-28) | NEEDS EYES (DMX side verified) |
| 19-29 | Hardware-only items (7R wheel names, MAC zoom, frost, Mini Led 9-16, Vortex, WX Auto, beam focus, lyre tilt, MAC RunMode, fog CH6/CH7, pad) | NEEDS EYES |

---

## 1. Ver en sala los cuatro modos de color automáticos — REFUTED

**Test A, the steps:** every step Collection of the four wheels (742 W 22 steps, 756 C 6, 791 L 17, 743 R 6) was started alone with `setFunctionStatus`, read after 1.5 s, and stopped.

**Test B, the buttons:** AUTO on, then press C (w65), L (w66), R (w67) and W (w64) in the COLOR frame, sampling 30 s at 0.5 s after each press.

What holds:

- **The COLOR solo frame replaces AUTO's wheel.** After pressing C: `742 Stopped, 756 Running`. After L: only 791 runs. After R: only 743. After W: only 742.
- **No wheel step uses white.** No step writes R=G=B on any RGB fixture, and no step puts a 7R on White, Light White, Grey or Calid White. The only 7R slots used are 12, 19, 27, 35, 43, 51, 59, 83 and 99.
- **The W steps have one or two colours.** The single-colour steps are one colour everywhere. The pixel "off" segments are the Fill matrix. The contrasts are:
  - 733: heads amber (255,183,0), 7R Orange; the rest (0,0,255).
  - 735: heads yellow, 7R Yellow; the rest blue.
  - 737: heads red, 7R Red; the rest cyan.
  - 739: heads magenta, 7R Pink; the rest green.
  - 741: heads red, 7R Red; the rest blue.
- **Which states start which wheel** (static reachability): AUTO, Tranquilo, Fiesta and Locura reach 742 only. No state reaches 743 (Multicolor), 756, 791 or 792.

**What fails: Pastel tenue on RGB-only fixtures.** Rig Pastel Rojo (758) produces:

- CromoWash, CLB2.4, Vortex, MiN Wash, WX panels and fog LEDs: **(115,0,0)**
- Mini Led: (115,0,0) with **W=140**
- LED bars and MAC (through the matrices): (255,140,140) with W=0

The scene itself writes `fx0:5,115,6,0,7,0` for CromoWash (Red 115, Green 0, Blue 0). So "mezclados un 55% hacia el blanco" happens only on the Mini Led and on the pixel matrices. The other 23 fixtures get a dim, saturated colour at 45 % of full: `rgbw_split` subtracted the white share and there is no White emitter to put it back.

It is the same in all 17 pastel steps, for example Pastel Cyan: CromoWash (0,115,115), Mini Led (0,115,115)+W140, matrices (140,255,255).

Still for eyes: whether the five contrasts read as two colours and not as "feria".

## 2. Ver en sala los movimientos nuevos — REFUTED

**Test:** each of the 25 CABEZAS picks (w112-w136), pressed alone, with pan/tilt of all 14 heads sampled every 80 ms for 17 s. Circulo (w112) was also sampled 36 s at 50 ms to measure periods. The EFX definitions were compared in the workspace.

- **The beams now move in `Square` and `Lissajous`.** Beam pan/tilt span is 40x26 on Cuadrado Simultaneo/Alternado and 40x26 on all three Lissajous variants. VERIFIED.
- **The beams take half as long as the washes.** On Circulo the 7R #1 pan/tilt period is 8.0 s, and MAC #1 and #2 are 16.0 s / 15.9 s (autocorrelation error 0.06-0.21). VERIFIED.
- **`Simultaneo` washes move together.** Neighbour pan and tilt correlation is 1.0 across all washes. MAC #2 is the exception: its pan is mirrored (corr -1.0, `Backward` in the EFX).
  - On the beams, pan correlation is -1.0 on Circulo, Ocho and Lissajous, so #2 and #4 are mirrored (`Backward`).
  - On Cuadrado Simultaneo and Hoja Simultaneo the beam neighbour correlation is about 0 (-0.04 and -0.12): running a Square backwards from the same start is not "at the same time" in any visible sense.
- **`Alternado` is a no-op on the beams.** For all 7 figures, `Beam X Alternado` has the same fixture list as `Beam X`: `20 Forward 0, 21 Backward 90, 22 Forward 180, 23 Backward 270`. The engine agrees, with identical correlation signatures: Circulo and Circulo Alternado beams both give pan corr (0.04, -0.04, 0.04), and Cuadrado and Cuadrado Alternado both give (-1.0, 1.0, -1.0).
  - The wash `Alternado` only flips the direction of every other wash (0 F, 1 B, 13 F, 14 B, 15 F, 16 B) and keeps the 45° phase spread.
  - The two rigged washes are identical in both versions: MAC #1 is `Forward 270` and MAC #2 is `Backward 315` in both.
  - So on the rigged heads (4 beams and 2 MACs), **the 7 `Alternado` buttons do exactly what the 7 default buttons do**. They differ only on the spare CromoWash, MiN Wash and Mini Led.
- **Window check** (7R 62-103 / 207-234 and MAC 76-108 / 212-230, from `movement_aim.py` and `audience_window`):
  - All figures stay inside, except **Diamante (all 3 variants): 7R tilt 200-239**, out of the window in 46-57 of about 190 samples per head. Hoja (all 3 variants) reaches tilt 205-206 in 8-16 samples.
  - Beams Abanico and Beams Cruce do not drive the washes, so the MACs sit at 127/127. See concern C4.

Still for eyes: whether 8 s is too fast for a 7R, and whether the text on the 26 narrow buttons is readable on the tablet.

## 3. Confirmar que los golpes de color salen del mismo color en toda la sala — NEEDS EYES (DMX side verified)

**Test:** AUTO running, each of the 10 GOLPES DE COLOR (w52-w61, Flash + ForceLTP) held 0.6 s, then released and sampled 6 times at 100 ms.

**While held:** all nine RGB families (CromoWash, bars all segments, CLB2.4, Vortex, MiN Wash, Mini Led, WX, fog LEDs, MAC all rings) carry the same RGB. For example ROJO is (255,0,0) everywhere.

- The White emitter is 0 on every colour. BLANCO is (255,255,255) with W=255 on the Mini Led and on all MAC rings.
- The 7R wheel goes to the slot with the matching name: ROJO 12 Red, VERDE 35 Green, AZUL 43 Blue, UV 99, AMARILLO 27 Yellow, CYAN 59 Ice, MAGENTA 51 Pink, BLANCO 4 White, NARANJA 19 Orange, ROSA 51 Pink.
- The HTP dimmers are at 255.

**After release:** the previous AUTO colour returns within one read.

The half that remains for eyes is the 7R wheel naming, which is still unconfirmed (item 19). If the names are wrong, the beams get a neighbouring colour.

Note: every golpe also strobes. The shutter goes to 248 on the CromoWash, 247 on the CLB, Vortex, Mini Led and WX, 248 on the MAC, **234 on the 7R ("Strobe slow to fast")** and 236 on the MiN Wash ("Strobe"). The item does not mention this.

## 4. Decidir en sala la matriz de dos colores sobre Cabezas — NEEDS EYES (decision)

**Test:** Cabezas matrices run alone (`Cabezas - Fill Rojo` 252). The 7R shutter, blade and wheel were read at 20 ms for 3 s.

- The beams never change: shutter 255, blade 0, wheel 59, constant for the whole run. The item states this correctly.
- The Cabezas group has 12 cells: the 4 beams (cells 0-3), which a matrix cannot drive, and 8 washes that the stage plot lists as spares. **On the rigged fixtures, any Cabezas matrix, `Alternate Verde Menta/Azul Profundo` included, produces no visible output.**

That point belongs in the owner's decision.

## 5. "Quitar y poner un color no apaga las beam": probar la hipótesis — VERIFIED (the hypothesis is right)

**Test:** Rig Rojo pick (w70) on and then off, run twice.

**With AUTO stopped:**

- Pick on: 7R shutter/blade/wheel = (255, 0, 12). The blade is 0, "Blade closed", so the beams are dark anyway.
- Pick off: the 7R stay at wheel 12. The RGB fixtures go to (0,0,0) with dimmers at 0.

**With AUTO running:**

- Before the pick: 7R = (255, 255, 59), CromoWash (0,255,255) at dimmer 110.
- Pick on: 7R wheel 12, and every RGB fixture at (255,0,0).
- **Pick off, sampled at +0.2, +1, +3 and +5 s:**
  - The 7R stay at shutter 255 (Open), blade 255 (Blade open), wheel 12 (Red): lit, and red.
  - Every RGB fixture goes to RGB (0,0,0) while its dimmer stays at 110 (MAC 255): the rest of the rig is black.
  - Function status: `742 Stopped`, `807 Running`. The colour wheel does not come back.

Both readings in the item are confirmed. The beams stay on with the last colour, which is the asymmetry. And releasing a pick leaves the room dark instead of returning it to AUTO; only pressing W (item 11) brings the wheel back. The same pattern applies to other frames; see concern C3.

## 6. Confirmar en sala los bancos y los picks mantenidos — VERIFIED (part of the text is stale)

**Test:** with AUTO plus the Rig Cyan pick as a steady cyan base.

- **Key `1`** (Rojo in all five banks, w186/199/212/225/238, Flash + Override + ForceLTP), held:
  - The heads are red, not white: Mini Led (255,0,0) W0, CromoWash (255,0,0), MAC (255,0,0), bars (255,0,0), 7R wheel 12.
  - On release, the next read at 50 ms is back to (0,255,255) and 7R 59, with no intermediate frame. The two isolated partial-zero reads at 0.41 s and 2.12 s are torn reads.
- **The other buttons:**
  - Beam colour Blue (w272) held: 7R wheel 43; released: 59 within 50 ms.
  - Mezcla Ro/Am Cabezas (w308): the heads split red/yellow and the 7R go to 12/27; released: back to cyan.
  - Blanco Cabezas (w206): Mini Led (255,255,255,255) and 7R 4; released: back to cyan.

The text is stale. The gobos, the prism and `Escenario` are no longer Flash buttons: in this workspace they are Toggle picks in solo frames (w143-170, w175-183, w137).

The CLB2.4 PARs (fx 4, 5) and the four fog LEDs are in no bank group, so they stay cyan while `1` is held. See C6.

## 7. Confirmar `STROBO` / `STROBO SUAVE` mantenidos — REFUTED

**Test:** with AUTO running, holding F (w17) and T (w18) and reading every shutter channel.

**STROBO:**

| Fixture | Value | Meaning |
|---|---|---|
| CromoWash | 248 | "Strobe 1-20Hz" |
| CLB2.4 | 247 | strobe |
| Vortex | 247 | strobe |
| Mini Led | 247 | strobe |
| 7R | 234 | "Strobe slow to fast" |
| WX | 247 | strobe |
| MAC | 248 | "Strobe slow to fast" |
| **MiN Wash** | **255** | **"Open"** |
| fog LEDs | 0 | "No strobe" |

STROBO SUAVE gives 202/200/200/200/199/200/202, and again **MiN 255 (Open)** and fog 0.

The scenes do write the MiN Wash strobe: 684 `Strobo Rapido` writes `fx15: 5,236` and 685 writes `5,217`. That channel is "Dimmer/Strobe", in the Intensity group, so it is merged HTP. The level scenes (`Intensidad Ambiente/Total/Peak`) hold it at 255, so max(255, 236) = 255 and **the two MiN Wash never strobe while any level runs**.

The fog LEDs have a strobe channel (ch6 "Strobe, slow to fast"), but no strobe scene writes it. "The LED bars do not strobe because they have no shutter" is correct: bar segment 1 just follows the colour.

## 8. `<ExcludeFade>` en las ruedas — VERIFIED

**Test:** AUTO for 45 s, reading 7R ch8 on all four beams every 35 ms (1297 samples) through 14 colour changes of the 800 ms crossfade wheel.

- The only values seen are 12, 19, 35, 43, 51 and 99, all slot values.
- Changes are single jumps (Blue 43 to Orange 19 at 2.338 s, and so on). No intermediate value ever appeared, while the RGB fixtures were visibly mid-crossfade at the same instants, for example CromoWash (80,215,175) with the 7R already on Orange.

QLC+ 5.2.2 honours the tag.

## 9. Los blancos usan ahora el emisor White — REFUTED

**Test:** all scenes were scanned for the Mini Led White emitter, then confirmed in the engine: CHARLA (w5), the pastel steps, the golpes, and FLASH / FLASH LENTO.

What holds:

- **Achromatic requests use all four emitters.** Blanco Total, Flash 100%/50%, Golpe Blanco, Golpe Graves and the Desk FLASH/BLANCO bursts give (255,255,255)+W255 on the Mini Led and on every MAC ring. Engine: Golpe Blanco gives Mini (255,255,255,255) and MAC (255,255,255,255).
- **Chromatic colours with a white share use the Mini Led correctly:** Rig Pastel Rojo gives (115,0,0)+W140.

What fails:

- **The same split is written to fixtures that have no White emitter**, so their white share is simply gone.
  - **CHARLA (the talk light):** the Mini Led and MACs get (85,44,0)+W170, which is warm white. The CromoWash, bars, CLB2.4, Vortex, MiN Wash, WX panels and fog LEDs get **(85,44,0)**, a dim amber-brown. The engine read shows every one of them at (85,44,0). The desk swatch for `charla` is `#552c00`, the same brown.
  - **All 17 pastel steps:** see item 1.
- **The Lyres matrices bypass the split entirely.** In Rig Pastel steps the MAC rings get (255,140,140) with W=0.

Still for eyes: whether the white looks colder or brighter than the old RGB white.

## 10. `HUMO VERT` saca la columna del color de la sala, no blanca — VERIFIED

**Test:** holding U (w16) under four bases. Fog LED columns are (fog, dimmer, R, G, B, strobe, colour change).

| Base | Before | U held | Released |
|---|---|---|---|
| AUTO | (0,255,255,239,0,0,0); CromoWash (255,239,0) | (255,255,255,143/127,0,0,0), tracking the wheel with CromoWash at (255,143/127,0); all 4 columns identical | pump 0, colour stays the room's |
| TODO NEGRO | — | (255,255,0,0,0,0,0): pump on, column dark | — |
| AUTO + Rig Cyan | — | (255,255,0,255,255,0,0) | — |

The column is never white.

## 11. Confirm JUGAR on site — VERIFIED

**Test:** sequential presses over the websocket, following the item's own steps.

1. **AUTO, then Rig Rojo (w70):** CromoWash, bars, CLB, Vortex, MiN, Mini, WX, fog and MAC are all red. 7R wheel 12 (Red), blade 255, shutter 255. The bar pixels are red with Fill gaps. Status `814 Running, 742 Stopped`.
2. **F1 (CHARLA, w5):** `807 Stopped, 810 Running, 814 Stopped`. The pick is released.
3. **W (w64):** `742 Running`. The wheel returns (red, then green 4 s later, 7R 12 then 35).

Variant: pressing Q again while AUTO is on toggles AUTO off (`807 Stopped`) and leaves the pick running. W brings the wheel back but all dimmers are at 0.

## 12. Ver en sala lo que cambió la rejilla — REFUTED for Cabezas

**Test:** with the matrices started alone, reading the lit cells every 20 ms.

1. **The Lyres grid is 3x2** (one cell per ring). On both MACs:
   - Fill Rojo (326) fills ring 1, then 1+2, then 1+2+3.
   - Even/Odd (332) alternates rings (1,3)/(2) against (2)/(1,3).
   - Waves (344) walks 1, 1+2, 2+3, 3.

   All three rings are painted. VERIFIED. Whether it reads as a pattern or as flicker is for eyes.
2. **Stage order:**
   - **PAR** (Fill Rojo 289, Fill Azul 291) lights Vortex at x=854, 3076, 5298, 6410, 8632 and 10854 in that order, one every ~480 ms, left to right, with the spare last. VERIFIED.
   - **Cabezas** (Fill Rojo 252): the beam cells are now in x order (1916, 4405, 7205, 9694), but the matrix does not move the beams at all (item 4).
   - The 8 RGB cells are spares, and they light in the order x=9000, 10200, 1800, 3000, ..., which is not stage order. So a Fill on Cabezas cannot "cross the room in one direction" on the rigged rig.
3. The console at 13" and the CABEZAS frame at 15 columns are for eyes.

## 13. Humo, las dos cosas nuevas — VERIFIED (DMX side)

1. The column colour: see item 10. Under `Todo Negro` the column is dark, which is the item's own expectation.
2. **The haze rhythm** (relaunched pid 56684):
   - AUTO starts `J` (664 Running), and the AF-150 pump fires at once: 255, then 0 after 2 s.
   - Pressing `cada 2 min` (w30): `664 Stopped, 665 Running`, and the pump fires immediately (255, then 0 at +3 s). Pressing `cada 8 min` (w32): `665 Stopped, 667 Running`, and the pump fires. So the frame is solo and each press fires straight away.
   - The chaser holds are 2 s on, then 60 / 120 / 240 / 480 s off.
3. **The column never fires by itself.** The vertical fog pump (ch1 at 317/324/331/338) stayed at 0 through the whole 60 s AUTO run and the 15 s Locura run.

Which rhythm the room needs is for eyes.

## 14. Montaje 2026-08-29: las 4 máquinas de humo vertical LED — REFUTED on "subir/bajar con los niveles"

- **Step 2** asks for a white column. That is superseded by the owner's 2026-08-30 decision (item 10). `HUMO YA · H` moves only the AF-150: pump 255, vertical fog ch1 0. VERIFIED.
- **Step 3:**
  - "Del color de la sala": VERIFIED.
  - "Apagarse con Todo Negro": VERIFIED (all 0).
  - **"Subir/bajar con los niveles": REFUTED.** The fog LED dimmer (ch2) is 255 in `Intensidad Ambiente`, `Total` and `Peak` (scenes 797/798/800 all write `fx29: 1,255`), while the Vortex PARs are at 110 in Ambiente. Under Locura the fog dimmer stays flat at 255 (2 distinct values in 60 samples: 0 at start, then 255) while the PAR dimmers chase 0-253.
- **Step 4:** CH6 = 0 and CH7 = 0 are what the show writes (engine: fog strobe 0, colour change 0). Whether 0 means "off" on the real machine is for eyes.

## 15. Probar con el rig el contenido nuevo del 2026-08-28 — NEEDS EYES

| Piece | DMX finding |
|---|---|
| Ola Vertical (w133) | 7R pan fixed at 82, tilt waving 207-232, starting head by head (#1 at 0 s, #2 ~1.1 s, #3 ~2.6 s, #4 ~4.2 s). **Until its turn comes, each head sits at 127/127**: MAC #1 for ~10 s, MAC #2 for ~11.6 s (concern C4). |
| Barrido Unison (w134) | Beam pan corr -1.0 between neighbours: mirrored, the sides meet. |
| Beams Cruce (w136) | Beam pans 102/89/75/62 at tilt 220, the mirror of Abanico (62/75/89/102), same tilt. |
| Rig Multicolor 1/2 | **The claim "beams en rainbow scroll ~186" is stale.** The beams get fixed slots: MC1 = 43/83, MC2 = 43/51/99. Across 30 s of the R wheel the 7R never left 12-99. The rainbow range (128-255) appears only in the Arcoiris picks (159). |
| Ciclo Paneles Mixto (200) | Hold 480000 ms on `Ciclo Paneles`, then 240000 ms on `Paneles Manual`. |
| Nivel Fiesta Dinámico (805) | Run for 46 s: smooth chase from 0 to 30 s (26-29 distinct dimmer values per 3 s), 0/255 ping-pong from 30 to about 38 s, then the chase again. |
| Gobo Shake (w168) | 7R gobo 10, jitter 64 ("Slow to fast"). |
| Prisma (Insert Prism) | Rotation 25 ("Forward slow to fast"), prism 191. |

The holds and speeds are opinions for eyes.

## 16. Probar en casa los flashes recuperados — REFUTED in part

**Test:** targeted runs against each control.

Verified:

- **Espacio (FLASH, w12):** CLB 247 and CromoWash 248 (the item says 247/248), Vortex 247, WX 247, Mini 247, MAC 248, 7R 234. White everywhere with W255.
- **`-` (FLASH LENTO, w13):** CLB 200 and CromoWash 202 (the item says 200/202), 7R 199. White.
- **`.` (FLASH COLOR, w14):** strobe 248/247 on top of the running colour (CromoWash (255,255,0), 7R 27).
- **Golpe Graves (w257):** white (Mini W255, 7R 4) with every shutter at 0/Open. No strobe.

Refuted:

- **On all three flashes the MiN Wash reads 255 "Open".** The scenes write 236/217 into its HTP Dimmer/Strobe channel and the level's 255 wins, as in item 7.

The other controls:

- **`B` (w252):** it runs `Dimmer Chase 2`. Over 6 s neither V nor B sweeps the seven Vortex PARs in stage order: the V pulse order is roughly Vx1, 3, 2, 6, 5, 1, 4, 7. Whether it reads as "inverse" is for eyes.
- **`Centro` (w111):** 7R pan 0 / tilt 130 (the audit value). The MACs are parked at 127/127.
- **`Escenario` (w137):** 7R pan 156-162, tilt 196/204/192/189. **The MACs are not aimed** (127/127); the scene still aims the spare CromoWash #1/#2. When toggled off, every head goes to 127/127 and AUTO movement does not resume.
- **Prism subsets `1/2/3/4/1y3/2y4`:** prism 191 on the selected beams, 63 on the others. They do not set rotation; the previous pick's rotation stays (224 after Giro Inverso).
- **MultiColor BEAM (w368-375):** writes 7R ch9 "Color Effect" = 255 on the selected beams and returns to 0 on release. What 255 looks like is for eyes; the definition only says "half-colour position, continuous".
- **`Vel. Paneles` fader (w585):** 0, 128 and 255 appear exactly on WX ch8.
- **`HUMO VERTICAL · N` (w264):** chaser 201 runs (Effect 1 for 60 s, then Effect 3 for 600 s); WX fn 128, effect 2 ("Effect 1").
- **`M` tap:** not tested. The web API gives no tap on a speed dial.

## 17. Momento Locura ya no abre como pared blanca plana — VERIFIED

**Test:** F4 (w8), 60 samples at 250 ms.

- The dimmers move: CromoWash #1-#4, CLB, Vortex and Mini Led each take 34-49 distinct values between 0 and 253, in a travelling chase (at 4.6 s, for example, CromoWash #1..#4 = 32/190/0/0).
- The colour comes from the wheel: red, UV and pink in 15 s. CromoWash was white in 0 of 60 samples.
- Flat at 255 (the owners of their own intensity): MiN Wash, the 7R blade, WX, MAC and the fog LED dimmer. The 7R shutter is Open throughout.

## 18. Recuperado lo que el show viejo hacía — NEEDS EYES (DMX side verified)

- The 7 recovered palette colours are emitted: Rojo Fuego (255,20,0), Verde Menta (0,255,128), Celeste (0,200,255), Azul Cielo (0,127,255), Azul Profundo (0,35,255), Morado (85,0,255), Fucsia (255,0,176).
- Keys 9 and 0 are Az/Ro and Ro/Az in every bank.
- `'` (Arcoiris junto): all Vortex share one hue that cycles.
- `¡` (Arcoiris fases): hues phased across the Vortex.
- Vel. Paneles Auto (206) steps through 160, 232, 200, 255 with a 45 s fade.
- Cabezas Centro: pan 0 / tilt 130.
- Prisma Animación order: 4; 2y4; 1; 2; all; 3; 1y3; none. Two more steps have been appended since (Giro Rápido, Giro Inverso).

The prism pacing, the rainbow holds and the 12-button bank at 13" are for eyes.

## 19-29. Hardware-only items — NEEDS EYES

| # | Item | What the DMX shows |
|---|---|---|
| 19 | 7R wheel colour names | The slot values and names are as above. Whether a slot is really that colour is on the lamp. |
| 20 | MAC WASH zoom only open | Zoom ch6 = 0 under AUTO (`Pixeles ON` writes 0). Whether 0 is wide is a question for the lamp. |
| 21 | 7R frost (ch12) never used | Atomization = 0 in every run. |
| 22 | Mini Led channels 9-16 | Colour macro 0, program 0, reset 0 under AUTO. Their function is a question for the lamp. |
| 23 | Vortex PC-64 test bench | Ch4 (dimmer) and ch5 (strobe) are written as described (110/255 and 0/247). |
| 24 | WX panels in Auto mode | Function 128 "Auto Mode", ch7 effect. The item says "RGB a 0", but under AUTO the Rig scenes also write RGB to the panels (for example 207,0,48) while in Auto mode. What the panels show is for eyes. |
| 25 | 7R beam focus | Focus = 127 in every gobo look. Sharpness is for eyes. |
| 26 | Lyre tilt aim | The item's text (88/170) is stale: the generator now uses the measured windows. The engine keeps the 7R in 62-102 / 207-233 and the MACs in 76-108 / 212-230 (Diamante and Hoja excepted, item 2). |
| 27 | MAC RunMode menu | Function mode ch21 = 0, speed 0, reset 0 under AUTO. The menu itself is on the lamp. |
| 28 | Fog CH6/CH7 = 0 means off | See item 14. |
| 29 | Pad (USB or BLE), dongle flashes, pad LED palette | Not DMX-observable from here. |

---

## Concerns found along the way

- **C1: the MiN Wash cannot dim or strobe under the levels.** Its combined HTP Dimmer/Strobe channel sits at 255 (Open) in Ambiente, while every other fixture is at 110; the definition gives 8-134 = 100-0 %. So the MiN Wash are at full in the ambient level and never strobe (items 7 and 16).
- **C2: `rgbw_split` is applied to fixtures without a White emitter.** It affects the talk light and every pastel (items 1 and 9). It is a generator bug, and no `qlctool check` rule caught it.
- **C3: releasing a pick leaves its family without an owner, in every JUGAR frame.**
  - Colour: the rig goes black and the beams stay red (item 5).
  - Gobo Shake: pressed and released under AUTO or FIESTA, the beams stay on gobo 10 with jitter 64 indefinitely (checked at +0.5, +3 and +6 s). The AUTO gobo animation and `Gobo Reposo` do not resume.
  - Escenario, Centro, Abanico and Cruce: releasing them sends every head to 127/127, and movement does not resume.
- **C4: the MACs park at 127/127 during beam-only looks.** Beam-only looks (Abanico, Cruce, Escenario, Centro) and the Ola Vertical start leave the two MACs, the only rigged washes, at 127/127. The notes put 127 outside their window (212-230).
- **C5: the Cabezas group is 8 spares plus 4 beams that ignore matrices.** On the rigged rig every Cabezas matrix is invisible (items 4 and 12). The movement "variants" differ only on spares (item 2).
- **C6: the CLB2.4 PARs and the fog LEDs are in no colour-bank group.** They keep the old colour while a bank key (1-0) is held.
- **C7: a race between AUTO and a pick.** Pressing a colour pick and AUTO in the same tick (0 s apart, pick first) left both 742 and the pick stopped: RGB 0 while AUTO runs. It was not reproducible at 0.2 s or more. It is unlikely by hand, but possible from simultaneous MIDI or tablet events.
- **C8: sporadic torn reads** from `getChannelsValues` (about 1.2 %). Any future DMX-sampling tool should read twice or ignore single-frame outliers.
- **C9: the operator's QLC+ crashed during this session.**
  - The instance on port 9998, **pid 24473, crashed at 21:26:46**: SIGSEGV in `QV4::QObjectWrapper::markWrapper` (the QML garbage collector). Crash report: `~/Library/Logs/DiagnosticReports/qlcplus-qml-2026-09-26-212658.ips`. It had been up since 19:30.
  - It was not signalled by this session: the only signals sent were `kill 9876` and `kill 56684`, both of my own port-9996 instances.
  - A new instance now serves 9998 (pid 56012), started by someone else.
  - The 9997 test instance, pid 4592, exited normally at 21:43:44, with no crash report.
