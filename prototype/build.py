"""Build paywall-v2.html from src/ by inlining Kickresume Design System fonts + logos.

Usage: python3 build.py <path-to-unzipped-Kickresume_Design_System>
"""
import base64, pathlib, re, sys

ds = pathlib.Path(sys.argv[1])
here = pathlib.Path(__file__).parent
src = (here / "src/paywall-v2.src.html").read_text()

def svg(path, cls):
    s = (ds / path).read_text().strip()
    s = re.sub(r"<\?xml.*?\?>", "", s)
    return s.replace("<svg ", f'<svg class="{cls}" role="img" aria-label="Kickresume" ', 1)

faces = [
    ("Graphik Web", "Graphik-Regular-Web.woff2", "woff2", 400, "normal"),
    ("Graphik Web", "Graphik-Medium-Web.woff2", "woff2", 500, "normal"),
    ("Graphik Web", "Graphik-Semibold-Web.woff2", "woff2", 600, "normal"),
    ("Graphik Web", "Graphik-Bold-Web.woff2", "woff2", 700, "normal"),
    ("Henk-Work", "Henk-Work-Regular.woff", "woff", 400, "normal"),
    ("Henk-Work", "Henk-Work-Bold.otf", "opentype", 700, "normal"),
]
mime = {"woff2": "font/woff2", "woff": "font/woff", "opentype": "font/otf"}
css = "\n".join(
    f'@font-face{{font-family:"{fam}";src:url(data:{mime[fmt]};base64,{base64.b64encode((ds / "fonts" / f).read_bytes()).decode()}) format("{fmt}");font-weight:{w};font-style:{st};font-display:swap}}'
    for fam, f, fmt, w, st in faces
)
out = (src.replace("/*__FONTS__*/", css)
          .replace("__LOGO_SYM__", svg("assets/logos/kickresume-symbol-red.svg", "logo-sym"))
          .replace("__LOGO__", svg("assets/logos/kickresume-wordmark-default.svg", "logo")))
assert "`" not in out.split("const LOGO = `")[1].split("`;")[0]
(here / "paywall-v2.html").write_text(out)
print("wrote", len(out) // 1024, "KB")
