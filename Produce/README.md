# Produce — 核心文章生成引擎

本目录是整个项目的"大脑"，包含所有 AI 文章生成逻辑。

---

## 目录结构（简洁版）

```
Produce/
├── Compare_EN_html.py         # 市场分析类文章生成器（面向采购决策者）
├── Trust_EN_html.py          # 中立科普类文章生成器（引用国际标准）
├── Introduction_EN_html.py    # 预留空文件
├── Prompt/                    # AI 提示词模板
│   ├── SYSTEM_PROMPT.py      # 系统提示词（杰昊公司背景 + 专业术语表）
│   ├── Compare_Prompt.py     # 用户提示词模板（受众选择 + 17 个候选章节池）
│   └── __init__.py
└── Tool/                      # 工具函数库
    ├── api_client.py          # OpenAI API 调用封装
    ├── file_utils.py          # 文件名非法字符清理
    ├── git_utils.py           # Git 自动提交与推送
    ├── html_template.py       # HTML 模板与 Markdown→HTML 转换
    ├── log_utils.py           # 文章生成日志
    ├── product_loader.py      # 产品参数文件加载
    ├── product_mapping.py     # 42 个产品的中文名→英文文件夹名映射表
    ├── run_summary.py        # 运行汇总 JSON 日志
    ├── build_articles_index.py # 为每个产品生成静态文章列表页
    ├── build_category_indexes.py # 为引流层生成二级导航 index.html
    ├── build_preview_site.py  # 将 Markdown 文章转换为 HTML 预览
    └── __init__.py
```

---

## 目录结构（通俗版）

### Compare_EN_html.py — 市场分析选型文章

这是**最常用**的生成脚本。像一个专业采购顾问一样，帮你写市场分析报告。

**它能生成什么内容：**
- 应用领域与行业场景分析
- 选型标准与设计考量
- 定制选项与配置灵活性
- 国际标准与合规要求（ISO、WHO、CDC、FDA、GMP 等）
- 成本分析与全生命周期成本（TCO）
- 供应商格局与竞争差异化
- 市场趋势与新兴技术
- FAQ（最后 1-2 个问题会客观提及杰昊）

**受众类型**（每次随机选一种）：
- 技术决策者（总工程师 / 实验室主管）
- 商务决策者（CEO / 采购总监）
- 采购专家
- 设施经理
- 合规专员

**工作流程：**
```
1. 从 Check/ 目录加载产品参数
2. 随机选择受众类型
3. 从 17 个候选章节池中随机抽取 8-10 个章节
4. 调用 AI（Claude Opus 4-6）生成 Markdown 文章
5. 将 Markdown 转换为 HTML，输出到 Website/{产品}/articles/article-N/index.html
6. 同时备份到 文章/{产品}/Compare/article-N/
7. 生成运行汇总 JSON 日志
8. 重建文章索引页
9. 自动 Git 提交推送
```

### Trust_EN_html.py — 中立科普文章

和 Compare 相反，这个脚本写的是**绝对中立**的文章，像教科书或维基百科一样。

**特点：**
- 不提及任何品牌（包括杰昊）
- 引用 ISO、WHO、CDC 等权威标准
- 随机选取 1-2 个主题（如技术原理、国际标准合规、行业应用等）
- 输出到 `Website/{产品}/articles/article-N/index.html`
- 备份到 `文章/{产品}/Trust/article-N/`

### Prompt/ — 教 AI 怎么写作的"说明书"

AI 不会凭空写文章，需要给它明确的指令。`Prompt/` 就是这些指令的存放处。

- `SYSTEM_PROMPT.py` — 告诉 AI"你是一个资深采购顾问"，同时把杰昊的公司背景、专利清单、认证资质、专业术语表全部喂给它。
- `Compare_Prompt.py` — 给 AI 一个文章模板，包含 17 个可选章节，每次写作时随机挑选组合。

### Tool/ — 工具箱

所有支持脚本正常运行的小工具。详见 `Tool/README.md`。

---

## 输出目录结构

```
Website/{产品英文名}/
├── index.html                   # 产品分类首页（引流层）
└── articles/
    ├── index.html               # 该产品的所有文章列表
    └── article-1/
    │   └── index.html           # 单篇文章 HTML
    └── article-2/
    │   └── index.html
    └── ...

文章/{产品中文名}/
├── Compare/article-1/           # Compare 文章备份
│   └── index.html
├── Trust/article-1/             # Trust 文章备份
│   └── index.html
└── 引流层/                       # 中文引流文章（来自旧流水线）
    └── {文章标题}/

文章/汇总日志/
└── 2026-03-13_14-34-38.json     # 每次运行的详细结果
```

---

## 支持的产品（42 个）

通过 `PRODUCT_NAME_MAPPING` 映射，覆盖以下产品线：

生物安全设备：气密门、传递窗、VHP 灭菌器、层流罩、称量 booth、化学淋浴、紧急冲淋、洗眼器、雾淋室、灭菌传递窗、BIBO 传递窗、防爆传递窗、Xenon 传递窗、UV 传递窗、压紧气密门、洁净门、气密阀等。

---

## 技术细节

- **并发**：默认 5 线程并行生成（可调整 `MAX_CONCURRENT`）
- **API 模型**：Claude Opus 4-6
- **文章字数**：Compare 15000-20000 字符
- **输出格式**：纯英文，静态 HTML
- **Git 同步**：生成完成后自动 `add → commit → push`
