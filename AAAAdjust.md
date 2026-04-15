# Base 模块 User Prompt 调整方案（完整版 V3）

> 作者：AI | 日期：2026-04-15
> 状态：基于AAAdjust讨论后的最终整合方案 + 新增内部规划增强
> 目标：解决"模块塞入后生硬"的问题，让 AI 既能自由发挥又不会跑偏
> 适用范围：Base_User_Prompt.py

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
- FAQ中品牌引导问题的植入痕迹过重，影响第三方人设的可信度

---

## 二、修改后的新流程

```
抽到5个模块 + 产品信息 + 受众定位
    ↓
【Step 1】明确文章结构框架（结构在前，让AI知道"坑位"在哪里）
    ↓
【Step 2】内部规划逻辑大纲（不出现在最终文章中，通过隐式约束生效）
    ↓
【Step 3】基于逻辑主线生成标题
    ↓
【Step 4】基于逻辑主线重写 Section 2-6 的小标题
    ↓
【Step 5】写完整文章内容（模块融会贯通，非一一对应）
    ↓
【Step 6】FAQ（7-8个，品牌引导问题自然混入客观问题中）
    ↓
【Step 7】插入文献来源 + 免责声明
```

---

## 三、完整修改后的文件结构

```
【Product Basic Information】
【Target Audience】
【Writing Angles — Pre-Selected for This Article】
    ↓
【Article Structure Requirements — 明确框架，让AI先知道"坑位"】  ← 新增结构框架
    ↓
【Internal Logic Planning — 内部规划，不输出在最终文章】  ← 新增内部规划（增强版）
    ↓
【Title Generation — 基于逻辑主线生成】  ← 位置调整
【Section Writing Guidance — 基于逻辑主线动态生成小标题】  ← 修改（增强过渡约束）
【FAQ — 7-8个，品牌引导问题混入客观问题】  ← 修改
【References & Data Sources】
【Disclaimer】
【Writing Guidelines】
```

---

## 四、新增内容详解

### 4.1 【Article Structure Requirements】— 明确框架在先

在 `【Writing Angles】` 之后、`【Internal Logic Planning】` 之前，插入明确的结构框架。**让AI先知道文章有几段，再去规划如何填充内容。**

```
【Article Structure Requirements — Fixed Framework for This Article】

Your article will follow this structure. Read it carefully before planning your logic outline.

## 1. Executive Summary
- One-sentence definition: Clearly state the core role of {english_product_name} in its primary application scenario.
- Market landscape overview: Segment existing solutions into tiers (e.g., standard commercial grade vs. high-spec grade), identify the core differentiating criteria.

## 2. [Section Title — Rewritten by You]

## 3. [Section Title — Rewritten by You]

## 4. [Section Title — Rewritten by You]

## 5. [Section Title — Rewritten by You]

## 6. [Section Title — Rewritten by You]

## 7. FAQ

## 8. References & Data Sources

## 9. Disclaimer

Note: Sections ## 2 through ## 6 are the core body of the article. You will plan how to weave the 5 pre-selected angles into these 5 sections. The section count is fixed at 5, but the mapping between angles and sections is flexible — see Internal Logic Planning below.
```

> **说明**：此处给出完整的固定框架，让AI知道总共有9个章节（## 1-9），Section 2-6是正文核心，FAQ、References、Disclaimer是固定尾部。

---

### 4.2 【Internal Logic Planning — Enhanced】— 内部规划，不输出在最终文章

**重要决策**：本节内容**不允许出现在最终文章中**，仅供AI内部规划使用。这是因为：
1. 显式输出逻辑大纲会占用500-1000字符，直接压缩正文空间
2. 当前文章字符限制为15000-20000，已有截断风险
3. 逻辑大纲的约束力可以通过"隐式嵌入"的方式生效，无需显式输出

**隐式约束嵌入方式 — 将逻辑大纲的5个维度分散到后续步骤中：**

#### 4.2.1 叙事主线的隐式约束（嵌入标题生成环节）— 增强版

在标题生成指令前加入完整的5步内部规划检查，要求AI在生成标题前先完成整体内容规划（**所有步骤均为内部思考，不输出任何内容**）：

