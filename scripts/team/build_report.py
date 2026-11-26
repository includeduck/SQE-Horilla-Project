"""Build the final project report PDF from docs/team/report/REPORT.md.

REPORT.md is the main body. It embeds other team documents with two directives:

    <!-- include: ../TRACEABILITY_MATRIX.md shift=1 strip-title -->
    <!-- appendix: A | Title | ../SCOPE.md from="# Test Scope" ; ../OTHER.md -->

Included files keep their content unchanged. Headings are shifted down one level,
fenced code is left alone, relative links point to the file on GitHub (branch
sqe-team) and images are embedded from the local file. Mermaid blocks are rendered
by mermaid.js in Chromium. A second pass adds page numbers to the contents page.

Run (needs `markdown` and `playwright`; page numbers need `pypdf`, from this
interpreter or the one given in --pdf-python):

    python scripts/team/build_report.py --decision release --date "28 November 2026"
"""

import argparse
import base64
import json
import mimetypes
import re
import subprocess
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs/team/report/REPORT.md"
OUT = ROOT / "docs/team/report/Project_24I-3071_24I-3000_24I-3130_B.pdf"
GITHUB = "https://github.com/includeduck/SQE-Horilla-Project"
BRANCH = "sqe-team"
MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"
FOOTER = "Project_24I-3071_24I-3000_24I-3130_B · SE3002 Software Quality Engineering, SE-5B"

DECISIONS = {
    "release": (
        "Decision: RELEASE the tested leave workflows (W1 and W2).",
        "All three release criteria (EC-1, EC-2, EC-3) and the other two exit criteria are met on "
        "`sqe-team` after the integration pull request [#52](" + GITHUB + "/pull/52) was merged with the "
        "required `gate` check green. #11 and #46 are closed as fixed and verified.",
    ),
    "conditional": (
        "Decision: RELEASE once integration PR #52 is merged with the required gate green; HOLD until then.",
        "EC-1 and EC-3 are met outright. EC-2 depends on the high-severity defect #46 in the "
        "highest-scored risk (PR-01). Its fix (PR #51) is part of the integration pull request "
        "[#52](" + GITHUB + "/pull/52): the recovery tests failed before (2 red) and pass after (5/5), "
        "and the unit, coverage and mutation gates are unchanged. Until #52 is merged, `sqe-team` still "
        "has the defect, so the decision there is HOLD.",
    ),
}

