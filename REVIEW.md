# REVIEW.md — what still needs your input

Every `[ADD: ...]` in the CV is a question only you can answer. Nothing has been
invented: every figure in the CV traces back to your previous CV, and everything
that does not trace back is marked here.

Run `python scripts/check.py` to see the current placeholder count per file.

**Priority order matters.** Items 1–3 are the ones a hiring manager will notice
first. Items 4+ are polish.

---

## 1. The headline — what title to claim

Appears in the header of all six variants. This is the single highest-leverage
line in the document.

You are `Sr. Manager Solutions Engineering` and acting `Director of PreSales`.
A CV that claims a title you do not hold gets caught in the first reference
check, and the cost is far higher than the benefit. A CV that under-claims a
director-sized remit gets read as a manager.

The variants currently use **"Director of Solutions Engineering — ..."** because
that is the target role, not necessarily your current one. Decide which you want:

- Applying into a role → the target title is fine and normal.
- Referenced by a current employer or for a promotion conversation → use the real
  one: "Sr. Manager Solutions Engineering, Acting Director of PreSales (CEE)".

File: `content/en/base.yaml` and `content/de/base.yaml`, key `headline`.

## 2. The 2012–2016 gap — a missing job

Your CV had **no entry** for the SharePoint / Project Server role you describe in
the summary prose, and nothing at all between 2012 and 2016. A four-year hole in
a ten-year career gets asked about in the first interview.

An entry now exists but is a placeholder, with dates deliberately left blank.
Inventing a date range would have been worse than an empty field.

Needed:

- The full legal name of the employer. Your CV calls it **"PSoD"** — I have not
  guessed what that expands to. Give the name as it would appear on a
  reference or a LinkedIn profile.
- Exact job title.
- City.
- Start and end dates (month/year is enough).
- Scale: roughly how many users, SharePoint sites, instances, or projects.
- One concrete problem you solved there — a migration, a rollout, an uptime or
  performance improvement. This is the bullet that makes the entry worth three
  lines instead of one.

File: `content/*/base.yaml`, entry `__merge_key__: psod-sharepoint`.

## 3. Metrics — the numbers you do not currently have

Your previous CV contained these figures in total: `5`, `7`, `12`, `1.5M ARR`,
`>200%`, `>300%`, `team of 5`. For a Director-level application that is not
enough. The `Leadership Snapshot` block was built to hold them — it is the first
block a hiring manager reads.

Needed, ideally for the last 2–3 fiscal years:

| Metric | Why it matters |
|---|---|
| Regional ARR you support or own | The size of the business you are accountable for. If you only support and do not own it, say so — that is a legitimate scope. |
| Win rate, or deal conversion % | Shows whether the team is effective, not just large. |
| Number of SEs hired via your PreSales Academy | Turns "I ran an academy" into a recruiting result. |
| Markets covered by those hires | Proves multi-country execution, which is the whole point of a CEE remit. |
| Average time-to-fill | Optional, but strong if it is good. |
| SEs promoted into Lead or Architect roles | The clearest single proof that you develop people rather than just staffing them. |
| Forecast accuracy | Only if you actually own forecasting. Do not claim it otherwise. |

**Use whichever numbers you can defend under questioning.** A metric you cannot
explain in the interview is worse than an absent one. If you genuinely do not
know a figure, say so in the interview rather than guessing on paper.

Files: `content/*/base.yaml` → `Leadership Snapshot` / `Kennzahlen`, and the
matching block in each variant.

## 4. The AvePoint 2018 award conflict — needs resolving

Your CV contains two claims that cannot both be true:

> "#1 Sales Engineer worldwide in 2018 (over 200% achievement)"
> "#2 Sales Engineer worldwide in 2018 (over 300% achievement)"

Same year, two different ranks, and the lower rank has the higher attainment.
One of these is a typo. As written it invites a question you will not enjoy.

Needed: the correct rank for 2018, and the attainment percentage. The current
CV claims `#1 SE worldwide 2018` in the experience section and `#2, 2019, >200%`
in the variants.

## 5. Xing profile URL

Your CV had LinkedIn filled in and **Xing empty**. In the German market Xing is
not optional — most recruiters and every agency screen start there. RenderCV has
no built-in Xing network, so it is wired in as a custom connection with an icon.

Needed: the URL of your Xing profile.

File: `content/*/base.yaml` → `custom_connections`.

## 6. Phone number

Currently **omitted**, not empty-stringed. RenderCV validates it as a real
international phone number, so a `[ADD: ...]` placeholder would have broken the
build rather than rendering.

