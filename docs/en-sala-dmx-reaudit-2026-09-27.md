# Re-audit of the en-sala items against the DMX of the v0.1.9 show (2026-09-27)

Workspace: `QLC+ Setups/Vibra.qxw`, sha256 `097d28d5255823fe6ff5bf1c3cb9f5750a52d5ef8552e03d3e70854d6b5d1f88` (checked before the run; it matches `Vibra.desk.json`).

## Summary

| # | Item | Before (2026-09-26) | Now (v0.1.9) |
|---|---|---|---|
| 1 | Los cuatro modos de color automaticos | REFUTED | **FIXED**: pastel on RGB-only fixtures is (255,140,140), and the Mini Led gets (115,0,0)+W140 |
| 2 | Los movimientos nuevos | REFUTED | **FIXED-AS-RULED (D5)**: `Alternado` alternates by stage order and differs from the default on every figure. Diamante still leaves the beam window (see section) |
| 7 | STROBO / STROBO SUAVE mantenidos | REFUTED | **FIXED (D2, D3)**: MiN Wash 236/217, and the fog LED columns 247/200 |
| 9 | Los blancos usan el emisor White | REFUTED | **FIXED**: CHARLA is (255,214,170) on RGB-only fixtures and (85,44,0)+W170 on the Mini Led and MAC |
| 12 | Lo que cambio la rejilla | REFUTED for Cabezas | **FIXED-AS-RULED (D6)**: no Cabezas matrices remain. PAR and Lyres are unchanged and correct |
| 14 | Las 4 maquinas de humo vertical LED | REFUTED on "subir/bajar con los niveles" | **FIXED-AS-RULED (D4)**: the column dimmer is 255 in every level, and the rest verified |
| 16 | Los flashes recuperados | REFUTED in part | **FIXED (D1, D3, D7)**: MiN strobes on all three flashes; the columns strobe on FLASH/FLASH LENTO and go white on FLASH COLOR; the MACs aim at 92/221 |
| 5 | "Quitar y poner un color no apaga las beam" | VERIFIED | **CHANGED-AS-RULED (D8)**: releasing the pick now closes the 7R blade (0) along with the rig, so no beam stays red over a black room. The rig stays dark until W or the hook |
| 6 | Bancos y picks mantenidos | VERIFIED | **NO REGRESSION**, and D9 applied: CLB2.4 and the fog LEDs follow bank 1 (BarrasLed) |
| 8 | `<ExcludeFade>` en las ruedas | VERIFIED | **NO REGRESSION**: 1326 reads in 45 s show slot values only, in 12 single jumps |
| 10 | HUMO VERT saca la columna del color de la sala | VERIFIED | **NO REGRESSION** |
| 11 | JUGAR | VERIFIED | **NO REGRESSION** |
| 13 | Humo, las dos cosas nuevas | VERIFIED | **NO REGRESSION**: the vertical pump stays 0 through 45 s of AUTO |
| 17 | Locura no abre como pared blanca | VERIFIED | **NO REGRESSION**: dimmers take 39-50 distinct values; CromoWash is white in 0 of 60 samples |

No item STILL FAILS on the ground it was refuted for. Two findings are left over, and neither was the cause of a REFUTED verdict:

- Diamante (all variants) still puts the 7R tilt at 200-240, outside the window, in about 30 % of samples. Hoja does it in about 7 %.
- A position pick released with no state running drops every head to 127/127. Under a state, the heads go to `Cabezas Suelo`, and the movement comes back only at the next energy step.

## Method

