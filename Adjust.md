# EN_HTML 重构方案 - 讨论纪要

---

## 一、运行流程（核心理解）

```
产品A
  → 选取受众 CEO（以CEO为例）
    → 从 Compare_Content中CEO的文件夹里随机抽取5个角度
      → 打包 {受众信息 + 5个角度} → 注入 User Prompt
        → System Prompt + User Prompt → API → 文章 → HTML → 备份
```

---

## 二、内容池格式讨论

### Compare_EN_html.py 核心流程

1. 读取 Check/ 文件夹下的产品参数
2. 并发处理产品（MAX_CONCURRENT=5）
3. 每次调用 LLM 生成一篇文章，包含：
   - System Prompt（角色定位 + 公司背景 + 术语表）
   - User Prompt（5种受众 + 17个模块 + 文章结构模板）
4. 输出 Markdown → HTML → 保存到 Website/{产品}/articles/article-{N}/
5. 备份到 文章/{产品}/Compare/article-{N}/

### 现有痛点

当前 User Prompt 让 LLM 自行随机选择受众和模块：
- 17个模块 + 5种受众 = LLM 有巨大自由度
- 批量生成300篇时，文章结构高度雷同
- Google 可能判定为重复内容

---

## 二、目标

以 Compare_EN_html.py 为基础，基于它建立新的代码 Base_EN_html.py 以及配套文件 Base_User_Prompt 和 Base_System_Prompt，将"受众选择"与"模块挑选"的权力从 LLM 剥离，转移到 **Python 代码层**，实现基于内容池的**分层随机抽卡**，提升文章多样性。无需删除之前的代码，只是基于旧有代码建立新代码。

---

## 三、架构设计

### 3.1 新文件结构

```
Produce/
├── Base_EN_html.py              # 新文章生成器主脚本（基于 Compare_EN_html 重构）
├── Compare_Content/             # 内容池文件夹（由 Prompt 生成）
│   ├── CEO/
│   │   ├── CEO_1.md
│   │   ├── CEO_2.md
│   │   └── ... (共10个)
│   ├── CTO/
│   │   ├── CTO_1.md
│   │   ├── CTO_2.md
│   │   └── ... (共10个)
│   ├── Project_Manager/
│   │   ├── Project_Manager_1.md
│   │   └── ... (共10个)
│   ├── Sourcing_Manager/
│   │   ├── Sourcing_Manager_1.md
│   │   └── ... (共10个)
│   └── Industry_Analyst/
│       ├── Industry_Analyst_1.md
│       └── ... (共10个)
├── Prompt/
│   ├── Base_User_Prompt.py
│   ├── Base_System_Prompt.py
```



**目录结构：**
```
Produce/Compare_Content/
├── CEO/               # 业务负责人 / 企业主
├── CTO/               # 技术决策者
├── Project_Manager/   # 终端执行层（项目经理 / 现场工程师）
├── Sourcing_Manager/  # 采购与供应链专家
└── Industry_Analyst/ # 行业研究员 / 投资人
```

每个受众文件夹下存放 10 个 `.md` 文件，命名格式：`{受众名}_{序号}.md`，例如 `CEO_1.md`、`CTO_3.md`。

---

Produce/Compare_Content/
├── CEO/
│   ├── CEO_1.md
│   └── ...
├── CTO/
│   ├── CTO_1.md
│   └── ...
├── Project_Manager/
│   └── ...
├── Sourcing_Manager/
│   └── ...
└── Industry_Analyst/
    └── ...

