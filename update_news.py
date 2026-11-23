#!/usr/bin/env python3
"""Collect public fashion/costume RSS headlines into data/news.json.
Collected headlines are discovery leads, not verified academic conclusions.
"""
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "data" / "news.json"

FEEDS = [
    ("V&A Museum", "https://www.vam.ac.uk/blog/category/fashion/feed"),
    ("FashionUnited", "https://fashionunited.com/rss"),
    ("Vogue Runway", "https://www.vogue.com/feed/fashion"),
]

KEYWORDS = re.compile(
    r"fashion|costume|textile|embroidery|silk|museum|heritage|craft|"
    r"Chinese|China|design|runway|fashion week|服饰|服装|纺织|刺绣|非遗|新中式",
    re.I,
)

def local_name(tag):
    return tag.rsplit("}", 1)[-1].lower()

def clean(value):
    value = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", value).strip()

def child_text(node, names):
    for child in list(node):
        if local_name(child.tag) in names:
            if local_name(child.tag) == "link":
                href = child.attrib.get("href")
                if href:
                    return href
            return "".join(child.itertext()).strip()
    return ""

def parse_date(value):
    if not value:
        return ""
    try:
        return parsedate_to_datetime(value).date().isoformat()
    except Exception:
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
        except Exception:
            return ""

def extract_items(root, source):
    found = []
    for node in root.iter():
        tag = local_name(node.tag)
        if tag not in ("item", "entry"):
            continue
        title = clean(child_text(node, {"title"}))
        link = clean(child_text(node, {"link"}))
        summary = clean(child_text(node, {"description", "summary", "content"}))
        pub = clean(child_text(node, {"pubdate", "published", "updated", "date"}))
        if not title or not link or not link.startswith(("http://", "https://")):
            continue
        if not KEYWORDS.search(title + " " + summary):
            continue
        found.append({
            "title": title[:240],
            "link": link,
            "summary": summary[:500],
            "source": source,
            "date": parse_date(pub),
            "collected_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "verification": "待编辑核验原文",
        })
    return found

def main():
    items = []
    for source, url in FEEDS:
        try:
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 YimaiCostumeArchive/1.0"},
            )
            with urllib.request.urlopen(request, timeout=25) as response:
                root = ET.fromstring(response.read())
            feed_items = extract_items(root, source)
            print(f"[OK] {source}: {len(feed_items)} matching items")
            items.extend(feed_items)
        except Exception as exc:
            print(f"[WARN] {source}: {type(exc).__name__}: {exc}")

    unique = {item["link"]: item for item in items}
    result = sorted(
        unique.values(),
        key=lambda item: (item.get("date", ""), item.get("collected_at", "")),
        reverse=True,
    )[:80]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[DONE] Wrote {len(result)} RSS leads to {OUT}")

if __name__ == "__main__":
    main()
