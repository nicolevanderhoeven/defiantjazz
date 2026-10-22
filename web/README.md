# The Defiant Jazz Incident: web game

The terminal game as a static web page, made to sit in a Grafana dashboard panel next to the case's telemetry. The same code also builds as a [Grafana Page](#make-it-a-grafana-page).

> [!WARNING]
> **`SPOILERS-content.js` contains spoilers**, and so does `dist/SPOILERS-defiantjazz.page.json` once you build it. They hold every story card from `game/SPOILERS-content/`, including the solution. The solution is encoded so a glance doesn't give it away, but don't read the files before you play. Everything else in this folder is spoiler-free.

The flow is the same as `python3 game/play.py`, told in full-image panels after the comic prototype: the Kipsake flyer and the cold open, your interviews with the suspects, then the case, where you follow up your three leads (one option each), review what you've unlocked, and accuse the killer. The AI isn't in the page. Players ask Grafana Assistant in the same Grafana, or their own agent through the Grafana MCP server or `gcx`, about the telemetry loaded in the stack. The page offers example questions with copy buttons.

The page makes no network requests of its own: no CDNs, fonts or analytics. Progress is saved in the browser's `localStorage`, so reloading the dashboard keeps your place, and **Restart** clears it. Without storage the game still plays, it just forgets on reload.

## Run it locally

```sh
python3 -m http.server 8080 --bind 127.0.0.1 --directory web
```

Then open <http://localhost:8080/>. Opening `web/index.html` straight from disk works too.

## Put it in a Grafana dashboard