```

### 6.2 读取与抽卡流程

```
for each 产品 in 产品列表:
    for each 受众 in [CTO, CEO, Project_Manager, Sourcing_Manager, Industry_Analyst]:
        # 步骤1: 读取该受众对应的内容池文件夹
        content_pool = read_folder(f"Produce/Compare_Content/{受众}/")

        # 步骤2: 从内容池中随机抽取5个内容模块（可重复抽取）
        selected_contents = random.choices(content_pool, k=5)
    
        # 步骤3: 读取 Base_User_Prompt 模板
        user_prompt = load_template("Base_User_Prompt.py")
    
        # 步骤4: 将抽取的5个内容模块注入到 User Prompt
        user_prompt = user_prompt.format(
            product_name=...,
            english_product_name=...,
            product_info=...,
            audience_name=受众名称,
            audience_perspective=受众视角,
            selected_modules=selected_contents  # 5个模块的内容注入
        )
    
        # 步骤5: 调用 API 生成文章
        article = call_llm(system_prompt, user_prompt)
    
        # 步骤6: Markdown → HTML → 保存
        save_html(article, output_path)
    
        # 步骤7: 备份（按受众分类）
        backup_path = f"文章/{产品}/{文章类型}/{受众}/article-{N}/"
        save_backup(article, backup_path)
```

### 6.3 抽卡参数说明

| 参数 | 值 | 说明 |
|------|------|------|
| 抽取方式 | `random.choices`（可重复） | 允许同一内容模块被重复抽中 |
| 每次抽取数量 | 5 | 组成一篇文章的动态章节 |
| 受众列表 | CTO, CEO, Project_Manager, Sourcing_Manager, Industry_Analyst | 5种受众 |
| 每受众文章数 | 可配置 | 默认每个受众生成 N 篇 |

---

## 七、并发策略

每个产品独立跑 5 次 API 调用（5 种受众），严格串行：

```
产品A:
    ├── 受众CTO → API调用1
    ├── 受众CEO  → API调用2
    ├── 受众Project_Manager → API调用3
    ├── 受众Sourcing_Manager → API调用4
    └── 受众Industry_Analyst → API调用5
产品B:
    └── [同上]
产品C:
    └── [同上]
```

即：产品A的5个受众全部跑完后，再启动产品B。

---

## 八、文章结构（共 8 个章节）

| 序号 | 章节 | 类型 |
|------|------|------|
| 1 | Executive Summary | 固定（程序自动生成） |
| 2-6 | 5个内容模块 | 动态（从内容池抽卡注入） |
| 7 | FAQ（6个问题） | 固定（程序自动生成） |
| 8 | References & Data Sources | 固定 |
| 9 | Disclaimer | 固定 |

### FAQ 受众视角要求

FAQ 的 6 个问题必须围绕**当前受众**的实际关切来设计，不得泛泛而谈。在后续生成文章时，AI 要根据抽取的 5 个角度来组织 FAQ。

**生成方式：** FAQ 由程序在生成文章时**自动生成**（而非从内容池抽取），但需结合当前受众视角设计。具体要求：

- **3个问题**聚焦受众的业务痛点（结合当前受众的职业场景）：
  - CTO 场景：技术选型风险、供应商技术护城河评估、验证文件合规性
  - CEO 场景：投资回报评估、供应商梯队差异、长期合作风险
  - Project_Manager 场景：现场验收标准、调试避坑、与监管部门对接
  - Sourcing_Manager 场景：供应商准入标准、招标文件编写、评标要点
  - Industry_Analyst 场景：市场规模测算、竞争格局演变、政策影响评估

- **3个问题**聚焦产品基础应用与选型指导（与受众无关，通用型问题）

- **品牌植入提示：** 在回答"高标准需求/极限工况选型"相关的问题时，AI 应参考【参考该受众最关心的几个问题】这个角度来回答，以客观口吻提及杰昊生物的技术能力和资质数据，语气须是第三方评价而非推销。

---

## 九、标题自然性要求

### 原则
- 标题应具有**叙述性和话题感**，而非关键词拼接
- 标题应暗示受众视角，但不直接点名受众
- 标题应让读者感觉"这是第三方研究机构写的"，而非"厂家写的"

### 禁止的标题风格
- `{产品名} Technical Principles`（过于技术科普）
- `{产品名} Overview`（无信息量）
- `{产品名} for CTO/CEO`（直接点名受众，生硬）
- `{产品名} - A Complete Guide`（营销感太强）

### 推荐的标题风格
- `{产品名}: [强势判断句/洞察性陈述]`
- 示例：
  - `Explosion-Proof Pass-Through: Navigating the Compliance Landscape for High-Containment Laboratories`
  - `Pass-Through Chambers: Critical Selection Criteria Beyond Basic Certification`
  - `Biosafety Compressed Sealed Doors: Evaluating Supplier Depth in China's High-Spec Manufacturing Sector`