```
【Title Generation Instructions】

Before drafting the title, complete this internal planning process (do not output anything — this is for your internal planning only):

Step 1 — Integrate:
- What is the ONE core narrative thread that connects all 5 pre-selected angles?

Step 2 — Map:
- Assign the 5 angles to the 5 body sections (## 2-6).
- For each section, identify which 1-2 angles it will primarily develop.
- Note: One section can cover multiple angles; one angle can be referenced in multiple sections.

Step 3 — Validate:
- Check for gaps: is any section's content too thin (less than 300 words)?
- If so, merge angles or borrow material from other sections to fill the gap.
- Check for overlaps: are any two sections saying essentially the same thing?
- If so, differentiate the focus of each section.

Step 4 — Transition:
- Confirm the logical flow: ## 2 should introduce the core tension, ## 3 should deepen it, ## 4 should complicate it, ## 5 should bring it to a climax, ## 6 should resolve it.
- For each section, identify the ONE unresolved question it will leave behind to lead into the next section.

Step 5 — Theme:
- Based on all above, identify the ONE keyword that best represents the narrative thread.
- This keyword MUST appear in your article title.

Now generate a single English title following the requirements below:
- Must include the English product name "{english_product_name}"
- Must reflect a third-party market analysis and selection guidance perspective
- Must NOT directly name the target audience in the title (forbidden: CTO, CEO, Sourcing Manager, Project Manager, Industry Analyst)
- Must NOT use low-information-value words (forbidden: Overview, Complete Guide, Introduction, Summary)
- Must contain the keyword identified in Step 5
- Title should have narrative force and topical relevance — not a keyword list
- Recommended length: 60–90 English characters
- Synthesize all 5 angles into one overarching direction; do not list them individually

Forbidden examples:
- "{english_product_name}: Technical Principles and Applications"
- "{english_product_name} Overview"
- "{english_product_name} for Decision-Makers: A Complete Guide"

Recommended examples:
- "{english_product_name}: Navigating the Compliance Landscape for High-Containment Laboratories"
- "{english_product_name}: Critical Selection Criteria Beyond Basic Certification"
- "{english_product_name}: Evaluating Supplier Depth in China's High-Spec Manufacturing Sector"
```

#### 4.2.2 出场顺序与过渡策略的隐式约束（嵌入Section写作指引）

Section写作指引（见4.3节）中包含以下约束，隐式覆盖了出场顺序和过渡策略。

#### 4.2.3 收尾方向的隐式约束（嵌入FAQ前的过渡指令）

在FAQ章节前加一段，收尾方向隐式生效：

```
Before moving to the FAQ section, the final body section (## 6) must:
- Synthesize insights from all 5 angles into a unified conclusion
- End with a forward-looking statement or actionable guidance aligned with the target audience's decision-making context
- The closing paragraph must organically connect to the FAQ — do not write a hard break between ## 6 and ## 7
```

---

### 4.3 【Section Writing Guidance — Enhanced】— 基于逻辑主线动态生成小标题

原来的空白占位符改为有明确写作指引的动态结构，**每节新增过渡策略约束**：

