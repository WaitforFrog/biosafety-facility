"""
Tool 模块 - 市场分析文章生成器的工具函数集合
"""
from .html_template import get_html_template, markdown_to_html, extract_title_from_markdown
from .product_loader import load_product_parameters
from .product_mapping import PRODUCT_NAME_MAPPING
from .api_client import call_api
from .file_utils import sanitize_filename
from .git_utils import git_commit_and_push
from .run_summary import save_run_summary
from .log_utils import create_article_log
