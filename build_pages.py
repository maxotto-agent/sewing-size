"""Generate brands/<slug>.html (size chart per brand, cm and in) and sitemap.xml from sizes.json."""
import json, html, re, os
BASE = "https://maxotto-agent.github.io/sewing-size/"
data = json.load(open("sizes.json"))
FOOT = "This application was autonomously scaffolded and deployed using generative software agents. Designed for lightweight, single-purpose utility. Curated and maintained by @maxim-k."
CSS = open("index.html").read().split("<style>")[1].split("</style>")[0]
CSS += "table{border-collapse:collapse;margin:.5rem 0 1.2rem;font-size:.9rem}td,th{border:1px solid #ccc;padding:.2rem .5rem;text-align:right}th:first-child,td:first-child{text-align:left}footer{color:#777;font-size:.75rem;margin-top:2rem}"
slug = lambda b: re.sub(r"[^a-z0-9]+", "-", b.lower()).strip("-")
e = html.escape
def cell(v):
    if not v: return "–"
    lo, hi = v
    f = lambda x: f"{x/2.54:.1f}".rstrip("0").rstrip(".")
    g = lambda x: f"{x:g}"
    return (f"{g(lo)} cm / {f(lo)} in" if lo == hi else f"{g(lo)}–{g(hi)} cm / {f(lo)}–{f(hi)} in")
brands = {}
for r in data: brands.setdefault(r["brand"], []).append(r)
os.makedirs("brands", exist_ok=True)
urls = [""]
for b, rs in brands.items():
    body = f'<p class="sub"><a href="../">Sewing pattern size finder</a> › {e(b)}</p>\n<h1>{e(b)} size chart: bust, waist and hip in cm and inches</h1>\n'
    body += f'<p>Body measurements for each {e(b)} size range, as printed on the maker\'s sizing page. <a href="../"><b>Enter your own measurements to see which size and range to cut →</b></a></p>\n'
    for r in rs:
        hb = any(s.get("hb") for s in r["sizes"])
        head = "<tr><th>Size</th>" + ("<th>High bust</th>" if hb else "") + "<th>Bust</th><th>Waist</th><th>Hip</th></tr>"
        rows = "\n".join("<tr><td>%s</td>%s<td>%s</td><td>%s</td><td>%s</td></tr>" % (e(s["size"]), f'<td>{cell(s.get("hb"))}</td>' if hb else "", cell(s["bust"]), cell(s["waist"]), cell(s["hip"])) for s in r["sizes"])
        body += f'<h2>{e(r["range"])}</h2>\n<p class="sub">{e(r["note"])}. <a href="{e(r["url"])}">Maker\'s chart</a>, checked {e(r["checked"])}.</p>\n<table>\n{head}\n{rows}\n</table>\n'
    body += f'<p class="sub">Copied from {e(b)}\'s own sizing page; makers revise charts, and conversion between units can differ by rounding, so check theirs before cutting. Not affiliated with {e(b)}.</p>'
    p = f"brands/{slug(b)}.html"
    t = f"{b} size chart: bust, waist, hip in cm and inches"
    d = f"{b} body measurements by size ({', '.join(r['range'] for r in rs)}) in centimetres and inches, copied from the maker's sizing page."
    open(p, "w").write(f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>{e(t)}</title>\n<meta name="description" content="{e(d)}">\n<link rel="canonical" href="{BASE}{p}">\n<style>{CSS}</style>\n</head>\n<body>\n<main>\n{body}\n<footer>{FOOT}</footer>\n</main>\n</body>\n</html>\n')
    urls.append(p)
open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{BASE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
print(len(urls), "pages")
