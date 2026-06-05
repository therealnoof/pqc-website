#!/usr/bin/env python3
"""
Convert the PQC Field Guide .docx into per-chapter Markdown + metadata for Astro.

Why stdlib only: python-docx/lxml is broken in this environment
(`ImportError: cannot import name getargspec`), so we parse the OOXML directly
with zipfile + xml.etree. No third-party dependencies — also makes the repo
reproducible anywhere with a stock Python 3.

Inputs : a .docx (default: ~/Downloads/pqc-field-guide-complete.docx)
Outputs:
  src/content/chapters/<NN>-<slug>.md   one page per H1 section (notes folded in)
  src/data/book-meta.json               title/authors/sections/toc
  public/book-media/*                   extracted images
"""
from __future__ import annotations

import json
import os
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SRC = Path.home() / "Downloads" / "pqc-field-guide-complete.docx"
CHAP_DIR = ROOT / "src" / "content" / "chapters"
META_OUT = ROOT / "src" / "data" / "book-meta.json"
MEDIA_DIR = ROOT / "public" / "book-media"

# H1 titles that form the front matter (everything else before the appendices
# is a numbered chapter).
FRONT_TITLES = {"foreword", "how to read this book", "about the authors"}
# First appendix H1 — everything from here on is back matter / reference.
APPENDIX_START = "quantum risk scoring methodology"

PLACEHOLDER_RE = re.compile(
    r"\[(?:[^\]]*?(?:will be added|placeholder|to be (?:added|written|completed)|tbd|todo)[^\]]*?)\]",
    re.I,
)


# --------------------------------------------------------------------------- #
# OOXML helpers
# --------------------------------------------------------------------------- #
def load(src: Path):
    z = zipfile.ZipFile(src)
    styles = ET.fromstring(z.read("word/styles.xml"))
    id2name = {}
    for s in styles.iter(W + "style"):
        sid = s.get(W + "styleId")
        nm = s.find(W + "name")
        if sid and nm is not None:
            id2name[sid] = (nm.get(W + "val") or "").lower()
    # relationships (hyperlinks + image targets)
    rels = {}
    try:
        rx = ET.fromstring(z.read("word/_rels/document.xml.rels"))
        for rel in rx:
            rels[rel.get("Id")] = rel.get("Target")
    except KeyError:
        pass
    doc = ET.fromstring(z.read("word/document.xml"))
    return z, doc, id2name, rels


def style_of(p, id2name) -> str:
    pPr = p.find(W + "pPr")
    if pPr is None:
        return "normal"
    ps = pPr.find(W + "pStyle")
    if ps is None:
        return "normal"
    return id2name.get(ps.get(W + "val"), (ps.get(W + "val") or "").lower())


def run_is_mono(r) -> bool:
    rPr = r.find(W + "rPr")
    if rPr is None:
        return False
    rf = rPr.find(W + "rFonts")
    if rf is None:
        return False
    name = (rf.get(W + "ascii") or "") + (rf.get(W + "hAnsi") or "")
    return any(k in name for k in ("Mono", "Consol", "Courier"))


def run_flags(r):
    rPr = r.find(W + "rPr")
    b = i = False
    if rPr is not None:
        be = rPr.find(W + "b")
        b = be is not None and be.get(W + "val") not in ("0", "false")
        ie = rPr.find(W + "i")
        i = ie is not None and ie.get(W + "val") not in ("0", "false")
    return b, i


def run_text(r) -> str:
    out = []
    for el in r.iter():
        if el.tag == W + "t":
            out.append(el.text or "")
        elif el.tag == W + "tab":
            out.append(" ")
        elif el.tag in (W + "br", W + "cr"):
            out.append("\n")
    return "".join(out)


