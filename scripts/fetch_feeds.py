#!/usr/bin/env python3
"""Fetch RSS feeds server-side and write a static JSON file for GitHub Pages."""
import json, re, time, urllib.request, urllib.parse, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "headlines.json"
FEEDS = [
    ("OpenAI", "https://openai.com/news/rss.xml"),
    ("Google DeepMind", "https://deepmind.google/blog/rss.xml"),
    ("Hugging Face", "https://huggingface.co/blog/feed.xml"),
    ("Microsoft AI", "https://blogs.microsoft.com/ai/feed/"),
    ("GitHub Blog", "https://github.blog/feed/"),
    ("Systems, storage & C++", "https://news.google.com/rss/search?q=(distributed+systems+OR+storage+systems+OR+database+engineering+OR+C%2B%2B)+when:7d&hl=en-US&gl=US&ceid=US:en"),
    ("AI agents & coding", "https://news.google.com/rss/search?q=(AI+agents+OR+AI+coding+tools+OR+open-source+LLM)+when:7d&hl=en-US&gl=US&ceid=US:en"),
]
def clean(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", unescape(s)).strip()
def child_text(node, names):
    for name in names:
        el = node.find(name)
        if el is not None and el.text:
            return el.text.strip()
    return ""
def parse_date(s):
    if not s: return ""
    try:
        d = parsedate_to_datetime(s)
        if d.tzinfo is None: d = d.replace(tzinfo=timezone.utc)
        return d.astimezone(timezone.utc).isoformat()
    except Exception:
        return s
def fetch(name, url):
    req = urllib.request.Request(url, headers={"User-Agent":"TechBriefingFeedBot/1.0 (RSS reader)"})
    with urllib.request.urlopen(req, timeout=20) as r:
        raw = r.read()
    root = ET.fromstring(raw)
    found=[]
    # RSS and Atom
    for item in root.findall(".//item"):
        title=clean(child_text(item,["title"]))
        link=child_text(item,["link"])
        desc=clean(child_text(item,["description","content:encoded"]))
        date=parse_date(child_text(item,["pubDate","date"]))
        if title and link: found.append({"title":title,"link":link,"desc":desc[:260],"date":date,"source":name})
    ns={"atom":"http://www.w3.org/2005/Atom"}
    for item in root.findall(".//atom:entry",ns):
        title=clean(child_text(item,["{http://www.w3.org/2005/Atom}title"]))
        linkel=item.find("atom:link",ns)
        link=linkel.attrib.get("href","") if linkel is not None else url
        desc=clean(child_text(item,["{http://www.w3.org/2005/Atom}summary","{http://www.w3.org/2005/Atom}content"]))
        date=parse_date(child_text(item,["{http://www.w3.org/2005/Atom}published","{http://www.w3.org/2005/Atom}updated"]))
        if title and link: found.append({"title":title,"link":link,"desc":desc[:260],"date":date,"source":name})
    return found
def main():
    items=[]; failures=[]
    for name,url in FEEDS:
        try:
            entries=fetch(name,url)
            items.extend(entries[:10])
            print(f"OK {name}: {len(entries)} entries")
        except Exception as e:
            failures.append({"source":name,"error":str(e)})
            print(f"WARN {name}: {e}")
    seen=set(); unique=[]
    for x in sorted(items,key=lambda v:v.get("date",""),reverse=True):
        key=x["title"].casefold()
        if key not in seen:
            seen.add(key); unique.append(x)
    payload={"updated_at":datetime.now(timezone.utc).isoformat(),"items":unique[:60],"sources_failed":failures}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"Wrote {len(payload['items'])} headlines to {OUT}")
    if not payload["items"]:
        raise SystemExit("All feeds failed; refusing to publish an empty feed.")
if __name__=="__main__": main()
