#!/usr/bin/env python3
import json, re, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"data"/"news.json"
FEEDS=[
 ("中国传统服饰与非遗","https://news.google.com/rss/search?q=%E4%B8%AD%E5%9B%BD%E4%BC%A0%E7%BB%9F%E6%9C%8D%E9%A5%B0+OR+%E9%9D%9E%E9%81%97%E6%9C%8D%E9%A5%B0&hl=zh-CN&gl=CN&ceid=CN:zh-Hans"),
 ("全球时尚与设计","https://news.google.com/rss/search?q=fashion+design+OR+fashion+week+OR+textile+museum&hl=en-US&gl=US&ceid=US:en"),
 ("中国新中式与品牌","https://news.google.com/rss/search?q=%E6%96%B0%E4%B8%AD%E5%BC%8F+OR+%E4%B8%AD%E5%9B%BD%E8%AE%BE%E8%AE%A1%E5%B8%88+%E6%97%B6%E5%B0%9A&hl=zh-CN&gl=CN&ceid=CN:zh-Hans"),
]
def clean(v):
 return re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",v or "")).strip()
def main():
 items=[]
 for source,url in FEEDS:
  try:
   req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 YimaiArchive/1.0"})
   root=ET.fromstring(urllib.request.urlopen(req,timeout=25).read())
   count=0
   for node in root.findall(".//item")[:25]:
    title=clean(node.findtext("title"));link=clean(node.findtext("link"));desc=clean(node.findtext("description"));pub=clean(node.findtext("pubDate"))
    if not title or not link: continue
    try: date=parsedate_to_datetime(pub).date().isoformat()
    except Exception: date=""
    items.append({"title":title[:240],"link":link,"summary":desc[:500],"source":source,"date":date,"collected_at":datetime.now(timezone.utc).isoformat(timespec="seconds"),"verification":"待编辑核验原文"})
    count+=1
   print(f"[OK] {source}: {count} items")
  except Exception as e:
   print(f"[WARN] {source}: {type(e).__name__}: {e}")
 unique={x["link"]:x for x in items}
 result=sorted(unique.values(),key=lambda x:(x.get("date",""),x.get("collected_at","")),reverse=True)[:80]
 OUT.parent.mkdir(parents=True,exist_ok=True)
 OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(f"[DONE] {len(result)} items saved")
if __name__=="__main__": main()
