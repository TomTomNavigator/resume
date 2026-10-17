# Thomas Heinz — CV

Director-level CV for Solutions Engineering, Identity & Security, Central &
Eastern Europe. Built as code: one YAML source of truth, two canonical versions (English & German),
and real PDF/DOCX output that applicant tracking systems can actually read.

This replaces the previous [Jekyll `online-cv` setup](../), which had three
problems worth naming:

1. **The exported PDF had no text layer.** It was generated in the browser by
   rasterising the DOM into a canvas, so it was an image of a CV. Greenhouse,
   Lever and Workday extract nothing from it. Every PDF here is vector text —
   verified on every build, and the build fails if that regresses.
2. **No structure.** Six years at Okta appeared as three overlapping job
   entries, one of them running in parallel to the others.
3. **No variants.** Every application got the same document regardless of role.

---

## Quick start

```bash
make setup     # create a virtualenv and install dependencies (needs Python 3.12+)
make build     # render every variant to PDF, DOCX, HTML
make site      # build the GitHub Pages landing page
```

Everything lands in `dist/`. Nothing in `dist/` is committed — it is regenerated
on every CI run.

To build one variant while editing:

```bash
make one VARIANT=resume.en
make check          # fast structural check, no rendering
```

## Layout

```
content/
  en/  base.yaml        the source of truth for English
  de/  base.yaml        independent German version (not a machine translation)
  */design.yaml        theme, colours, spacing
  */settings.yaml      locale, PDF metadata
variants/
  resume.en.yaml        canonical English version
  lebenslauf.de.yaml    canonical German version
scripts/
  build.py              merge -> compose -> render -> DOCX -> verify
  site.py               landing page generator
  check.py              pre-commit structural check
assets/thomas.png       photo used in the CV header
dist/                   generated output (gitignored)
```

### How variants work

A variant is an **overlay**, not a copy. It deep-merges onto
`content/<lang>/base.yaml`, so correcting your Okta entry once updates all six
documents.

```yaml
name: Identity & Security (EN)
lang: en
cv:
  headline: Director of Solutions Engineering — Identity & Security, CEE
  sections:
    Professional Experience:
      - __merge_key__: okta-leadership       # patches one entry
        highlights:                          # replaces that entry's bullets
          - "..."
```

`__merge_key__` lets an overlay change one experience entry without restating
the whole list. `__drop__: true` removes an entry entirely. Both are stripped
before RenderCV validates the file.

Merge rules, and the one sharp edge:

| Case | Behaviour |
|---|---|
| dict + dict | recursive merge, overlay wins |
| list + list | **replaced**, unless every element on both sides has `__merge_key__` |
| keyed list | merged by key, new keys appended |
| anything else | overlay wins |

`highlights` is a plain list of strings, so it is **replaced**, not appended.
That is usually what you want when re-ordering bullets.

## Before you send anything

Read **[REVIEW.md](REVIEW.md)**. Every `[ADD: ...]` marker in the CV is a
question only you can answer — a real metric, a date, a name. Nothing in this
repository has been invented.

```bash
python scripts/check.py     # shows placeholder counts per file
```

## Deployment

`.github/workflows/build.yml` runs on pushes to `main`, on `v*` tags, on pull
requests, and on manual dispatch. It:

- builds and validates all variants
- **fails if any PDF has no extractable text layer**
- publishes the landing page to GitHub Pages from `dist/site`
- attaches PDFs and DOCX to a GitHub release when a `v*` tag is pushed

```bash
git tag -a v1.0.0 -m "..." && git push origin v1.0.0   # cut a release
```

### Enabling Pages (one manual step)

The landing page needs GitHub Pages turned on for the repository. This cannot be
done from the API — `POST /repos/:owner/:repo/pages` returns success but leaves
the site 404-ing, and `deploy-pages` then reports success without running, which
is a confusing failure to debug.

1. Open <https://github.com/TomTomNavigator/resume/settings/pages>
2. Under **Build and deployment → Source**, choose **GitHub Actions**
3. Save

After that, every push to `main` publishes automatically. To serve from your own
domain instead, point a CNAME at it in the repository settings, or change the
defaults in `scripts/site.py`.

Releases work independently of Pages, so the PDFs are downloadable whether or
not the landing page is enabled.

## Why RenderCV

- **Real PDFs.** Typeset with Typst, selectable text, no rasterisation.
- **Self-contained.** Typst ships as a Python package, so there is no LaTeX
  system install. `pip install` is the whole setup.
- **Schema validation.** A wrong field type fails at build time with a useful
  message, not silently in the output.
- **Git-native.** Diffable, reviewable, branchable — which is what makes six
  consistent variants maintainable.

Alternatives worth knowing about: [YAMLResume](https://github.com/yamlresume/yamlresume)
(LaTeX-based, exports DOCX too) and
[Reactive Resume](https://github.com/AmruthPillai/Reactive-Resume) (web editor,
self-hostable, weaker version control).

## Adding a variant

1. Copy an existing file in `variants/` and change `name` and `lang`.
2. Adjust `headline`, `Leadership Snapshot`, `Core Competencies`, and the
   `highlights` of the roles you want to emphasise.
3. `make check && make one VARIANT=<your-file-without-.yaml>`
4. Open the PDF and read it as a hiring manager would.