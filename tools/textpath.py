"""Text → SVG outlines. Each glyph is defined once in <defs> and placed with <use>,
so the SVG renders identically everywhere (no web fonts inside <img>)."""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
import os

FD = os.environ.get("FONTS_DIR", os.path.join(os.path.dirname(__file__), "fonts"))

FONT_FILES = {
    "sans-b": FD + "/pre/package/dist/public/static/Pretendard-Bold.otf",
    "sans-sb": FD + "/pre/package/dist/public/static/Pretendard-SemiBold.otf",
    "sans-m": FD + "/pre/package/dist/public/static/Pretendard-Medium.otf",
    "sans": FD + "/pre/package/dist/public/static/Pretendard-Regular.otf",
    "mono": FD + "/jbm/package/files/jetbrains-mono-latin-400-normal.woff",
    "mono-m": FD + "/jbm/package/files/jetbrains-mono-latin-500-normal.woff",
}
_cache = {}


def font(key):
    if key not in _cache:
        f = TTFont(FONT_FILES[key])
        _cache[key] = (f, f.getGlyphSet(), f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm)
    return _cache[key]


class Glyphs:
    """Collects glyph outlines used by one SVG document."""

    def __init__(self, prefix):
        self.prefix = prefix
        self.defs = {}

    def _gid(self, key, name):
        gid = f"{self.prefix}{key.replace('-', '')}_{name}".replace(".", "_")
        if gid not in self.defs:
            f, gs, cmap, hmtx, upm = font(key)
            pen = SVGPathPen(gs)
            gs[name].draw(pen)
            self.defs[gid] = pen.getCommands()
        return gid

    @staticmethod
    def resolve(ch, key):
        """Font key that actually has this character (mono falls back to the sans of similar weight)."""
        if ord(ch) in font(key)[2]:
            return key
        return "sans-m" if key.startswith("mono") else "sans"

    def width(self, text, key, size, track=0.0):
        w = 0.0
        for ch in text:
            k = self.resolve(ch, key)
            f, gs, cmap, hmtx, upm = font(k)
            w += hmtx[cmap[ord(ch)]][0] * size / upm + track * size
        return w - (track * size if text else 0)

    def text(self, s, x, y, key, size, fill, anchor="start", track=0.0, cls=None, opacity=None):
        w = self.width(s, key, size, track)
        if anchor == "end":
            x -= w
        elif anchor == "middle":
            x -= w / 2
        parts = []
        cx = x
        for ch in s:
            k = self.resolve(ch, key)
            f, gs, cmap, hmtx, upm = font(k)
            sc = size / upm
            name = cmap[ord(ch)]
            if ch != " ":
                gid = self._gid(k, name)
                parts.append(f'<use href="#{gid}" transform="translate({cx:.2f} {y:.2f}) scale({sc:.5f} {-sc:.5f})"/>')
            cx += hmtx[name][0] * sc + track * size
        attrs = f' fill="{fill}"'
        if cls:
            attrs += f' class="{cls}"'
        if opacity is not None:
            attrs += f' opacity="{opacity}"'
        return f"<g{attrs}>" + "".join(parts) + "</g>"

    def defs_svg(self):
        return "<defs>" + "".join(f'<path id="{k}" d="{v}"/>' for k, v in self.defs.items()) + "</defs>"