- Engine: QLC+ 5.2.2 (`/Applications/QLC+ 5.2.2.app`), started with `open -n -g -a ... --args -w --wp 9995 -o <copy>`.
  - Own pid **40519**, on port 9995 only.
  - Stopped with `kill 40519`. Afterwards 9995 was free, and pid 56012 (the operator's instance on 9998) was untouched.
  - Another QLC+ on 9997 (pid 36759, not started by this session) was left alone.
- The copy was made outside the repository. Every `<Input>`, `<Output>` and `<Feedback>` was removed from `<InputOutputMap>`, leaving an empty `Universe 1`. The file was already saved with `CurrentWindow="VC"`.
- Driven with Node's built-in WebSocket on `ws://127.0.0.1:9995/qlcplusWS`:
  - `<widget>|255/0` presses and releases a button;
  - `QLC+API|setFunctionStatus`, `getFunctionStatus` and `getChannelsValues|1|1|390` do the rest.
- Every read is two reads. If they differ, a third is taken and each channel gets the median of the three (the torn-read filter). Each test starts with PARAR TODO (w20) and a 1.7 s settle.
- Widget and function ids were taken from this workspace. They differ from the 2026-09-26 audit:
  - Rueda Colores 702, Simples 716, Pastel 751, Multicolor 703;
  - Rig Pastel collections 718-750 (even ids);
  - Intensidad Ambiente/Total/Peak 757/758/760;
  - AUTO 767 and Humo Auto 624-627;
  - PAR matrices w422+ and Lyres matrices w459+.
- Channels were decoded against the workspace patch and the fixture definitions (`QLC+ Fixtures/*.qxf`, plus the bundled LED Bar and Generic Smoke). Stage x comes from `vibra-stage-plot.json`.

---

## 1. Los cuatro modos de color automaticos - FIXED

Each `Rig Pastel X + Pixeles` collection (718...750) was started alone and read after 1.5 s.

| Step | CromoWash, CLB2.4, Vortex, MiN, WX, fog LEDs | Mini Led (RGBW) | Bars / MAC rings (matrix) | 7R wheel |
|---|---|---|---|---|
| 718 Pastel Rojo | (255,140,140) | (115,0,0)+W140 | (255,140,140) W0 | 12 |
| 732 Pastel Cyan | (140,255,255) | (0,115,115)+W140 | (140,255,255) W0 | 59 |
| 738 Pastel Azul | (140,140,255) | (0,0,115)+W140 | lit cells up to (140,140,255) | 43 |
| 750 Pastel Rosa | (255,140,185) | (115,0,45)+W140 | (255,140,185) | 51 |

- All 17 steps behave the same way.
- RGB-only fixtures now get the full pastel mix, with the white share kept as equal RGB.
- Only the Mini Led, which has a White emitter, gets the split.
- In the steps where bar segment 1 or MAC ring 1 read 0, the pixel matrix was in its "off" segment:
  - 30 reads over 3 s show the lit cells at the pastel colour (for example 722: 255,197,140);
  - Waves steps also show its dimmed fractions.
- Before: RGB-only fixtures read (115,0,0), 45 % of a saturated colour.

Test B still holds. From AUTO, C starts 716, L 751, R 703 and W 702, and each one stops the other three.

## 2. Los movimientos nuevos - FIXED-AS-RULED (D5)

**Static.** The fixture lists now differ.

- Beams, default: `20F0 22F90 23B180 21B270`, in stage order 20, 22, 23, 21 (x 1916, 4405, 7205, 9694). The two halves are mirrored.
- Beams, Alternado: `20F0 22B90 23F180 21B270`. The direction alternates head by head in stage order.
- Washes, default: `33F0 34B180`.
- Washes, Alternado: `33F0 34F180`, both Forward 180 degrees apart. This is D5's rule for 2 or fewer rigged washes.

**Engine.** Each pick was pressed alone and sampled every ~70 ms for 17 s (about 250 samples). The table gives the neighbour pan correlation in stage order (20-22, 22-23, 23-21) and the MAC pan and tilt correlations.

| Figure | Default beams | Alternado beams | Default MAC pan/tilt | Alternado MAC pan/tilt |
|---|---|---|---|---|
| Ocho | -1, 1, -1 | 1, 1, 1 | -1 / -1 | 1 / -1 |
| Linea | ~0 | ~0 | 1 / 1 | -1 / -1 |
| Diamante | ~0 | ~0 | 1 / -1 | -1 / -1 |
| Cuadrado | 0.05, 1, 0.05 | -1, 1, -1 | ~0 / ~0 | -1 / -1 |
| Hoja | 0.05, 0.89, 0.07 | -0.89, 0.89, -0.89 | 1 / -1 | -1 / -1 |
| Lissajous | -1, 1, -1 | 1, 1, 1 | -1 / -1 | 1 / -1 |

Circulo correlates near 0 at 90-degree offsets, so it was checked by rotation sense (the sign of the angular momentum):

- Default: 20 CCW, 22 CCW, 23 CW, 21 CW; MAC 33 CCW, 34 CW.
- Alternado: 20 CCW, 22 CW, 23 CCW, 21 CW; MAC 33 CCW, 34 CCW, with pan peaks about 7 s apart in the 16 s period (about 180 degrees at this sampling).

So the 7 `Alternado` buttons no longer repeat the defaults on the rigged heads. Before, the correlation signatures were identical and the MACs were `F270`/`B315` in both versions.

Window check (7R 62-103 / 207-234, MAC 76-108 / 212-230):

- The MACs stay inside on every figure.
- The beams stay inside on everything except:
  - **Diamante**: 7R tilt 200-240, out in 72-84 of about 250 samples per head, in every variant. This is the same as before, not fixed.
  - **Hoja**: tilt 205-234, out in 17-26 samples.

The Simultaneo variants still work as before. Circulo Simultaneo gives beam tilt correlation 1, 1, 1, with the second pair's pan mirrored.

## 7. STROBO / STROBO SUAVE mantenidos - FIXED (D2, D3)

With AUTO running (Nivel Ambiente and Intensidad Ambiente running), the button was held and read 5 times over 0.6 s.

| Fixture | STROBO (w17) | STROBO SUAVE (w18) | Released |
|---|---|---|---|
| CromoWash | 248 | 202 | 0 |
| CLB2.4 / Vortex / Mini / WX | 247 | 200 | 0 |
| 7R | 234 | 199 | 255 |
| MAC | 248 | 202 | 0 |
| **MiN Wash #1 / #2** | **236 / 236** | **217 / 217** | 255 |
| **fog LEDs ch6 (all 4)** | **247** | **200** | 0 |

- The MiN combined Dimmer/Strobe channel now wins over the level's 255 while the button is held, and goes back to 255 on release.
- D2: MiN stays at full in Ambiente. Intensidad Ambiente, Total and Peak all read 255 on both MiN.
- The strobe never touches the fog pump (ch1): it stays 0 on STROBO and STROBO SUAVE without smoke held, and 255 while HUMO VERT is held.

## 9. Los blancos usan el emisor White - FIXED

CHARLA (w5) was read after 2.5 s:

- CromoWash, bars (all 8 segments), CLB2.4, Vortex, MiN, WX and fog LEDs: **(255,214,170)**, a warm white. Before, they were (85,44,0), a dim brown.
- Mini Led and MAC: **(85,44,0)+W170**, the RGBW split.
- 7R wheel 4 (White). Every dimmer is at 255.

The pastels are as in item 1. Achromatic flashes still use every emitter: FLASH and FLASH LENTO give (255,255,255) with W255 on the Mini and MAC, and so does Golpe Graves.

## 12. Lo que cambio la rejilla - FIXED-AS-RULED (D6)

- **Cabezas:** the workspace has no Cabezas RGBMatrix. There are 77 BarrasLed, 64 Lyres and 36 PAR matrices, and no `Cabezas - ` function or VC button. So no invisible Cabezas pattern is left (D6).
- **PAR (no regression):** Fill Rojo (w422) and Fill Azul (w424) light the Vortex in stage order, one every ~480 ms, with the spare #7 (x=600) last:
  - x = 854 at 37 ms, 3076 at 493, 5298 at 971, 6410 at 1446, 8632 at 1943, 10854 at 2423, 600 at 2903.
- **Lyres (no regression):** 3 rings per MAC, and both MACs are painted.
  - Fill (w459): 100 -> 110 -> 111.
  - Even/Odd (w465): 101/010 against 010/101.
  - Waves (w477): 100 -> 110 -> 011 -> 001.

## 14. Las 4 maquinas de humo vertical LED - FIXED-AS-RULED (D4)

- Fog LED dimmer (ch2), all four columns:
  - 255 in Intensidad Ambiente, Total and Peak;
  - flat 255 through Locura;
  - 0 under Todo Negro.

  For comparison, the Vortex dimmers read 110 in Ambiente and 255 in Total. This is D4, "stepped at 255", so the note "subir/bajar con los niveles" is superseded rather than failing.
- "Del color de la sala": verified (item 10).
- "Apagarse con Todo Negro": verified, all 7 channels are 0 on all 4 columns.
- CH6/CH7 at rest: strobe 0 and colour change 0. What 0 means on the machine is still for eyes.
- New with D3: ch6 strobes on STROBO, STROBO SUAVE, FLASH and FLASH LENTO (item 16).

## 16. Los flashes recuperados - FIXED (D1, D3, D7)

Each flash was held under AUTO.

| Control | Shutters | MiN | fog LEDs | Colour |
|---|---|---|---|---|
| FLASH (w12) | Cromo 248, CLB/Vortex/Mini/WX 247, MAC 248, 7R 234 | **236** | strobe **247**, (255,255,255) | white, W255 on Mini and MAC, 7R wheel 4 |
| FLASH LENTO (w13) | 202/200/200/200/200/202, 7R 199 | **217** | strobe **200**, white | white |
| FLASH COLOR (w14) | 248/247..., 7R 234 | **236** | strobe **0**, **(255,255,255)** | the running colour on the other fixtures |
| Golpe Graves (w257) | all 0 / Open, 7R 255 | 255 | 0 | white with W255 |

- **D3:** the columns strobe on FLASH and FLASH LENTO. On FLASH COLOR they go white and do not strobe. The scene writes `fx29 1,255 2..4,255 5,0`, which is the owner's "Flash Color: white, not strobing".
- **D1:** the buttons w12-w18 carry `Override="1" ForceLTP="1"`, and no Flash scene writes a pump channel.
  - Engine, HUMO YA (w15) held: the AF-150 stays 255 while FLASH, FLASH LENTO, FLASH COLOR, STROBO and STROBO SUAVE are each held and released. It goes to 0 only when HUMO YA is released.
  - HUMO VERT (w16) held: the column pump stays 255 through the same five flashes.
  - A flash neither starts nor cuts smoke.
- **D7 (MAC aim):** the two MACs read **92/221**, the wash window centre, in each of Centro (w111), Escenario (w137), Beams Abanico (w135) and Beams Cruce (w136), with or without AUTO. Before, they were 127/127.
  - Ola Vertical: over the first 13 s (148 samples), the MACs were at 127/127 **0 times**. They start at 92/229 and 92/216 and wave from there.
- **Beam fans are in stage order:**
  - Abanico: 20/22/23/21 = pan 62/75/89/102, tilt 220.
  - Cruce: 102/89/75/62, tilt 220.
- Centro: 7R pan 0 / tilt 130, unchanged. Escenario: 7R 156-162 / 189-204, unchanged.
- **Release of a position pick (D8):**
  - Under AUTO, the heads go to `Cabezas Suelo` (903, part of AUTO): 7R 0/130, MAC 92/221, never 127/127.
  - The movement collection does not restart by itself (522, 548 and 549 all Stopped at +6 s). It returns at the next energy step, as the frame label says.
  - With no state running, a release drops every head to 127/127.

## 5. "Quitar y poner un color no apaga las beam" - CHANGED-AS-RULED (D8)

The test was Rig Rojo (w70) under AUTO.

- Before: 7R (shutter 255, blade 255, wheel 99), RGB (85,0,255) at dimmer 110.
- Pick on: 7R blade 255, wheel 12, and every RGB family at (255,0,0). Status: 702 Stopped, 774 Running.
- **Pick off, at +0.2, +1, +3 and +5 s:**
  - 7R **blade 0** (Blade closed), wheel 12;
  - every RGB family at (0,0,0), dimmers 110 (MAC 255);
  - status 702 Stopped, 774 Stopped.
- Re-press the pick: blade 255 and everything red again. W after the release: 702 Running, blade 255, colour back.

So the half-lit case (beams red over a black rig) is gone: the beams now share the rig's fate. The room stays dark until W or the hook (the tablet presses the hook on release, per D8). The item's old reading, "the beams stay on", no longer holds, by design.

With AUTO stopped, the pick lights the 7R (blade 255, wheel 12) while every RGB dimmer is 0. On release the blade closes.

Gobo Shake (w168) is also clean on release:

- Under AUTO: gobo/jitter 10/64 while on, then **3/0** at +0.5, +3 and +6 s. Before, it stayed at 10/64 indefinitely.
- Under FIESTA: the same result, 3/0. The AUTO gobo animation 583 does not resume, and neither does 620.

## 6. Bancos y picks mantenidos - NO REGRESSION, with D9 applied

Base: AUTO plus Rig Cyan (w77). Key `1` was held in each bank.

| Bank (widget) | Held | Released (+50 ms) |
|---|---|---|
| BarrasLed (w186) | bars (255,0,0), **CLB2.4 #1 and #2 (255,0,0), fog LEDs 1 and 4 (255,0,0)**; the rest cyan | all (0,255,255) |
| Cabezas (w199) | CromoWash, Mini, MiN (255,0,0), 7R wheel 12 | all cyan, 7R 59 |
| PAR (w212) | Vortex (255,0,0) | cyan |
| PixelesLed (w225) | WX (255,0,0) | cyan |
| Lyres (w238) | MAC (255,0,0) | cyan |

- Beam Blue (w272): 7R 43 on all four heads, and 59 after release.
- Mezcla Ro/Am Cabezas (w308): Mini #1 red and #2 yellow; 7R 12, 12, 27, 27.
- Blanco Cabezas (w206): Mini (255,255,255,255), 7R 4.
- Each one returns to cyan within one read.

## 8. `<ExcludeFade>` en las ruedas - NO REGRESSION

- AUTO ran for 45 s. 7R ch8 was read on all four beams in 1326 reads, with no reads discarded.
- Values seen: 12, 19, 27, 35, 43, 51, 59, 83 and 99, all of them slot values.
- There were 12 changes, each one a single jump on all four heads at once (for example 51 -> 99 at 8.43 s), while the CromoWash was mid-crossfade (251,0,255).

## 10. HUMO VERT (U, w16) - NO REGRESSION

Fog columns as (pump, dimmer, R, G, B, strobe, colour change):

| Base | U held | Released |
|---|---|---|
| AUTO | (255,255,160,0,255,0,0), then it tracks the wheel (91,110,145) and (7,243,12); all 4 identical | pump 0, room colour |
| TODO NEGRO | (255,255,0,0,0,0,0): pump on, column dark | all 0 |
| AUTO + Rig Cyan | (255,255,0,255,255,0,0) | (0,255,0,255,255,0,0) |

The column is never white.

## 11. JUGAR - NO REGRESSION

1. AUTO, then Rig Rojo (w70): every family red, 7R wheel 12 with blade 255. Status: 774 Running, 702 Stopped, 767 Running.
2. F1 (w5): 767 Stopped, 770 Running, 774 Stopped.
3. W (w64): 702 Running, and the colour follows the wheel.

Variant: releasing AUTO (Q again) while the pick runs gives 767 Stopped and 774 Running, as before.

## 13. Humo, las dos cosas nuevas - NO REGRESSION

- AUTO starts 624 Running. The AF-150 fires at +0.2 s (255) and drops to 0 at +2.07 s.
- `cada 2 min` (w30): 624 Stopped and 625 Running; the pump fires at once (255, then 0 at +2.06 s).
- `cada 8 min` (w32): 627 Running; the pump fires at +0.2 s and drops at +2.07 s.
- Chaser holds: 2000 ms on, then 60000, 120000, 240000 or 480000 ms off.
- The vertical fog pump (ch1 on fx 29-32) read only 0 through the 45 s AUTO run.

## 17. Momento Locura - NO REGRESSION

F4 (w8), 60 samples at 250 ms:

- Dimmers: CromoWash #1-#4 take 39-46 distinct values, CLB 40, Vortex 40-50 and Mini 40, all between 0 and 253. At 4.6 s the CromoWash dimmers were 207/80/134/158.
- Colour: CromoWash was white in 0 of 60 samples, across 19 distinct wheel colours.
- Flat at 255: MiN, WX, MAC and the fog LED dimmer. The 7R shutter is 255.
- The 7R blade reads 255, apart from a 0 -> 255 ramp in the first 0.9 s. That ramp is the 1 s fade-in after PARAR TODO: in a 30 s trace it covers 8 reads, followed by 268 reads at 255.