CSS = """
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
html { font-family: "Segoe UI", Calibri, Arial, sans-serif; font-size: 9.6pt; color: #1b1f24; line-height: 1.42; }
body { margin: 0; }
h1, h2, h3, h4, h5, h6 { color: #12355b; line-height: 1.25; break-after: avoid; page-break-after: avoid; }
h1 { font-size: 18pt; border-bottom: 2px solid #12355b; padding-bottom: 4px; margin: 0 0 10px; break-before: page; }
h2 { font-size: 13pt; margin: 18px 0 6px; }
h3 { font-size: 11pt; margin: 14px 0 5px; }
h4, h5, h6 { font-size: 10pt; margin: 12px 0 4px; }
.appendix-doc h2 { font-size: 13pt; } .appendix-doc h3 { font-size: 11.5pt; }
p, li { orphans: 3; widows: 3; }
a { color: #0b5cad; text-decoration: none; word-break: break-word; }
code { font-family: Consolas, "Cascadia Mono", monospace; font-size: 8.6pt; background: #f1f3f5; padding: 0 2px; border-radius: 2px; word-break: break-word; }
pre { background: #f6f8fa; border: 1px solid #d8dee4; padding: 6px 8px; font-size: 8pt; white-space: pre-wrap; word-break: break-word; break-inside: avoid; }
pre code { background: none; padding: 0; font-size: 8pt; }
table { border-collapse: collapse; width: 100%; margin: 6px 0 10px; font-size: 8.3pt; }
th, td { border: 1px solid #c9d1d9; padding: 3px 5px; vertical-align: top; text-align: left; overflow-wrap: break-word; hyphens: auto; }
td code { word-break: break-all; }
.cover td:first-child { white-space: nowrap; }
th { background: #e8eef5; color: #12355b; }
tr { break-inside: avoid; }
thead { display: table-header-group; }
img { max-width: 100%; max-height: 115mm; display: block; margin: 8px auto; break-inside: avoid; }
blockquote { margin: 6px 0; padding: 2px 10px; border-left: 3px solid #c9d1d9; color: #444; }
hr { border: 0; border-top: 1px solid #d8dee4; margin: 10px 0; }
.mermaid { background: none; border: 0; text-align: center; white-space: normal; }
.cover { height: 250mm; display: flex; flex-direction: column; justify-content: center; }
.cover h1 { break-before: auto; font-size: 30pt; border: 0; margin: 6px 0 4px; }
.cover .course { font-size: 11pt; color: #555; margin: 0; }
.cover .subtitle { font-size: 14pt; color: #12355b; margin: 0 0 26px; }
.cover table { font-size: 10pt; width: auto; min-width: 70%; }
.cover .meta { font-size: 10pt; color: #333; margin-top: 22px; }
.toc-page { break-before: page; }
.toc-page h2 { font-size: 18pt; border-bottom: 2px solid #12355b; padding-bottom: 4px; }
.toc { list-style: none; padding: 0; margin: 0; }
.toc li { display: flex; align-items: baseline; margin: 2px 0; }
.toc li.l1 { font-weight: 600; margin-top: 7px; }
.toc li.l2 { padding-left: 16px; }
.toc li .dots { flex: 1; border-bottom: 1px dotted #999; margin: 0 4px; transform: translateY(-3px); }
.toc a { color: #1b1f24; }
.decision { border: 2px solid #1f7a3a; background: #eef8f0; padding: 6px 12px; font-size: 11pt; margin: 8px 0; }
.appendix-note { font-size: 8.6pt; color: #555; border-left: 3px solid #d8dee4; padding-left: 8px; margin-bottom: 10px; }
.doc-source { font-size: 8.6pt; color: #555; margin: 14px 0 4px; border-top: 1px solid #d8dee4; padding-top: 4px; }
"""

FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})")


def split_fences(text):
    """Yield (is_code, chunk) so text outside fenced code can be edited safely."""
    out, buf, fence = [], [], None
    for line in text.splitlines(keepends=True):
        m = FENCE.match(line)
        if fence is None and m:
            out.append((False, "".join(buf))); buf = [line]; fence = m.group(2)[0] * 3
        elif fence is not None and m and m.group(2).startswith(fence):
            buf.append(line); out.append((True, "".join(buf))); buf = []; fence = None
        else:
            buf.append(line)
    out.append((fence is not None, "".join(buf)))
    return out


def outside_code(text, fn):
    return "".join(chunk if code else fn(chunk) for code, chunk in split_fences(text))


def github_url(path):
    rel = path.resolve().relative_to(ROOT).as_posix()
    kind = "tree" if path.is_dir() else "blob"
    return f"{GITHUB}/{kind}/{BRANCH}/{rel}"


def data_uri(path):
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def rewrite_links(text, base_dir):
    def target(raw, image):
        if re.match(r"^[a-z]+:|^#|^/", raw):
            return raw
        file_part, _, anchor = raw.partition("#")
        path = (base_dir / file_part).resolve()
        try:
            path.relative_to(ROOT)
        except ValueError:
            return raw
        if image and path.is_file():
            return data_uri(path)
        return github_url(path) + (("#" + anchor) if anchor else "")

    def md_link(m):
        bang, label, raw, title = m.group(1), m.group(2), m.group(3), m.group(4) or ""
        return f"{bang}[{label}]({target(raw, bool(bang))}{title})"

    def html_attr(m):
        return f'{m.group(1)}="{target(m.group(2), m.group(1) == "src")}"'

    def fix(chunk):
        chunk = re.sub(r"(!?)\[([^\]]*)\]\(<?([^)\s>]+)>?(\s+\"[^\"]*\")?\)", md_link, chunk)
        return re.sub(r'\b(href|src)="([^"]+)"', html_attr, chunk)

    return outside_code(text, fix)