def fmt_run(r) -> str:
    txt = run_text(r)
    if not txt:
        return ""
    stripped = txt.strip()
    if not stripped:
        return txt  # whitespace only — keep spacing, don't decorate
    lead = txt[: len(txt) - len(txt.lstrip())]
    trail = txt[len(txt.rstrip()):]
    # superscript / subscript (e.g. footnote reference markers)
    rPr = r.find(W + "rPr")
    if rPr is not None:
        va = rPr.find(W + "vertAlign")
        if va is not None:
            val = va.get(W + "val")
            if val == "superscript":
                return f"{lead}<sup>{stripped}</sup>{trail}"
            if val == "subscript":
                return f"{lead}<sub>{stripped}</sub>{trail}"
    if run_is_mono(r):
        return f"`{txt}`"
    b, i = run_flags(r)
    core = stripped
    if b and i:
        core = f"***{core}***"
    elif b:
        core = f"**{core}**"
    elif i:
        core = f"*{core}*"
    return lead + core + trail


def image_for(run_or_el, z, rels, media_index) -> str | None:
    """Return a markdown image if the element embeds a picture, else None."""
    blip = run_or_el.find(".//" + A + "blip")
    if blip is None:
        return None
    rid = blip.get(R + "embed")
    target = rels.get(rid)
    if not target:
        return None
    src_name = "word/" + target.replace("../", "")
    try:
        data = z.read(src_name)
    except KeyError:
        return None
    ext = os.path.splitext(target)[1] or ".png"
    media_index[0] += 1
    out_name = f"img-{media_index[0]:02d}{ext}"
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    (MEDIA_DIR / out_name).write_bytes(data)
    return f"![figure](/book-media/{out_name})"


def para_inline(p, z, rels, media_index) -> str:
    """Render a paragraph's children (runs + hyperlinks + images) in order."""
    parts = []
    for child in p:
        if child.tag == W + "r":
            img = image_for(child, z, rels, media_index)
            if img:
                parts.append("\n\n" + img + "\n\n")
            else:
                parts.append(fmt_run(child))
        elif child.tag == W + "hyperlink":
            inner = "".join(fmt_run(r) for r in child.findall(W + "r"))
            rid = child.get(R + "id")
            url = rels.get(rid)
            inner = inner.strip()
            if url and inner:
                parts.append(f"[{inner}]({url})")
            else:
                parts.append(inner)
    return "".join(parts).strip()


def all_runs_mono(p) -> bool:
    runs = p.findall(W + "r")
    runs = [r for r in runs if run_text(r).strip()]
    return bool(runs) and all(run_is_mono(r) for r in runs)


def cell_text(tc, z, rels, media_index) -> str:
    lines = []
    for p in tc.findall(W + "p"):
        t = para_inline(p, z, rels, media_index)
        if t:
            lines.append(t)
    return "<br>".join(lines).replace("|", "\\|")


def table_md(tbl, z, rels, media_index) -> str:
    rows = tbl.findall(W + "tr")
    if not rows:
        return ""
    out = []
    ncols = 0
    for ri, row in enumerate(rows):
        cells = [cell_text(tc, z, rels, media_index) for tc in row.findall(W + "tc")]
        ncols = max(ncols, len(cells))
        out.append(cells)
    # Single-column tables are callout/sidebar boxes in the source, not data
    # tables. Render them as blockquotes so they read as callouts.
    if ncols == 1:
        body = "<br>".join(c[0] for c in out if c and c[0].strip())
        lines = [seg.strip() for seg in body.split("<br>") if seg.strip()]
        return "\n".join("> " + ln for ln in lines)
    # normalise width
    for row in out:
        while len(row) < ncols:
            row.append("")
    md = ["| " + " | ".join(r) + " |" for r in out]
    md.insert(1, "| " + " | ".join(["---"] * ncols) + " |")
    return "\n".join(md)


# Standalone "Chapter 7" label paragraphs that sit on section boundaries.
CHAPTER_LABEL_RE = re.compile(r"^chapter\s+\d+$", re.I)

# Headings (and everything under them, up to the next sibling/higher heading)
# to drop entirely from the output.
DROP_HEADINGS = {"additional contributors"}

# Rename section titles (keyed by lowercased original). Single-author edition.
TITLE_REMAP = {"about the authors": "About the Author"}