```
【Section Writing Guidance — Based on Internal Logic Planning】

Instructions for Sections ## 2 through ## 6:

## 2. [Section Title — Rewritten by You]

- Primary angle coverage: Identify which 1-2 of the 5 pre-selected angles this section will primarily develop
- Narrative function: How does this section advance the core narrative thread? (answer for yourself, do not write it in the article)
- Opening requirement: The FIRST paragraph must organically connect to the Executive Summary's market-tier segmentation — do not write a standalone "This section will discuss..." sentence; the opening should feel like a natural continuation that picks up a thread from the Executive Summary
- Transition requirement: The LAST paragraph must pose ONE unresolved question or tension that logically leads into ## 3 — this question should be a direct consequence of the argument developed in ## 2

## 3. [Section Title — Rewritten by You]

- Primary angle coverage: Identify which 1-2 angles this section will develop
- Narrative function: How does this section build on the foundation laid in ## 2? (answer for yourself, do not write it in the article)
- Opening requirement: The FIRST paragraph must pick up the unresolved question from ## 2's closing and begin resolving it — the reader should feel a logical chain, not a new topic. Do not start with a generic statement; start by directly engaging with the tension left in ## 2.
- Transition requirement: The LAST paragraph must leave behind a new, deeper unresolved tension that leads into ## 4

## 4. [Section Title — Rewritten by You]

- Primary angle coverage: Identify which 1-2 angles this section will develop
- Narrative function: How does this section deepen the analysis from ## 3? (answer for yourself, do not write it in the article)
- Opening requirement: The FIRST paragraph must engage with the tension raised at the end of ## 3 — build on it, complicate it, or offer a new dimension. Do not treat ## 4 as a standalone topic.
- Transition requirement: The LAST paragraph should bring the reader to the climax — prepare the ground for ## 5's deeper analysis

## 5. [Section Title — Rewritten by You]

- Primary angle coverage: Identify which 1-2 angles this section will develop
- Narrative function: How does this section approach the climax of the narrative? (answer for yourself, do not write it in the article)
- Opening requirement: The FIRST paragraph must feel like the turning point — pick up the tension from ## 4 and escalate it or provide a decisive insight that shifts the perspective
- Transition requirement: The LAST paragraph must set up ## 6 as the synthesis section — end with a question or challenge that ## 6 will resolve

## 6. [Section Title — Rewritten by You]

- Primary angle coverage: This is the synthesis section — weave in remaining angles and cross-reference insights from previous sections
- Narrative function: Synthesize all 5 angles into a unified conclusion (answer for yourself, do not write it in the article)
- Opening requirement: The FIRST paragraph must directly engage with the climax tension from ## 5 — provide the key insight or resolution that ties everything together. Do not introduce a new topic.
- Closing requirement: End with a forward-looking statement or actionable guidance aligned with the target audience's decision-making context. This closing paragraph must organically lead into the FAQ section — the transition from ## 6 to ## 7 should feel like a natural flow, not a hard topic switch.

【Cross-Reference Requirement — Module Integration】
The 5 pre-selected angles are a SHARED素材池 (material pool), not individual section assignments:
- You MAY reference data or insights from any angle at any point in any section
- You MAY use a data point from Angle 2 to support an argument in the section primarily covering Angle 5
- Cross-referencing strengthens the narrative; treating each angle as a standalone block creates a checklist, not an article
- Do NOT dedicate an entire section to a single angle unless the angle's content genuinely spans 400+ words

【Structure Enforcement — Absolute Requirement】
- Each section (## 2-6) must have at least one ### subsection header OR meaningful paragraph-level structure
- The article must NOT be a single block of unorganized text
- Use ### subheadings to organize complex sections, but ensure the article reads as flowing prose between sections, not as isolated topic chunks

【Negative Constraints — What NOT to Do】
- Do NOT write any section as a standalone essay that ignores the previous section's argument
- Do NOT use the same transition strategy for every section — each transition should feel distinct and purposeful
- Do NOT write section openings that could be moved to any other section — each opening must feel tied to the specific argument of that section
- Do NOT repeat the same data point or argument across two consecutive sections without adding new insight
- Do NOT write a closing for any section (except ## 6) that reads like a conclusion — only ## 6 should conclude
```

---

### 4.4 【Title Generation】— 位置调整至结构框架和内部规划之后

从原来文件底部移到【Internal Logic Planning】之后，标题生成指令本身不需要大的调整，只需要在上方嵌入"内部叙事主线确认"步骤（见4.2.1）。

---

### 4.5 【FAQ】— 品牌引导问题混入客观FAQ

**核心策略**：品牌引导问题必须"淹没"在客观FAQ中，让读者分不清哪个是引导的、哪个是客观的。软植入效果最强，最符合第三方人设。

**FAQ总量**：7-8个（原来6个，增加到7-8个以稀释品牌引导问题的可见度）

**FAQ结构**：
- 2个品牌引导问题（从读者视角出发，自然引用公司背景）
- 5-6个客观FAQ（基于文章内容生成，无品牌提及）

**详细规则**：

