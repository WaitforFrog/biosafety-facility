# Setting.md — 配置文件（无需 Python 知识即可修改）
# KEY = VALUE，每行一个，等号两侧禁止空格
# 注释行：独立成行，以 # 开头

## 路径配置区
# 主目录
PRODUCE_DIR  = PROJECT_ROOT / "Produce"
APP_DIR      = PROJECT_ROOT / "APP"
WEBSITE_DIR  = PROJECT_ROOT / "Website"
TITLE_DIR    = PROJECT_ROOT / "Title"
# 文章原始出处（文章存放的上级目录）
SOURCE_ROOT  = PROJECT_ROOT.parent / "文章"
# 内容池总目录
CONTENT_POOL_DIR = {"Compare": PROJECT_ROOT / "Produce" / "Compare_Content", "Question": PROJECT_ROOT / "Produce" / "Question_Content", "Installation": PROJECT_ROOT / "Produce" / "Installation_Content", "Regulatory": PROJECT_ROOT / "Produce" / "Regulatory_Content"}

## 路径配置区（运行时模式切换）
# 文章输出主目录（运行时切换为 Check 或 参数）
ARTICLES_DIR_STR = PROJECT_ROOT / "文章"
# 产品参数读取目录（运行时切换为 Check 或 参数）
PARAMETERS_DIR_STR = PROJECT_ROOT / "Check"
# 网站输出目录（运行时切换为 Check 或 参数）
WEBSITE_DIR_STR = PROJECT_ROOT / "Website"

## 内容生成参数
# 每次从内容池抽取多少个模块
CARD_DRAW_COUNT = 5
# 每种受众生成多少篇文章
ARTICLES_PER_AUDIENCE = 1
# 发布日期间隔范围（天内随机）
PUBLISH_DATE_RANGE_DAYS = 30
# 处理完每个产品后休息多少秒
INTER_PRODUCT_DELAY = 5

## API配置区
# API调用参数
API_TEMPERATURE = 1.0
API_MAX_TOKENS = 8192
API_TIMEOUT = 120
# 当前：小象API
OPENAI_API_KEY = "sk-j4kGaMBeZYyma78n"
API_BASE_URL   = "https://acloudvip.top/v1"
MODEL_NAME     = "claude-opus-4-6-a"

## 工作流配置
# 是否自动 git push（True / False）
AUTO_GIT_PUSH = True

## 备份目录配置
# 每个脚本对应一个备份子目录名
BACKUP_COMPARE_JIEHAO     = "Base"
BACKUP_COMPARE_NEUTRAL    = "Base"
BACKUP_QUESTION_JIEHAO    = "Question"
BACKUP_QUESTION_NEUTRAL   = "Question"
BACKUP_INSTALL_JIEHAO     = "Installation"
BACKUP_INSTALL_NEUTRAL    = "Installation"
BACKUP_REGULATORY_JIEHAO  = "Regulatory"
BACKUP_REGULATORY_NEUTRAL = "Regulatory"

## Trust脚本专用配置
TRUST_MAX_CONCURRENT = 2
TRUST_TEMPERATURE   = 1.0
TRUST_MAX_TOKENS     = 4096
TRUST_MODEL          = "claude-opus-4-6-a"
