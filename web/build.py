#!/usr/bin/env python3
"""Bundle the game's story cards into web/SPOILERS-content.js for the web version.

    python3 web/build.py           # write web/SPOILERS-content.js
    python3 web/build.py --check   # exit 1 if it's out of date

    python3 web/build.py --page --template FILE   # write web/dist/SPOILERS-defiantjazz.page.json
    python3 web/build.py --page                   # the same, reusing that file's template
    python3 web/build.py --page --check           # exit 1 if that file is out of date

    python3 web/build.py --art     # cut the comic sheet into web/assets/scene-*.webp
    python3 web/build.py --art FILE NAME   # make web/assets/NAME.webp from the picture FILE

--page builds the game as a Grafana Page: a page export file to import in Grafana
(Pages > Import page). A page is a small React project that Grafana builds itself,
so the file is source only. The game's own files (game.js, style.css and the story
cards) go into src/ next to a few lines of glue; the project around them (package.json,
lockfile and the vendored pages SDK) comes from FILE, an export of any existing page,
since only a page Grafana made has the versions that Grafana's builder expects.

--art cuts the four scene strips out of the comic prototype's art sheet,
comic-prototype/assets/scenes.png (read only, never changed), into one WebP file per
scene in web/assets/. With FILE and NAME, it makes one of the game's pictures (IMAGES below)
from any picture instead, at the size the game uses. The game shows them as header art,
and the title's key art. Each picture is its own file, so new art for one just replaces
that file. It needs Pillow (python3 -m pip install Pillow); the pictures are committed, so
nothing else needs it. Their captions, hotspots and the web game's text beside them are in
game/SPOILERS-content/scene-art.md, bundled with the cards.

SPOILERS: the bundle holds every card in game/SPOILERS-content/, including the
reveal. The reveal is base64-encoded so a glance at the file doesn't spoil it,
and the page only decodes it after the player accuses and confirms.

The cards are parsed by game/content.py, the same loader the terminal game uses,
so game/SPOILERS-content/ stays the one source of truth. Run this after editing
any card there.
"""

import argparse
import base64
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "SPOILERS-content.js")
PAGE_PATH = os.path.join(HERE, "dist", "SPOILERS-defiantjazz.page.json")
ASSETS = os.path.join(HERE, "assets")
ART_PATH = os.path.join(os.path.dirname(HERE), "game", "SPOILERS-content", "scene-art.md")
SHEET = os.path.join(os.path.dirname(HERE), "comic-prototype", "assets", "scenes.png")
# The sheet's four scene strips, top to bottom, as (name, first row, end row). The strips
# aren't quite equal, so these are the seams measured in the sheet.
SCENES = (
    ("scene-1-broadcast", 0, 361),
    ("scene-2-break-room", 361, 707),
    ("scene-3-elevator", 707, 1071),
    ("scene-4-clement-home", 1071, 1448),
)
# The pictures the game shows, as name: (width, height). Wide scenes and portraits are 3:1,
# the title's key art 16:9; game.js knows the sizes. The partner's sheet scenes that new art
# replaced stay in web/assets/, unused, so they can be put back by naming them here.
IMAGES = {
    "scene-broadcast": (1200, 400),
    "scene-break-room": (1200, 400),
    "scene-3-elevator": (1086, 364),
    "scene-clement-home": (1200, 400),
    "portrait-agnes": (1200, 400),
    "portrait-bertram": (1200, 400),
    "portrait-clement": (1200, 400),
    "title-splash": (1536, 864),
}
# The title's key art goes with the title screen, not a card, so scene-art.md doesn't list it.
TITLE_ART = "title-splash"
# Lossy WebP: the sheet is painted, not drawn on a pixel grid, so lossless is 5 to 10 times
# larger for no visible gain. The page scales the scenes with image-rendering: pixelated.
WEBP_QUALITY = 80
# Spoiler-free: Grafana shows the title in lists and gives it to Assistant as context.
PAGE_TITLE = "The Defiant Jazz Incident"
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "game"))

import content  # noqa: E402
import engine  # noqa: E402

HEADER = """\
// SPOILERS: generated from game/SPOILERS-content/ by web/build.py. Don't edit by hand.
// The reveal is base64-encoded JSON; the page decodes it only after the player accuses.
"""


def _card(card):
    return {"title": card.title, "body": card.body, "meta": card.meta}


