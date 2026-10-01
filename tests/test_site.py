"""Tests a static site built by the Website Agent (skill: chef-anto-website).

Usage: python3 tests/test_site.py demo/baba-site
Needs: pip install playwright && playwright install chromium
Renders the page at 375, 768 and 1440 px, saves screenshots, and checks
structure, accessibility basics, brand rules and WCAG AA contrast.
"""
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

site = pathlib.Path(sys.argv[1]).resolve()
html = (site / "index.html").read_text(encoding="utf-8")
css = (site / "styles.css").read_text(encoding="utf-8")
shots = site.parent / "screenshots"
shots.mkdir(exist_ok=True)
checks = []


def check(name, ok, detail=""):
    checks.append((name, ok, detail))


def lum(hex_):
    r, g, b = (int(hex_[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4  # noqa: E731
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


# Static checks
lower = re.sub(r"<[^>]+>", " ", html).lower()
for w in ["revolutionary", "game-changer", "hurry", " deal "]:
    check(f"No forbidden word '{w.strip()}'", w not in lower)
check("No forbidden styles (gradients, backdrop blur)", "gradient" not in css and "backdrop-filter" not in css)
check("Sign-off in footer", "Chef Anto 🌿🤓❤️" in html.split("<footer")[-1])
check("Testimonial slot clearly marked PLACEHOLDER", "PLACEHOLDER" in html)
check("Max one Google Font import", html.count("fonts.googleapis.com/css") <= 1)
check("No bracketed placeholders in copy", not re.search(r"\[[A-Z ]+\]", lower.upper()))

pairs = [("#1F1B16", "#F6EFE4", "ink on cream"), ("#FFFFFF", "#B5482A", "white on paprika button"),
         ("#F6EFE4", "#3F4A2E", "cream on olive"), ("#3F4A2E", "#F6EFE4", "olive on cream"),
         ("#5A5146", "#F6EFE4", "note text on cream"), ("#B5482A", "#FBF7F0", "paprika caption on card")]
for fg, bg, label in pairs:
    r = ratio(fg, bg)
    check(f"Contrast {label} ≥ 4.5:1 (WCAG AA)", r >= 4.5, f"{r:.2f}:1")

# Rendered checks
with sync_playwright() as p:
    browser = p.chromium.launch()
    for width in (375, 768, 1440):
        page = browser.new_page(viewport={"width": width, "height": 900})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(site.joinpath("index.html").as_uri())
        page.wait_for_timeout(300)
        sw = page.evaluate("document.documentElement.scrollWidth")
        check(f"{width}px: no horizontal scroll", sw <= width, f"scrollWidth {sw}")
        check(f"{width}px: no JS errors", not errors, "; ".join(errors))
        page.screenshot(path=str(shots / f"baba-{width}.png"), full_page=True)
        if width == 375:
            info = page.evaluate("""() => ({
              h1: document.querySelectorAll('h1').length,
              lang: document.documentElement.lang,
              skip: !!document.querySelector('a.skip[href="#main"]') && !!document.getElementById('main'),
              unlabeled: [...document.querySelectorAll('img:not([alt]), svg[role=img]:not([aria-label])')].length,
              sections: [...document.querySelectorAll('main section')].map(s => ({
                id: s.querySelector('h2,h1')?.textContent.trim(),
                primary: s.querySelectorAll('a.btn:not(.btn-ghost)').length,
                ctas: s.querySelectorAll('a.btn').length})),
              brokenAnchors: [...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href'))
                 .filter(h => h.length > 1 && !document.getElementById(h.slice(1))),
              tapTargets: [...document.querySelectorAll('a.btn')].filter(a => a.getBoundingClientRect().height < 44).length
            })""")
            check("Exactly one <h1>", info["h1"] == 1, str(info["h1"]))
            check("lang attribute set", info["lang"] == "en")
            check("Skip link targets #main", info["skip"])
            check("Every image/illustration has alt text or aria-label", info["unlabeled"] == 0)
            check("No broken in-page anchors", not info["brokenAnchors"], str(info["brokenAnchors"]))
            check("Buttons are at least 44px tall (tap targets)", info["tapTargets"] == 0, f"{info['tapTargets']} too small")
            for s in info["sections"]:
                check(f"Section '{s['id']}': exactly one CTA", s["ctas"] == 1, f"{s['ctas']} CTAs")
        page.close()
    browser.close()

passed = sum(ok for _, ok, _ in checks)
for name, ok, detail in checks:
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail else ""))
print(f"\n{passed}/{len(checks)} checks passed")
sys.exit(0 if passed == len(checks) else 1)
