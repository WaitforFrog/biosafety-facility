

# Base 模块 User Prompt 调整方案（完整版）

> 作者：AI | 日期：2026-04-15
> 状态：待确认后修改代码
> 目标：解决"模块塞入后生硬"的问题，让 AI 既能自由发挥又不会跑偏

---

## 一、现状问题

当前 `Base_User_Prompt.py` 的结构顺序：

```
1. 产品基础信息
2. 目标受众
3. 5个写作角度（预抽样的模块）
4. 文章结构要求（## 1-9，含占位符 ## 2-6）
5. 标题生成指令（底部）
6. 写作准则
```

**核心问题**：5个模块被直接塞进结构要求里，AI 没有机会先去"理解这5个模块之间的关系"，就直接被要求写内容。这导致：
- AI 可能会把5个模块当作独立的知识点逐一列举，而不是串成一条流畅的故事线
- Section 2-6 的占位符缺少足够指引，AI 自由发挥空间太大，容易跑偏
- 标题是在所有内容写完之后才生成的，标题和内容之间缺乏互相校验

---

## 二、修改后的新流程

```
抽到5个模块 + 产品信息 + 受众定位
    ↓
【新增】AI分析5个模块内在联系 → 输出文章逻辑大纲（内部文档，不出现在最终文章）
    ↓
基于逻辑大纲生成标题
    ↓
基于逻辑大纲重写 Section 2-6 的小标题
    ↓
写完整文章内容
    ↓
FAQ
    ↓
插入文献来源 + 免责声明
```

---

## 三、完整修改后的文件结构

```
【Product Basic Information】
【Target Audience】
【Writing Angles — Pre-Selected for This Article】
    ↓
【Article Logic Outline — Internal Working Document, Do Not Output in Final Article】  ← 新增
    ↓
【Title Generation — Based on Logic Outline】  ← 位置调整
【Article Structure Requirements】
    ## 1. Executive Summary
    ## 2-6. Section Titles and Writing Guidance  ← 修改
    ## 7. FAQ
    ## 8. References & Data Sources
    ## 9. Disclaimer
【Writing Guidelines】
```

---

## 四、新增内容详解

### 4.1 【Article Logic Outline】— 新增的中间层

在 `【Writing Angles】` 和 `【Article Structure Requirements】` 之间插入以下内容：

```
【Article Logic Outline — Internal Working Document, Do Not Output in Final Article】

请先阅读产品信息、受众定位、以及5个写作角度，然后输出以下逻辑规划内容（仅供内部工作使用，不会出现在最终文章中）：

1. 核心叙事主线（用一句话概括）：
   → [AI输出：例如"从采购决策者最关心的成本认知出发，逐层深入到技术选型、供应商评估，最终给出可操作的评估框架"]

2. 5个模块的推荐出场顺序及理由：
   - 模块？先 → 理由
   - 模块？次 → 理由
   - 模块？再次 → 理由
   - 模块？再次 → 理由
   - 模块？最后 → 理由

3. 模块之间的过渡策略：
   - 从模块？到模块？：如何自然过渡？（描述过渡逻辑，不写具体过渡句）
   - 从模块？到模块？：如何自然过渡？
   - 从模块？到模块？：如何自然过渡？
   - 从模块？到模块？：如何自然过渡？

4. 推荐的收尾方向（最后一个模块如何收束全文）：
   → [AI输出]

5. 全文叙事弧线（一句话描述）：
   → [例如：从"打破误区"开始，经过"技术分层"、"供应商深度"分析，以"行动清单"收尾]
```

这里我在想要不要进行修改，不是输出，而是让ai用这种方式进行思考，即以文章大纲的思路处理插入的五个模块。如果输出的话，会影响他的输出字符长度，以及后续会涉及到一些过滤的东西（这是我自己的思路）

然后还有一个点，就是在生成文章大纲的时候，就应该已经知道结构了，所以要不要把结构前移到文章大纲前？

我现在的思路是，之前是插入模块后开始写文章。我想修改成，先告诉ai文章的结构。在选取好模块后，ai先根据产品参数，受众方向，题材（这个Base里是市场选型）以及五个模块，ai会想好一个文章大纲（在已经知道结构的情况下去想这个文章大纲），知道这个文章怎么讲以及讲了什么，根据整个大纲生成一个合适的标题（如prompt里所写，汇集了产品名字，从受众视角和大纲内容进行取名）。然后根据这个，开始生产文章。生产到最后的FAQ的时候，会根据公司的背景以及文章内容，提出两个能恰到好处引出杰昊的问题（详情可见Base User Prompt关于FAQ的内容，只是这里要添加一句根据文章内容进行提问，其余都和baseuserprompt里的一样），其余FAQ则根据文章内容进行生产客观的faq。最后插入文献来源和免责声明。

---

### 4.2 【Title Generation】— 位置调整至逻辑大纲之后

从原来文件底部移到【Article Logic Outline】之后：

```
【Title Generation — Based on Logic Outline】

基于上述逻辑大纲和核心叙事主线，请生成一个英文标题。

Title Requirements:
1. Must include the English product name "{english_product_name}".
2. Must reflect a third-party market analysis and selection guidance perspective.
3. Must NOT directly name the target audience in the title (forbidden: CTO, CEO, Sourcing Manager, Project Manager, Industry Analyst).
4. Must NOT use low-information-value words (forbidden: Overview, Complete Guide, Introduction, Summary).
5. Title should have narrative force and topical relevance—not a keyword list.
6. Recommended length: 60–90 English characters.
7. Synthesize all 5 angles into one overarching direction; do not list them individually.

Forbidden:
- "{english_product_name}: Technical Principles and Applications"
- "{english_product_name} Overview"
- "{english_product_name} for Decision-Makers: A Complete Guide"

Recommended:
- "{english_product_name}: Navigating the Compliance Landscape for High-Containment Laboratories"
- "{english_product_name}: Critical Selection Criteria Beyond Basic Certification"
- "{english_product_name}: Evaluating Supplier Depth in China's High-Spec Manufacturing Sector"
```

---

### 4.3 【Article Structure Requirements】— Section 2-6 重写

原来的空白占位符：

```
## 2. [Section Title — Rewritten by You]
## 3. [Section Title — Rewritten by You]
## 4. [Section Title — Rewritten by You]
## 5. [Section Title — Rewritten by You]
## 6. [Section Title — Rewritten by You]
```

改为：

根据文章大纲，进行文章撰写。





## 五、保持不变的部分

- 【Product Basic Information】结构
- 【Target Audience】结构
- 【Writing Angles — Pre-Selected for This Article】的呈现方式（5个模块的展示格式）
- 【Writing Guidelines】写作准则
- 【References & Data Sources】参考文献格式要求
- 【Disclaimer】免责声明格式要求

---

## 六、预期效果

1. **叙事流畅性提升**：AI 先规划逻辑大纲，确保5个模块被串成一条流畅的故事线
2. **标题与内容互相校验**：标题在写文章之前生成，基于逻辑大纲生成，确保标题准确反映内容
3. **小标题质量提升**：Section 2-6 的小标题基于逻辑大纲动态生成，不再是简单的占位符
5. **AI 跑偏概率降低**：通过逻辑大纲提供明确的写作方向，减少 AI 自由发挥的空间

