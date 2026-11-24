"""Find the photo an article's own page offers for link previews (MW 2026-11-15, approved build).

Most news pages name a preview image in their page header (og:image or twitter:image). The CNAP team asks for it
from the staff form; the photo stays hidden until a person approves it. Nothing here runs on its own."""

import re
from html import unescape
from urllib.parse import urljoin
from urllib.request import Request, urlopen

_META = re.compile(r"<meta\b[^>]*>", re.I)
_IMG = re.compile(r"<img\b[^>]*>", re.I)
# A site's all-purpose share picture says nothing about the article, so it counts as no photo (MW 2026-11-24, from a
# test run on K-State News: one article named its own photo, another only the site's "Web-Link-Image.jpg").
_GENERIC = re.compile(
    r"(web[-_]?link[-_]?image|default|placeholder|logo|social[-_]?share|share[-_]?image)", re.I
)


def _attr(tag, name):
    m = re.search(r"\b" + name + r'\s*=\s*("([^"]*)"|\'([^\']*)\')', tag, re.I)
    return unescape(m.group(2) if m.group(2) is not None else m.group(3)) if m else ""


def find_preview(url, timeout=6):
    """Return (image_url, description) from the page at url, or ("", "") when the page names none."""
    if not url or not url.startswith(("http://", "https://")):
        return "", ""
    req = Request(url, headers={"User-Agent": "CNAP Member Hub (preview photo lookup)"})
    with urlopen(req, timeout=timeout) as r:  # noqa: S310  (https only, staff-initiated)
        head = r.read(400_000).decode("utf-8", "replace")
    return parse_preview(head, url)


def parse_preview(html, base_url):
    found = {}
    for tag in _META.findall(html):
        key = (_attr(tag, "property") or _attr(tag, "name")).lower()
        if key in (
            "og:image",
            "og:image:url",
            "twitter:image",
            "og:image:alt",
            "twitter:image:alt",
        ):
            found.setdefault(key, _attr(tag, "content"))
    img = found.get("og:image") or found.get("og:image:url") or found.get("twitter:image") or ""
    alt = found.get("og:image:alt") or found.get("twitter:image:alt") or ""
    if not img or _GENERIC.search(img.rsplit("/", 1)[-1]):
        return "", ""
    img = urljoin(base_url, img)
    if not alt:
        alt = _alt_from_article(html, base_url, img)
    return img, alt


def _alt_from_article(html, base_url, img):
    """No description in the header: borrow the alt text of the article's own picture, the same file or one from
    the same folder (K-State News keeps a crop for sharing beside the article's photo)."""
    folder = img.rsplit("/", 1)[0] + "/"
    near = ""
    for tag in _IMG.findall(html):
        src, alt = urljoin(base_url, _attr(tag, "src")), _attr(tag, "alt").strip()
        if not alt:
            continue
        if src == img:
            return alt
        if not near and src.startswith(folder):
            near = alt
    return near