# Profile links appended to the author page (not present in the source doc).
AUTHOR_LINKS = [
    ("LinkedIn", "https://www.linkedin.com/in/arnulfo-hernandez-cissp-ccsp-0990b6a0/"),
]


def drop_sections(blocks, drop_titles):
    """Remove any heading whose text is in drop_titles, plus all blocks beneath
    it until the next heading of the same or higher level."""
    out = []
    skip_level = None
    for kind, val in blocks:
        lvl = int(kind[1]) if kind in ("h1", "h2", "h3", "h4") else None
        if skip_level is not None:
            if lvl is not None and lvl <= skip_level:
                skip_level = None  # back out to a sibling/higher section
            else:
                continue
        if lvl is not None and val.strip().lower() in drop_titles:
            skip_level = lvl
            continue
        out.append((kind, val))
    return out


# --------------------------------------------------------------------------- #
# Block model
# --------------------------------------------------------------------------- #
def iter_blocks(body, id2name, z, rels, media_index):
    """Yield ('h1'|'h2'|'h3'|'p'|'li'|'code'|'table'|'img', text)."""
    for child in body:
        if child.tag == W + "tbl":
            t = table_md(child, z, rels, media_index)
            if t:
                yield ("table", t)
            continue
        if child.tag != W + "p":
            continue
        st = style_of(child, id2name)
        # picture-only paragraph
        if child.find(".//" + A + "blip") is not None and not run_text_all(child).strip():
            img = image_for(child, z, rels, media_index)
            if img:
                yield ("img", img.strip())
            continue
        text = para_inline(child, z, rels, media_index)
        if not text:
            continue
        if PLACEHOLDER_RE.search(text):
            continue  # drop bracketed "will be added" placeholders
        if CHAPTER_LABEL_RE.match(text.strip()):
            continue  # drop stray "Chapter N" label paragraphs
        if st == "heading 1":
            yield ("h1", text)
        elif st == "heading 2":
            yield ("h2", text)
        elif st == "heading 3":
            yield ("h3", text)
        elif st == "list paragraph":
            yield ("li", text)
        elif all_runs_mono(child):
            yield ("code", run_text_all(child))
        else:
            yield ("p", text)


def run_text_all(p) -> str:
    return "".join(run_text(r) for r in p.findall(W + "r"))


# --------------------------------------------------------------------------- #
# Assemble sections
# --------------------------------------------------------------------------- #
def plain_text(s: str) -> str:
    """Strip markdown/HTML to readable plain text for excerpts and metadata."""
    s = re.sub(r"<sup>.*?</sup>|<sub>.*?</sub>", "", s)  # drop footnote markers
    s = re.sub(r"<[^>]+>", "", s)                         # any other inline HTML
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)        # md links -> link text
    s = re.sub(r"[*`]", "", s)                            # emphasis / code ticks
    return re.sub(r"\s+", " ", s).strip()


def slugify(s: str) -> str:
    s = s.lower().replace("’", "").replace("'", "")
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    return s[:60] or "section"


