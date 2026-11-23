import json, os, re
from datetime import datetime, timezone, timedelta
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

QUERIES = [
    '中国传统服饰 OR 汉服 OR 传统纺织工艺',
    '民族服饰 OR 非遗服饰 OR 传统刺绣',
    '新中式 时装 OR Chinese fashion design',
    'fashion history museum exhibition costume collection',
    'costume history textile museum fashion exhibition'
]

def clean(s):
    return re.sub(r'\\s+', ' ', s or '').strip()

items=[]
for query in QUERIES:
    url='https://news.google.com/rss/search?q='+__import__('urllib.parse').parse.quote(query)+'&hl=zh-CN&gl=CN&ceid=CN:zh-Hans'
    try:
        req=Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; YimaiArchive/1.0)'})
        root=ET.fromstring(urlopen(req,timeout=20).read())
        for node in root.findall('.//item')[:8]:
            title=clean(node.findtext('title'))
            link=clean(node.findtext('link'))
            pub=clean(node.findtext('pubDate'))
            source=clean(node.findtext('source')) or '公开资讯'
            if title and link and not any(x['link']==link for x in items):
                items.append({'title':title,'link':link,'date':pub,'source':source,'summary':'请打开原文核验报道时间、事实与图片版权。'})
    except Exception as e:
        print('Feed fetch failed:', query, str(e))
items=items[:30]
os.makedirs('data',exist_ok=True)
with open('data/news.json','w',encoding='utf-8') as f:
    json.dump(items,f,ensure_ascii=False,indent=2)
print('Saved',len(items),'news items')
