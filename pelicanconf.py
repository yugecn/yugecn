AUTHOR = "Kendy"
SITENAME = "Liao's Weblog"
SITESUBTITLE = "Enlarge dream, achieve future!"
TOPBAR_TEXT = "Kendy 的个人博客"
THEME = "themes/massiveblue"
SEARCH_SITE = "yugecn.github.io"
COPYRIGHT_YEAR = "2009–2026"
SITEURL = ""
PATH = "content"
TIMEZONE = "Asia/Shanghai"
DEFAULT_LANG = "zh-CN"
DEFAULT_DATE_FORMAT = "%Y-%m-%d"
ARTICLE_PATHS = ["posts"]
PAGE_PATHS = ["pages"]
STATIC_PATHS = ["images", "extra/.nojekyll"]
EXTRA_PATH_METADATA = {"extra/.nojekyll": {"path": ".nojekyll"}}
ARTICLE_URL = "{date:%Y}/{date:%m}/{slug}.html"
ARTICLE_SAVE_AS = ARTICLE_URL
PAGE_URL = "{slug}.html"
PAGE_SAVE_AS = PAGE_URL
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
LINKS = (
    ("GitHub", "https://github.com/yugecn"),
    ("yuge.cn", "http://www.yuge.cn/"),
    ("Chinese Tea", "http://lifetea.org/"),
)
SOCIAL = (("GitHub", "https://github.com/yugecn"),)
DEFAULT_PAGINATION = 10
RELATIVE_URLS = True

# 插件；站内搜索由 Pagefind 在线上构建后生成（支持中文分词）
PLUGINS = ["neighbors", "sitemap", "related_posts", "statistics"]
SEARCH_ENABLED = False  # 本地预览用 Bing；线上构建在 publishconf 打开 Pagefind
SITEMAP = {
    "format": "xml",
    "priorities": {"articles": 0.8, "indexes": 0.6, "pages": 0.5},
    "changefreqs": {"articles": "monthly", "indexes": "daily", "pages": "monthly"},
}
RELATED_POSTS_MAX = 5

# 评论（Giscus，存于仓库 Discussions）；GISCUS_REPO_ID 留空则不显示
GISCUS_REPO = "yugecn/yugecn.github.io"
GISCUS_REPO_ID = "MDEwOlJlcG9zaXRvcnk3NTU3Mjg1Nw=="
GISCUS_CATEGORY = "Announcements"
GISCUS_CATEGORY_ID = "DIC_kwDOBIEmec4DLLDM"
