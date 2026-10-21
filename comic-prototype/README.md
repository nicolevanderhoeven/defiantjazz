# Kipsake: interactive comic preview

A standalone, silent five-scene prototype for Nicole. Everything lives in this folder; the existing web and terminal games are unchanged.

Run from the repository root:

```sh
python3 -m http.server 8080 --bind 127.0.0.1 --directory comic-prototype
```

Open http://localhost:8080. No build, install, external fonts, or service connection is required. Opening index.html directly also works.

Click numbered markers or type HELP, LOOK, EXAMINE <object>, TALK <person>, NEXT, or RESTART. Scene tabs allow direct review. The home scene has three repeatable evidence close-ups; Escape closes them. Progress resets on reload.

This is an authored visual demo, not an AI chat. No Grafana requests, accusation flow, audio, or saved progress. The selected home visit occurs later than the opening incident. The box adapts the original cardboard folder. Physical evidence is human-facing; no full story or solution bundle is loaded.

Scenes, frames, aliases, hotspots, and responses are in scenes.js. app.js handles the console and navigation. Artwork is a local AI-generated four-panel pixel-art sheet in assets/scenes.png; CSS selects each quarter. Text and readable evidence are HTML, not embedded in the art. Reduced-motion settings disable the marker animation.

## Regenerate or continue

[PROMPT.md](PROMPT.md) contains the reusable regeneration brief, artwork prompt, and instructions for extending this prototype to the complete canonical story. The full-story section is a future implementation brief; the prototype contains selected scenes only. Keep future changes within this directory so the prototype can evolve independently of the existing game.


## Comic statement pages

The opening uses `assets/sleep-self-v4.png`: the same woman sleeping, then a transparent double exposure of her getting up and walking, then working at her desk at night. No spectral glow or ghost trail. Earlier variants are retained in `assets/sleep-self.png` and `assets/sleep-self-v2.png`. The Kipsake emblem is a local SVG; the company name and “Earn while you sleep” slogan are readable HTML. This is an advertising metaphor, not an additional supernatural rule of the mystery. The original four-strip artwork is preserved.

After the elevator chapter, The statements shows Agnes, Bertram, and Clement on separate interview pages, with three sequential panels for one person on each page. NEXT moves from Agnes to Bertram to Clement. The panels stack on narrow screens. Speech bubbles are selectable HTML text; TALK echoes the current person’s full statement in the console. Dialogue is adapted from the canonical opening testimonies without loading the solution. `statements.js` contains this human-facing adaptation and the opening-art override; `assets/statements.png` supplies the portrait triptych. Other scenes also show a speech bubble when you TALK to someone.

The transparent sleepwalking figure belongs in the middle foreground, in front of the bed: her body overlaps the duvet, which remains visible through her. Preserve the earlier image variants when revising the art.

The recruitment chapter has one panel: Kipsake and “Your rest. Our progress.” at upper left, “Earn while you sleep” at upper right above the worker. NEXT goes directly to Cocoa Hour.


Cocoa Hour is one panel (“Please enjoy your reward.”), using `assets/cocoa-night.png`. Its cast is exactly three sleepwalking clerks plus awake supervisor Mr. Hale. Timings, first-name character labels, and interview dialogue follow Nicole’s updated night-shift story: cocoa at 03:00, outage at 03:02–03:07, interviews after the outage, home visit at 06:40. The player asks the questions. The older six-clerk art remains only in the archived sheet; the runtime uses the new scene image.

Interview layout update: group by person. The Agnes page shows all three of her exchanges, then NEXT opens Bertram’s three panels, then Clement’s. Each page repeats only that person’s portrait. TALK repeats the current person’s complete statement. The elevator chapter is one panel summarizing the 03:02–03:07 outage and discovery; NEXT goes directly to Agnes’s interview.