Needed: your number in `+49 ...` form. German recruiting processes generally
treat it as mandatory.

File: `content/*/base.yaml`, uncomment the `phone:` line.

## 7. Certifications

The section exists but is empty apart from a placeholder. For an identity and
security remit this is a genuine credibility signal, not padding.

Needed: any credentials you hold — Okta Certified Consultant, Okta Identity
Governance, AWS Security Specialty, a relevant Microsoft security certification,
or equivalent. Include the year.

If you hold none, **delete the section** rather than leaving it empty. See the
`__drop__` mechanism in the build script.

## 8. Speaking engagements

Your CV had a section titled "Publications" that contained one sentence saying
you sometimes blog. That undersells you badly. For a Solutions Engineering
leader, having stood up and presented in front of a room is the stronger signal,
and it is currently entirely absent.

Needed: any webinar, conference talk, user group session or customer-facing
session — with title, event and year. Internal Okta sessions count if you
designed them. If you have done internal enablement or mentoring sessions that
are worth naming, those count too.

The section is named "Speaking, Writing & Community" to invite this.

## 9. Education details

- **BBA** — confirm the current official name. Fachhochschule Südwestfalen is now
  Hochschule Südwestfalen; using the current name avoids a "does this person
  check details" moment. Also needs the campus city.
- **Siemens / ATOS apprenticeship** — confirm whether you completed the IHK
  journeyman examination, and the year. The degree field is currently a
  placeholder.
- Both entries need a city.

## 10. French language level

Your CV says **"Beginner"**. In a German or French-language application this
reads as a liability rather than a qualification.

Needed: the real level. If it is genuinely beginner, consider leaving French off
entirely — the EN and DE variants both have it as a removable row inside
`Core Competencies` / `Kompetenzen`.

---

## Things I changed that you should sanity-check

These were judgement calls, not errors. Push back if you disagree.

**Three overlapping Okta roles became one.** Your CV listed `Sr. Manager`
(Feb 2024 –), `Team Lead` (Feb 2023 – Feb 2024) and `Senior Solutions Engineer`
(March 2020 –) as three separate entries. They overlap, so it reads as three
concurrent jobs at one employer and triple-counts about four years. It is now one
entry with the hands-on SE mandate stated in the summary rather than shown as a
parallel job.

**The 2012–2016 role now exists.** Even with placeholders, an empty field is
visible and fixable; a missing role is invisible and indefensible.

**The Projects section was removed.** 3D printing, Ender3/Klipper firmware, a
Proxmox homelab and running evilginx. At Director level this reads as a senior
individual contributor hobbying, and it occupied space that business impact
should have held. The underlying signal — genuine hands-on curiosity — survives
under `Platforms` and via the blog link.

**The percentage-bar skills widget was removed.** It offered things like
"PreSales 98%", which carries no information. Replaced with `Core Competencies`:
areas of scope, so a hiring manager knows what to probe you on.

**Awards were compressed to two lines.** You had six award bullets. At Director
level outcomes outweigh awards, and six awards was a disproportionate share of
the document.

**The career profile went from seven paragraphs to one.** It ended with *"People
who work with me would probably say I'm open-minded, positive..."* — that is
LinkedIn About-section copy. The summary is now about 80 words and leads with
scope, scale and domain.

**A `Leadership Snapshot` block was added at the top.** This is new structure,
not a rewrite of something existing.

**Dates were normalised** to `MMM YYYY` across all roles. Your CV mixed
`Feb 2024`, `March 2020` and `2019`.

**Typos fixed:** `knopwledge`, `successfull`, `Aprenticeship`, `Achievments`
(×2, and this one was rendered on the page), `virtualizied`, and "in a acting
Director" → "an".

---

## Housekeeping on the old repository

Independent of the content, these still need doing on `online-cv`:

1. **`CNAME` contains `online-cv.webjeda.com`** — the theme author's demo domain,
   left over from the fork. Your custom-domain configuration is pointed at
   someone else's site. Delete the file, or point it at a domain you own.
2. **`_config.yml` is entirely upstream leftovers:** `title: My Resume`,
   `url: 'http://webjeda.com'`, and `analytics: UA-83979019-1` — a dead
   Universal Analytics property belonging to the theme author. Universal
   Analytics stopped processing data in July 2023; remove it rather than
   replacing it, or use a privacy-respecting alternative.
3. **The `experiences:` section has no `title:` key**, so the Experience heading
   renders blank.
4. **The old "PDF" had no text layer at all.** It was generated in the browser by
   rasterising the DOM into a canvas. Applicant tracking systems cannot read it.
   That is the single biggest reason to use this new repository instead.