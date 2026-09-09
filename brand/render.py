# -*- coding: utf-8 -*-
"""Render every PNG the site serves from the SVG masters in this folder.

The logo used to exist only as two flat PNGs with no source, so it could
not be produced at any other size and would have been unrecoverable if
those files were lost. Everything is now derived from brand/*.svg by this
script, which is the only thing that should ever write those PNGs.

Run from the repo root:  python3 brand/render.py

Uses the Chromium that Playwright already ships, so the output is exactly
what a browser draws — no second SVG renderer to disagree with the one
the site is viewed in.
"""
import asyncio
import functools
import http.server
import io
import os
import socketserver
import threading

from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# Chromium as shipped by the image; Playwright's own download is disabled.
CHROME_CANDIDATES = [
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    "/opt/pw-browsers/chromium/chrome-linux/chrome",
]

# (svg source, output png, pixel size)
TARGETS = [
    ("logo.svg",          "icon-192.png",             192),
    ("logo.svg",          "icon-512.png",             512),
    ("logo.svg",          "apple-touch-icon.png",     180),
    ("logo-maskable.svg", "icon-maskable-512.png",    512),
    ("logo-small.svg",    "favicon-32.png",            32),
    ("logo-small.svg",    "favicon-16.png",            16),
    ("og-image.svg",      "og-image.png",      (1200, 630)),
]


def chrome():
    for path in CHROME_CANDIDATES:
        if os.path.exists(path):
            return path
    raise SystemExit("no Chromium found; looked in %s" % ", ".join(CHROME_CANDIDATES))


def wrap(svg_markup, width, height):
    """An SVG loaded directly is a standalone document with no <head> to
    style, so it goes inside a minimal HTML page instead. Transparent
    background throughout: the icon has to composite onto whatever surface
    a launcher, tab strip, or dark theme puts behind it."""
    return (
        "<!doctype html><meta charset='utf-8'>"
        "<style>html,body{margin:0;padding:0;background:transparent}"
        "svg{display:block;width:%dpx;height:%dpx}</style>%s"
        % (width, height, svg_markup)
    )


def serve(root):
    """Serve the repo on a spare port.

    The social card pulls the site's real typefaces from /fonts.css, and a
    root-absolute path like that resolves to the filesystem root under
    file://. Serving over HTTP makes the render use exactly the fonts a
    visitor sees, instead of silently falling back to a system face."""
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=root)
    httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
    httpd.allow_reuse_address = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


async def main():
    httpd, port = serve(ROOT)
    scratch = os.path.join(HERE, "_render.html")
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            executable_path=chrome(),
            args=["--no-sandbox", "--force-color-profile=srgb"],
        )
        for src, out, size in TARGETS:
            width, height = size if isinstance(size, tuple) else (size, size)
            svg = io.open(os.path.join(HERE, src), encoding="utf-8").read()
            page = await browser.new_page(
                viewport={"width": width, "height": height},
                device_scale_factor=1,
            )
            io.open(scratch, "w", encoding="utf-8").write(wrap(svg, width, height))
            await page.goto("http://127.0.0.1:%d/brand/_render.html" % port)
            await page.evaluate("document.fonts.ready")
            await page.screenshot(
                path=os.path.join(ROOT, out),
                omit_background=True,   # keeps real alpha; the old PNGs
                                        # were saved opaque and carried
                                        # white square corners.
            )
            await page.close()
            print("%-26s %sx%s" % (out, width, height))
        await browser.close()
    os.remove(scratch)
    httpd.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
