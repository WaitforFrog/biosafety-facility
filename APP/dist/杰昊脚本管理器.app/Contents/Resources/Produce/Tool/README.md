# Tool — 工具函数库

`Produce/` 目录下所有生成脚本的"工具箱"，提供 API 调用、文件处理、HTML 生成、Git 同步等功能。

---

## 目录结构（简洁版）

```
Tool/
├── api_client.py               # OpenAI API 调用封装
├── file_utils.py               # 文件名非法字符清理
├── git_utils.py                # Git 自动提交与推送
├── html_template.py            # HTML 模板与 Markdown→HTML 转换
├── log_utils.py                # 文章生成日志创建
├── product_loader.py           # 产品参数文件加载
├── product_mapping.py          # 42 个产品的中文名→英文文件夹名映射表
├── run_summary.py            # 运行汇总 JSON 日志保存
├── build_articles_index.py    # 为每个产品生成静态文章列表页
├── build_category_indexes.py  # 为引流层生成二级导航 index.html
├── build_preview_site.py     # 将 Markdown 文章转换为 HTML 预览
└── __init__.py
```

---

## 目录结构（通俗版）

### api_client.py — 和 AI 对话

负责调用 AI 接口。把提示词发过去，把 AI 的回答收回来。

```
核心函数：call_api(client, system_prompt, user_prompt, temperature, max_tokens)
使用模型：claude-opus-4-6
返回内容：AI 生成的文字（choices[0].message.content）
```

### file_utils.py — 清理文件名

文件名字里不能有 `\/:*?"<>|` 这些符号。这个工具负责把它们全部删掉，防止文件保存时报错。

```
核心函数：sanitize_filename(name)
输入：任意字符串
输出：清理后的安全文件名
```

### html_template.py — 生成网页

这个工具有两个功能：

1. **生成网页模板**：输出一个完整的 HTML 页面，包含 SEO meta 标签、CSS 样式（响应式设计）、header 导航、footer 版权信息。把 AI 写的文章内容塞进去就是一个完整的网页了。

2. **Markdown 转 HTML**：把 AI 输出的 Markdown 格式文字转成 HTML。支持标题、列表、表格、代码块等。

```
核心函数：
- get_html_template()           # 返回完整 HTML 页面模板
- markdown_to_html(md_text)    # Markdown → HTML 转换
- extract_title_from_markdown(md_text)  # 从 Markdown 提取标题
```

### log_utils.py — 记录生成日志

每生成一篇文章，这个工具会创建一个"生成日志.md"文件，记录：产品名、英文名、文章编号、时间戳、API 返回长度、标题、关键词、输出路径、耗时。

```
核心函数：create_article_log(...)
输出：生成日志.md 文件
```

### product_loader.py — 读取产品参数

从 `Check/` 目录里读取所有产品的参数文件（`.md` 格式）。文件名就是产品名，内容就是参数。

```
核心函数：load_product_parameters(parameters_dir)
输入：Check/ 目录路径
输出：{产品名: 参数内容} 的字典
```

### product_mapping.py — 中英文名对照表

42 个产品的中文名和英文文件夹名的对照表。比如：

| 中文名 | 英文文件夹名 |
|--------|-------------|
| 传递窗 | pass-through-chambers |
| 气密门 | airtight-valves |
| BIBO 传递窗 | bibo-bag-in-bag-out |
| VHP 传递窗 | vhp-pass-through |
| ... | ... |

### run_summary.py — 保存运行汇总

每次运行生成脚本后，把这次运行的整体结果（成功多少篇、失败多少篇、耗时多少）保存成一个 JSON 文件到 `文章/汇总日志/` 目录。

```
核心函数：save_run_summary(results, output_dir)
输出：文章/汇总日志/{时间戳}.json
```

### git_utils.py — 自动同步 Git

文章生成完毕后，自动把变更提交到 Git 仓库并推送到远程。包含 3 次重试 + 指数退避（如果网络不好就等久一点再试）。

```
核心函数：git_commit_and_push(commit_message, build_script_path)
流程：git add -A → git commit → git push
```

### build_articles_index.py — 生成文章列表页

每个产品文件夹里的 `articles/` 目录需要有一个 `index.html`，用来展示该产品下的所有文章列表。

这个脚本遍历 `Website/` 下所有产品的 `articles/` 目录，从每个 `article-*/index.html` 提取 h1 标题和 `datetime` 属性，生成一个可折叠的静态列表页面。

```
输入：Website/{产品}/articles/article-N/index.html（多个）
输出：Website/{产品}/articles/index.html（每个产品一个）
```

### build_category_indexes.py — 生成二级导航页

每个产品的"引流层"目录下需要一个 `index.html`，作为该产品的二级导航页面。

这个脚本遍历 `Website/` 中所有 `*/引流层/` 目录，找出子目录中的 `*_EN.html` 文件，生成暗色系风格的二级导航 `index.html`。

```
输入：文章/{产品}/引流层/*_EN.md（多个）
输出：Website/{产品}/引流层/index.html
```

### build_preview_site.py — 生成预览网站

把 `文章/` 目录下的所有 Markdown 文章转换成 HTML 输出到 `Website/` 目录。用于在正式发布前预览文章效果。

```
输入：文章/ 目录下的所有 *_EN.md 文件
输出：Website/ 目录下对应的 HTML 文件
```

---

## 模块关系图

```
Compare_EN_html.py / Trust_EN_html.py（主脚本）
         │
         ├──→ api_client.py（调用 AI）
         ├──→ product_loader.py（读取产品参数）
         ├──→ product_mapping.py（中文→英文映射）
         ├──→ html_template.py（生成网页）
         ├──→ log_utils.py（记录日志）
         │         │
         │         └──→ run_summary.py（保存运行汇总）
         │
         ├──→ file_utils.py（清理文件名）
         │
         └──→ git_utils.py（Git 同步）
                   │
                   └──→ build_articles_index.py（重建文章索引）

build_category_indexes.py（独立运行）
         │
         └──→ 遍历 Website/ → 生成引流层导航页

build_preview_site.py（独立运行）
         │
         └──→ 遍历 文章/ → 生成 HTML 预览
```