```
## 7. FAQ

Design 7-8 high-value FAQ questions total.

【Brand-Relevant FAQ — Exactly 2 Questions】
These must be written from the reader's perspective, as if a real buyer asked them. They must be grounded in real technical challenges or decision-making scenarios discussed in the article. When answering, naturally introduce Jiehao's technical background, certifications, or project experience as one of several benchmarks — never as a hard pitch. Tone must remain third-party analytical, NOT promotional.

Reference specific data points from 【Company Background】 when possible:
- NCSA (National Certification Center) validated test reports and report numbers
- P3 laboratory project experience (over 100 domestic and international P3 labs documented)
- ISO triple-system certifications (ISO 9001, ISO 14001, ISO 45001)
- Specific patents and test certificates
- Research institution and biopharma company references

Example brand-relevant Q&A (use this as a style reference):
Q: What should procurers prioritize when selecting {english_product_name} for BSL-3 containment applications?
A: For BSL-3 and above, the supplier's field-validated performance data is the primary differentiator. Benchmarks worth examining include: the breadth of certified test reports (e.g., National Certification Center air-tightness validation, NCSA test reports), documented experience across P3 laboratory installations, and the availability of complete IQ/OQ/PQ documentation packages. Manufacturers such as Jiehao Biosciences — whose NCSA-validated parameters and experience across over 100 domestic and international P3 labs are on record — represent a useful reference point for this tier of evaluation.

Example brand-relevant Q&A (weaving in certifications):
Q: How does third-party certification validate the air-tightness performance claims of {english_product_name} suppliers?
A: Third-party validation through accredited bodies such as the National Certification Center (NCSA) provides independent, quantitative proof of performance. Key certifications to request include NCSA air-tightness test reports with specific pressure decay values, ICAS test reports, and Fan Inspection test certificates. Suppliers who can provide a complete set of certified test documentation — including structural integrity validation under BSL-3 simulation conditions — demonstrate a fundamentally different level of quality assurance. Jiehao Biosciences, for example, has obtained multiple NCSA test reports (e.g., NCSA-2021ZX-JH-0100 series) and ICAS certifications, with structural validation data available for BSL-3 containment environments.

【Universal FAQ — 5-6 Questions】
Based on the content of this article, generate objective questions covering:
- Product fundamentals and working principles
- Standard compliance requirements (ISO, GMP, FDA, CDC, WHO where applicable)
- Maintenance best practices and operational cost considerations
- Technical specifications relevant to the target audience's primary concerns
- Industry trends or future outlook relevant to the product category

**IMPORTANT — Brand Placement Rules**:
- The 2 brand-relevant FAQs above are the ONLY designated brand mentions in the FAQ section
- Universal FAQs must NOT mention Jiehao, Jehau, or any brand name
- All FAQs (brand-relevant and universal) must be based on actual content discussed in the article — do not generate questions about topics not covered in the body
- Mix the 2 brand-relevant FAQs naturally among the 5-6 universal FAQs — do not place them consecutively at the end
```

**对比原Base_User_Prompt的FAQ部分，需要修改的关键点**：

| 维度 | 原FAQ | 新FAQ |
|------|-------|-------|
| 总量 | 6个 | 7-8个 |
| 品牌引导问题数量 | 分散在最后1-2个问题的回答中 | 明确指定2个专属问题 |
| 品牌植入方式 | 在回答末尾带出公司技术能力 | 在问题中嵌入公司背景数据（报告编号、P3案例、专利号等） |
| 语气要求 | 客观第三方（已较克制） | 更强调"软植入"，要求引用具体数据而非泛泛提及 |
| 问题分布 | 受众专项3个 + 通用3个 | 品牌引导2个 + 客观5-6个，混合排列 |
| 与文章内容的关联 | 受众专项问题来自audience_focus参数 | 品牌引导问题必须基于文章实际讨论的技术场景 |

---

### 4.6 References & Data Sources — 保持不变

```
## 8. References & Data Sources
[保持原Base_User_Prompt的内容不变]
```

---

### 4.7 Disclaimer — 保持不变

```
## 9. Disclaimer
[保持原Base_User_Prompt的内容不变]
```

---

## 五、保持不变的部分

- 【Product Basic Information】结构
- 【Target Audience】结构
- 【Writing Angles — Pre-Selected for This Article】的呈现方式（5个模块的展示格式）
- 【Writing Guidelines】写作准则
- 【Disclaimer】免责声明格式要求
- System Prompt中的字符限制要求（15000-20000字符）和表格数量要求（1-2个）

