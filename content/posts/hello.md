Title: 你好，世界：这个博客是怎么搭起来的
Date: 2026-11-15 15:30
Category: 折腾
Tags: Pelican, GitHub Pages, 建站, 插件, 新手教程
Slug: hello-world
Summary: 不花一分钱、不租服务器，用 Pelican + GitHub Pages 搭一个带搜索、评论、留言板、归档日历的个人博客。从零开始，写给小白。

新博客开张，第一篇就写写它是怎么搭起来的。

整套下来**不花一分钱、不用租服务器、不用装数据库**。写文章就是写一个文本文件，交到 GitHub 上，一两分钟后网站自己更新。下面尽量写得细一点，没碰过建站的朋友也能照着做。

## 一、先弄懂几个词

- **静态博客**：网站就是一堆现成的 HTML 网页，没有后台、没有数据库。好处是快、安全、免费托管；代价是评论、搜索这类“动”的功能要借助外部服务。
- **Pelican**：一个用 Python 写的静态博客生成器。你写 Markdown 文本，它帮你套上主题，生成整个网站。
- **Markdown**：一种很简单的写作格式。`## 标题` 就是标题，`**加粗**` 就是加粗，几分钟就能学会。
- **GitHub**：放代码的网站，这里用来放博客的“源文件”。
- **GitHub Pages**：GitHub 免费提供的网页托管，地址就是 `用户名.github.io`。
- **GitHub Actions**：GitHub 免费的自动化流水线。每次你提交文章，它自动帮你生成网站并发布。

一句话概括：**我写 Markdown → 提交到 GitHub → Actions 用 Pelican 生成网页 → Pages 把它放到网上**。

## 二、准备工作

1. 注册一个 GitHub 账号，比如我的是 `yugecn`；
2. 新建一个**公开**仓库，名字必须是 `用户名.github.io`，比如 `yugecn.github.io`。这样网站地址就是 `https://yugecn.github.io/`；
3. 仓库 **Settings → Pages → Build and deployment → Source** 选 **GitHub Actions**。

为什么要公开？免费账号的 GitHub Pages 只能用公开仓库。博客本来就是给人看的，公开没关系，但**千万别把密码、密钥写进仓库**，后面会讲密钥放哪里。

## 三、仓库里都有什么

```
yugecn.github.io/
├── content/
│   ├── posts/        ← 文章，一篇一个 .md
│   ├── pages/        ← 独立页面：关于、留言板
│   └── images/       ← 图片
├── themes/massiveblue/   ← 主题（网站长什么样）
├── tools/            ← 小脚本，比如同步到 Blogger
├── pelicanconf.py    ← 主配置
├── publishconf.py    ← 发布时额外的配置
├── requirements.txt  ← 需要安装的东西清单
└── .github/workflows/pages.yml  ← 自动发布流水线
```

日常写博客，只需要碰 `content/` 这一个文件夹。

## 四、怎么写一篇文章

在 `content/posts/` 里新建一个文件，比如 `my-first-post.md`，内容这样写：

```
Title: 文章标题
Date: 2026-11-15 20:00
Category: 随笔
Tags: 生活, 旅行
Slug: my-first-post
Summary: 一两句话的摘要，会显示在首页列表里。

这里开始写正文，支持 Markdown。

## 小标题

一段文字。**加粗**，[一个链接](https://example.com)。

![图片说明]({static}/images/2026/photo.jpg)
```

开头几行叫“头部信息”，每行一个 `名字: 值`，写完空一行再开始正文：

| 字段 | 作用 | 必填吗 |
|---|---|---|
| Title | 标题 | 必填 |
| Date | 发布时间，北京时间 | 必填 |
| Category | 分类，一篇只能一个 | 建议填 |
| Tags | 标签，可以多个，用逗号隔开 | 选填 |
| Slug | 网址里的英文名，不写就用标题自动生成 | 建议填英文 |
| Summary | 摘要 | 选填 |

文章网址的格式是 `年/月/Slug.html`，比如这篇就是 `/2026/11/hello-world.html`。

**图片**：把图片放进 `content/images/2026/`，文中用 `{static}/images/2026/文件名.jpg` 引用。`{static}` 是 Pelican 的写法，它会自动换成正确的地址。图片记得先压缩一下，手机原图动辄好几 MB，打开会很慢。

## 五、不用电脑也能发

**方法一：直接在 GitHub 网页上发。** 手机浏览器打开仓库，进 `content/posts`，点 **Add file → Create new file**，文件名填 `xxx.md`，贴上头部信息和正文，点 **Commit changes**。一两分钟后网站就更新了。

**方法二：电脑上用编辑器写好再推。** 熟悉 Git 的话，本地写完 `git push` 就行。

