"""Exercise navigation, search, figures, and mobile layout in a real browser."""

import argparse
import json
from pathlib import Path

from playwright.sync_api import sync_playwright


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000/GFMR/")
    parser.add_argument("--output", type=Path, default=Path("preview-artifacts"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    pages = ["index", "overview", "parameters", "hydraulics", "lifetime", "geometry", "materials", "references", "disclaimer"]
    errors = []
    requests = []
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(timeout=20000)
        context = browser.new_context(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
        page = context.new_page()
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("response", lambda response: requests.append(f"{response.status} {response.url}") if response.status >= 400 else None)

        for width in [1440, 390]:
            page.set_viewport_size({"width": width, "height": 1000 if width == 1440 else 844})
            for name in pages:
                page.goto(args.base_url.rstrip("/") + f"/{name}.html", wait_until="domcontentloaded")
                page.evaluate("document.fonts.ready")
                page.locator("img[loading='lazy']").evaluate_all("images => images.forEach(image => image.loading = 'eager')")
                page.wait_for_function("Array.from(document.querySelectorAll('img[src]')).every(image => image.complete && image.naturalWidth > 0)")
                assert page.locator("h1").count() == 1, f"Heading missing or duplicated: {name}"
                assert page.locator(".gfmr-footer__disclaimer").is_visible(), f"Disclaimer missing: {name}"
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), f"Horizontal page overflow: {name} at {width}px"
                assert page.locator("img[src]").evaluate_all("images => images.every(image => image.complete && image.naturalWidth > 0)"), f"Broken image: {name}"
                results.append(f"{name} at {width}px")
                print(f"Checked {name} at {width}px", flush=True)
                if name in {"index", "parameters", "geometry", "materials", "disclaimer"}:
                    page.screenshot(path=str(args.output / f"{name}-{width}.png"), full_page=True)

        page.set_viewport_size({"width": 1440, "height": 1000})
        page.goto(args.base_url.rstrip("/") + "/geometry.html", wait_until="domcontentloaded")
        page.locator(".zoomable").first.click()
        assert page.locator(".figure-dialog").is_visible(), "Figure viewer did not open"
        page.keyboard.press("Escape")
        assert not page.locator(".figure-dialog").is_visible(), "Figure viewer did not close with Escape"
        assert page.locator(".zoomable").first.evaluate("el => el === document.activeElement"), "Figure viewer did not restore keyboard focus"
        if args.base_url.startswith("file:"):
            page.locator("a[download]").first.click()
            page.wait_for_url("**/geometry-xy.png")
            page.go_back(wait_until="domcontentloaded")
        else:
            with page.expect_download() as download:
                page.locator("a[download]").first.click()
            assert download.value.suggested_filename == "gfmr-top-view.png"

        search = page.locator("input[data-md-component='search-query']")
        search.fill("hafnium")
        page.wait_for_function("document.querySelector('.md-search-result__list').textContent.toLowerCase().includes('hafnium')")
        assert page.locator(".md-search-result__link").count() > 0, "Search has no results"
        page.keyboard.press("Escape")

        page.set_viewport_size({"width": 390, "height": 844})
        page.goto(args.base_url.rstrip("/") + "/index.html", wait_until="domcontentloaded")
        page.locator("label[for='__drawer'].md-header__button").click()
        assert page.locator("#__drawer").is_checked(), "Mobile drawer did not open"
        page.locator(".md-nav--primary").get_by_role("link", name="Geometry", exact=True).click()
        page.wait_for_url("**/geometry.html")
        assert not page.locator("#__drawer").is_checked(), "Mobile drawer did not close"

        assert not errors, errors
        assert not requests, requests
        context.close()
        browser.close()

    image_check = "PNG opens directly from disk" if args.base_url.startswith("file:") else "PNG download"
    report = {"pages_checked": results, "interaction_checks": ["figure viewer", "Escape and focus return", image_check, "search", "mobile navigation"], "browser_errors": errors, "failed_http_responses": requests}
    (args.output / "browser-check.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
