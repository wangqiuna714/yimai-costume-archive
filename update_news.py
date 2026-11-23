#!/usr/bin/env python3
# Daily RSS discovery feed. Collected entries are leads, not verified research.
import json, re, urllib.request, xml.etree.ElementTree as ET
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
KEYWORDS = re.compile(r"fashion|costume|textile|embroidery|silk|museum|heritage|craft|Chinese|China|design|runway|服饰|服装|纺织|刺绣|非遗|新中式", re.I)

def clean(s):
    return re.sub(r"\\s+", " ", re.sub(r"<[^>]+>", "", s or "")).strip()

def get_date(s):
    try: return parsedate_to_datetime(s).date().isoformat()
    except Exception: return ""

items = []
for source, url in FEEDS:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "YimaiArchiveBot/1.0"})
        with urllib.request.urlopen(req, timeout=20) as response:
            root = ET.fromstring(response.read())
        for node in root.findall(".//item")[:30]:
            title, link = clean(node.findtext("title")), clean(node.findtext("link"))
            summary, pub = clean(node.findtext("description")), clean(node.findtext("pubDate"))
            if title and link and KEYWORDS.search(title + " " + summary):
                items.append({"title": title[:240], "link": link, "summary": summary[:420],
                              "source": source, "date": get_date(pub),
                              "collected_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                              "verification": "待编辑核验原文"})
    except Exception as exc:
        print(f"[WARN] {source}: {exc}")
unique = {x["link"]: x for x in items}
result = sorted(unique.values(), key=lambda x: x.get("date", ""), reverse=True)[:80]
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(f"Wrote {len(result)} RSS leads")