def shift_headings(text, by):
    return outside_code(text, lambda c: re.sub(r"(?m)^(#{1,6})(?=\s)", lambda m: "#" * min(6, len(m.group(1)) + by), c))


def mermaid_blocks(text):
    return re.sub(r"(?ms)^```mermaid\s*\n(.*?)^```\s*$",
                  lambda m: '<div class="mermaid">\n' + m.group(1).replace("<", "&lt;") + "</div>", text)


def load_doc(rel, base, start=None, strip_title=False, shift=1):
    path = (base / rel).resolve()
    text = path.read_text(encoding="utf-8")
    if start:
        idx = 0 if text.startswith(start) else text.find("\n" + start) + 1
        if idx == 0 and not text.startswith(start):
            sys.exit(f"{rel}: start marker {start!r} not found")
        text = text[idx:]
    if strip_title:
        text = re.sub(r"\A\s*# [^\n]*\n", "", text, count=1)
    text = rewrite_links(text, path.parent)
    return mermaid_blocks(shift_headings(text, shift)), path


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def assemble(decision, date):
    base = SOURCE.parent
    text = SOURCE.read_text(encoding="utf-8")
    title, body = DECISIONS[decision]
    text = text.replace("{{DATE}}", date).replace("{{DECISION}}", title).replace("{{DECISION_TEXT}}", body)
    text = rewrite_links(text, base)
    text = mermaid_blocks(text)

    def include(m):
        args = m.group(2)
        shift = int(re.search(r"shift=(\d)", args).group(1)) if "shift=" in args else 1
        doc, _ = load_doc(m.group(1), base, strip_title="strip-title" in args, shift=shift)
        return doc

    text = re.sub(r"<!-- include: (\S+)([^>]*)-->", include, text)

    def appendix(m):
        letter, name, sources = (s.strip() for s in m.group(1).split("|"))
        parts = [f"# Appendix {letter}. {name} {{#appendix-{letter.lower()}}}", ""]
        parts.append('<p class="appendix-note">Reproduced unchanged from the repository; headings are one level lower '
                     "than in the source file and relative links point to the file on GitHub. Dated status lines inside "
                     "a document describe the state on that date; §8 of this report gives the final decision.</p>")
        for src in sources.split(";"):
            src = src.strip()
            start = None
            if " from=" in src:
                src, start = src.split(" from=")
                start = start.strip().strip('"')
            doc, path = load_doc(src.strip(), base, start=start)
            parts += ["", f'<p class="doc-source">Source: <a href="{github_url(path)}">{path.relative_to(ROOT).as_posix()}</a></p>',
                      "", '<div class="appendix-doc" markdown="1">', "", doc, "", "</div>", ""]
        return "\n".join(parts)

    text = re.sub(r"<!-- appendix: (.+?) -->", appendix, text)
    text = text.replace("<!-- appendices -->", "")

    # Give every main-body heading of level 1/2 an explicit id and collect the contents.
    toc, main_end = [], text.find("# Appendix A.")

    def ids(m):
        hashes, title = m.group(1), m.group(2).strip()
        if "{#" in title:
            hid = re.search(r"\{#([^}]+)\}", title).group(1)
            title = re.sub(r"\s*\{#[^}]+\}", "", title)
        else:
            hid = slug(title)
        if title not in ("Final Project Report", "Contents"):
            toc.append((len(hashes), title, hid))
        return f"{hashes} {title} {{#{hid}}}"

    head, tail = text[:main_end], text[main_end:]
    head = outside_code(head, lambda c: re.sub(r"(?m)^(#{1,2}) (.+)$", ids, c))
    tail = re.sub(r"(?m)^(#) (Appendix .+)$", ids, tail)
    return head + tail, toc


