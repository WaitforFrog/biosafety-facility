# Produce/ — 文章生成引擎

这是整个项目的"大脑"，负责让 AI 自动帮你写文章。

---

## 直接可运行的脚本

| 脚本 | 干嘛的 |
|------|--------|
| `Compare_JIEHAO.py` | 生成市场分析选型文章。像采购顾问一样帮客户对比产品，FAQ 里会提到杰昊 |
| `Compare_Neutral.py` | 生成中立的市场分析文章。不带任何品牌倾向 |
| `Question_JIEHAO.py` | 生成问答类文章，以杰昊视角回答常见问题 |
| `Question_Neutral.py` | 生成中立问答文章，不提及任何品牌 |
| `Regulatory_JIEHAO.py` | 生成合规标准类文章，以杰昊视角解读法规 |
| `Regulatory_Neutral.py` | 生成中立合规标准文章，引用国际标准 |
| `Installation_JIEHAO.py` | 生成安装调试类文章，以杰昊视角 |
| `Installation_Neutral.py` | 生成中立安装调试文章 |
| `Trust_EN_html.py` | 生成中立科普文章，像教科书一样介绍技术原理 |
| `Introduction_EN_html.py` | 生成产品介绍文章 |

---

## 子文件夹

### Prompt/
提示词模板文件夹。"教" AI 怎么写文章的说明书。

- `*_System_Prompt.py` — 系统提示词，告诉 AI 扮演什么角色（比如"你是杰昊公司的采购顾问"）
- `*_User_Prompt.py` — 用户提示词，告诉 AI 具体要写什么内容
- `*_JIEHAO_System_Prompt.py` — 杰昊视角的系统提示词
- `*_Neutral_System_Prompt.py` — 中立视角的系统提示词

### Tool/
工具箱，里面是一堆辅助函数。

| 文件 | 干嘛的 |
|------|--------|
| `api_client.py` | 和 AI（Claude）对话的封装 |
| `html_template.py` | 把 Markdown 转成带样式的 HTML 网页 |
| `git_utils.py` | 文章生成完后自动提交到 Git |
| `product_loader.py` | 读取产品参数文件 |
| `product_mapping.py` | 产品中文名→英文文件夹名的对照表 |
| `file_utils.py` | 文件名清理（去掉非法字符） |
| `run_summary.py` | 生成运行汇总 JSON 日志 |
| `build_articles_index.py` | 生成文章列表页面 |
| `build_category_indexes.py` | 生成分类索引页面 |
| `build_preview_site.py` | 生成网站预览 |
| `log_utils.py` | 日志工具 |

### *Content/ 文件夹们
存放各种文章内容素材的文件夹。

| 文件夹 | 内容 |
|--------|------|
| `Compare_Content/` | 市场分析类文章素材 |
| `Question_Content/` | 问答类文章素材 |
| `Regulatory_Content/` | 合规标准类文章素材 |
| `Installation_Content/` | 安装调试类文章素材 |

每个文件夹里有多个子文件夹，代表不同的角色视角（比如 CEO、CTO、QA合规官等），里面放着具体的 markdown 素材文件。

### 备份/
旧版本脚本的备份，不影响正常运行。

---

## 怎么运行

方式一：用应用程序（推荐）
1. 打开 `杰昊脚本管理器.app`
2. 勾选想要的脚本
3. 点运行

方式二：命令行直接跑
```bash
cd /path/to/Code
python Produce/Compare_JIEHAO.py
```

---

## 输出到哪

生成的文章会放到：
- `Website/` — 网站文章（最终要部署的）
- `文章/` — 备份文章

每个产品一个文件夹，里面是多篇文章。
