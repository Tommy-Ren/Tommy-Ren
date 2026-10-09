# 维护这张个人主页

主页入口是根目录的 `README.md`。图片均在 `assets/`，没有统计卡片图片服务、访问计数器或额外 API Key 依赖。

## 更新内容

- 学历、经历、介绍文字：编辑 `README.md`。
- 联系方式：使用简历提供的 SFU 邮箱和 LinkedIn；修改时搜索整个 README。
- README 聚焦个人介绍、技术方向与联系方式；项目展示留在个人网站中。
- 横幅与技术栈：编辑脚本中的 `hero()` 和 `stack()`，再生成图片。
- 网站上线后，可在顶部和底部联系区添加 `https://tommy-ren.github.io/`。
- 简历与求职信原件保留在仓库外；主页没有电话号码或求职信中的申请公司信息。

## 本地生成

需要 Python 3.11 或以上，无须 pip 依赖。在仓库目录运行：

```powershell
python scripts/build_profile.py
```

默认使用 `assets/profile-data.json` 中保存的公开数据，可以离线生成。

刷新 GitHub 数据：

```powershell
python scripts/build_profile.py --refresh
```

可选环境变量 `GITHUB_TOKEN` 只用于 API 认证，不会写入生成文件。用户名固定为 Tommy-Ren。

统计口径：公开仓库数包含 fork；原创仓库数排除 fork；语言图按有主要语言的原创仓库数量统计，不代表熟练程度或代码行数。贡献图来自 GitHub 公开贡献日历，未来日期留空。扫描动画只是视觉装饰，不代表实时活动。

## 自动更新

工作流在每天 09:23 UTC、脚本修改推送到 main，以及手动运行时更新图片。温哥华夏令时约为 02:23，冬令时约为 01:23；任务可能延迟。

推送后打开 **Actions → Refresh profile artwork → Run workflow** 可以立即刷新。使用仓库自带的 `GITHUB_TOKEN`，通常不需要新增 secret。如仓库规则禁止 Actions 写 main，需调整提交流程；本地图片仍可展示。公开仓库连续 60 天没有活动时，定时工作流可能被 GitHub 停用，可到 Actions 重新启用。

贡献数据采用 GitHub 的公开日历 HTML。若 GitHub 更改结构，刷新会报错并保留上次成功生成的图，可按错误更新解析器。刷新先完整获取和校验数据，再更新快照。

## 设计来源

研究了 [BEPb/BEPb](https://github.com/BEPb/BEPb) 的 SVG 横幅、徽章、贡献动画与定时更新思路。本主题的插画、排版、脚本均重新制作，没有复制其个人资料、奖项或统计数据。

SVG 动画支持 `prefers-reduced-motion`。禁用动画时仍显示完整姓名和贡献日历。
