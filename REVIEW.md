# REVIEW.md — all questions resolved

**Status: 0 placeholders remaining.** All items have been clarified and updated directly in the YAML configurations across base and variant files. Run `python scripts/check.py` to verify.

---

## Resolved since the first pass

Supplying your LinkedIn profile closed several of these outright:

- **The 2012–2016 gap is gone.** The employer is **ATOS IT Solutions & Services
  GmbH**, the title **IT Engineer**, running **Jun 2012 – Apr 2016**. "PSoD" is
  *Project Service on Demand* — an in-house subscription service with an
  automated billing agent and custom reporting dashboards. That detail was
  buried in prose in your old CV and is one of the better bridges you have into
  a SaaS Solutions Engineering career: subscription delivery, metering and
  commercial packaging, before you ever worked for Okta. It is now a headline
  bullet. Only the city is still open.
- **The Okta progression is now accurate.** LinkedIn shows Senior SE
  (Mar 2020 – Mar 2023) and Team Lead (Feb 2023 – Feb 2024) as *completed*
  roles, not concurrent ones. Your old CV listed the Senior SE role as
  "March 2020 – Present", which is what made it read as a parallel job. It is
  now two sequential entries: Senior SE / Team Lead, then Sr. Manager.
- **Team size is confirmed at 12 direct reports**, covering Commercial,
  Enterprise and Strategic accounts, and made up of dedicated Okta and Auth0
  SEs. Previously this was buried in prose.
- **The talent-development metric is answered.** Promotions at every level —
  Associate→SE, SE→Senior, Senior→Principal — plus SDRs coached into technical
  SE roles. That was one of my placeholders and it is stronger than anything I
  would have suggested.
- **Team Lead scope expanded.** The role covered Emerging & Corporate in CEE
  *and* Team Lead Solutions Engineering Switzerland. Both are now stated.
- **Community presence added.** PreSales Collective (since 2020) and Presales &
  Pretzels SE Networking Munich (since 2022) now appear under Speaking,
  Writing & Community.

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

## 2. The Atos entry — one field left

Everything here is resolved except the **city**. LinkedIn lists the role under
Atos with no location, but AvePoint in Munich followed immediately in Apr 2016,
so it is very likely Munich. It is marked `[ADD: city]` rather than guessed.

Also optional but worth adding: the scale of the SharePoint / Project Server
estate, and one concrete problem you solved. The current third bullet asks for
this — it is the difference between a one-line entry and a credible one.

File: `content/*/base.yaml`, entry `__merge_key__: psod-sharepoint`.

## 3. Metrics — the numbers still missing

The promotion-track metric is now answered (see above). These remain:

| Metric | Why it matters |
|---|---|
| Regional ARR you support or own | The size of the business you are accountable for. If you only support and do not own it, say so — that is a legitimate scope. |
| Win rate, or deal conversion % | Shows whether the team is effective, not just large. |
| Number of SEs hired via the SE Academy | The CV says you drove recruitment for it; a count makes it a result. |
| Average time-to-fill | Optional, but strong if it is good. |

**Use whichever numbers you can defend under questioning.** A metric you cannot
explain in the interview is worse than an absent one. If you genuinely do not
know a figure, say so in the interview rather than guessing on paper.

Files: `content/*/base.yaml` → `Leadership Snapshot` / `Kennzahlen`, and the
matching block in each variant.

## 4. The AvePoint 2018 award conflict — still needs resolving

Your CV contains two claims that cannot both be true:

> "#1 Sales Engineer worldwide in 2018 (over 200% achievement)"
> "#2 Sales Engineer worldwide in 2018 (over 300% achievement)"

Same year, two different ranks, and the lower rank has the higher attainment.
One of these is a typo. As written it invites a question you will not enjoy.

Your LinkedIn profile does not list the AvePoint awards at all, so it cannot
settle this either. Needed: the correct rank for 2018, and the attainment
percentage.

Note the timings, since these attach to different periods: Technical Solutions
Professional Apr 2016 – Jan 2019, Senior Solution Engineer Jan 2019 – Feb 2020.

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

**Three overlapping Okta roles became two sequential ones.** Your CV listed
`Sr. Manager` (Feb 2024 –), `Team Lead` (Feb 2023 – Feb 2024) and `Senior
Solutions Engineer` (March 2020 – **Present**) as three entries. LinkedIn shows
the Senior SE role actually ended in Mar 2023, so the "Present" was the error —
and that single wrong end date is what made three sequential promotions look
like three concurrent jobs. It now reads as the promotion track it was: Senior SE
→ Team Lead → Sr. Manager → acting Director of PreSales.

**"Grew the team 5 to 12"** comes from your old CV, which described leading "a
team of 5 SEs" as Team Lead, against the 12 direct reports LinkedIn confirms
now. Worth a sanity check that the 5 is the figure you want — it is the baseline
of your growth claim.

**The awards attach to the Senior SE period, not the manager role.** President's
Club FY22/FY23, EMEA PreSales Rockstar FY23 and Technical Hot Shot FY22 were all
earned before you were Sr. Manager. They sit in a separate section rather than
attached to the current role, which is the honest presentation. Be aware of it
if a reference checks dates.

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