def block_to_md(kind, val, shift=0) -> str:
    if kind in ("h1", "h2", "h3"):
        lvl = int(kind[1]) + shift
        lvl = max(2, min(lvl, 6))  # page title is the H1; body starts at H2
        return "#" * lvl + " " + val
    if kind == "code":
        return "```\n" + val + "\n```"
    if kind == "li":
        return "- " + val
    if kind in ("table", "img"):
        return val
    return val


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SRC
    if not src.exists():
        sys.exit(f"Source not found: {src}")

    z, doc, id2name, rels = load(src)
    body = doc.find(W + "body")
    media_index = [0]

    blocks = list(iter_blocks(body, id2name, z, rels, media_index))

    # Split into H1 sections (preamble before first H1 is ignored / title page).
    sections = []
    cur = None
    for kind, val in blocks:
        if kind == "h1":
            cur = {"title": val, "blocks": []}
            sections.append(cur)
        elif cur is not None:
            cur["blocks"].append((kind, val))

    # Classify + fold Notes sections into their target page.
    pages = []          # ordered list of real pages
    notes_by_key = {}   # "foreword" / "chapter-N" -> blocks
    chapter_no = 0
    in_appendix = False
    for sec in sections:
        title = sec["title"].strip()
        low = title.lower()
        if low.startswith("notes"):
            m = re.search(r"chapter\s+(\d+)", low)
            key = f"chapter-{m.group(1)}" if m else "foreword"
            notes_by_key[key] = sec["blocks"]
            continue
        if low == APPENDIX_START:
            in_appendix = True
        if low in FRONT_TITLES:
            section = "Front Matter"
            cno = None
            key = "foreword" if low == "foreword" else None
        elif in_appendix:
            section = "Appendices & Reference"
            cno = None
            key = None
        else:
            chapter_no += 1
            section = "Chapters"
            cno = chapter_no
            key = f"chapter-{chapter_no}"
        pages.append({"title": TITLE_REMAP.get(low, title), "section": section,
                      "chapter": cno, "key": key, "blocks": sec["blocks"]})

    # Attach notes
    for pg in pages:
        notes = notes_by_key.get(pg["key"]) if pg["key"] else None
        if notes:
            pg["blocks"].append(("h2", "Notes"))
            pg["blocks"].extend(("h3", v) if k == "h2" else (k, v) for k, v in notes)

    # Write chapter files + build meta
    CHAP_DIR.mkdir(parents=True, exist_ok=True)
    for old in CHAP_DIR.glob("*.md"):
        old.unlink()

    toc = []
    for order, pg in enumerate(pages, 1):
        pg["blocks"] = drop_sections(pg["blocks"], DROP_HEADINGS)
        if pg["title"].strip().lower().startswith("about the author") and AUTHOR_LINKS:
            links = "  ·  ".join(f"[{name} ↗]({url})" for name, url in AUTHOR_LINKS)
            pg["blocks"].append(("p", f"**Connect:** {links}"))
        display = (f"Chapter {pg['chapter']}: " if pg["chapter"] else "") + pg["title"]
        slug = f"{order:02d}-" + slugify(pg["title"])
        body_md = "\n\n".join(block_to_md(k, v) for k, v in pg["blocks"])
        words = len(re.findall(r"\w+", body_md))
        excerpt = ""
        for k, v in pg["blocks"]:
            if k == "p" and len(v) > 80:
                excerpt = plain_text(v)[:220].strip()
                break
        fm = {
            "title": pg["title"],
            "displayTitle": display,
            "section": pg["section"],
            "chapter": pg["chapter"],
            "order": order,
            "words": words,
            "readingMinutes": max(1, round(words / 220)),
            "excerpt": excerpt,
        }
        yaml = "---\n" + "".join(
            f"{k}: {json.dumps(v, ensure_ascii=False)}\n" for k, v in fm.items()
        ) + "---\n\n"
        (CHAP_DIR / f"{slug}.md").write_text(yaml + body_md + "\n", encoding="utf-8")
        toc.append({"slug": slug, **fm})

    # Front-matter metadata for the landing page.
    foreword = next((p for p in pages if p["title"].lower() == "foreword"), None)
    abstract = ""
    if foreword:
        for k, v in foreword["blocks"]:
            if k == "p" and len(v) > 120:
                abstract = plain_text(v)
                break

    meta = {
        "title": "The Post-Quantum Cryptography Field Guide",
        "subtitle": "A Practitioner's Handbook",
        "authors": ["Arnulfo “Noof” Hernandez"],
        "abstract": abstract,
        "totalWords": sum(t["words"] for t in toc),
        "readingMinutes": sum(t["readingMinutes"] for t in toc),
        "pageCount": len(toc),
        "chapterCount": sum(1 for t in toc if t["chapter"]),
        "images": media_index[0],
        "source": src.name,
        "chapters": toc,
    }
    META_OUT.parent.mkdir(parents=True, exist_ok=True)
    META_OUT.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"OK pages={len(pages)} chapters={meta['chapterCount']} "
          f"words={meta['totalWords']} images={media_index[0]}")
    print(f"OK -> {CHAP_DIR}")
    print(f"OK -> {META_OUT}")


if __name__ == "__main__":
    main()