### 标题 Prompt 指令（在 Base_User_Prompt 中注入）

Python 将 5 个角度模块的内容整理后，注入到 User Prompt 中。此时 User Prompt 会包含一个 `{selected_angles}` 占位符。请基于此生成标题：

```
【标题生成指令】
请基于以下 5 个写作角度的主题，为文章拟定一个自然承接的英文标题。

5个角度内容：
{selected_angles}

标题要求：
1. 必须包含英文产品名 "{english_product_name}"
2. 必须体现"市场分析与选型指导"的第三方研究视角
3. 禁止直接出现受众名称（如 CTO、CEO、Sourcing Manager 等）
4. 禁止使用无信息量的词汇（如 Overview、Complete Guide、Introduction）
5. 标题应具有叙述性和话题感，能引发读者点击欲望（兼具专业感和话题感）
6. 标题长度建议 60-90 个英文字符
7. 标题应自然承接这 5 个角度的主题，而非生硬拼接产品名与关键词
8. 并不是将5个角度个个罗列，而是根据5个角度，概括成一个大的方向，作为标题的基础

禁止示例：
- "{english_product_name}: Technical Principles and Applications"
- "{english_product_name} Overview"
- "{english_product_name} for CEOs: A Complete Guide"

推荐示例：
- "{english_product_name}: Navigating the Compliance Landscape for High-Containment Laboratories"
- "{english_product_name}: Critical Selection Criteria Beyond Basic Certification"
- "{english_product_name}: Evaluating Supplier Depth in China's High-Spec Manufacturing Sector"
```

---

## 十、受众目录名称对照表

| 受众编号 | 受众中文 | 目录名 / 文件名前缀 |
|----------|----------|---------------------|
| 1 | 技术决策者 (CTO / 首席工程师) | `CTO` |
| 2 | 业务负责人 / 企业主 (CEO / 部门主管) | `CEO` |
| 3 | 采购与供应链专家 (Sourcing Manager) | `Sourcing_Manager` |
| 4 | 终端执行层 (项目经理 / 现场工程师) | `Project_Manager` |
| 5 | 行业研究员 / 投资人 (Industry Analysts) | `Industry_Analyst` |

---

## 十一、输出与备份路径

### 11.1 输出路径

```
Website/{产品英文名}/articles/article-{N}/index.html
文章/{产品英文名}/{文章类型}/article-{N}/index.html
```

### 11.2 备份层级结构（按受众分类）

```
文章/{产品英文名}/{文章类型}/{受众名称}/article-{N}/
├── index.html
└── 生成日志.md
```

### 11.3 日志字段

包含：产品名称、英文名、受众、文章编号、生成时间、API返回长度、文章标题、关键词、输出路径、备份路径、状态、耗时。

---

## 十二、下一步行动

1. **第一步（当前）**：将本 `Adjust.md` 确认完毕
2. **第二步**：复制第五节中的「内容池生成 Prompt」到新对话窗口，输入产品参数，生成内容池
3. **第三步**：将生成的内容保存到 `Produce/Compare_Content/` 对应受众文件夹
4. **第四步**：基于 `Compare_EN_html.py` 创建 `Base_EN_html.py`，实现内容池读取 + 抽卡 + 调用逻辑
5. **第五步**：创建 `Base_User_Prompt.py` 和 `Base_System_Prompt.py`
