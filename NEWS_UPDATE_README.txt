衣脉每日资讯修复说明

本次必须上传并保留以下路径：
1. index.html
2. update_news.py
3. data/news.json
4. .github/workflows/daily-update.yml

重要：
- GitHub Actions 只识别 .github/workflows/ 内的 yml 文件。
- 如果仓库根目录有 daily-update.yml，它不会作为工作流运行；可在确认新文件上传后删除根目录的旧文件。
- GitHub 仓库 Settings → Actions → General → Workflow permissions，选择 Read and write permissions。
- 上传后进入 Actions，打开 Daily costume culture RSS update，点击 Run workflow 手动运行一次。
- 运行成功后，data/news.json 会写入采集到的RSS资讯线索；首页会读取该JSON文件。
- RSS来源可能限流、改版或无匹配内容；采集失败会在Actions日志中显示。采集结果都标记为“待编辑核验原文”，不是已审核的学术结论。
- 定时任务 cron 为 UTC 01:20，即北京时间 09:20。
