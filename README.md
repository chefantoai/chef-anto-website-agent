# Chef Anto Website Agent 🏡

**Builds cozy, premium static websites for the Chef Anto brands (chefanto.com, Baba, Dream House, portfolio) in plain HTML and CSS, ready to drag into Netlify.**
Part of the [Chef Anto AI Agency](https://github.com/chefanto80-design/chef-anto-agent). Built by Chef Anto (Antoanela Alexander), Miami. Based on Richmond Taylor's `luxury-static-site` skill (Creativity Hub Miami, Session 5).

## What it does
- Plain HTML + CSS, no build step. Deploy by dragging the folder into Netlify.
- Brand palette (cream, olive, paprika, ink), serif headings, one CTA per section
- Accessibility: skip link, labeled illustrations, visible focus, WCAG AA contrast
- Responsive at 375, 768 and 1440 px
- No invented testimonials: quote slots are clearly marked PLACEHOLDER

## Files
| Path | What it is |
|---|---|
| [`skill/SKILL.md`](skill/SKILL.md) | The agent's full instructions (Claude skill) |
| [`demo/baba-site/index.html`](demo/baba-site/index.html) | Real demo output: Baba by Chef Anto landing page |
| [`demo/baba-site/styles.css`](demo/baba-site/styles.css) | Its stylesheet |
| [`tests/test_site.py`](tests/test_site.py) | 33 automated checks in a real browser (Playwright) |

## How to use
**Claude app:** zip the `skill` folder renamed to `chef-anto-website`, upload it in Claude's Settings → Skills, then ask:
> Use chef-anto-website. Build a landing page for …

**Claude Code:** `mkdir -p ~/.claude/skills/chef-anto-website && cp skill/SKILL.md ~/.claude/skills/chef-anto-website/`

**Preview the demo:** download `demo/baba-site` and open `index.html`, or drag the folder into Netlify.

## Real demo
Run on **2026-10-01 (UTC)** in Claude (Cowork), model `claude-opus-5-5`, by invoking the `chef-anto-website` skill.

**Input (exact):**
```
Demo order: Build a one-page landing page for Baba by Chef Anto (Balkan pop-up, Tuesdays)
using the confirmed brand defaults (palette, fonts, CTAs). Real reservation link and
testimonials are not available yet; mark them as placeholders. Files: index.html and styles.css.
```

**Output:** [`demo/baba-site/`](demo/baba-site/): hero, "Why Baba?" story, sample Tuesday menu, guest-quote placeholder + real credentials, reservation block (email link, marked PLACEHOLDER until a booking link exists), free-guide signup, footer with sign-off.

## Test results (only tests actually run)
| # | Test | Result |
|---|---|---|
| 1 | Live run of the skill on the demo input | ✅ index.html + styles.css produced |
| 2 | `python3 tests/test_site.py demo/baba-site`, first run | ❌ **32/33**: the "From the table" section had **no CTA**, breaking the one-CTA-per-section rule |
| 3 | Fixed (added "Reserve your seat" to that section) and re-ran | ✅ **33/33 passed** |

What the 33 checks cover, rendered in headless Chromium:
- No horizontal scroll and no JS errors at **375, 768 and 1440 px**
- One `<h1>`, `lang="en"`, skip link to `#main`, every illustration labeled, no broken anchors, buttons ≥ 44 px tall
- Exactly one CTA in each of the 6 sections
- Contrast (WCAG AA ≥ 4.5:1): ink on cream 14.99, white on paprika 5.35, cream on olive 8.24, olive on cream 8.24, note text 6.81, paprika caption 5.01
- No forbidden words or styles, sign-off in the footer, one Google Font import, placeholders marked

The test also saves full-page screenshots to `demo/screenshots/` when you run it.

**Not tested yet:** Lighthouse score was not run. The Google Font could not load in the build sandbox, so screenshots there used the Georgia fallback. Not deployed to Netlify.

## Run the tests
```bash
pip install playwright && playwright install chromium
python3 tests/test_site.py demo/baba-site
```

---
Chef Anto 🌿🤓❤️
