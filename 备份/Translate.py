import os
import sys
import shutil
from openai import OpenAI

# ================= 配置区 =================
# 自动读取你上一段代码生成的文章根目录
BASE_DIR = "/Users/guot/Desktop/杰昊/AI推广/文章"

API_KEY = "sk-j4kGaMBeZYyma78n"
BASE_URL = "https://acloudvip.top/v1"  

# 强制终端使用 UTF-8 编码
sys.stdout.reconfigure(encoding='utf-8')

client = OpenAI(
    api_key=API_KEY, 
    base_url=BASE_URL,
    timeout=360.0  
)

# ================= 提示词设定 =================
def get_translation_system_prompt():
    return """
You are a senior mechanical engineer and a top-tier Technical SEO (AIO) expert specializing in cleanroom and biopharmaceutical engineering. Your task is to translate the provided Chinese engineering article into highly professional, native English suitable for global procurement teams and AI search engines (like Perplexity, SearchGPT).

【Core Directives】
1. Authentic Industry Terminology (Anti-Chinglish): NEVER translate word-for-word. You must use authentic, internationally recognized engineering terminology standard in the cleanroom, biosafety (BSL-3/BSL-4), and HVAC industries (aligned with ISO, GMP, FDA, and WHO standards).
- Avoid aggressive or overly dramatic commercial rhetoric (e.g., avoid "fatal flaws" or "camps"). Use objective, authoritative engineering language (e.g., "critical vulnerabilities", "market segments").
- Favor passive voice and objective structures where appropriate for technical whitepapers.
2. AI SEO Optimization: Naturally embed relevant LSI keywords (e.g., BSL-3, pneumatic seal, VHP sterilization, pressure decay test, airtight containment). Ensure logical flow so AI agents can easily extract entities and relationships.
3. Markdown Retention: You MUST strictly preserve all original Markdown formatting (headers `#`, bold `**`, lists `-`, etc.). Do not alter the structural hierarchy.
4. Output Constraint: ONLY output the translated English text. Do not include any conversational filler, greetings, or explanations before or after the article.

【Glossary (Strict Adherence)】
- 杰昊生物 / 杰昊 / Jiehao -> Jiehao Biotechnology
- 充气气密门 / 充气式柔性密封 -> Pneumatic Airtight Doors / Inflatable Seal Doors
- VHP传递窗 -> VHP Pass Box
- 压缩永久变形率 -> Compression Set
- 压差衰减测试 -> Pressure Decay Test
- 充放气循环 -> Inflation-deflation cycles
- 差压变送器 -> Differential Pressure Transmitter
- 全生命周期成本 -> Total Cost of Ownership (TCO)
"""

# ================= 工具函数 =================
def call_translation_api(text_to_translate):
    print("  ⏳ 正在调用大模型进行工程级翻译与 SEO 润色 (耗时较长，请稍候)...")
    try:
        response = client.chat.completions.create(
            model="claude-opus-4-6", # 继续使用你的中转站模型标识
            messages=[
                {"role": "system", "content": get_translation_system_prompt()},
                {"role": "user", "content": f"Please translate the following Markdown article into English strictly following the rules:\n\n{text_to_translate}"}
            ],
            temperature=0.3 # 翻译任务需要较低的 temperature 以保证准确性和严谨性
        )
        if isinstance(response, str):
            return None
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"  ❌ 翻译 API 调用失败: {e}")
        return None

# ================= 主程序逻辑 =================
print(f"📂 开始扫描目标目录: {BASE_DIR}")

if not os.path.exists(BASE_DIR):
    print("❌ 找不到文章根目录，请检查路径。")
    sys.exit(1)

# 遍历所有产品文件夹
for product_folder in os.listdir(BASE_DIR):
    product_path = os.path.join(BASE_DIR, product_folder)
    
    # 确保是文件夹
    if not os.path.isdir(product_path):
        continue
        
    yinliu_path = os.path.join(product_path, "引流层")
    
    # 如果该产品没有引流层，跳过
    if not os.path.exists(yinliu_path):
        continue

    print(f"\n🚀 进入产品目录: {product_folder}")
    
    # 扫描引流层下的所有文件
    for item_name in os.listdir(yinliu_path):
        item_path = os.path.join(yinliu_path, item_name)
        
        # 只处理 .md 文件（排除已经是文件夹的项目，防止重复嵌套）
        if os.path.isfile(item_path) and item_name.endswith('.md'):
            # 去掉 .md 后缀，作为中英文对照文件夹的名字
            article_base_name = item_name[:-3]
            
            # 1. 在引流层下，以文章名创建专属文件夹
            article_dir = os.path.join(yinliu_path, article_base_name)
            os.makedirs(article_dir, exist_ok=True)
            
            print(f"\n  📄 发现中文稿件: {item_name}")
            print(f"  📁 已创建专属归档文件夹: {article_base_name}")
            
            # 读取中文内容
            with open(item_path, 'r', encoding='utf-8') as f:
                chinese_content = f.read()
                
            # 2. 执行翻译
            english_content = call_translation_api(chinese_content)
            
            if english_content:
                # 3. 保存英文翻译稿到新文件夹内
                # 为了区分，英文稿加上 _EN 后缀
                eng_file_path = os.path.join(article_dir, f"{article_base_name}_EN.md")
                with open(eng_file_path, "w", encoding="utf-8") as f:
                    f.write(english_content)
                print(f"  ✅ 英文版已生成并保存至: {eng_file_path}")
                
                # 4. 将原本的中文文件移动到新文件夹内
                new_chn_file_path = os.path.join(article_dir, item_name)
                shutil.move(item_path, new_chn_file_path)
                print(f"  📦 原中文版已移入专属文件夹。归档完成！")
            else:
                print(f"  ⚠️ 翻译失败，跳过文件移动操作，保留原状。")

print("\n🎉 所有目录扫描及翻译归档任务执行完毕！")