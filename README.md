# 圈图 · Moments Studio

在浏览器中粘贴文案、选择头像和手机画布，实时预览并导出朋友圈风格的长图。图片排版在浏览器本地完成，日常使用不调用 AI，也不需要数据库、API 密钥或付费服务。

## 在线使用

**[打开圈图 · GitHub Pages](https://schrieeeffer.github.io/moments-studio/)**

网站由 GitHub Pages 免费托管，通过 HTTPS 访问。全部功能使用静态 HTML、CSS、JavaScript 和本地素材，不需要运行 Node.js 服务器；文案、上传图片与草稿仍在访问者自己的浏览器中处理。

`.github/workflows/pages.yml` 在推送到 `main` 后自动发布 `public/`，也可在 Actions 中手动运行。Fork 后需在仓库 Settings → Pages 中选择 GitHub Actions。资源路径同时支持网站根目录和 `/仓库名/` 子目录，可直接用于其他项目站点；仓库中 README 的在线地址需自行更新。

## 功能

- 360 张内置头像：232 张摄影、68 张一次性生成的 AI 图片、60 张日本动漫角色头像；支持 8 个分类和上传自己的头像。
- 发布文案、两条评论与可选链接卡片；用户输入原样保留。
- 5 种常见长屏比例，长文案自动延长画布。
- 14 款通知栏，支持手动选择以及时间、电量和风格随机。
- 可选择随机发布者、昵称、点赞头像、点赞人数和画布尺寸。
- 一键生成 1–50 张图片，导出单张 PNG 或包含图片与方案信息的 ZIP。
- 可选示例水印；预览和导出共用同一套渲染逻辑。
- 本地草稿、移动端界面、逐张素材来源说明。

此工具用于文案排版与界面示例；生成的头像、时间和互动数量是设定值，不代表实际社交互动。

## 快速开始

安装 [Node.js](https://nodejs.org/) 22 或更高版本，然后：

```sh
git clone https://github.com/schrieeeffer/moments-studio.git
cd moments-studio
node server.cjs
```

打开 <http://localhost:8088>。所有运行素材已包含在仓库中，启动时无需安装依赖或下载图片。

### 修改端口

macOS / Linux：

```sh
PORT=8089 node server.cjs
```

Windows PowerShell：

```powershell
$env:PORT = '8089'
node server.cjs
```

服务仅提供 `public/` 内的静态文件以及 `/healthz`。它默认监听所有网络接口；公网部署时请自行配置域名、HTTPS 和反向代理。systemd 模板见 [deploy/moments-studio.service.example](deploy/moments-studio.service.example)，使用前需修改账户及目录。

## 批量规则

- 默认时间范围为 11:00–22:00，可在界面中调整。
- 评论时间带“昨天”前缀，第二条比第一条晚 1 或 2 分钟。
- 每张图使用 6–35 个不重复的点赞头像。
- 单批 1–50 张；手机建议每批不超过 20 张，电脑不超过 50 张。
- 单批电量不重复；开启身份随机时，发布者头像和昵称也不重复。选项少于批量数量时，通知栏、画布尺寸等字段会轮换使用。
- 随机头像范围可选全部 360 张、本次替换 200 张、保留 100 张或日本动漫 60 张。

## 开发与验证

维护静态依赖和头像清单时：

```sh
npm ci
npm run check
npm run assets
python scripts/build-avatar-credits-v3.py
```

运行阶段只需要 Node.js；Python 仅用于素材维护及验证。浏览器测试需要 Python、Playwright 和 Pillow：

```sh
python -m pip install playwright pillow
python -m playwright install chromium
python scripts/test_app.py http://localhost:8088
python scripts/test_avatar_expansion.py http://localhost:8088
python scripts/test_anime_avatars.py http://localhost:8088
```

其他检查见 `scripts/test_status_bars.py`、`test_status_sprites.py` 和 `test_flexible_batch.py`，可使用相同的地址参数。测试导出保存在 `test-output/`，不加入 Git。

验证纯静态子目录托管（两个终端分别运行）：

```sh
python scripts/serve-static-preview.py --port 17888 --prefix /moments-studio/
python scripts/test_static_paths.py http://localhost:17888/moments-studio/
```

该预览只提供静态文件，不运行项目的 Node.js 服务。现有浏览器测试也可使用带子目录的地址。

## 项目结构

```text
public/                界面、Canvas 渲染代码及运行所需素材
  assets/avatars/       360 张 256×256 JPEG 头像
  assets/icons/         点赞与底部评论栏图标
  assets/status-bars-v2/ 通知栏网络图标、字体和来源记录
scripts/                构建、验证和素材维护脚本
deploy/                 通用 systemd 服务模板
server.cjs              无第三方运行依赖的静态服务
ASSETS.md               图片、字体与第三方组件说明
```

素材采集和 AI 导入脚本只用于维护，不在网站运行时执行。开发时的原始截图、未采用候选图、AI 原稿和本机部署打包脚本未公开；部分维护脚本需要自行准备 `source-assets/` 中的输入。已发布的 360 张头像和全部运行素材均包含在仓库中。

## Git 与文件大小

本仓库使用普通 Git，**没有启用 Git LFS**。网站运行文件合计约 8.25 MiB，单个素材较小。`node_modules/`、`source-assets/`、`test-output/`、压缩包、环境变量文件和本机服务配置均已忽略；克隆后不需要 `git lfs pull`。

## 隐私

文案、上传头像和封面仅在当前浏览器中处理，没有文件上传接口。草稿存于浏览器本地存储，可通过“重置示例”清除。静态服务器不保存这些内容；这不包含托管环境可能产生的基础访问日志。

## 许可证与素材

项目代码和自行编写的文档采用 [MIT License](LICENSE)。第三方图片、字体、组件和动漫角色的权利不由 MIT 许可证覆盖，详见 [ASSETS.md](ASSETS.md) 与运行后可访问的 `/credits.html`。

摄影图保留逐张作者、原图与 Unsplash 许可链接。动漫角色图保留作品、角色与 AniList 来源记录；来源记录不代表商业使用授权，原作品及图片权利归相应权利人。需要其他授权范围时，可以替换内置头像库。