---

## 六、待确认事项（需要你进一步决策）

### 6.1 Section数量是否保持固定为5个（## 2-6）？

当前方案将Section 2-6固定为5个，对应5个模块。但根据"融会贯通"原则：
- 如果某个Section融合了两个相邻模块，可能有剩余空间不够的问题
- 如果某个模块特别复杂需要展开，可能需要更多段落

**两个选项**：
- 选项A：保持固定5个Section（## 2-6），AI自行决定模块融合方式
- 选项B：改为弹性范围"至少3个，至多6个Section"，AI根据模块间的融合可能性自行决定数量

### 6.3 是否需要调整FAQ的问题总数？

当前方案建议7-8个FAQ（原Base_User_Prompt是6个）。增加的原因：
- 更多客观问题可以提升FAQ的信息密度
- 品牌引导问题混入更多内容中更自然

但如果担心字符超限，可以：
- 选项A：维持7-8个FAQ
- 选项B：维持在6个，但调整品牌引导问题和客观问题的比例（2+4）

---

## 七、预期效果

1. **叙事流畅性提升**：通过内部逻辑规划，5个模块被串成一条流畅的故事线，而非清单式列举
2. **标题与内容一致性提升**：标题生成前先确认叙事主线关键词，减少跑偏概率
3. **模块融会贯通**：5个模块作为共享素材池，AI在任意位置引用任意模块的数据，增强文章整体感
4. **文章结构依然清晰**：三级标题体系确保文章不是一大段文字，结构底线得以保持
5. **品牌植入更自然**：2个品牌引导问题混入5-6个客观问题中，以第三方推荐语气引用具体数据（P3项目数、NCSA报告编号等），读者感知为专业分析而非广告
6. **零额外字符消耗**：内部逻辑规划不出现在最终文章中，不影响15000-20000的字符空间
7. **过渡质量提升（新增）**：通过每节 Opening/Closing 的过渡策略约束，章节之间不再孤立，读者能感受到清晰的逻辑递进
8. **质量底线保障（新增）**：Negative Constraints 明确告诉 AI 不要做什么，给 AI 划出清晰的边界

## 九、最终prompt文件结构预览（供代码编写参考）

```
Base_User_Prompt.py 新结构（V3）：

USER_PROMPT_TEMPLATE = '''

【Product Basic Information】
【Target Audience】
【Writing Angles — Pre-Selected for This Article】

【Article Structure Requirements — Fixed Framework for This Article】
（## 1-9完整结构，Section 2-6为空白占位符，说明模块融合的灵活性）

【Internal Logic Planning — Do Not Output in Final Article】
（5步内部规划检查：Integrate �� Map → Validate → Transition → Theme）

【Title Generation Instructions】
（5步内部规划 + 标题生成要求）

【Section Writing Guidance — Based on Internal Logic Planning】
（## 2-6各节的写作指引，含模块融合规则和过渡策略约束，以及 Negative Constraints）

【FAQ — 7-8个，品牌引导问题混入客观FAQ】
（详细规则见4.5节）

【Writing Guidelines】
（保持不变）

【References & Data Sources】
（保持不变）

【Disclaimer】
（保持不变）
'''
```

---

## 十、V2 → V3 核心升级点对照

| 位置 | V2（AAAAdjust原版） | V3（增强版） |
|------|-------------------|-------------|
| 4.2.1 标题生成前内部检查 | 3步（叙事主线确认） | **5步（Integrate → Map → Validate → Transition → Theme）** |
| 4.2.1 输出内容 | 不输出 | **不输出，但5步中的第5步（Theme）要求标题必须包含某关键词** |
| 4.3 Section Writing Guidance | Opening/Closing 有基本描述 | **每节 Opening 新增"必须承接上一节Closing"的明确约束； Closing 新增"必须引出下一节"的未解问题要求** |
| 4.3 新增 Negative Constraints | 无 | **明确列出"不要做什么"，给AI划边界** |
| 4.2.3 收尾方向 | 基本收尾要求 | **新增"## 6 到 ## 7 的过渡要自然，不能hard break"** |