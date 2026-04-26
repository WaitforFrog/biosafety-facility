"""
运行日志工具
"""


def create_article_log(product_name, english_folder, article_num, current_time, result_text, title, keywords_str, html_path, backup_path, start_time):
    """生成文章生成日志"""
    log_md = f"""# 文章生成日志

## 基本信息
- 产品名称: {product_name}
- 英文名称: {english_folder}
- 文章编号: article-{article_num}
- 生成时间: {current_time}
- 文章类型: 市场分析与选型测评

## API 请求
- 请求时间戳: {current_time}

## 生成结果
- API返回长度: {len(result_text)} 字符
- 文章标题: {title}
- 关键词: {keywords_str}

## 输出文件
- HTML: {html_path}
- 备份: {backup_path}

## 状态
- 状态: 成功
- 耗时: {__import__('time').time() - start_time:.1f} 秒
"""
    return log_md