def toc_html(toc, pages=None):
    rows = []
    for level, title, hid in toc:
        page = str(pages.get(hid, "")) if pages else ""
        rows.append(f'<li class="l{level}"><a href="#{hid}">{title}</a><span class="dots"></span><span>{page}</span></li>')
    return '<ul class="toc">' + "".join(rows) + "</ul>"


def render_html(text, toc, pages=None):
    text = text.replace("{{TOC}}", toc_html(toc, pages))
    text = re.sub(r'<div class="(cover|toc-page|decision)">', r'<div class="\1" markdown="1">', text)
    html = markdown.markdown(text, extensions=["tables", "fenced_code", "attr_list", "md_in_html", "sane_lists"])
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><title>Final Project Report</title>"
            f"<style>{CSS}</style><script src=\"{MERMAID}\"></script></head><body>{html}"
            "<script>mermaid.initialize({startOnLoad:false, theme:'neutral'});"
            "window.mermaidDone = mermaid.run({querySelector:'.mermaid'}).then(()=>true).catch(e=>String(e));</script>"
            "</body></html>")


def print_pdf(html, out):
    from playwright.sync_api import sync_playwright

    tmp = out.with_suffix(".html")
    tmp.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(tmp.as_uri(), wait_until="networkidle")
        result = page.evaluate("window.mermaidDone")
        if result is not True:
            sys.exit(f"mermaid failed: {result}")
        page.pdf(path=str(out), format="A4", print_background=True, display_header_footer=True,
                 margin={"top": "16mm", "bottom": "16mm", "left": "15mm", "right": "15mm"},
                 header_template="<span></span>",
                 footer_template=(f'<div style="font-size:7pt;color:#666;width:100%;padding:0 15mm;display:flex;'
                                  f'justify-content:space-between"><span>{FOOTER}</span>'
                                  '<span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>'))
        browser.close()
    tmp.unlink()


PAGE_TEXT = "import json,sys,pypdf;r=pypdf.PdfReader(sys.argv[1]);print(json.dumps([p.extract_text() or '' for p in r.pages]))"


def page_texts(pdf, pdf_python):
    try:
        import pypdf  # noqa: F401
        python = sys.executable
    except ImportError:
        python = pdf_python
    if not python:
        return None
    res = subprocess.run([python, "-I", "-c", PAGE_TEXT, str(pdf)], capture_output=True, text=True, encoding="utf-8")
    return json.loads(res.stdout) if res.returncode == 0 else None


def find_pages(texts, toc):
    norm = lambda s: re.sub(r"\s+", "", s).lower()  # noqa: E731
    pages, start = {}, 2  # skip the cover and the contents page
    for _, title, hid in toc:
        key = norm(title)[:40]
        for i in range(start, len(texts)):
            if key in norm(texts[i]):
                pages[hid] = i + 1
                start = i
                break
    return pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--decision", choices=DECISIONS, default="conditional")
    ap.add_argument("--date", default="26 November 2026")
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--pdf-python", help="interpreter with pypdf, if this one has none (for page numbers)")
    args = ap.parse_args()

    text, toc = assemble(args.decision, args.date)
    print_pdf(render_html(text, toc), args.out)
    texts = page_texts(args.out, args.pdf_python)
    if texts:
        pages = find_pages(texts, toc)
        print_pdf(render_html(text, toc, pages), args.out)
        missing = [t for _, t, h in toc if h not in pages]
        print(f"pages: {len(texts)}; contents entries with page numbers: {len(pages)}/{len(toc)}"
              + (f"; missing: {missing}" if missing else ""))
    else:
        print("pypdf not available: contents page has no page numbers")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
