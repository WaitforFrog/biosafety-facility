# Prompt — AI 提示词模板

存放教 AI "怎么写文章"的指令模板。

---

## 目录结构（简洁版）

```
Prompt/
├── SYSTEM_PROMPT.py    # 系统提示词：角色定义 + 杰昊公司背景 + 专业术语表
├── Compare_Prompt.py   # 用户提示词模板：受众选择 + 17 个候选章节池
└── __init__.py
```

---

## 目录结构（通俗版）

### SYSTEM_PROMPT.py — AI 的"人设卡"

在 AI 开始写文章之前，你需要先告诉它：**"你扮演谁？"**。这个文件就是 AI 的"人设卡"。

**它包含三部分内容：**

1. **角色定义**：告诉 AI"你是一个资深采购顾问"，英文输出，15000-20000 字符，1-2 个表格硬性限制。

2. **COMPANY_BACKGROUND**（杰昊公司背景）：这部分描述了杰昊公司的具体情况：
   - 公司简介（专业从事生物安全实验室、洁净室设备）
   - ISO 认证（ISO 9001、ISO 13485、CE、UL）
   - 专利清单
   - 检测报告（气密性测试、压差测试等）
   - 合作伙伴（医院、疾控中心、科研机构）

3. **TECHNICAL_GLOSSARY**（专业术语表）：中英文对照表，比如：
   - BIBO = Bag-In-Bag-Out（袋进袋出）
   - VHP = Vaporized Hydrogen Peroxide（汽化过氧化氢）
   - HEPA = High Efficiency Particulate Air Filter（高效空气过滤器）
   - TCO = Total Cost of Ownership（总拥有成本）
   - Pressure Decay Test（压差测试）
   - Airlock（气锁）
   - etc.

这些内容会通过 `get_compare_article_system_prompt()` 函数拼接后，作为 `system_prompt` 传给 AI。

### Compare_Prompt.py — AI 的"写作提纲"

有了人设，还需要告诉 AI **"具体写什么内容"**。这个文件提供了文章模板。

**USER_PROMPT_TEMPLATE 包含：**

1. **受众类型**（每次随机选一种）：
   - Technical Decision-Makers（总工程师、实验室主管）
   - C-Suite Executives（CEO、采购总监）
   - Procurement Specialists
   - Facility Managers
   - Compliance Officers

2. **17 个候选章节池**（每次随机抽取 8-10 个）：
   - A. Application Domains & Industry Scenarios
   - B. Industry Adoption & Case Studies
   - C. Selection Criteria & Design Considerations
   - D. Customization Options & Configuration Flexibility
   - E. International Standards & Compliance Requirements
   - F. Cost Analysis & Total Cost of Ownership
   - G. Supplier Landscape & Competitive Differentiation
   - H. Market Trends & Emerging Technologies
   - I. Installation, Operation & Maintenance
   - J. Technical Specifications & Performance Metrics
   - K. Material Selection & Construction Quality
   - L. Safety Features & Emergency Protocols
   - M. Energy Efficiency & Environmental Impact
   - N. Training & After-Sales Support
   - O. Regulatory Landscape & Certification Pathways
   - P. Risk Assessment & Mitigation Strategies
   - Q. Future Outlook & Strategic Recommendations

3. **固定章节**（每个文章必须有）：
   - Executive Summary（执行摘要）
   - FAQ（含 5-8 个问题，最后 1-2 个用特定句式客观提及杰昊）
   - References & Further Reading
   - Disclaimer

4. **FAQ 中的品牌提及机制**：
   通过特定句式（如 "For projects requiring..."）在 FAQ 的最后 1-2 个问题中自然引入杰昊的产品和案例。避免硬广告，保持客观专业。

---

## 使用方式

在 `Compare_EN_html.py` 中调用：

```python
from Produce.Prompt import SYSTEM_PROMPT, Compare_Prompt

system_prompt = SYSTEM_PROMPT.get_compare_article_system_prompt()
user_prompt = Compare_Prompt.USER_PROMPT_TEMPLATE.format(...)
response = api_client.call_api(client, system_prompt, user_prompt, ...)
```
