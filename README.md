# Kendy 的博客

用 [Pelican](https://github.com/getpelican/pelican) 生成、GitHub Pages 托管的个人博客。

- 写文章：在 `content/posts/` 新建 `.md` 文件（开头写 Title、Date、Category、Tags）。
- 独立页面：放在 `content/pages/`。
- 图片：放在 `content/images/`，文中用 `![说明]({static}/images/文件名.jpg)` 引用。
- 推送到 master 后，GitHub Actions 自动构建并发布。

本地预览：

```
pip install -r requirements.txt
pelican content -l -r
```
