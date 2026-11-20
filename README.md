# Fusion Reverse Modeling

面向 Autodesk Fusion / Fusion 360 的精准逆向建模 Skill。一个入口，两种模式：**按工程图建模**，或**确定型号后主动搜索、标定照片并重建**。

An evidence-driven product reconstruction skill for Autodesk Fusion: dimensioned drawings or official research plus calibrated photographs. English skill instructions; Chinese usage guide below.

## 一句话总结

把产品逆向建模整理成一条可复用的流程：**确定型号 → 收集尺寸证据 → 建立参数与组件 → 在 Fusion 中建模 → 核对最终实体与参考图 → 交付可编辑模型和验证记录**。

适合把手机、电脑、外壳等真实产品从工程图或照片还原成 CAD，也适合只修正现有模型的指定细节。它是给 AI 代理使用的工作方法与辅助工具，不是输入一张图片就能自动生成精确模型的软件。

## 工作流总览

| 阶段 | 具体做什么 | 留下什么 |
|---|---|---|
| 识别产品 | 确认型号、年份、版本、姿态、单位和坐标方向 | 明确的建模范围与基准 |
| 整理证据 | 有图纸读尺寸、剖面和公差；无图纸先查官方资料，再标定多视图照片 | 来源台账、尺寸表、估算与未知项 |
| 建立结构 | 先做外轮廓、主要截面和关键接口，再补局部细节 | 可编辑参数、组件和特征 |
| 在 Fusion 中执行 | 使用环境实际提供的 API、连接器或电脑控制能力 | 原生 CAD 模型与操作记录 |
| 分项验证 | 独立测量最终 BRep、对照同视角参考图，另做装配和导出检查 | 当前版本的检查结果与未解决项 |
| 交付 | 保存原生设计、所需交换格式、对比视图和证据记录 | 可继续修改、可追溯的成果 |

## 它解决什么

有工程图时，读取尺寸、基准、剖面与公差，先建立外轮廓和关键接口，再做细节；未标注的倒角不会被当成已验证尺寸。

没有工程图时，主动搜索准确型号的官方规格、维修手册、零件图和多角度照片，再用第三方实测补充。记录照片标定、尺寸推导与不确定性；缺少隐藏结构证据时，不用通用机构冒充真实结构。

已有模型只修改用户指出的问题。使用真实组件和装配关系；分别检查最终实体尺寸、参考图一致性、运动干涉和文件导出。避免把“能转动、无干涉”当成“完全还原”。

## 安装

需要可使用 Skill 的代理环境，以及可控制的 Autodesk Fusion。此包**不包含 Fusion 控制插件或通用建模引擎**：代理使用当前环境已有的连接器/API，或电脑控制工具与 Fusion 原生 Python 控制台。辅助脚本只需要 Python 3.9+，无第三方依赖。

先获取这个公开仓库：

```sh
git clone https://github.com/hanyu040304/fusion-reverse-modeling.git
cd fusion-reverse-modeling
```

也可以在 GitHub 仓库页面选择 **Code → Download ZIP**，解压后打开仓库目录。

将 `skills/fusion-reverse-modeling` 整个文件夹复制到代理配置的 skills 目录。以 macOS / Linux 上 Codex 的个人目录为例，在仓库根目录运行；已有同名技能时先比较内容或备份，避免覆盖自己的修改：

```sh
mkdir -p ~/.codex/skills
cp -R skills/fusion-reverse-modeling ~/.codex/skills/
```

Windows PowerShell（同样先检查有无同名安装）：

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse .\skills\fusion-reverse-modeling "$env:USERPROFILE\.codex\skills\"
```

如果你的客户端使用 `~/.agents/skills` 或项目内 `.agents/skills`，复制到对应目录即可。重新加载 Skill 或打开新对话后，用下面的名称调用。公开仓库网址可直接发给使用者，安装时只需复制技能子目录，无需复制整套测试记录。

## 用法

有工程图：

```text
$fusion-reverse-modeling
根据我提供的工程图，在 Fusion 中还原这个产品。
先核对尺寸与基准，重点保证充电口位置和整机外轮廓。
提供可编辑原生文件、STEP、尺寸来源和验证结果。
```

没有工程图：

```text
$fusion-reverse-modeling
给 2024 款 14 英寸 MacBook Pro，基础 M4，银色建立整机模型。
主动查找官方资料，再结合多视图照片和实测信息重建。
重点是充电口位置、外轮廓和真实铰链；估算处说明误差与依据。
```

修正已有模型：

```text
$fusion-reverse-modeling
检查当前模型，只修正铰链和键盘丝印，保留已确认的机壳及接口。
先查真实结构与字体比例的参考，检查最终实体和同视角对照。
```

## 包含的内容

- `SKILL.md`：自动选择工程图、照片或混合证据路线。
- `references/`：两种路线、Fusion 执行、尺寸证据记录规范。
- `scripts/evidence_tools.py`：尺寸记录核对、同平面图像长度标定。
- `examples/`：虚构产品的 JSON 示例，不包含用户模型或厂商图纸。
- `tests/`、`evals/`、`VALIDATION.md`：辅助脚本测试和流程评估记录。

辅助脚本示例（从仓库根目录）：

```sh
python3 skills/fusion-reverse-modeling/scripts/evidence_tools.py audit skills/fusion-reverse-modeling/examples/drawing.json
python3 skills/fusion-reverse-modeling/scripts/evidence_tools.py calibrate --reference-mm 100 --reference-px 1000 --feature-px 200 --reference-uncertainty-mm 0.1 --pixel-error-px 1
python3 -m unittest discover -s tests -v
```

示例故意包含未解决的关键倒角，因此第一条命令返回 2；这表示关键项仍待确认。返回 0 也不代表实物精度认证。脚本只核对输入记录，不能读取 Fusion、认证来源或自动证明照片标定正确。

## 精度与验收

输出区分“有来源并检查的尺寸”“照片估算”“未知项”。图纸公差、CAD 检查容差和测量不确定性分别记录。照片通常不能唯一确定隐藏结构，不能承诺每个细节都达到工厂尺寸。

当前验证范围见 [VALIDATION.md](VALIDATION.md)：流程情景评估和辅助脚本测试，不等于在所有 Fusion 版本上完成实机建模测试。欢迎用自己的图纸、实测数据和 Fusion 版本补充可复现案例。

## 开源与贡献

原创 Skill、代码和虚构示例采用 [MIT License](LICENSE)。仓库不分发 Apple 或其他厂商的工程图、照片、商标素材，也不包含用户的 CAD 文件。研究时记录原始来源链接，公开案例前确认素材可公开。

提交改进时请说明：问题情景、证据、预期行为、实际行为及验证方式；新增脚本修改请运行测试。不要把来源不明的细节标为精确尺寸。
