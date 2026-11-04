# 同对象提示词视觉词典

[新手逐步使用指南](USER_GUIDE.md) · [用途与适用人群介绍](INTRODUCTION.md)

`same-object-visual-dictionary` · 独立技能仓库 · MIT

适合：整理风格对比图、提示词案例的设计师与教学作者

## 解决什么问题

把同一参考对象的不同图片变体并排展示，保留提示词和来源状态，便于比较、复制和复用。

## 安装

```sh
python -m pip install -r requirements.txt   # 只有 Pillow
python scripts/build_gallery.py examples/manifest.json output-gallery   # 跑自带的合成示例
```

作为技能使用时，把整个目录放进 `%USERPROFILE%\.workbuddy\skills\` 即可，无额外安装步骤。

## 快速开始

Python 3.10+ 和 Pillow：python -m pip install -r requirements.txt。

在本仓库根目录运行：

```sh
python scripts/build_gallery.py examples/manifest.json output-gallery
```

## 输入与输出

**输入**：anchor 图片、variants 数组；每项包含相同 anchor、image、prompt、status。图片必须在 manifest 目录内，输出目录必须不存在。

**输出**：本地网页和 images 子目录；提示词会转义显示。复制按钮依赖浏览器剪贴板权限，失败时可直接选中文字复制。

## 本次完善

原有缺口：只检查图片后缀，坏图也能进入网页；缺能直接运行的完整清单和图片样例。

已补：加入 Pillow 实际解码校验、清单字段检查、友好报错和提示词复制按钮；提供合成参考图片与 manifest。

## 适用用户

**适合：** 用 AI 生图做主图/场景图的电商运营——需要把「参考图」「生成图」「来源不明」分开存档，
以便在被平台问到时拿得出留痕；以及需要给设计外包定交付标准的人。

**不适合：** 想直接生成商品图的人（本技能不生成图片，只组织和标注已有的图与提示词）；
需要图库 SaaS 那种在线协作的人。

## 当前限制

独立Python脚本负责登记与展示，不调用生图服务；生图由宿主可用工具完成。示例已记录真实生成，但物体精确一致性和美术质量仍待使用者验收，AI目视意见不标成人工验收。没有自动调度未获授权的付费服务。

## 验证与使用注意

```sh
python -m unittest discover -s tests -v
```

测试覆盖被断言的离线行为，不等于真实平台、生产模型或业务效果验证。

示例数据和图片均为合成演示，不是真实客户、交易、销量或模型成绩。不要提交真实凭据和私有输入。

## 来源与工作记录

由 miaorrr8888-cloud 在 AI 辅助下积累和维护，来源与边界见 [PROVENANCE.md](PROVENANCE.md)，许可见 [LICENSE](LICENSE)。

[全部独立技能与阶段性工作记录](https://github.com/miaorrr8888-cloud/agent-skills-worklog)

## 第二轮：视觉人工验收记录

新增逐图人工验收清单与图片哈希；接受图片必须明确检查同一对象与文字，未检查保持待验收。

在仓库根目录运行：

```sh
python scripts/review_gallery.py examples/manifest.json examples/reviews.json
```

新增工具的输入字段见脚本参数与 examples/。快照示例采用固定日期，过期后正常返回 HOLD；需要检查新采集的页面时填写真实带时区的采集时间，不要改日期伪装新证据。

## 第三轮：真实生成图接入词典

用宿主内置图像生成工具实际生成参考杯子，再基于参考图生成换场景版本；新增输出登记，保留实际提示词、来源声明、文件哈希，并可直接生成图库。

```sh
python scripts/build_gallery.py examples/generated-mug/manifest.json generated-mug-gallery
python scripts/review_gallery.py examples/generated-mug/manifest.json examples/generated-mug/reviews.json
# 新图登记：python scripts/register_generation.py anchor.png variant.png generation.json new-case
# generation.json 必须含 prompt、provider、带时区 generated_at；可选 model（未知不猜）。
```

## 许可证

MIT，全文见 [LICENSE](LICENSE)。可商用、可修改、可再分发，保留版权与许可声明即可。

**不提供任何形式的担保。** 本技能输出的是辅助判断，不构成法律、财税或平台合规意见；
生成图片的可商用范围取决于所用模型服务条款，需使用者自行确认。

第三方依赖各自遵循其原始许可证，本项目不再分发它们的代码或模型权重，详见 `PROVENANCE.md`（如有）。

## 运行环境

| 项 | 状态 |
|---|---|
| Windows 11 + Python 3.12 / 3.13 | ✅ 实测通过 |
| Linux / macOS | ⚠️ **未实测**。代码用 `pathlib`，无硬编码分隔符，理论上可跑，但测试只在 Windows 跑过，不声称支持 |

诚实标注：没实跑过的平台，不要在对外文案里写「已支持」。
