# 同一对象的提示词对比图库：用户使用指南

## 它能帮你做什么

把参考对象与变体整理成网页图库，保留提示词、来源状态、文件指纹和验收记录；可登记宿主生图工具的实际输出。

## 适合谁

设计师、图片创作者、提示词学习者和需要整理案例库的教学作者。

## 具体解决什么问题

生成了很多图片，但参考图、提示词和来源散落各处，不方便并排比较和复用。

**不适合这些目标：**独立Python脚本自动生图、保证每张图片物体完全一致、自动证明生成来源与版权。

## 下载与准备

- [打开独立仓库](https://github.com/miaorrr8888-cloud/same-object-visual-dictionary)
- [直接下载源码ZIP](https://github.com/miaorrr8888-cloud/same-object-visual-dictionary/archive/refs/heads/main.zip)

也可在仓库页面点 Code → Download ZIP。解压后打开包含 SKILL.md、README.md、USER_GUIDE.md 的那层文件夹。不要停在外层目录或只复制一个脚本。

建议使用Windows电脑和Python 3.12；这是本次验证环境。先在该文件夹打开PowerShell，再执行：

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe --version
```

这里直接使用虚拟环境里的Python，不需要运行激活脚本或修改系统执行策略。安装步骤及其他系统说明见[通用安装说明](https://github.com/miaorrr8888-cloud/agent-skills-worklog/blob/main/INSTALLATION.md)。

安装本示例需要的依赖：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 第一次使用：先跑自带示例

打开本次真实生成的杯子参考图与换场景版本，生成对比网页并查看待验收记录。

```powershell
.\.venv\Scripts\python.exe scripts/build_gallery.py examples/generated-mug/manifest.json reader-demo-gallery
.\.venv\Scripts\python.exe scripts/review_gallery.py examples/generated-mug/manifest.json examples/generated-mug/reviews.json
```

## 结果怎么看

新建 reader-demo-gallery/index.html 与 images 目录。双击HTML可看图和提示词；验收示例仍为 needs_review，不能当成人工已接受。

## 换成自己的资料

manifest.json 写 anchor 和 variants；每个变体填相同anchor、image、prompt、status。图片须在清单目录内。

把自己的参考图和变体放到同一工作目录，复制示例清单再改相对路径和实际提示词。需要新图时，让有生图能力的宿主生成后登记；未知模型名保留未披露。

## 不想手动敲命令：给AI助手的任务

以下任务适用于能读取所选目录、执行本地命令的助手。WorkBuddy需要先确认当前版本的权限与技能启用状态；本项目未完成WorkBuddy实际导入验收。

```text
请先读取我选定文件夹中的 SKILL.md 和 USER_GUIDE.md，只在该项目范围内处理。
读取自带的generated-mug清单，生成新的本地对比图库。说明参考图、提示词、来源声明和待验收状态分别是什么。不要调用额外付费生图服务；不要将AI目视意见改成人工验收通过。
缺少依赖时先说明用途，优先放进本项目虚拟环境；不要读取其他目录中的密码、密钥或浏览器登录数据。
```

## 常见问题

**输出目录已存在**

改用 reader-demo-gallery-2 等新目录，工具会保护已有结果。

**网页有字但没有图**

连同images目录一起保留或复制，不要只移动index.html。

**找不到文件或脚本**

确认终端当前目录就是包含SKILL.md的技能根目录；路径含空格时加双引号。输出目录已存在时换新名字，不覆盖已有结果。

## 当前能力边界

图库与登记脚本不直接调用生成服务。配套案例是真实生图，但对象精确一致性与美术质量需使用者验收；AI目视意见不能标成人工验收。

## 验证范围

本指南示例已在Windows独立副本中运行复核，见[命令复核结果](https://github.com/miaorrr8888-cloud/agent-skills-worklog/blob/main/USER_GUIDES_VERIFICATION.md)。已有回归测试只覆盖被测试行为，不证明真实业务结果。WorkBuddy实际运行、手机端使用和所有系统版本均不在本次已验证范围内。

许可证和素材来源分别见 [LICENSE](LICENSE)、[PROVENANCE.md](PROVENANCE.md)。
