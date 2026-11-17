Title: 把 Pelican 博客全文自动同步到 Blogger
Date: 2026-11-17 15:20
Category: 折腾
Tags: Pelican, Blogger, GitHub Actions, 建站
Slug: sync-to-blogger
Summary: 主站在 GitHub Pages，每次发新文自动把全文推到 yugecn.blogspot.com，记录一下思路和踩过的坑。

主站搬到 GitHub Pages 之后，我那个老 Blogger（[yugecn.blogspot.com](https://yugecn.blogspot.com/)）就闲着了。与其让它荒着，不如让它当个镜像：这边发一篇，那边自动出现一篇。

## 想要的效果

- 全文同步，不是摘要加“阅读全文”链接
- 不加“本文首发于……”之类的注记
- 只同步以后的新文，主站旧文不搬
- 改了文章，Blogger 那边跟着更新，而不是再发一篇

全文同步的代价心里有数：同一篇内容出现在两个站，Google 只会挑一边收录。无所谓，两边都是我的。

## 思路

博客本来就是 push 到 `master` 后由 GitHub Actions 构建、部署，只要在部署流程最后加一步：

1. Pelican 构建完，脚本读 `output/` 里每篇文章的 HTML，取出正文部分；
2. 把正文里的图片、链接改成主站的绝对地址（Blogger 那边不存图，直接引用主站的）；
3. 调 Blogger API v3：没发过的新建，发过且内容变了的更新；
4. 用一个 `.blogger-sync.json` 记下每篇对应的 Blogger 文章 ID 和内容指纹，下次就知道该跳过还是更新。

分类和标签变成 Blogger 的标签，发布时间沿用文章自己的 `Date`。脚本放在 `tools/blogger_sync.py`，工作流里大概长这样：

```yaml
- name: Sync new posts to Blogger
  if: github.event_name == 'push'
  continue-on-error: true
  env:
    BLOGGER_CLIENT_ID: ${{ secrets.BLOGGER_CLIENT_ID }}
    BLOGGER_CLIENT_SECRET: ${{ secrets.BLOGGER_CLIENT_SECRET }}
    BLOGGER_REFRESH_TOKEN: ${{ secrets.BLOGGER_REFRESH_TOKEN }}
  run: python tools/blogger_sync.py
```

`continue-on-error` 是故意的：Blogger 那边万一出问题，不能拖累主站部署。

## 三把钥匙

脚本要替我往 Blogger 发文，得有 Google 的授权，一共三样东西，都存在仓库的 Settings → Secrets and variables → Actions 里，不进代码：

- `BLOGGER_CLIENT_ID`：OAuth 客户端 ID
- `BLOGGER_CLIENT_SECRET`：客户端密钥
- `BLOGGER_REFRESH_TOKEN`：刷新令牌，脚本每次用它换临时访问令牌

拿钥匙的步骤：

1. 去 Google Cloud 控制台新建一个项目，在「API 和服务 → 库」里启用 Blogger API v3；
2. 配置 OAuth 同意屏幕，用户类型选「外部」，然后**一定要点「发布应用」改成正式版**。停在测试状态的话，刷新令牌 7 天就失效；
3. 新建 OAuth 客户端，类型选「Web 应用」，重定向 URI 填 `https://developers.google.com/oauthplayground`，记下 ID 和密钥；
4. 打开 [OAuth Playground](https://developers.google.com/oauthplayground)，右上角齿轮里勾上「Use your own OAuth credentials」并填入 ID 和密钥，再授权 Blogger 权限，换出 Refresh token。

## 踩过的坑

**令牌被 Google 拒绝（invalid_grant）。** 第一次拿到的刷新令牌死活用不了。原因是 Playground 齿轮里「Use your own OAuth credentials」没勾，令牌其实是发给 Google 自己的测试客户端的，跟我的客户端对不上。

**齿轮里找不到保存按钮。** 本来就没有，填完自动生效，点 Close 就行。

**授权完了却没有 Refresh token。** 齿轮里还有两个选项：Access type 要选 Offline，Force prompt 选 Consent Screen。还不行就去 Google 账号的「第三方应用」里删掉旧授权再来一遍。

**客户端对不上号。** 折腾中途删过一个客户端又新建了一个，GitHub 里存的还是旧 ID。三把钥匙必须来自同一个客户端：ID、密钥、以及用这对 ID 和密钥换出来的令牌，缺一不可。

**密钥只能看一次。** 客户端密钥创建后，后台只显示末尾几位，再也看不到全文。创建时就该直接填进 GitHub。

**通行密钥那一步只能本人来。** 授权时 Google 要求用通行密钥确认身份，这步只能自己在电脑上点。

## 结果

三把钥匙对上之后，先在 Blogger 上建了个草稿再删掉，读写都通。这篇就是第一篇真正走这条路的文章：在主站发布，几分钟后 Blogger 上也会有一份。

以后的打算，是把饭否和 X 的内容也收回自己的博客里，不过那是另一篇文章的事了。
