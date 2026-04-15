# 生物安全实验室设备独立站 - AI 内容工厂

本项目是一套**自动化 SEO 内容生成系统**，用于批量生产生物安全实验室及洁净室设备领域的专业采购指南文章。

**最新版本**：v2.0 - 多维度内容生成引擎

---

## 目录结构（简洁版）

```
Code/
├── APP/                              # 三种脚本启动器：tkinter GUI、AppleScript、Electron 桌面应用
├── Produce/                          # 核心文章生成引擎
│   ├── Compare_EN_html.py            # 市场分析类文章生成器（英文，面向采购决策者）
│   ├── Trust_EN_html.py             # 中立科普类文章生成器（英文，引用国际标准）
│   ├── Introduction_EN_html.py       # 预留空文件
│   ├── Prompt/                      # AI 提示词模板
│   │   ├── SYSTEM_PROMPT.py         # 系统提示词（杰昊公司背景 + 专业术语表）
│   │   └── Compare_Prompt.py        # 用户提示词模板（受众选择 + 17 个候选章节池）
│   └── Tool/                        # 工具函数库
│       ├── api_client.py            # OpenAI API 调用封装
│       ├── file_utils.py            # 文件名非法字符清理
│       ├── git_utils.py             # Git 自动提交与推送
│       ├── html_template.py         # HTML 模板与 Markdown→HTML 转换
│       ├── log_utils.py             # 文章生成日志
│       ├── product_loader.py        # 产品参数文件加载
│       ├── product_mapping.py       # 42 个产品的中文名→英文文件夹名映射表
│       ├── run_summary.py           # 运行汇总 JSON 日志
│       ├── build_articles_index.py  # 为每个产品生成静态文章列表页
│       ├── build_category_indexes.py # 为引流层生成二级导航 index.html
│       └── build_preview_site.py    # 将 Markdown 文章转换为 HTML 预览
├── Title/                            # 35 个产品的英文标题文本文件
├── Website/                          # 生成的静态网站（35 个产品，每个含多篇文章）
├── 文章/                              # 备份文章与运行汇总日志
├── 备份/                              # 备份文件
├── docs/                              # 项目文档
├── Compare.md                         # Compare 模块说明文档
├── School.md                          # 学校相关文档
└── README.md                          # 本文件
```

---

## 目录结构（通俗版）

### APP/ — 三种方式启动脚本

当你想要生成文章时，你需要先"启动"生成脚本。`APP/` 提供了三种不同的启动方式：

| 方式 | 文件 | 说明 |
|------|------|------|
| 图形界面 | `run_app.py` | 用 tkinter 做的窗口程序，左边选脚本，右边看历史记录，点按钮就能跑 |
| Mac 原生弹窗 | `script_manager_app.py` | 用 macOS 自带对话框交互（苹果风格的弹出窗口） |
| 桌面应用 | `script-runner-app/` | Electron 构建的独立桌面应用，功能和 GUI 版类似 |

里面还有 4 个 `.command` 文件（双击直接运行的脚本），分别对应：一键运行 Trust 文章生成、一键运行脚本管理器、一键构建脚本运行器 app、一键构建管理器 app。

### Produce/ — 文章生成的核心工厂

这是整个项目的"大脑"。`Produce/` 负责用 AI 生成所有文章。

**直接运行的脚本：**
- `Trust_EN_html.py` — 生成**中立科普文章**，像写教科书一样介绍技术原理、国际标准合规等，不带任何品牌倾向。
- `Compare_EN_html.py` — 生成**市场分析选型文章**，像专业采购顾问一样帮客户对比选型，会引用杰昊的案例和参数。

**Prompt/ — 教 AI 怎么写文章的"说明书"：**
- `SYSTEM_PROMPT.py` — 告诉 AI"你是杰昊公司的采购顾问"，把公司背景、专利、认证、术语表都喂给它。
- `Compare_Prompt.py` — 给 AI 一个写作提纲模板，包含 17 个可选章节（如 TCO 分析、供应商对比、技术选型标准等），每次随机挑选组合。

