"""
文件操作工具
"""


def sanitize_filename(name):
    """清理文件名中的非法字符"""
    return "".join([c for c in name if c not in r'\/:*?"<>|'])
