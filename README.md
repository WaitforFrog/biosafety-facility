# 生物安全实验室设备独立站 - AI 内容工厂

本项目是一套**自动化 SEO 内容生成系统**，用于批量生产生物安全实验室、洁净室设备领域的专业采购指南文章。

---

## 目录结构

```
Code/
├── Introduction.py              # AI 文章生成器（核心）
├── Translate.py                # 英文化与归档工具
├── build_category_indexes.py   # 分类索引构建脚本
├── build_preview_site.py       # 预览站点构建脚本
├── Website/                     # 主站静态页面（35+ 产品分类）
├── preview_site/                # 预览站点（用于预览生成的文章）
├── 参数/                         # 产品参数数据（Markdown 格式）
├── 独立站矩阵搭建步骤说明.md      # 项目搭建流程说明
├── .venv/                       # Python 虚拟环境
└── .git/                        # Git 版本控制
```

---

## 核心脚本

### 1. Introduction.py

**用途**：AI 文章生成器（核心脚本）

**功能**：
- 读取 `参数/` 文件夹下的产品参数文件
- 调用 AI 生成 3 个不同视角的选题：
  - 宏观盘点向（行业选型指南、厂家盘点）
  - ROI 避坑向（成本对比、全生命周期分析）
  - 极端场景向（高压差、VHP 灭菌等严苛工况）
- 根据选题自动撰写中文营销文章
- 保存到 `文章/{产品名}/引流层/` 目录

**输出**：`文章/` 目录下的中文 Markdown 文章

---

### 2. Translate.py

**用途**：英文化与归档工具

**功能**：
- 扫描 `文章/` 目录下的中文文章
- 调用 AI 进行工程级专业翻译（保留 Markdown 格式）
- 自动创建专属文件夹归档：
  - 中文版：`原文件名.md`
  - 英文版：`原文件名_EN.md`

**特点**：
- 使用国际标准术语（ISO、GMP、FDA、WHO）
- 优化 SEO 关键词（BSL-3、VHP、Pressure Decay Test 等）
- 避免中式英语，注重工程专业表达

---

### 3. build_category_indexes.py

**用途**：分类索引构建脚本

**功能**：
- 读取 `文章/` 目录下的所有生成文章
- 自动生成各产品分类的索引页面（HTML）
- 输出到 `Website/` 对应分类的 `articles/` 目录

---

### 4. build_preview_site.py

**用途**：预览站点构建脚本

**功能**：
- 将生成的文章转换为可预览的 HTML 页面
- 输出到 `preview_site/` 目录
- 用于在正式发布前预览文章效果

---

## 数据目录

### 参数/

存放各产品的技术参数文档（Markdown 格式），作为 AI 生成文章的参考资料。

**文件示例**：
- `不锈钢密闭门.md`
- `VHP 传递窗.md`
- `强制淋浴.md`
- ...（按产品分类）

每个文件包含产品的技术规格、材料特性、工作原理等信息。

---

### 文章/

由 `Introduction.py` 生成的原创文章存放目录。

**结构**：
```
文章/
└── {产品名}/
    └── 引流层/
        ├── {文章标题1}/
        │   ├── {文章标题1}.md        # 中文版
        │   └── {文章标题1}_EN.md    # 英文版
        └── {文章标题2}/
            └── ...
```

---

### Website/

**主站静态页面**，已部署上线的生产环境网站。

**结构**：
```
Website/
├── index.html                    # 首页
├── {产品分类}/
│   ├── index.html                # 分类首页（引流层）
│   └── articles/
│       ├── index.html            # 文章索引
│       └── article-N/
│           └── index.html        # 具体文章页
```

涵盖 35+ 产品分类：
- 不锈钢气密门、洁净门
- VHP 传递窗、BIBO 传递窗
- 化学淋浴、强制淋浴
- 洗眼器、雾淋室
- 层流罩、称量罩
- ... 等

---

### preview_site/

**预览站点**，用于在正式发布前预览生成的 HTML 文章效果。

---

## 完整工作流水线

```
1. 准备参数
   └── 参数/*.md（产品技术资料）

2. 生成文章
   └── Introduction.py → 文章/*/引流层/*.md（中文）

3. 翻译归档
   └── Translate.py → 文章/*/引流层/*/*.md（中英文双版）

4. 构建索引
   └── build_category_indexes.py → Website/*/articles/index.html

5. 预览效果
   └── build_preview_site.py → preview_site/

6. 发布上线
   └── 上传 Website/ 到服务器
```

---

## 技术栈

- **语言**：Python 3.x
- **AI 引擎**：OpenAI API（通过中转站）
- **模型**：Claude Opus 4-6
- **前端**：纯静态 HTML（无框架）
- **部署**：静态网站托管

---

## 快速开始

### 1. 激活虚拟环境

```bash
cd /Users/guot/Desktop/杰昊/AI推广/域名推广/Code
source .venv/bin/activate
```

### 2. 运行文章生成

```bash
python Introduction.py
```

### 3. 运行翻译归档

```bash
python Translate.py
```

---

## 配置说明

如需修改 API 配置，请在各脚本开头的**配置区**调整：

```python
API_KEY = "your-api-key"
BASE_URL = "https://your-proxy-url.com/v1"
```

---

## 注意事项

1. **API 费用**：AI 调用会产生 Token 费用，请关注使用量
2. **内容审核**：生成的文章建议人工审核后再发布
3. **SEO 效果**：文章按标准 SEO 规范撰写，侧重 AI 搜索引擎优化（AIO/GEO）
4. **品牌合规**：文章中禁止出现具体品牌名称（除杰昊外），需保持客观中立

---

## 相关文档

- `独立站矩阵搭建步骤说明.md` - 项目整体搭建流程详解