def data(cards=None):
    """Everything the web page needs, as plain JSON-ready values."""
    cards = cards or content.load()
    reveal = json.dumps([_card(c) for c in cards.reveal.cards], ensure_ascii=False)
    return {
        "banner": engine.BANNER,
        "suspects": content.SUSPECTS,
        "leadKinds": engine.LEAD_KIND,
        "leadShort": engine.DECISION_SHORT,
        "advert": _card(cards.advert),
        "coldOpen": _card(cards.cold_open),
        "testimonyIntro": cards.testimony_intro,
        "testimonies": [_card(c) for c in cards.testimonies],
        "outsideWorld": _card(cards.outside_world),
        "decisions": [
            {"title": d.title, "prompt": d.prompt, "options": [_card(c) for c in d.options]}
            for d in cards.decisions
        ],
        "aliases": cards.aliases,
        "art": scene_art(cards),
        "reveal": base64.b64encode(reveal.encode("utf-8")).decode("ascii"),
    }


def fingerprint(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]


def scene_art(cards=None, path=ART_PATH):
    """game/SPOILERS-content/scene-art.md as {card title: its scene}: the image, its caption,
    the web game's text for the card, and the hotspots. The file's comment has the format."""
    cards = cards or content.load()
    shown = [cards.advert, cards.cold_open, cards.outside_world] + list(cards.testimonies)
    shown += [c for d in cards.decisions for c in d.options]
    by_title = {c.title: c for c in shown}
    names = [name for name in IMAGES if name != TITLE_ART]
    with open(path, encoding="utf-8") as f:
        section = content.parse_section(f.read(), path)
    art, current = {}, None
    for c in section.cards:
        where = f"{os.path.relpath(path)}: {c.title!r}"
        if c.title.startswith(("scene-", "portrait-")):
            if c.title not in names:
                raise content.ContentError(f"{where}: no such picture in IMAGES in web/build.py")
            card = by_title.get(c.meta.get("card"))
            if not card or card.title in art:
                raise content.ContentError(f"{where}: 'card:' must name a story card no other scene has")
            if not c.meta.get("where") or not c.meta.get("caption"):
                raise content.ContentError(f"{where}: needs 'where:' and 'caption:'")
            if c.body and c.meta.get("source") != fingerprint(card.body):
                raise content.ContentError(
                    f"{where}: the card {card.title!r} has changed since this text was written from it. "
                    f"Update the text to match, then set 'source: {fingerprint(card.body)}'.")
            current = {"scene": c.title, "where": c.meta["where"], "caption": c.meta["caption"],
                       "story": c.meta.get("story"), "before": c.meta.get("before"),
                       "body": c.body or None, "hotspots": []}
            art[card.title] = current
            continue
        at = re.fullmatch(r"(\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?)", c.meta.get("at", ""))
        if current is None or not at or not c.body:
            raise content.ContentError(f"{where}: a hotspot needs a scene above it, 'at: x, y' and some text")
        x, y = (float(v) if "." in v else int(v) for v in at.groups())
        if not (0 <= x <= 100 and 0 <= y <= 100):
            raise content.ContentError(f"{where}: 'at:' is a percentage of the image, 0 to 100")
        current["hotspots"].append({"label": c.title, "x": x, "y": y, "body": c.body})
    if sorted(a["scene"] for a in art.values()) != sorted(names):
        raise content.ContentError(f"{os.path.relpath(path)}: expected one card for each of {', '.join(names)}")
    return art


def render(cards=None):
    body = json.dumps(data(cards), ensure_ascii=False, indent=1)
    return f"{HEADER}window.DJ_CONTENT = {body};\n"


# ---- Scene art -------------------------------------------------------------------

def scene_path(name):
    return os.path.join(ASSETS, name + ".webp")


def cut_scenes(sheet=SHEET, out=ASSETS):
    """Write one WebP file per scene strip of the sheet into out. The sheet isn't changed."""
    try:
        from PIL import Image
    except ImportError:
        sys.exit("--art needs Pillow: python3 -m pip install Pillow")
    with Image.open(sheet) as im:
        im = im.convert("RGB")
        if im.height != SCENES[-1][2]:
            sys.exit(f"{os.path.relpath(sheet)} is {im.width}x{im.height}, not the {SCENES[-1][2]} rows "
                     "SCENES in web/build.py expects: measure the new seams and update SCENES.")
        os.makedirs(out, exist_ok=True)
        for name, top, bottom in SCENES:
            path = os.path.join(out, name + ".webp")
            im.crop((0, top, im.width, bottom)).save(path, "WEBP", quality=WEBP_QUALITY, method=6)
            print(f"Wrote {os.path.relpath(path)} ({os.path.getsize(path) // 1024} KB).")


