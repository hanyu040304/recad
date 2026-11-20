# 使用 ReCAD

ReCAD 面向真实产品的逆向建模，当前执行端为 Autodesk Fusion。工程图、照片、实测尺寸和已有模型都可以作为输入。

## 安装

需要支持 Skill 的代理环境、Autodesk Fusion，以及代理可用的 Fusion 连接器/API 或电脑控制能力。包内不包含 Fusion 控制服务器。辅助脚本需要 Python 3.9+，无第三方依赖。

从 [Releases](https://github.com/hanyu040304/recad/releases/latest) 下载 `recad-skill.zip` 并解压。将其中的 `fusion-reverse-modeling` 文件夹复制到代理的 skills 目录。已有同名安装时，先备份或比较内容。

也可以克隆仓库：

```sh
git clone https://github.com/hanyu040304/recad.git
cd recad
```

macOS / Linux，在仓库根目录运行：

```sh
mkdir -p ~/.codex/skills
cp -R skills/fusion-reverse-modeling ~/.codex/skills/
```

Windows PowerShell，在仓库根目录运行：

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse .\skills\fusion-reverse-modeling "$env:USERPROFILE\.codex\skills\"
```

如果客户端使用 `~/.agents/skills` 或项目内 `.agents/skills`，复制到对应目录。重新加载技能或打开新对话后，用 `$fusion-reverse-modeling` 调用。

ReCAD 是项目展示名；技能目录和调用名保留 `fusion-reverse-modeling`，已有使用方式继续有效。

## 使用示例

### 有工程图

```text
$fusion-reverse-modeling
按这份支架工程图在 Fusion 中建模。
以安装面为基准，核对孔距、板厚和折弯轮廓。
交付可编辑原生文件、STEP 和尺寸检查结果。
```

### 只有照片和实测尺寸

```text
$fusion-reverse-modeling
根据这组照片和外形尺寸，还原这个手持仪器的外壳。
先查准确型号的官方规格，再结合多视图重建。
重点核对接口和拼缝；估算处注明依据与误差范围。
```

### 修正已有模型

```text
$fusion-reverse-modeling
只修正当前装配体的转轴位置，保留已确认的壳体和安装孔。
先核对结构参考，再检查最终实体、运动范围和干涉。
```

## 建模原则

- 先确认准确型号、单位、基准和坐标方向。
- 工程图中明确标注的尺寸优先于图片比例。
- 先建立外轮廓、主要截面和关键接口，再补局部细节。
- 尺寸来源、照片估算、推导值和未知项分别记录。
- 独立测量最终实体，并将尺寸、外观、装配与导出分开验证。
- 提供可编辑模型与检查记录；不把运动可用当成真实机构已还原。

## 辅助工具

以下命令从仓库根目录运行：

```sh
python3 skills/fusion-reverse-modeling/scripts/evidence_tools.py audit skills/fusion-reverse-modeling/examples/drawing.json
python3 skills/fusion-reverse-modeling/scripts/evidence_tools.py calibrate --reference-mm 100 --reference-px 1000 --feature-px 200 --reference-uncertainty-mm 0.1 --pixel-error-px 1
python3 -m unittest discover -s tests -v
```

示例故意包含未解决的关键倒角，第一条命令返回 2。返回 0 也不代表实物精度认证：工具只核对输入记录，不能读取 Fusion 实体、认证来源或证明照片标定正确。

详细规范见 [证据记录](../skills/fusion-reverse-modeling/references/evidence-records.md)，已验证范围见 [VALIDATION.md](../VALIDATION.md)。

## 项目文件

- [`SKILL.md`](../skills/fusion-reverse-modeling/SKILL.md)：技能入口。
- [`references/`](../skills/fusion-reverse-modeling/references/)：工程图、照片、Fusion 执行和证据记录规范。
- [`examples/`](../skills/fusion-reverse-modeling/examples/)：虚构产品的 JSON 示例。
- [`tests/`](../tests/) 与 [`evals/`](../evals/)：脚本测试和流程评估。

## 贡献

提交问题或改进时，请附情景、证据、实际行为和预期行为。修改辅助脚本后运行测试。公开案例前确认参考素材可公开；用户 CAD 和厂商原始资料保留在自己的项目中。

原创指令、代码、工程线稿与虚构示例采用 [MIT License](../LICENSE)。
