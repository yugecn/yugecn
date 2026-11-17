"""Push new (and edited) posts to Blogger after the Pelican build.

Posts already listed in .blogger-sync.json with "skip" are never sent.
Needs env: BLOGGER_CLIENT_ID, BLOGGER_CLIENT_SECRET, BLOGGER_REFRESH_TOKEN.
"""
import datetime
import hashlib
import json
import os
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

BLOG_ID = os.environ.get("BLOGGER_BLOG_ID", "226870845379784330")
SITE = os.environ.get("SITEURL", "https://yugecn.github.io").rstrip("/") + "/"
ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / ".blogger-sync.json"
OUTPUT = ROOT / "output"
URL_ATTRS = {"src", "href", "poster", "data-src"}


class Rewriter(HTMLParser):
    """Return the inner HTML of div.entry-content with absolute URLs."""

    def __init__(self, base):
        super().__init__(convert_charrefs=False)
        self.base, self.depth, self.out, self.done = base, 0, [], False

    def _attrs(self, attrs):
        parts = []
        for k, v in attrs:
            if v is None:
                parts.append(k)
                continue
            if k in URL_ATTRS and not v.startswith(("#", "mailto:", "data:")):
                v = urllib.parse.urljoin(self.base, v)
            if k == "srcset":
                v = ", ".join(
                    " ".join([urllib.parse.urljoin(self.base, p.split()[0])] + p.split()[1:])
                    for p in v.split(",") if p.strip())
            parts.append('%s="%s"' % (k, v.replace('"', "&quot;")))
        return (" " + " ".join(parts)) if parts else ""

    def handle_starttag(self, tag, attrs):
        if self.done:
            return
        if self.depth:
            if tag == "div":
                self.depth += 1
            self.out.append("<%s%s>" % (tag, self._attrs(attrs)))
        elif tag == "div" and "entry-content" in (dict(attrs).get("class") or "").split():
            self.depth = 1

    def handle_startendtag(self, tag, attrs):
        if self.depth and not self.done:
            self.out.append("<%s%s />" % (tag, self._attrs(attrs)))

    def handle_endtag(self, tag):
        if not self.depth or self.done:
            return
        if tag == "div":
            self.depth -= 1
            if self.depth == 0:
                self.done = True
                return
        self.out.append("</%s>" % tag)

    def _raw(self, text):
        if self.depth and not self.done:
            self.out.append(text)

    handle_data = _raw

    def handle_entityref(self, name):
        self._raw("&%s;" % name)

    def handle_charref(self, name):
        self._raw("&#%s;" % name)

    def handle_comment(self, data):
        pass


def load_articles():
    sys.path.insert(0, str(ROOT))
    os.chdir(ROOT)
    from pelican.contents import Article
    from pelican.readers import Readers
    from pelican.settings import read_settings

    settings = read_settings("publishconf.py")
    readers = Readers(settings)
    base = Path(settings["PATH"])
    for sub in settings["ARTICLE_PATHS"]:
        for f in sorted((base / sub).rglob("*")):
            if f.suffix.lower() not in (".md", ".markdown", ".rst", ".html"):
                continue
            rel = f.relative_to(base).as_posix()
            art = readers.read_file(base_path=str(base), path=rel, content_class=Article)
            yield rel, art


def token():
    data = urllib.parse.urlencode({
        "client_id": os.environ["BLOGGER_CLIENT_ID"],
        "client_secret": os.environ["BLOGGER_CLIENT_SECRET"],
        "refresh_token": os.environ["BLOGGER_REFRESH_TOKEN"],
        "grant_type": "refresh_token",
    }).encode()
    with urllib.request.urlopen("https://oauth2.googleapis.com/token", data) as r:
        return json.load(r)["access_token"]


def api(method, url, tok, body):
    req = urllib.request.Request(url, json.dumps(body).encode(), method=method, headers={
        "Authorization": "Bearer " + tok, "Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def main():
    state = json.loads(STATE.read_text("utf-8")) if STATE.exists() else {}
    if "--mark-existing" in sys.argv:
        for rel, _ in load_articles():
            state.setdefault(rel, {"skip": True})
        STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", "utf-8")
        return
    if not all(os.environ.get(k) for k in ("BLOGGER_CLIENT_ID", "BLOGGER_CLIENT_SECRET", "BLOGGER_REFRESH_TOKEN")):
        print("Blogger secrets not set; skipping.")
        return
    tok, changed = None, False
    for rel, art in load_articles():
        entry = state.get(rel, {})
        if entry.get("skip") or getattr(art, "status", "published") != "published":
            continue
        page = OUTPUT / art.save_as
        if not page.exists():
            print("missing build output for", rel)
            continue
        rw = Rewriter(SITE + art.url)
        rw.feed(page.read_text("utf-8"))
        labels = [t.name for t in getattr(art, "tags", []) or []]
        if getattr(art, "category", None):
            labels.insert(0, art.category.name)
        body = {"title": art.title, "content": "".join(rw.out).strip(), "labels": labels,
                "published": datetime.datetime.isoformat(art.date)}
        digest = hashlib.sha256(json.dumps(body, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
        if entry.get("hash") == digest:
            continue
        tok = tok or token()
        base = "https://www.googleapis.com/blogger/v3/blogs/%s/posts/" % BLOG_ID
        if entry.get("id"):
            res = api("PUT", base + entry["id"], tok, dict(body, id=entry["id"]))
            print("updated", rel, res.get("url"))
        else:
            res = api("POST", base, tok, body)
            print("published", rel, res.get("url"))
        state[rel] = {"id": res["id"], "hash": digest, "url": res.get("url")}
        changed = True
    if changed:
        STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", "utf-8")


if __name__ == "__main__":
    main()
