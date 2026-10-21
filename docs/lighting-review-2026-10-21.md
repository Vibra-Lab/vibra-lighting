# Lighting review, 2026-10-21

## Scope and 3D capture

The three generated workspaces were rebuilt from their descriptions and loaded by QLC+ 5.2.2. The checker covers console reachability, fixture capabilities, smoke pump ownership, flash channels, colour ownership, movement coverage, and concurrent movement clocks. The tablet map is generated from the same workspace as the operator console.

For a visual check, an isolated QLC+ instance played the `Fiesta` AUTO state from a workspace copy with input, output, and feedback patches removed. Its DMX vectors were applied to the current stage MVR in BlenderDMX. The images below are frame captures, not photographs of the venue:

| Previous independent rotations | Shared figure clock |
| --- | --- |
| ![Previous AUTO state](evidence/auto-movement-before.jpg) | ![Rebuilt AUTO state](evidence/auto-movement-after.jpg) |

The previous `Movimientos Cabezas` Collection started a random wash rotation and a random beam rotation together. Their independent step clocks selected unrelated figures. The rebuilt Collection starts one ordered Chaser; each step starts the matching wash and beam figure together. The eighth step pairs the wash circle with `Cascada Beams`. Both optics families now use the same 16 second EFX duration value and 5 second transition; QLC+ subtracts the transition from the effective figure loop. The generator retains the separate family sizes and the measured audience windows.

The captures confirm the patch, colour output and symmetric fixture positions in the model. The preview does not reproduce every physical beam sharply enough to settle aim, glare or the travelling cascade. Judge those from the room before changing the measured windows.

## White flash runtime probe

`Flash 100%` writes the white wheel slot (`4`) to all four 7R heads and `255` to the RGBW channels of both MAC heads. Its QLC+ button requests Override and ForceLTP. The static scene and semantic checks therefore describe white on those fixtures.

With AUTO running in the isolated QLC+ instance, a held flash was sampled 80 times at roughly 200 ms intervals. In one run, two single API reads briefly differed from white: the 7R wheels showed their AUTO value once, and the MAC RGBW channels showed an AUTO colour once. In a second run using three reads per sample and the median, one sample showed MAC RGBW at zero. The next samples returned to white. This reproduces an intermittent value in QLC+'s web channel snapshot, but does not prove the same frame reached physical DMX output; the instance had no output patch. The flash scene's priority is correct in the generated workspace. A capture from the actual output while AUTO and flash overlap is the remaining test before changing flash programming.

## Follow-up at the rig

Check the new AUTO figure sequence from the floor at Ambiente, Fiesta and Peak; confirm the mirrored sides and cascade feel coherent. Hold `Flash 100%` over running AUTO while recording physical DMX for the 7R colour wheels and MAC RGBW channels. These are the two points the offline checks and 3D model cannot resolve.