def make_image(src, name, out=ASSETS):
    """Write web/assets/NAME.webp from the picture src, scaled to the size IMAGES gives it."""
    try:
        from PIL import Image
    except ImportError:
        sys.exit("--art needs Pillow: python3 -m pip install Pillow")
    if name not in IMAGES:
        sys.exit(f"{name} isn't one of the game's pictures: {', '.join(IMAGES)}")
    size = IMAGES[name]
    with Image.open(src) as im:
        if abs(im.width / im.height - size[0] / size[1]) > 0.01:
            sys.exit(f"{os.path.relpath(src)} is {im.width}x{im.height}, not the shape of {name} "
                     f"({size[0]}x{size[1]}): crop it first, or change its size in IMAGES and game.js.")
        path = os.path.join(out, name + ".webp")
        im.convert("RGB").resize(size, Image.LANCZOS).save(path, "WEBP", quality=WEBP_QUALITY, method=6)
    print(f"Wrote {os.path.relpath(path)} ({os.path.getsize(path) // 1024} KB).")


# ---- Grafana Page ----------------------------------------------------------------

# What a page takes from its template. Everything else in the template (its src/, its
# style and data bindings) belongs to the page it was exported from.
TEMPLATE_FILES = ("package.json", "pnpm-lock.yaml", "pnpm-workspace.yaml", "tsconfig.json")
TEMPLATE_DIRS = ("packages/",)

GENERATED = "Generated by web/build.py --page from web/. Edit web/ and rebuild, not this file."

MAIN_TSX = f"""\
// {GENERATED}
import {{ useEffect }} from 'react';
import {{ createRoot }} from 'react-dom/client';
import {{ PageProvider, pageReady, usePageContext }} from '@grafana/pages';
// Order matters: the host puts the markup in place and sets window.DJ_HOST before game.js runs.
import {{ setColorMode }} from './host';
import './style.css';
import './page.css';
import './SPOILERS-content.js';
import './game.js';

function Root() {{
  const {{ colorMode }} = usePageContext();
  useEffect(() => setColorMode(colorMode), [colorMode]);
  useEffect(pageReady, []);
  return null;
}}

createRoot(document.getElementById('root')!).render(
  <PageProvider>
    <Root />
  </PageProvider>
);
"""

HOST_TS = f"""\
// {GENERATED}
// The hooks game.js looks for in a Grafana Page: saved progress in the viewer's Grafana
// user storage, Grafana's theme, Ask Assistant and the header art. Only the question goes to Assistant.
import {{ grafana, openAssistant }} from '@grafana/pages';
import {{ MARKUP }} from './markup';
import {{ SCENES }} from './scenes';

declare global {{
  interface Window {{
    DJ_HOST?: object;
  }}
}}

let mode: string | undefined;
let onMode: ((mode: string) => void) | undefined;

export function setColorMode(next: string) {{
  mode = next;
  onMode?.(next);
}}

document.body.insertAdjacentHTML('afterbegin', MARKUP);

window.DJ_HOST = {{
  storage: {{
    getItem: (key: string) => grafana.userStorage.getItem(key),
    setItem: (key: string, value: string) => grafana.userStorage.setItem(key, value),
  }},
  onTheme(callback: (mode: string) => void) {{
    onMode = callback;
    if (mode) callback(mode);
  }},
  askAssistant: (prompt: string) => openAssistant({{ prompt }}),
  // The page's frame can't load files, so the header art comes inline.
  scenes: SCENES,
}};
"""

# Grafana's page frame styles body and fieldset after style.css loads; keep the game's.
PAGE_CSS = f"""\
/* {GENERATED} */
html body {{
  background: var(--bg);
  color: var(--text);
  font: 15px/1.55 Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}}
html fieldset {{ margin: 0 0 16px; }}
"""

SCRIPT_DTS = f"// {GENERATED}\n// A plain script, imported for its side effects.\nexport {{}};\n"


def page_markup():
    """The body of index.html without its scripts or the no-JavaScript note."""
    with open(os.path.join(HERE, "index.html"), encoding="utf-8") as f:
        page = f.read()
    body = page.split("<body>", 1)[1].split("<script", 1)[0]
    body = re.sub(r"\s*<noscript>.*?</noscript>", "", body, flags=re.S)
    return body.strip() + "\n"


