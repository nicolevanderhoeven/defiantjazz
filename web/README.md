# The Defiant Jazz Incident: web game

The terminal game as a static web page, made to sit in a Grafana dashboard panel next to the case's telemetry. The same code also builds as a [Grafana Page](#make-it-a-grafana-page).

> [!WARNING]
> **`SPOILERS-content.js` contains spoilers**, and so does `dist/SPOILERS-defiantjazz.page.json` once you build it. They hold every story card from `game/SPOILERS-content/`, including the solution. The solution is encoded so a glance doesn't give it away, but don't read the files before you play. Everything else in this folder is spoiler-free.

The flow is the same as `python3 game/play.py`: the Kipsake advert and the cold open, your interviews with the suspects, then the case, where you follow up your three leads (one option each), review what you've unlocked, and accuse the killer. The AI isn't in the page. Players ask Grafana Assistant in the same Grafana, or their own agent through the Grafana MCP server or `gcx`, about the telemetry loaded in the stack. The page offers example questions with copy buttons.

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

[Grafana Pages](https://grafana.com/docs/grafana-cloud/platform/grafana-assistant/platform/pages/) (public preview, Grafana Cloud only) runs the game inside Grafana, with no hosting and no dashboard. The example questions get **Ask Assistant** buttons that open the question in Grafana Assistant for the player to check and send. Progress is saved in the player's Grafana account, and the game follows Grafana's light or dark theme.

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

Pixel-art pictures sit above parts of the story: key art on the title screen, a scene above the Kipsake advert, the cold open's "What happened that night", and the Elevator car 1 and Clement at home leads, and a portrait above each suspect's opening statement. They're one WebP file each in `assets/`, listed with their sizes in `IMAGES` in `build.py` and `SCENES` in `game.js`.

The elevator scene is the comic prototype's, cut from the comic prototype's sheet, `comic-prototype/assets/scenes.png`, which isn't changed. The title art, the portraits and the broadcast, break room and Clement at home scenes are AI-generated in the comic prototype's style, and were picked by the game's author. They replaced the prototype's versions of those three scenes, which stay in `assets/` (`scene-1-broadcast`, `scene-2-break-room`, `scene-4-clement-home`), unused, so they can be put back.

```sh
python3 web/build.py --art                        # cut the sheet into assets/scene-1..4-*.webp
python3 web/build.py --art picture.png portrait-agnes   # make assets/portrait-agnes.webp from any picture
```

It needs [Pillow](https://pypi.org/project/Pillow/) (`python3 -m pip install Pillow`). The pictures are committed, so playing or building the page doesn't. To replace a picture, run `--art FILE NAME` with a picture of the same shape, or, for a new size, update it in both `IMAGES` and `SCENES` first. If the sheet changes, update the seams in `SCENES` in `build.py` and run `--art` again. The art holds no clue text, so the images have empty alt text and all the story stays in the page's text. The Grafana Page build inlines the pictures as `data:` URLs, since a page's frame can't load files.

**Spoilers:** what goes with each scene and portrait is in `game/SPOILERS-content/scene-art.md`: where and when we are, a caption, an optional line where the art doesn't match the story, and an optional web text for the card, which leaves out what the image shows. The terminal game keeps the cards as written. Each scene also has numbered hotspots, placed as a percentage of the image, that show a short note when hovered, focused or tapped, and stay open after a click or tap until Escape or a click elsewhere. The portraits have none: the statement below each one says what's on screen. The file's opening comment has the format. If a card with web text changes, `build.py` stops until that text is updated to match.

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

It checks that `SPOILERS-content.js` matches `game/SPOILERS-content/` and holds every card, that each scene has a caption and hotspots inside the image (portraits need only a caption) whose text names nothing the cards don't and quotes nothing from the reveal, that the solution isn't readable in it, that the page loads nothing from the network, that the game avoids what a Grafana Page's sandbox blocks (form submits and dialog forms), that each picture is a small WebP file of the size `build.py` and `game.js` give it, that `build.py --page` builds a complete page file with the pictures inlined, and that the example dashboard has the game panel. It doesn't quote any card, so it's spoiler-free.

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
| `dashboard-example.json` | An example dashboard with the game panel and two telemetry panels |
