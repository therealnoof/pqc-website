# The Post-Quantum Cryptography Field Guide — website

A fast, modern reading site for *The Post-Quantum Cryptography Field Guide*,
built with [Astro](https://astro.build) and deployed as **static assets on
Cloudflare Workers**.

- **Landing page** — dark-technical hero, abstract, chapter grid, authors.
- **Reader** — one page per chapter with a grouped sidebar TOC, prev/next paging,
  copy-link heading anchors, and a light/dark toggle (dark is the default).
- **Full-text search** — client-side, powered by [Pagefind](https://pagefind.app)
  (built at deploy time; press `/` or click **Search**).
- **PDF download** — `public/pqc-field-guide.pdf`, generated from the same
  content as the site (`npm run pdf`) so it always matches the latest manuscript.
- Zero client JS framework; ships as static HTML/CSS for instant edge loads.

## Quick start

```bash
npm install          # install deps
npm run convert      # (re)generate content from the .docx  — see below
npm run dev          # local dev at http://localhost:4321  (search is build-only)
npm run build        # astro build + pagefind index -> dist/
npm run preview      # serve the production build locally
npm run pdf          # regenerate the downloadable PDF from current content
```

### Regenerating the PDF

`npm run pdf` renders the hidden `/book-print` route (the whole book on one
print-styled page) to `public/pqc-field-guide.pdf` using headless Chrome, so the
download always reflects the latest content. After editing the source document:

```bash
npm run convert && npm run pdf && npm run build
```

Override the browser with `CHROME_BIN=/path/to/chrome npm run pdf` if needed.

## Content pipeline

Chapters are **generated from the source Word document**, not hand-written.

- Source: `~/Downloads/pqc-field-guide-complete.docx` (override:
  `python3 scripts/convert.py /path/to/file.docx`).
- `scripts/convert.py` parses the OOXML directly with the Python **standard
  library** (no `python-docx`/`lxml` dependency) and writes:
  - `src/content/chapters/NN-slug.md` — one Markdown file per section, with
    frontmatter (title, section, chapter #, reading time, excerpt). Chapter
    endnotes are folded into a **Notes** section on each chapter page.
  - `src/data/book-meta.json` — title, authors, abstract, and the table of
    contents consumed by the landing/reader UI.
  - `public/book-media/*` — images extracted from the document.

To refresh after editing the document: `npm run convert && npm run build`.

> **Note:** single-column "sidebar/callout" tables in the source are rendered as
> blockquote callouts; bracketed `[… will be added …]` placeholders and stray
> "Chapter N" labels are stripped automatically.

## Deploy to Cloudflare

The site is configured as a **Workers static-assets** project (`wrangler.toml`).

1. Authenticate once (run this yourself in the terminal):

   ```bash
   npx wrangler login
   ```

2. Build and deploy:

   ```bash
   npm run deploy        # = npm run build && wrangler deploy
   ```

   Wrangler uploads `dist/` and publishes to
   `https://pqc-field-guide.<your-subdomain>.workers.dev`.

3. (Optional) Set your final URL for canonical links + sitemap:

   ```bash
   SITE_URL="https://your-domain.example" npm run build
   ```

   …or edit the `SITE` default in `astro.config.mjs`. To use a custom domain,
   add a route in the Cloudflare dashboard or a `[[routes]]` block in
   `wrangler.toml`.

Preview the exact Workers runtime locally with `npm run cf:preview`.

## Project layout

```
scripts/convert.py            docx -> markdown + metadata + images
src/content/chapters/*.md     generated chapter content
src/data/book-meta.json       generated table of contents / metadata
src/content.config.ts         Astro content-collection schema
src/layouts/BaseLayout.astro  HTML shell, SEO, theme bootstrap
src/components/                Header, Footer, Sidebar, Search, ThemeToggle
src/pages/index.astro         landing page
src/pages/read/[slug].astro   chapter reader
src/pages/read/index.astro    table of contents
src/styles/                    global.css (design system) + reader.css (prose)
wrangler.toml                  Cloudflare Workers static-assets config
```