**Tool/ — 工具箱，里面是一堆辅助函数：**
- `api_client.py` — 负责和 AI（Claude Opus 4-6）对话。
- `html_template.py` — 把 AI 写的 Markdown 文字转成带 CSS 样式的网页。
- `git_utils.py` — 文章生成完后自动提交到 Git 仓库。
- `product_mapping.py` — 42 个产品的中文名和英文文件夹名的对照表（比如"传递窗"→"pass-through-chambers"）。
- `build_articles_index.py` / `build_category_indexes.py` — 生成文章列表页面，让网站有导航。
- `build_preview_site.py` — 把 Markdown 文章转成 HTML 预览文件。

### Title/ — 产品英文名标题库

35 个 `.txt` 文件，每个文件对应一个产品的英文文件夹名（用于 SEO 友好的 URL）。

### Website/ — 生成的网站（最终输出）

每个产品一个文件夹，里面是静态 HTML 文章页面。这就是最终要部署到服务器上的网站内容。

### 文章/ — 备份目录

所有生成的文章都会在这里留一份备份，包括中文版和英文版。`汇总日志/` 子目录里记录每次运行的详细结果（JSON 格式）。

### 备份/ — 旧版脚本备份

历史版本的脚本备份，以防需要回退。

### docs/ — 项目文档

存放一些项目相关的技术方案文档。

---

## 完整工作流水线

### 流水线 A：市场分析类英文文章

```
1. 参数准备
   └── Check/*.md（产品技术参数）

2. AI 生成
   └── Produce/Compare_EN_html.py → Website/*/articles/article-N/index.html

3. 备份文章
   └── 同时保存到 文章/*/Compare/article-N/

4. 生成汇总日志
   └── Produce/Tool/run_summary.py → 文章/汇总日志/*.json

5. 重建文章索引
   └── Produce/Tool/build_articles_index.py → Website/*/articles/index.html

6. Git 自动同步
   └── Produce/Tool/git_utils.py → git add → commit → push
```

### 流水线 B：中立科普类英文文章

```
1. 参数准备
   └── Check/*.md（产品技术参数）

2. AI 生成
   └── Produce/Trust_EN_html.py → Website/*/articles/article-N/index.html

3. 备份文章
   └── 同时保存到 文章/*/Trust/article-N/

4-6. 同流水线 A 步骤 4-6
```

---

## 技术栈

- **语言**：Python 3.x
- **AI 引擎**：OpenAI API（中转站）
- **模型**：Claude Opus 4-6
- **前端**：纯静态 HTML（无框架）
- **Markdown 处理**：Python-Markdown 库
- **并发处理**：ThreadPoolExecutor（默认 5 线程）
- **桌面应用**：Electron + tkinter + AppleScript
- **部署**：静态网站托管
- **版本控制**：Git 自动同步

---

## 快速开始

### 方式一：图形界面（推荐新手）

```bash
python APP/run_app.py
```

### 方式二：命令行直接运行

```bash
# 生成市场分析类文章
python Produce/Compare_EN_html.py

# 生成中立科普类文章
python Produce/Trust_EN_html.py
```

### 方式三：Mac 原生弹窗

```bash
python APP/script_manager_app.py
```

---

## 配置说明

API 配置在各脚本开头的**配置区**调整：

```python
API_KEY = "your-api-key"
BASE_URL = "https://your-proxy-url.com/v1"
```

---

## 注意事项

1. **API 费用**：AI 调用会产生 Token 费用，请关注使用量
2. **内容审核**：生成的文章建议人工审核后再发布
3. **并发控制**：`Compare_EN_html.py` 和 `Trust_EN_html.py` 支持并发（默认 5 线程），可根据 API 限制调整 `MAX_CONCURRENT`
4. **数据源**：`Check/` 目录下的参数文件为文章生成提供产品数据
5. **品牌合规**：Trust 文章保持绝对中立；Compare 文章 FAQ 部分在最后 1-2 个问题中客观提及杰昊（通过特定句式触发）
6. **Git 自动同步**：文章生成完成后会自动提交到 Git 仓库，请确保已配置远程仓库
