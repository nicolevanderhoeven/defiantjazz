# Kipsake: interactive comic preview

A standalone, silent four-scene prototype for Nicole. Everything lives in this folder; the existing web and terminal games are unchanged.

Run from the repository root:

```sh
python3 -m http.server 8080 --bind 127.0.0.1 --directory comic-prototype
```

Open http://localhost:8080. No build, install, external fonts, or service connection is required. Opening index.html directly also works.

Click numbered markers or type HELP, LOOK, EXAMINE <object>, TALK <person>, NEXT, or RESTART. Scene tabs allow direct review. The home scene has three repeatable evidence close-ups; Escape closes them. Progress resets on reload.

This is an authored visual demo, not an AI chat. No Grafana requests, accusation flow, audio, or saved progress. The selected home visit occurs later than the opening incident. The box adapts the original cardboard folder. Physical evidence is human-facing; no full story or solution bundle is loaded.

Scenes, frames, aliases, hotspots, and responses are in scenes.js. app.js handles the console and navigation. Artwork is a local AI-generated four-panel pixel-art sheet in assets/scenes.png; CSS selects each quarter. Text and readable evidence are HTML, not embedded in the art. Reduced-motion settings disable the marker animation.

## Regenerate or continue

[PROMPT.md](PROMPT.md) contains the reusable regeneration brief, artwork prompt, and instructions for extending this prototype to the complete canonical story. The full-story section is a future implementation brief; this PR contains the four-scene preview only. Keep future changes within this directory so the prototype can evolve independently of the existing game.
