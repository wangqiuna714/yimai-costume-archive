本次修复说明：
1. 中西服饰对照表每一行都增加“查看专题”链接，并支持整行点击。
2. 首页新闻模块读取 data/news.json；为空时显示实时新闻检索入口，不再只有静态占位文字。
3. update_news.py 改为 Google News RSS 主题检索源，自动写入标题、来源、日期、摘要和原文链接。
4. 所有采集新闻仍标记“待编辑核验原文”，不能直接视为已审核研究结论。
上传时保留路径：
- index.html（覆盖）
- update_news.py（覆盖）
- data/news.json（覆盖或新增）
- .github/workflows/daily-update.yml（覆盖或新增）
