# Regeneration and full-story continuation prompt

Copy the prompt below into a coding agent working in this repository. It describes both the approved prototype and the next stage. Regenerating the prototype does not require implementing the full game.

## Prompt

Build or continue **The Defiant Jazz Incident**, an interactive comic murder mystery in which the player uses an AI to query a Grafana dataset and combines those records with physical clues seen only by the player.

### Isolation

Keep all implementation, assets, documentation, and any new checks inside `comic-prototype/`. This is an independent alternative to Nicole’s existing game. Do not modify `web/`, `game/`, `telemetry/`, `loader/`, or `local/`. Read existing story and engine files as references, but do not import them at runtime or require their server. Work on a separate feature branch. Do not merge or publish without a separate request.

### Approved visual direction

Cinematic, detailed pixel art with dithered shading and consistent characters, inspired by 1980s text adventures and corporate daylight horror. Use cream, faded teal, dusty peach, and institutional symmetry; transition to bruised purple and emergency red during the blackout. The world is Port Quiet and the corporation is Kipsake. Kipsake pays people to sleep while their sleepwalking selves work. Waking selves remember home; sleepwalkers remember work. Day staff remain awake.

Use a wide illustrated panel above a persistent, crisp text console. Keep text, captions, and clue details in accessible HTML rather than relying on words inside the artwork. Support small ambient animations, readable close-ups, responsive layouts, keyboard navigation, visible focus, and reduced motion. Keep the experience silent. No heavy CRT distortion, external fonts, CDNs, or runtime service dependencies for the prototype.

The existing artwork in `assets/scenes.png` is an approved starting point. Preserve subsequent human art edits. Do not regenerate or overwrite assets just because this prompt is being reused; replace art only when explicitly requested, saving variants separately. The sheet has four equal horizontal scene strips stacked vertically. Use the imagegen skill for raster artwork when available.

### Recreate the four-scene prototype

Use plain static HTML, CSS, and JavaScript, with scenes defined as data containing frames, narration, hotspots, aliases, and authored responses. No installation or build step. Serve the directory with Python’s static HTTP server; direct file opening should also work.

1. **Recruitment broadcast:** corporate advertising promises productive sleep: “Your days are yours. Let your nights work for you.” Show a serene household beside an immense office of sleeping workers. Reveal unsettling details through inspection and successive captions.
2. **Cocoa Hour:** six Deep Sleep Operations clerks and Mr. Hale celebrate a quota reward in Break Room 2. Inspect cups, cocoa urn, emergency speaker, badges, and coworkers. Clement has brown wavy hair, a mustard shirt, and a multicoloured fringed scarf. Establish the memory split without resolving the mystery.
3. **Elevator and music:** main power fails, jazz wakes the workers, then stops when power returns five minutes later. Convey sound with captions and lighting. The supervisor is discovered dead; do not identify the killer. Use the canonical story for precise events.
4. **Clement at home:** at 18:40, Mr. Whitlow has no lanyard but wears his scarf and holds an open cardboard box. This deliberately adapts the original folder. Inspect the newspaper clipping, marked evacuation plan, and lighthouse photograph through readable, repeatable close-ups. Clearly distinguish physical evidence from telemetry.

Label time/location jumps as selected scenes. Support HELP, LOOK, EXAMINE <object>, TALK <person>, NEXT, and RESTART. Hotspots and suggested command buttons must use the same response path as typed commands. Unknown input should give useful guidance. Include review navigation between scenes. Label authored interaction honestly: no simulated AI query answers. No accusation, persistence, or live Grafana connection is needed for this prototype.

### Continue to the full story when requested

Read `game/README.md`, `game/engine.py`, and `game/content.py` to understand the existing rules before adapting them. **Story files under `game/SPOILERS-content/` contain spoilers, including the solution.** They are authoring references for the implementation agent, never context for the player’s investigating AI. Keep spoiler-bearing adaptations clearly named, and do not expose the reveal in previews or documentation.

Adapt the complete canonical flow, rather than inventing a new solution:

- Introduction and cold open, then all three suspects’ security statements.
- An investigation hub with questions to the external AI, unlocked-evidence review, investigation choices, and accusation.
- Three investigation stages in order: crime scene, home visit, final interview. Each stage offers three choices; the player sees only the chosen option. Present the Outside World handout at its canonical point before the home visit.
- Preserve the story’s dialogue, clue ownership, timing uncertainty, suspect aliases, and accusation/reveal behavior from the engine and content. Convert each selected card into interactive frames without adding facts that change the deduction.
- Keep unrestricted scene navigation confined to an explicitly labelled preview mode; the full game must respect evidence unlocks. Reuse canonical content through a documented local authoring/build process if useful, but output a self-contained directory and never change the source game.
- Keep readable physical clues and interviews available for review after unlocking them. Present an explicit confirmation before an accusation ends play and unlocks the solution.

For the first full-story adaptation, keep Grafana Assistant or another investigator AI alongside the comic, as in the existing web game, with copyable example questions. Never send human-only panels, dialogue, clue contents, or the solution automatically to that AI. A future embedded AI connection is a separate integration task: establish its backend, authentication, read-only Grafana access, and context boundary before implementing it. Never embed credentials in static assets or pretend authored answers came from Grafana.

### Validation and delivery

For the prototype, manually walk every frame and scene; compare typed and clicked commands; inspect all three home clues, including repeat opening and Escape dismissal; test unknown commands, restart, keyboard controls, and a narrow viewport without horizontal overflow. Respect reduced motion and check readable text contrast. Check browser errors and JavaScript syntax. Run `python3 -m unittest discover -s web` to verify the existing game stays intact.

For the full game, add meaningful checks inside `comic-prototype/` for branching/unlocking, evidence review, accusation confirmation, and keeping human-only evidence out of AI handoff payloads. Verify representative complete paths against the canonical engine. Document how to run, what is mocked or external, and any remaining limitations. Keep all changes reviewable as an isolated PR; do not merge automatically.

### Original artwork generation brief

If replacement artwork is explicitly requested, use this brief as a starting point:

> One cinematic pixel-art contact sheet, exactly four equal wide landscape panels stacked vertically, no gutters, no text or UI. Detailed adventure-game pixel art with dithered shading and cream, dusty teal, peach colours. Panel 1: serene sleeping woman in a peach bed on the left; immense teal office with rows of sleeping workers and an artificial sun on the right, cheerful but sinister. Panel 2: symmetrical cream-and-teal break room, six office clerks and an older male supervisor in a dark suit, cocoa cups on a long table, silver cocoa urn on the right, emergency speaker high on the left; Clement has brown wavy hair, mustard shirt, multicoloured fringed scarf. Panel 3: centred open elevator in a dark purple corridor with red emergency lighting, overhead indicator and wall speaker; no corpse or violence. Panel 4: the same Clement at home holding an open cardboard box, warm lamp, rainy window, lighthouse photograph and folded papers; intimate and melancholy. Consistent characters, deliberate pixels, full bleed.