def read_template(path):
    """The text files of a page export: a file saved with Export in Grafana (plain text),
    or the export API's response (base64)."""
    with open(path, encoding="utf-8") as f:
        doc = json.load(f)
    if doc.get("kind") == "PageExport":
        files = doc["source"]["files"]
    elif isinstance(doc.get("data"), dict) and "source" in doc["data"]:
        files = {k: base64.b64decode(v).decode("utf-8") for k, v in doc["data"]["source"]["files"].items()}
    else:
        sys.exit(f"{path} isn't a page export: export a page in Grafana (Pages, then Export) and pass that file.")
    missing = [name for name in TEMPLATE_FILES if name not in files]
    if missing or not any(k.startswith(TEMPLATE_DIRS) for k in files):
        sys.exit(f"{path} has no complete page project (missing {', '.join(missing) or 'packages/'}).")
    return files


def scene_modules():
    """src/scenes.ts and one module per picture, each a data: URL (the frame allows those)."""
    files, imports, entries = {}, [], []
    for i, name in enumerate(IMAGES):
        with open(scene_path(name), "rb") as f:
            url = "data:image/webp;base64," + base64.b64encode(f.read()).decode("ascii")
        files[f"src/scenes/{name}.ts"] = f"// {GENERATED}\nexport default '{url}';\n"
        imports.append(f"import scene{i} from './scenes/{name}';\n")
        entries.append(f"  '{name}': scene{i},\n")
    files["src/scenes.ts"] = (f"// {GENERATED}\n" + "".join(imports)
                              + "\nexport const SCENES: Record<string, string> = {\n" + "".join(entries) + "};\n")
    return files


def page_files(template, cards=None):
    files = {k: v for k, v in template.items() if k in TEMPLATE_FILES or k.startswith(TEMPLATE_DIRS)}

    def copy(name):
        with open(os.path.join(HERE, name), encoding="utf-8") as f:
            return f.read()

    files.update({
        "pages.bindings.json": "{}\n",
        "src/main.tsx": MAIN_TSX,
        "src/host.ts": HOST_TS,
        "src/markup.ts": f"// {GENERATED}\nexport const MARKUP = {json.dumps(page_markup(), ensure_ascii=False)};\n",
        "src/page.css": PAGE_CSS,
        "src/style.css": copy("style.css"),
        "src/game.js": copy("game.js"),
        "src/game.d.ts": SCRIPT_DTS,
        "src/SPOILERS-content.js": render(cards),
        "src/SPOILERS-content.d.ts": SCRIPT_DTS,
    })
    files.update(scene_modules())
    return dict(sorted(files.items()))


def render_page(template, cards=None):
    """A page export file (PageExport version 2) for Grafana's Import page."""
    doc = {
        "__inputs": [],
        "kind": "PageExport",
        "version": 2,
        "title": PAGE_TITLE,
        "source": {"version": 1, "files": page_files(template, cards), "binaryFiles": {}},
    }
    return json.dumps(doc, ensure_ascii=False, indent=2) + "\n"


def _read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None


def main(argv=None):
    p = argparse.ArgumentParser(description="Bundle game/SPOILERS-content/ for the web game.")
    p.add_argument("--check", action="store_true", help="exit 1 if the output is out of date")
    p.add_argument("--page", action="store_true", help="build the Grafana Page export file instead")
    p.add_argument("--art", nargs="*", metavar=("FILE", "NAME"),
                   help="cut comic-prototype/assets/scenes.png into web/assets/scene-*.webp, "
                        "or with FILE NAME, make web/assets/NAME.webp from FILE")
    p.add_argument("--template", metavar="FILE",
                   help="with --page: an exported page whose project to build on (default: the last build's)")
    args = p.parse_args(argv)
    if args.template and not args.page:
        p.error("--template needs --page")
    if args.art is not None:
        if args.page or args.check or args.template:
            p.error("--art takes no other options")
        if len(args.art) not in (0, 2):
            p.error("--art takes no arguments, or FILE NAME")
        if args.art:
            make_image(*args.art)
        else:
            cut_scenes()
        return
    if args.page:
        out, rebuild = PAGE_PATH, "python3 web/build.py --page"
        template = args.template or PAGE_PATH
        if not os.path.exists(template):
            sys.exit(f"{os.path.relpath(PAGE_PATH)} doesn't exist yet: run {rebuild} --template FILE, "
                     "where FILE is an exported Grafana page (see web/README.md).")
        text = render_page(read_template(template))
    else:
        out, rebuild = OUT_PATH, "python3 web/build.py"
        text = render()
    if args.check:
        if _read(out) != text:
            sys.exit(f"{os.path.relpath(out)} is out of date: run {rebuild}")
        print(f"{os.path.relpath(out)} is up to date.")
        return
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Wrote {os.path.relpath(out)}.")


if __name__ == "__main__":
    main()
