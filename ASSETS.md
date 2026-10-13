# 图片、字体与第三方组件

根目录的 MIT 许可证适用于本项目自行编写的程序代码和文档，不覆盖第三方图片、字体、依赖组件或动漫角色的权利。

## 360 张头像

| 素材 | 数量 | 来源说明 |
| --- | ---: | --- |
| 摄影 | 232 | Unsplash；每张作者、原图链接与许可链接见 `public/assets/all-photo-avatars.json`，使用遵循对应素材许可 |
| AI 原创图片 | 68 | 建库时一次性生成；图片记录见 `public/assets/all-generated-avatars.json`，写真人像为虚构人物 |
| 日本动漫角色 | 60 | AniList 角色资料库；每张角色、作品和来源见 `public/assets/anime-avatars.json`，原作品及图片权利归相应权利人 |

动漫来源记录不代表商业使用授权，也不将动漫图片重新许可为 MIT。使用者可以替换头像库或上传自己的图片。

## 其他资源

- 通知栏数字字体：Inter / Roboto，SIL Open Font License 1.1。许可证原文保存在 `public/assets/status-bars-v2/inter-OFL.txt`、`roboto-OFL.txt`；来源在 `font-sources.json`。
- 通知栏网络图标与点赞图标：建库时生成并校正，运行时不调用 AI。记录见 `sprite-sources.json` 和 SVG 文件。
- JSZip：第三方组件按其许可证使用；许可证原文见 `public/assets/jszip-LICENSE.markdown`，版本见 `public/assets/dependencies.json`。
- 应用中的商标、品牌名称和 UI 风格示意不表示获得相关品牌的认可或授权。

完整的逐张素材来源也可以在本地打开 `/credits.html` 查看。