提交之后，可以在仓库的 **Actions** 标签页看到一个正在跑的任务，绿色对勾就是发布成功，红叉就是出错了，点进去能看原因。最常见的错误是头部信息格式写错，比如冒号用了中文全角“：”。

## 六、在自己电脑上预览（可选）

想发之前先看看效果，可以在电脑上装 Python，然后：

```
pip install -r requirements.txt
pelican content -l -r
```

打开浏览器访问 `http://localhost:8000` 就能看到。`-r` 表示改了文件自动重新生成，`-l` 表示开一个本地预览服务器。

## 七、自动发布是怎么回事

`.github/workflows/pages.yml` 是一份“流水线说明书”，每次有提交推到 `master` 分支，GitHub 就照着它做这几步：

1. 准备一台临时的 Linux 机器，装好 Python 3.12；
2. `pip install -r requirements.txt` 装上 Pelican 和插件；
3. `pelican content -s publishconf.py -o output` 生成整个网站；
4. 用 Pagefind 给全站建搜索索引；
5. 把新文章同步到 Blogger（下面讲）；
6. 把生成好的网站交给 GitHub Pages 上线。

全程免费，一般一两分钟跑完。

## 八、主题：MassiveBlue

网站的样子由主题决定。我参考自己老站 yuge.cn 的风格，做了一个 `massiveblue` 主题，放在 `themes/massiveblue/`：

- `templates/` 里是网页模板，比如 `article.html` 是文章页、`index.html` 是首页、`base.html` 是所有页面共用的外框；
- `static/css/style.css` 是样式，颜色、字体、间距都在这里改。

几个小优化：

- **手机适配**：手机上顶栏只留导航，侧栏挪到正文下面；
- **防缓存**：样式表地址后面带一个版本号，是按 CSS 内容算出来的。改了样式，浏览器会自动拿新的，不用读者手动强制刷新；
- 每篇文章显示字数和阅读时长，文末有上一篇、下一篇和相关文章。

主题的基本信息在 `pelicanconf.py` 里改：

```
SITENAME = "Liao's Weblog"
SITESUBTITLE = "Enlarge dream, achieve future!"
TOPBAR_TEXT = "Kendy 的个人博客"
TIMEZONE = "Asia/Shanghai"
DEFAULT_LANG = "zh-CN"
LINKS = (
    ("GitHub", "https://github.com/yugecn"),
    ("yuge.cn", "http://www.yuge.cn/"),
)
```

`LINKS` 就是侧栏的“链接”，想加友情链接就往里加一行。

## 九、插件使用说明

Pelican 本身只管把 Markdown 变成网页，其他功能靠插件。安装方法都一样：

1. 在 `requirements.txt` 里加一行插件名和版本；
2. 在 `pelicanconf.py` 的 `PLUGINS` 列表里加上插件名；
3. 需要的话再加几行配置。

我现在用的是这几个：

```
PLUGINS = ["neighbors", "sitemap", "related_posts", "statistics"]
```

### 1. neighbors：上一篇 / 下一篇

- **安装**：`pelican-neighbors`
- **作用**：给每篇文章算出“上一篇”和“下一篇”，主题在文末显示成两个链接。
- **配置**：不用配置，装上就生效。

### 2. sitemap：网站地图

- **安装**：`pelican-sitemap`
- **作用**：生成 `sitemap.xml`，告诉 Google、必应网站有哪些页面，方便被搜索到。
- **配置**：

```
SITEMAP = {
    "format": "xml",
    "priorities": {"articles": 0.8, "indexes": 0.6, "pages": 0.5},
    "changefreqs": {"articles": "monthly", "indexes": "daily", "pages": "monthly"},
}
```

`priorities` 是告诉搜索引擎哪类页面更重要，`changefreqs` 是大概多久更新一次。照抄就行。想更快被收录，可以去 Google Search Console 提交 `https://你的地址/sitemap.xml`。

### 3. related_posts：相关文章

- **安装**：`pelican-related-posts`
- **作用**：根据**标签**找出相似的文章，显示在文末。
- **配置**：`RELATED_POSTS_MAX = 5`，最多显示 5 篇。
- **提示**：它靠标签匹配，所以**标签要认真打**。两篇文章有共同标签才会互相推荐。

### 4. statistics：字数和阅读时长

- **安装**：`pelican-statistics`
- **作用**：统计每篇字数，估算阅读时间，显示在标题下面，比如“约 1866 字 · 阅读约 5 分钟”。
- **配置**：不用配置。

### 5. 站内搜索：Pagefind

一开始用的是 Pelican 官方的 search 插件（背后是 Stork），后来发现它**不会给中文分词**，搜两个字的词经常搜不到，就换成了 Pagefind。