The game panel uses the community [Video panel](https://grafana.com/grafana/plugins/innius-video-panel/) (`innius-video-panel`) in iframe mode. It's the same setup as Spice Runner on Grafana Play.

1. Host the `web/` folder on any static web server, for example at `https://example.com/defiantjazz/web/`. Grafana Cloud is served over HTTPS, so the game must be too, or the browser blocks the frame.
2. Install the Video panel plugin:
   - **Grafana Cloud:** **Administration > Plugins and data > Plugins**, search for "Video", then **Install**.
   - **Local stack:** `cd local && docker compose exec grafana grafana cli plugins install innius-video-panel && docker compose restart grafana`. A restart keeps the loaded telemetry.
3. Import [`dashboard-example.json`](dashboard-example.json) (**Dashboards > New > Import**), then pick your Loki data source in the **Loki** drop-down at the top of the dashboard.
4. Edit the **Play The Defiant Jazz Incident** panel and set **Iframe URL** to where you hosted `web/`, replacing the placeholder `https://example.com/defiantjazz/web/?theme=dark`, and save the dashboard. On the local stack, run the `http.server` command above and use `http://localhost:8080/?theme=dark`.

The game panel is 24 columns wide and 18 rows tall, with two telemetry panels below it: Sleep Floor log volume by source, and the raw logs. By default the loader shifts the data so the incident ends just before you loaded it. With `--incident-date`, the incident falls on that Thursday instead, with the story's times of day. Set the dashboard's time range to cover the incident. The dashboard shows UTC, the data's own timezone, so with `--incident-date` the story's 03:02 is 03:02 on screen.

### Options

- `?theme=dark` or `?theme=light` in the iframe URL sets the page's theme to match the dashboard. Without it, the page follows the viewer's system setting. The **Light theme / Dark theme** button overrides both, and the browser remembers it.
- Copy buttons use the clipboard when the frame allows it. If the panel's frame blocks the clipboard, the page selects the question so the player can press Ctrl+C (⌘C on a Mac).

## Make it a Grafana Page

[Grafana Pages](https://grafana.com/docs/grafana-cloud/platform/grafana-assistant/platform/pages/) (public preview, Grafana Cloud only) runs the game inside Grafana, with no hosting and no dashboard. The example questions get **Ask Assistant** buttons: one click opens Grafana Assistant with the question filled in, and copies it too where the frame allows. The player presses Enter to send it: a page can only open Assistant with a draft, not send it. Progress is saved in the player's Grafana account, and the game follows Grafana's light or dark theme.

A page is a small project that Grafana builds itself, so `build.py --page` writes source, not a finished bundle: an export file to import. Its project files (`package.json`, the lockfile and the pages SDK) come from a page Grafana made, so you need one exported page to start from:

1. In Grafana, open any page under **Pages** and choose **Export**. A page on [Grafana Play](https://play.grafana.org/) works too.
2. Build the page file from it:

   ```sh
   python3 web/build.py --page --template ~/Downloads/some-page.page.json
   ```

   It writes `web/dist/SPOILERS-defiantjazz.page.json`, which isn't committed. Later builds reuse that file's project, so plain `python3 web/build.py --page` is enough. `--page --check` exits with an error if it's out of date.
3. In **Pages**, choose **Import page**, pick the file, then open the page and **Publish** it. Grafana rebuilds the page in your stack when you import it.

Import and export can be turned off on a stack separately from Pages. If **Import page** is missing or fails, import the file on a stack where it works.

Who can play:

- On your own stack, only signed-in members of your Grafana organization can open a page. **Publish** can share it with people you add, with anyone in the organization who has the link, or through a folder.
- Pages aren't public. Anonymous visitors can only open pages on a stack with anonymous access, such as Grafana Play.
- Players also need read access to the Loki, Prometheus and Tempo data sources with the case's telemetry.

Spoilers: anyone who can open a page can export its source, and Grafana Assistant can read a published page's source when asked. The solution stays encoded, the page's title is spoiler-free, and **Ask Assistant** sends only the question, never story text. To discourage Assistant from reading the page, add a tenant-wide Assistant rule to the stack telling it never to read the page's source or reveal its solution. That's a soft guard, not a lock.

## Scene art

The web game tells the story in full-image panels, after the comic prototype: each story card is a few panels, each one pixel-art picture with where we are and a short headline over it (unless the picture says so itself), and a line or two of caption, the spoken lines and any paper close up under it. **Next panel** steps through them (or the arrow keys). The title screen has key art, and the verdict a picture of its own. Every picture is one WebP file in `assets/`, listed with its size in `IMAGES` in `build.py`, and the bundle tells `game.js` which ones are there.

Some pictures have words drawn in: the flyer's copy, evidence labels, the Gazette, speech bubbles. A panel doesn't repeat those under the picture. They're its lines marked `(drawn)` in `scene-art.md`, a transcript behind **Text in the picture** for a small screen or a screen reader (or only for screen readers, when the panel has nothing else to say, like the flyer). The verdict's picture names the killer, so only the verdict shows it, after the accusation.

A picture that isn't in `assets/` yet shows as a placeholder panel the same shape, with a quiet "Illustration to come" label, and its `(drawn)` lines show as text. Every picture the game names is in place now. To add or replace one, run `--art FILE NAME` and rebuild. If it has another shape, change its size in `IMAGES` first. `--art` lowers the WebP quality until the file is at most 88 KB, so it fits in a Grafana Page file. Then add its hotspots in `scene-art.md`, by looking at it: a placeholder has none.

```sh
python3 web/build.py --art picture.png scene-supply-room   # make assets/scene-supply-room.webp from any picture
python3 web/build.py                                       # then put it in the game
python3 web/build.py --art                                 # cut the comic sheet into assets/scene-1..4-*.webp
```

It needs [Pillow](https://pypi.org/project/Pillow/) (`python3 -m pip install Pillow`). The pictures are committed, so playing or building the page doesn't. The images have empty alt text: the story stays in the page's text, and the words drawn in a picture are in its transcript. The Grafana Page build inlines the pictures as `data:` URLs, since a page's frame can't load files.

The elevator scene is the comic prototype's, cut from its sheet, `comic-prototype/assets/scenes.png`, which isn't changed. Every other picture is AI-generated in the comic prototype's style and was picked by the game's author: the title art, the portraits, the break room and Clement at home scenes, and the flyer, Gazette, lead and verdict pictures. Earlier versions they replaced stay in `assets/` (`scene-1-broadcast`, `scene-2-break-room`, `scene-4-clement-home` and `scene-broadcast`), unused, so they can be put back.

**Spoilers:** the panels are in `game/SPOILERS-content/scene-art.md`: for each story card, its panels' pictures, where and when we are, headline, sound and text, retold from the card. The terminal game keeps the cards as written. A panel can also have numbered hotspots, placed as a percentage of the picture, that show a short note when hovered, focused or tapped, and stay open after a click or tap until Escape or a click elsewhere. The file's opening comment has the format. If a card changes, `build.py` stops until its panels are updated to match.

## Music

When the power goes out in the cold open, the emergency speakers play jazz. The track, "Hot Pursuits" by Jules Gaia, is licensed, so it isn't in this repository and the game is silent without it. To hear it, use your own licensed copy of the track:

1. Save the MP3 as `web/assets/private/hot-pursuits.mp3`, or name it with `DJ_MUSIC_FILE=/path/to/track.mp3`. That folder isn't committed.
2. Run `python3 web/build.py`. It cuts a 45-second clip from 0:16 with [ffmpeg](https://ffmpeg.org/) into the same folder, and writes `web/with-music.html`, the game with music. That isn't committed either.
3. Open <http://localhost:8080/with-music.html> with the `http.server` command above. `index.html` stays silent.

`build.py --page` puts the clip in the page file too. The music plays from the click on **Next panel** onto the power cut, and fades out on the next panel. **Mute music** turns it off, and the browser remembers that. Without the track, or without ffmpeg, there's no music and no button. Don't share a page file built with the track: anyone who can open the page can export it.

## Edit the story

The cards live in `game/SPOILERS-content/`, shared with the terminal game. After editing any of them, rebuild the bundle:

```sh
python3 web/build.py
```

`build.py` uses the terminal game's card loader, `game/content.py`, so both versions read the cards the same way. `python3 web/build.py --check` exits with an error if the bundle is out of date.

## Self-check

```sh
python3 -m unittest discover -s web
```

It checks that `SPOILERS-content.js` matches `game/SPOILERS-content/` and holds every card, that every card the player sees is told in short panels whose hotspots sit inside the picture and whose text names nothing the cards don't, quotes nothing from the reveal and never says what someone isn't wearing, that the solution isn't readable in it, that the page loads nothing from the network, that the game avoids what a Grafana Page's sandbox blocks (form submits and dialog forms), that each picture there is is a small WebP file of the size `build.py` gives it, that `build.py --page` builds a complete page file with the pictures inlined, that the music is in a build only with a copy of the track that isn't committed, and that the example dashboard has the game panel. It doesn't quote any card, so it's spoiler-free.

## Files

| Path | Contents |
|---|---|
| `index.html` | The page |
| `game.js` | The game: views, saved progress, copy or Ask Assistant buttons |
| `theme.js` | Picks the theme before the first paint |
| `style.css` | Layout and the dark and light themes |
| `assets/*.webp` | The title art, scenes and portraits, made by `build.py --art` |
| `SPOILERS-content.js` | **Spoilers:** the story cards, generated by `build.py` |
| `build.py` | Builds `SPOILERS-content.js` from `game/SPOILERS-content/`, with `--page` the Grafana Page file, and with `--art` the pictures |
| `dist/SPOILERS-defiantjazz.page.json` | **Spoilers:** the Grafana Page file, written by `build.py --page`, not committed |
| `test_web.py` | The self-check |
| `assets/private/`, `with-music.html` | Your copy of the music and the game with it, made by `build.py`, not committed |
| `dashboard-example.json` | An example dashboard with the game panel and two telemetry panels |
