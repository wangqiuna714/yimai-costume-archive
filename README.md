# 衣脉 · 中西服饰文化数据库｜整合交付版

## 已整合的栏目
- 首页与总导航：`index.html`
- 中国历代服饰：`china-history.html`
- 历代男女服饰：`gender-costume.html`
- 纺织工艺、刺绣、印染、纹样与色彩：`textile-patterns.html`
- 中西名画服饰：`painting-costume.html`
- 中国民族服饰图谱：`ethnic-costume.html`
- 中西影视服饰：`film-costume.html`
- 全球新中式设计案例：`global-new-chinese.html`
- 服饰学者与人物研究：`people-research.html`
- 全球服装设计师：`global-designers.html`
- 五张水墨视觉素材：`assets/`
- RSS资讯线索：`data/news.json`、`update_news.py`
- 每日自动采集工作流：`.github/workflows/daily-update.yml`

## 一次性部署
1. 下载并解压本 ZIP。
2. 打开仓库 https://github.com/wangqiuna714/yimai-costume-archive
3. 点击 Add file → Upload files。
4. 把解压目录里的全部文件和文件夹上传，保留 `.github`、`assets`、`data` 目录结构。
5. 已存在的同名文件选择覆盖，新增文件直接添加。
6. Commit changes。
7. Settings → Pages 保持 Deploy from a branch / main / /(root)。
8. Actions 中确认 Daily costume culture RSS update 工作流出现；可手动运行 workflow_dispatch。

## 重要说明
- RSS自动采集只提供资讯线索，可能因网站调整、限流或RSS不可用而漏采；每条信息都需要人工核验原文、日期和出处。
- 每日专题的日期轮换不等于每天自动生成新的学术研究。
- 水墨图片是网站视觉素材，不代表历史服饰实物。
- 影视剧照、时装秀图片和博物馆藏品图片请从原始机构页面查看版权及授权条件，不要擅自复制公开。
- 民族服饰需注明具体地域、支系、场景和来源，不能把一个款式概括为整个民族。
- 页面文字为学习研究导读，正式论文引用应回到原始学术著作、馆藏档案和论文核验。