- **安装**：`requirements.txt` 里加 `pagefind[extended]`。`extended` 版本才带中文分词。
- **作用**：网站生成后，扫一遍所有网页，建一个搜索索引。读者在搜索框打字时，浏览器直接查这个索引，不需要服务器。
- **怎么启用**：它不是 Pelican 插件，而是在流水线里多跑一步：

```
python -m pagefind --site output
```

- **注意**：本地预览时没有这一步，所以本地的搜索框暂时用必应站内搜索代替；线上才是 Pagefind。

## 十、评论区和留言板：Giscus

静态博客没有数据库，评论存哪？答案是存在 GitHub 仓库的 **Discussions（讨论区）** 里，用的工具叫 Giscus。

设置步骤：

1. 仓库 **Settings → General → Features**，勾上 **Discussions**；
2. 打开 [giscus.app](https://giscus.app/zh-CN)，按页面提示给仓库安装 giscus 这个 GitHub App；
3. 在 giscus.app 页面填入仓库名，选一个讨论分类（我用 Announcements，这样只有我能新建讨论，读者只能回复，防止乱发帖）；
4. 页面最下面会生成一段代码，里面有 `data-repo-id`、`data-category-id` 两个值，抄到 `pelicanconf.py`：

```
GISCUS_REPO = "yugecn/yugecn.github.io"
GISCUS_REPO_ID = "……"
GISCUS_CATEGORY = "Announcements"
GISCUS_CATEGORY_ID = "……"
```

这两个 ID 不是密码，公开也没关系。

主题会在每篇文章底部放上评论框。读者用 GitHub 账号登录就能评论，每篇文章自动在 Discussions 里对应一个讨论帖，你在 GitHub 上就能收到通知、回复、删除。

试过 Giscus 加 Disqus 双评论，Disqus 国内打不开还带广告，最后只留了 Giscus，也关掉了文章底部的表情反应，看着更清爽。

**留言板**就是一个独立页面，也挂 Giscus。在 `content/pages/guestbook.md` 写：

```
Title: 留言板
Slug: guestbook
Comments: yes
Comments_title: 留言

欢迎路过的朋友留下几句话。
```

`Comments: yes` 就是让这个页面也显示评论框。

## 十一、侧栏归档日历

侧栏有一个小日历，有文章的日期会高亮，点一下就跳到那天的文章。这个是主题自己做的，配置在 `pelicanconf.py`：

```
DIRECT_TEMPLATES = ["index", "tags", "categories", "authors", "archives", "calendar"]
CALENDAR_SAVE_AS = "calendar.json"
YEAR_ARCHIVE_SAVE_AS = "{date:%Y}/index.html"
MONTH_ARCHIVE_SAVE_AS = "{date:%Y}/{date:%m}/index.html"
DAY_ARCHIVE_SAVE_AS = "{date:%Y}/{date:%m}/{date:%d}/index.html"
```

意思是：生成一份 `calendar.json`，记录哪天有文章；再生成按年、按月、按日的归档页。日历用这份数据画出来，点日期就打开当天的归档页。

## 十二、RSS 订阅

`publishconf.py` 里这两行负责生成订阅源：

```
FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"
```

读者把 `https://yugecn.github.io/feeds/all.atom.xml` 加到 RSS 阅读器里，就能收到新文章。顶栏右边的“RSS”就是它。

## 十三、自动同步到 Blogger

这是后来加的：每次发新文，全文自动发一份到我的老 Blogger。流程最后一步跑 `tools/blogger_sync.py`，需要三把 Google 授权钥匙。详细过程和踩过的坑单独写了一篇：[把 Pelican 博客全文自动同步到 Blogger]({filename}sync-to-blogger.md)。

这里只强调一点：**钥匙、密码一律放在仓库 Settings → Secrets and variables → Actions 里**，流水线运行时才读取，网页上谁也看不到，绝不写进代码。

## 十四、常见问题

**提交了，网站没变？** 先去 Actions 看是不是还在跑，或者是不是红叉。确认成功后，浏览器缓存可能还是旧的，手机上下拉刷新，电脑按 Ctrl+F5。

**仓库网页上提示“文件夹太多只显示 1,000 个”？** 只是网页显示限制，文件都在。图片多了按年份分文件夹就好。

**仓库会不会被撑爆？** GitHub 建议仓库小于 1 GB、单个文件小于 100 MB。纯文字写一辈子也用不完，主要是控制图片大小。

**能不能用自己的域名？** 能。买个域名，在 Settings → Pages 里填上，再去域名商那里加一条 CNAME 记录指向 `用户名.github.io` 就行。

**中文标题网址会变成乱码？** 所以建议每篇都写一个英文 `Slug`。

## 十五、一点体会

折腾下来，最喜欢的是**内容完全在自己手里**：每篇文章就是一个文本文件，存在 GitHub 上，有完整的修改历史，想搬到哪都行。老博客丢过一次，这次再也不想把文字交给别人保管了。

你好，世界。
