# -*- coding: utf-8 -*-
"""Trace the sea silhouette out of the original icon-192.png into an SVG path.

The logo only ever existed as two flat PNGs — no source file, no generator.
Rather than invent a new shape and quietly change the project's identity,
this lifts the actual silhouette out of the original raster so the vector
master is a reproduction, not a redesign.

Run:  python3 brand/extract_landmass.py
Prints an SVG path in a 0..192 coordinate space, ready to paste into
brand/logo.svg. Only needed if the mark is ever re-derived from the raster;
the committed logo.svg already contains its output.
"""
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from scipy import ndimage

SRC = "icon-192.png"
# The silhouette sits at #24323E against a #121924-ish field: a wide gap on
# every channel, so a plain luminance threshold separates them cleanly.
THRESHOLD = 46.0
# Ramer-Douglas-Peucker tolerance, in source pixels. 0.9 keeps every real
# inlet and drops the raster's anti-aliasing jitter.
RDP_EPSILON = 0.9


def largest_contour(mask):
    """The outline of the biggest connected blob in a boolean mask."""
    labels, n = ndimage.label(mask)
    if not n:
        raise SystemExit("no silhouette found — check THRESHOLD")
    biggest = 1 + np.argmax(ndimage.sum(mask, labels, range(1, n + 1)))
    blob = ndimage.binary_fill_holes(labels == biggest).astype(float)
    blob = ndimage.gaussian_filter(blob, 1.1)  # soften the staircase
    cs = plt.contour(blob, levels=[0.5])
    paths = cs.get_paths() if hasattr(cs, "get_paths") else cs.collections[0].get_paths()
    return max((p.vertices for p in paths), key=len)


def rdp(points, epsilon):
    """Ramer-Douglas-Peucker: drop vertices that add no shape."""
    if len(points) < 3:
        return points
    start, end = points[0], points[-1]
    line = end - start
    length = np.hypot(*line)
    if length == 0:
        dists = np.hypot(*(points - start).T)
    else:
        dists = np.abs(np.cross(line, points - start)) / length
    i = int(np.argmax(dists))
    if dists[i] <= epsilon:
        return np.array([start, end])
    return np.vstack([rdp(points[:i + 1], epsilon)[:-1], rdp(points[i:], epsilon)])


def to_smooth_path(pts):
    """Catmull-Rom through the points, emitted as SVG cubic beziers.

    A polygon traced from a raster reads as faceted at large sizes; the
    silhouette is a soft organic shape, so it wants curves."""
    pts = pts[:-1] if np.allclose(pts[0], pts[-1]) else pts
    n = len(pts)
    out = ["M %.2f %.2f" % (pts[0][0], pts[0][1])]
    for i in range(n):
        p0, p1 = pts[(i - 1) % n], pts[i]
        p2, p3 = pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = p1 + (p2 - p0) / 6.0
        c2 = p2 - (p3 - p1) / 6.0
        out.append("C %.2f %.2f %.2f %.2f %.2f %.2f"
                   % (c1[0], c1[1], c2[0], c2[1], p2[0], p2[1]))
    return " ".join(out) + " Z"


def main():
    img = np.asarray(Image.open(SRC).convert("RGB"), dtype=float)
    lum = img @ [0.299, 0.587, 0.114]
    # Ignore the white surround so it cannot register as "bright land".
    inside = np.zeros(lum.shape, bool)
    yy, xx = np.ogrid[:lum.shape[0], :lum.shape[1]]
    inside[(xx - 95.5) ** 2 + (yy - 95.5) ** 2 < 90 ** 2] = True

    contour = largest_contour((lum > THRESHOLD) & inside)
    simplified = rdp(contour, RDP_EPSILON)
    print("contour points: %d -> %d after simplify" % (len(contour), len(simplified)))
    print()
    print(to_smooth_path(simplified))


if __name__ == "__main__":
    main()
