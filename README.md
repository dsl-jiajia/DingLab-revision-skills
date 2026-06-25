# DingLab-revision-skills：
## skills的使用效果也取决于所使用模型的能力 ##
## **20260625**:本次更新一下使用的注意事项：
1. 想要使用文献调研的功能，需要先联网，让智能体自己/使用者安装相关文献检索skills（具备该功能的skills有很多）
2. prompt指令越详细越好，智能体会偷懒，这个问题目前还没有除了给出详细指令“鞭打”它以外更好的方法
3. 给智能体的相关材料（menu，数据，图表等等）也是越详细丰富越好，同时建议大家在本地进行使用，联网或许会有泄密问题（或许或许或许）
4. 一道题一道题输出比一次性给一整个文档/十几几十道题目效果要更好
## **20260623**:本次上传revision_skills_20260623.tar.gz.enc内含有2个skill：revision-response-drafter和revision-final-auditor
revision-response-drafter用于生成修回框架，可以提供题目类型/相关分析建议/文献参考建议和语言框架。

## **20260624**:本次更新了一下该skills所需的环境和解密解压方法👀👀👀📒
一、准备工作：

Codex Desktop/CLI等智能体模型  

Python >= 3.10 

PyMuPDF  

pypdf  

pdfplumber  

OpenSSL  

Internet access for literature verification（需要文献背书时需要联网）  

Local read/write permission  

Encrypted lab database for strict private-lab mode（存放于平台电脑Anydesk（475开头）的电脑"E:\Document Dataset"）


二、解压方法说明书：
```text
revision_skills_YYYYMMDD.tar.gz.enc
```

该文件包含两层：

1. `.enc`：OpenSSL 加密层；
2. `.tar.gz`：压缩归档层。

因此，必须按照以下顺序操作：

```text
.tar.gz.enc -> OpenSSL 解密 -> .tar.gz -> tar/7-Zip 解压
```
## 1. 自动解压脚本
`private_vault.py`为自动解压脚本，已经上传👌

## 2. 加密参数

发布包使用：

```text
AES-256-CBC
PBKDF2
200000 iterations
SHA-256
```

直接使用 OpenSSL 时，以下参数必须保持一致：

```text
-aes-256-cbc -pbkdf2 -iter 200000 -md sha256
```
# macOS 方法

## 3. macOS 环境准备

打开“终端 Terminal”，检查 Python、tar 和 OpenSSL：

```bash
python3 --version
tar --version
openssl version
```

Python 仅在使用 `private_vault.py` 时需要，建议 Python 3.10 或更高版本。

macOS 系统自带的 `openssl` 可能实际是较旧的 LibreSSL，并不一定支持当前 PBKDF2 参数。推荐使用 Homebrew 安装 OpenSSL 3：

```bash
brew install openssl@3
```

检查 Homebrew OpenSSL：

```bash
"$(brew --prefix openssl@3)/bin/openssl" version
```

如需让 `private_vault.py` 找到 OpenSSL 3，在当前终端执行：

```bash
export PATH="$(brew --prefix openssl@3)/bin:$PATH"
```

再次检查：

```bash
openssl version
```

应显示 OpenSSL 3.x，而不是不支持 `-pbkdf2` 的旧版本。

如果电脑尚未安装 Homebrew，需要先由成员按照实验室或单位的软件安装规范安装 Homebrew，再执行上述命令。

## 4. macOS 方法一：直接使用 OpenSSL

进入下载目录：

```bash
cd "$HOME/Downloads"
```

确认加密包存在：

```bash
ls -lh revision_skills_*.tar.gz.enc
```

使用 Homebrew OpenSSL 3 解密：

```bash
"$(brew --prefix openssl@3)/bin/openssl" enc \
  -d -aes-256-cbc -pbkdf2 -iter 200000 -md sha256 \
  -in "revision_skills_YYYYMMDD.tar.gz.enc" \
  -out "revision_skills.tar.gz"
```

将 `YYYYMMDD` 替换成实际日期和版本（即文件名）。终端要求输入密码时，输入内容不会显示，这是正常现象。

确认解密文件存在：

```bash
ls -lh "revision_skills.tar.gz"
```

创建输出目录并解压：

```bash
mkdir -p "revision_skills_extracted"

tar -xzf "revision_skills.tar.gz" \
  -C "revision_skills_extracted"
```

检查结果：

```bash
find "revision_skills_extracted" -maxdepth 3 -type f
```

也可以双击已经解密得到的 `revision_skills.tar.gz`，使用 macOS 归档实用工具解压。不要双击原始 `.tar.gz.enc` 文件。

## 5. macOS 方法二：使用自动解密脚本

确保以下文件位于同一目录：

```text
revision_skills_YYYYMMDD.tar.gz.enc
private_vault.py
README_macOS_Windows_decryption_installation.md
```

进入目录并启用 OpenSSL 3：

```bash
cd "$HOME/Downloads"
export PATH="$(brew --prefix openssl@3)/bin:$PATH"
```

执行：

```bash
python3 private_vault.py decrypt \
  --archive "revision_skills_YYYYMMDD.tar.gz.enc" \
  --out "revision_skills_extracted"
```

终端会提示：

```text
Vault passphrase:
```

输入密码时不会显示字符。该脚本会自动完成解密和安全解压。

如果输出目录已经存在且不是空目录，建议换一个新的目录。只有确认可以覆盖现有文件时才使用：

```bash
python3 private_vault.py decrypt \
  --archive "revision_skills_YYYYMMDD.tar.gz.enc" \
  --out "revision_skills_extracted" \
  --overwrite
```



---

# Windows 方法

## 6. Windows 环境准备

使用 Windows 10/11 的 PowerShell。

检查 OpenSSL：

```powershell
openssl version
```

建议使用支持以下参数的 OpenSSL 3.x：

```powershell
openssl enc -help
```

帮助信息中应能看到 `-pbkdf2` 和 `-iter`。

如果提示 `openssl is not recognized`，需要先安装 OpenSSL，并将 `openssl.exe` 所在目录加入系统 `PATH`。安装完成后，关闭并重新打开 PowerShell。

使用自动解密脚本时，还需要 Python 3.10 或更高版本：

```powershell
python --version
```

如果 `python` 不可用，可尝试：

```powershell
py --version
```

## 7. Windows 方法一：直接使用 OpenSSL

进入下载目录：

```powershell
cd "$HOME\Downloads"
```

确认文件存在：

```powershell
Get-ChildItem ".\revision_skills_*.tar.gz.enc"
```

解密：

```powershell
openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -md sha256 `
  -in ".\revision_skills_YYYYMMDD.tar.gz.enc" `
  -out ".\revision_skills.tar.gz"
```

将 `YYYYMMDD` 替换成实际日期。输入密码时屏幕可能不显示字符，这是正常现象。

确认解密文件存在：

```powershell
Get-Item ".\revision_skills.tar.gz"
```

使用 Windows 自带的 tar 解压：

```powershell
New-Item -ItemType Directory -Force `
  ".\revision_skills_extracted"

tar -xzf ".\revision_skills.tar.gz" `
  -C ".\revision_skills_extracted"
```

检查结果：

```powershell
Get-ChildItem ".\revision_skills_extracted" `
  -Recurse -Depth 3
```

也可以使用 7-Zip 打开已经解密得到的 `revision_skills.tar.gz`。7-Zip 可能需要先解开 `.gz`，再解开其中的 `.tar`。

## 8. Windows 方法二：使用自动解密脚本

确保以下文件位于同一目录：

```text
revision_skills_YYYYMMDD.tar.gz.enc
private_vault.py
README_macOS_Windows_decryption_installation.md
```

进入目录：

```powershell
cd "$HOME\Downloads"
```

使用 `python`：

```powershell
python .\private_vault.py decrypt `
  --archive ".\revision_skills_YYYYMMDD.tar.gz.enc" `
  --out ".\revision_skills_extracted"
```

或使用 Windows Python Launcher：

```powershell
py .\private_vault.py decrypt `
  --archive ".\revision_skills_YYYYMMDD.tar.gz.enc" `
  --out ".\revision_skills_extracted"
```

终端会提示：

```text
Vault passphrase:
```

输入密码时不会显示字符。脚本会自动完成解密和安全解压。

如果输出目录已经存在且不是空目录，建议换一个新的目录。只有确认可以覆盖现有文件时才使用：

```powershell
python .\private_vault.py decrypt `
  --archive ".\revision_skills_YYYYMMDD.tar.gz.enc" `
  --out ".\revision_skills_extracted" `
  --overwrite
```


---

# 通用检查与安全说明

## 9. 解压后的正确结构

正常情况下应找到：

```text
revision-response-drafter/
  SKILL.md
  agents/
  references/
  scripts/

revision-final-auditor/
  SKILL.md
  agents/
  references/
  scripts/
```


-------------
# Revision Response Drafter 使用说明

本文档说明如何使用 `revision-response-drafter` 框架生成 skill。这个 skill 用于**生成第一版高质量、可填写的修回回复框架**：语言、结构、逻辑链条、分析建议、图表建议、cover letter 和 Word 文件先搭好；尚未完成的数据分析、具体数值、图表编号和 manuscript 位置用明确占位符保留。

如果 response、cover letter、revised manuscript 和文件包已经基本完成，需要提交前质控，请使用 `revision-final-auditor`。

## 1. 什么时候使用

在以下情况使用 `revision-response-drafter`：

- 刚收到 reviewer/editor comments，需要起草 point-by-point response；
- response 还没写，或写得太短、太泛泛；
- 需要生成导师可修改的英文 response 框架；
- 需要把每条 comment 拆成多个部分回应；
- 需要根据 reviewer comment、figure menu、stable、已有 figures 判断还要补什么分析；
- 需要具体到组别、数据字段、统计模型、输出指标、图表形式和 manuscript 位置的分析建议；
- 需要主体段落写得非常详细，但结果和数值暂时留空；
- 需要文献背书、PubMed/PMID/DOI/link 候选；
- 需要 cover letter 初稿；
- 需要 Word `.docx` 可编辑文件；
- 需要给后续 `revision-final-auditor` 留 audit handoff checklist。

不要在以下情况使用：

- response 和 manuscript 已经完成，只想判断能不能提交；
- 需要做最终 package QC；
- 需要检查样本量、P value、figure/table 编号是否一致；
- 需要给最终修回包打分。

这些情况应使用 `revision-final-auditor`。

## 2. 安装方式

将两个 skill 文件夹复制到 Codex skill 目录：

```bash
mkdir -p "$HOME/.codex/skills"
cp -R revision-response-drafter "$HOME/.codex/skills/"
cp -R revision-final-auditor "$HOME/.codex/skills/"
```

安装后，重新打开 Codex 或开始一个新对话，即可使用：

```text
Use $revision-response-drafter.
```

## 3. 推荐准备的材料

材料越完整，输出越像可以直接给导师看的修回框架。

建议准备：

```text
1. Journal 名称
2. Manuscript title/topic
3. Manuscript ID, if available
4. Editor decision letter
5. Reviewer comments
6. Figure menu / result menu / revision menu
7. Figures, tables, stable, source data 路径
8. 已经完成的分析和具体数值
9. 还没完成但计划做的分析
10. 希望新增内容放到哪个 Figure/Table/Supplementary/Methods/Results
11. 是否需要严格使用实验室数据库风格
12. 是否需要 Word docx 输出
```

可以给文件夹路径，也可以直接粘贴 comments。若有 figure、stable、menu，建议提供绝对路径。

## 4. 最常用 prompt

复制下面模板，把内容补进去：

```text
Use $revision-response-drafter.

请为以下修回生成一个可填写的英文 point-by-point response framework，并输出 Word docx。

要求：
1. 每条 response 使用三段式：
   第一段：感谢 + 认可 + 分成几个 parts 回应；
   第二段：详细主体，每个小点按照自然逻辑写成 rationale -> action -> result -> conclusion，但不要出现 Rationale/To do/Results/Conclusion 机械标签；
   第三段：总结 + 再次感谢 + manuscript/figure/table backfill。
2. 对每条 comment 给出具体分析建议，具体到组别、数据字段、统计模型、输出数值、图表形式和目标位置。
3. 没有完成的分析不要假装完成，用 [[FILL: ...]]、[[VERIFY: ...]] 或 [[AUTHOR_INPUT_NEEDED: ...]]。
4. 如需要文献背书，请给出 PubMed/PMID/DOI/link 候选。
5. 最后输出 Word docx、TODO list、items to confirm、audit handoff checklist。

Journal:
[[FILL: journal name]]

Manuscript topic:
[[FILL: manuscript topic]]

Reviewer comments:
[[FILL: paste reviewer/editor comments]]

Available data:
[[FILL: available cohort, groups, variables, source data]]

Figures / tables / menu:
[[FILL: paths or descriptions]]

Completed results:
[[FILL: exact known values, if any]]

Pending analyses:
[[FILL: analyses not yet completed]]
```

## 5. 如果不知道要做什么分析

当你不知道怎么回应 reviewer、也不知道要补什么分析时，用这个 prompt：

```text
Use $revision-response-drafter.

我不知道针对这些 comments 需要做什么分析。请你根据 reviewer comments、figure menu 和现有数据，给出非常具体的 analysis recommendation matrix。

请具体说明：
1. 每条 comment 的 reviewer trust gap 是什么；
2. 应该比较哪些组；
3. 需要哪些数据字段；
4. 用什么统计模型或检验；
5. 应报告哪些数值，例如 n、AUC、OR/HR/beta、95% CI、P value、FDR、sensitivity/specificity、interaction P value；
6. 应画什么图，例如 ROC、boxplot、forest plot、Kaplan-Meier、heatmap、volcano、calibration curve、decision curve；
7. 应放到哪个 Figure/Table/Supplementary/Methods/Results；
8. 如果结果不显著或数据不可用，response 和 manuscript 应如何降调。

Reviewer comments:
[[FILL: comments]]

Available data:
[[FILL: data fields and groups]]

Figure/menu/stable:
[[FILL: paths]]

Output:
- analysis recommendation matrix
- figure/menu intake table
- point-by-point response framework
- Word docx
```

## 6. 如果需要读图和根据 menu 提建议

给出 figure、stable、legend、menu 或 source data 的路径：

```text
Use $revision-response-drafter.

请读取以下 figure/stable/menu，根据 reviewer comments 生成 response framework，并提出每条 comment 需要补什么分析和图。

Materials:
- [[FILL: /absolute/path/to/figure_or_pdf]]
- [[FILL: /absolute/path/to/stable.xlsx]]
- [[FILL: /absolute/path/to/figure_menu.docx]]

Reviewer comments:
[[FILL: comments]]

要求：
- 先输出 figure/menu interpretation；
- 再输出 detailed analysis-and-figure plan；
- 每条建议必须具体到 groups/comparisons、data fields、statistical model、output metrics、figure/table/panel target；
- 不确定的图上信息用 [[VERIFY: ...]]；
- 不要从图片中臆测精确数值。
```

## 7. 如果需要文献背书

当 reviewer 要求 rationale、机制、临床意义、统计方法合理性、field-standard practice 时，可以这样写：

```text
Use $revision-response-drafter.

请为 response 第二段加入文献背书。需要 small-peer 和 big-peer 两类支持：
1. small-peer: 尽量接近本研究疾病、样本、平台或分析任务；
2. big-peer: 支持更广泛的领域标准方法或验证策略。

请给出候选文章 title、journal/year、PMID/DOI/link、支持什么句子，并把文献逻辑自然融入 response body。

Reviewer comments:
[[FILL: comments]]

Manuscript topic:
[[FILL: topic]]
```

不要要求 skill 编造 PMID、DOI 或文章标题。无法检索或无法确认时，应使用：

```text
[[AUTHOR_INPUT_NEEDED: verify literature support and PMID/link]]
```


## 8. 输出结果如何解读

完整输出通常包含：

```text
Overall revision strategy
Response strategy summary with draft readiness
Case-style guidance used
Lab-grounded evidence advisory
Figure/menu interpretation and detailed analysis-and-figure plan
Literature support for response body
High-impact response strategy
Comment triage and evidence/action map
Fillable point-by-point response draft
Fillable cover letter draft
Data-analysis and manuscript-revision TODO list
Items to confirm before finalization
Audit handoff checklist for final review
Word output status
```

### Draft readiness

```text
draft_with_placeholders
```

说明框架已经能用，但还需要填数据、数值、图表编号或 manuscript 位置。

```text
needs_author_input
```

说明缺少关键作者信息，不补充会影响可信度。

```text
blocked
```

说明缺少核心材料，无法生成可信框架。

### 占位符

```text
[[FILL: ...]]
```

需要作者填写缺失数值或内容。

```text
[[VERIFY: ...]]
```

需要核对已有材料中是否真实存在。

```text
[[DECIDE: ...]]
```

需要作者或导师做策略决定。

```text
[[AUTHOR_INPUT_NEEDED: ...]]
```

缺少作者信息，AI 不能合理推断。

## 9. Word 输出

完整 response framework 默认建议输出 Word `.docx`。最终回复中应出现类似：

```text
Word output status:
- File: /absolute/path/to/revision_response_framework_xxx.docx
- Export method: scripts/export_response_framework_docx.py
- DOCX QA status: pass
- Placeholder status: preserved
```

如果 `DOCX QA status` 不是 `pass`，需要先修复 Word 文件再交给导师。

## 10. 输出后下一步做什么

推荐工作流：

```text
1. 用 revision-response-drafter 生成 response framework。
2. 作者/分析人员按照 TODO list 补分析、补图、补数值。
3. 把 [[FILL]]、[[VERIFY]]、[[AUTHOR_INPUT_NEEDED]] 逐一处理掉。
4. 完成 revised manuscript、figures、tables、source data。
5. 用 revision-final-auditor 做最终审核。
6. 根据 audit report 修正后再提交。
```


## 11. 常见问题

### Q1: 它会直接生成最终可提交 response 吗？

通常不会。它生成的是高质量框架。没有完成的分析、数值、图表位置和 manuscript 修改必须由作者补齐。

### Q2: 它会自动编造结果吗？

不应该。没有提供的数值必须保留为 `[[FILL: ...]]` 或 `[[VERIFY: ...]]`。

### Q3: 它会做数据分析吗？

它主要负责提出分析计划和 response 框架。若你提供数据和明确要求，它可以辅助写分析脚本或建议统计方法，但最终结果必须由作者核实。

### Q4: 需要每次都提供实验室数据库吗？

不需要。没有数据库时，它仍可用通用高质量修回模式工作。只有当你要求“严格模仿实验室数据库/实验室文章证据/老板偏好”时，才需要提供解密后的私有 runtime。

### Q5: 为什么主体段落很长？

高质量修回不能只说 “we performed additional analysis”。主体段落需要说明为什么做、做了什么、结果应该报告什么、结论意味着什么，以及补到 manuscript/figure/table 的哪里。

### Q6: 为什么不能出现 Rationale/To do/Results/Conclusion？

内部逻辑必须有，但 journal-facing response 不能像机械填表。正确写法是用自然连接词表达：

```text
This point is important because ...
In order to address this issue ...
The results showed/should report ...
Taken together ...
```



# Revision Final Auditor 使用说明

本文档说明如何使用 `revision-final-auditor` 审核 skill。这个 skill 用于**最终修回提交前质控**，不是用来起草第一版 response。若还没有写好 point-by-point response，请先使用 `revision-response-drafter`。

## 1. 什么时候使用

在以下情况使用 `revision-final-auditor`：

- response to reviewers 已经写好，需要提交前检查；
- cover letter 已经写好，需要检查是否过度承诺；
- revised manuscript、tracked manuscript、figures、supplements、source data 等文件基本齐全；
- 需要导师/PI 风格的最终 QC；
- 需要检查 reviewer 是否逐条覆盖；
- 需要检查 response 中说 “we added/revised/performed/uploaded” 的内容是否真的在 manuscript 或文件包中出现；
- 需要检查样本量、P value、AUC、HR/OR、CI、figure/table 编号、accession、ethics ID 等精确事实是否一致；
- 需要输出 Word `.docx` 审核报告；
- 需要多维度打分和综合评分。

不要在以下情况使用：

- reviewer comments 刚拿到，还没有 response draft；
- 只是想生成回复框架；
- 分析还没做，想让 AI 规划应该补什么分析。

这些情况应使用 `revision-response-drafter`。

## 2. 安装方式

将两个 skill 文件夹复制到 Codex skill 目录：

```bash
mkdir -p "$HOME/.codex/skills"
cp -R revision-final-auditor "$HOME/.codex/skills/"
cp -R revision-response-drafter "$HOME/.codex/skills/"
```

安装后，重新打开 Codex 或开始一个新对话，即可使用：

```text
Use $revision-final-auditor.
```

## 3. 推荐准备的文件

最好把最终修回文件放在一个文件夹中，例如：

```text
revision_package/
  cover_letter.docx
  response_to_reviewers.docx
  revised_manuscript.docx
  tracked_changes_manuscript.docx
  figures/
  supplementary_tables/
  supplementary_information.docx
  source_data/
  data_availability.txt
  code_availability.txt
```

至少建议提供：

```text
1. response to reviewers
2. cover letter
3. revised manuscript
4. tracked manuscript, if available
5. figures/tables/supplements/source data, if available
6. journal name and manuscript ID, if available
```

如果文件不全，也可以审，但结论会更保守，通常会出现 `Cannot verify` 或 `Not ready`。

## 4. 最常用 prompt

复制下面模板，把路径替换成自己的文件夹：

```text
Use $revision-final-auditor.

请对这个最终修回包进行提交前审核，并输出 Word docx 审核报告。

Audit requirements:
1. 检查 editor/reviewer comments 是否逐条覆盖。
2. 检查 response 里所有 "we added / revised / performed / uploaded / deposited / clarified" 是否能在 manuscript 或文件包中找到证据。
3. 检查样本量、P value、AUC、HR/OR、CI、figure/table 编号、accession、ethics ID、文件名等 exact facts 是否一致。
4. 检查 manuscript-response alignment。
5. 检查 diagnostic/prognostic/mechanistic/clinical/statistical/novelty/data-availability claims 是否证据充分。
6. 检查文字、分析、统计、实验、临床证据、图表、source data、data/code availability、file package 等多个维度。
7. 给出每个维度 0-5 分、综合 100 分、readiness verdict。
8. 最后输出 required supplementation table，说明每个维度还需要补什么。
9. 输出 editable Word docx 文件。

Journal:
[[FILL: journal name]]

Manuscript ID:
[[FILL: manuscript ID]]

Revision package path:
[[FILL: /absolute/path/to/revision_package]]
```

## 5. 只审核 response 和 cover letter 的 prompt

如果还没有完整 package，可以先做文本级审核：

```text
Use $revision-final-auditor.

请先对 response to reviewers 和 cover letter 做文本级审核。
目前没有完整 revised manuscript 和 source data，所以请明确标记哪些内容 Cannot verify。

Files:
- Response: [[FILL: /path/to/response.docx]]
- Cover letter: [[FILL: /path/to/cover_letter.docx]]

Output:
- critical findings first
- reviewer coverage audit
- evidence trace matrix
- exact-fact risk list
- claim-specific audit
- multidimensional scorecard
- required fixes
- Word docx audit report
```

## 6. 输出结果如何解读

审核报告通常包含以下部分：

```text
Verdict
Critical findings
Automation status and package manifest summary
Reviewer coverage audit
Lab-style response audit
Evidence trace matrix
Promise trace checker
Exact-fact crosscheck
Manuscript-response alignment
Claim-type-specific audit
Scientific claim and evidence audit
File package and journal-compliance audit
Multidimensional audit scorecard
Required supplementation table
Score summary
Required fixes before resubmission
Optional language polish
Unverified items
Word output status
```

### Verdict

```text
Ready
```

可以提交，只有很小的残余风险。

```text
Ready after minor fixes
```

基本可以提交，但必须先处理列出的 minor fixes。

```text
Not ready
```

不建议提交。通常存在未覆盖 reviewer、promise 没有证据、exact facts 冲突、核心文件缺失、claim 过强等问题。

```text
Cannot determine
```

文件不足，无法判断是否可提交。

### 多维度评分

每个维度 0-5 分，综合加权为 100 分。低于 4 分的维度都必须有明确补充项。

重点看：

```text
blocking dimensions
lowest-scoring dimensions
required supplementation table
required fixes before resubmission
```

这些是提交前必须处理的部分。

## 7. Word 输出

完整审核默认建议输出 Word `.docx`。最终回复中应出现类似：

```text
Word output status:
- File: /absolute/path/to/revision_final_audit_xxx.docx
- Export method: scripts/export_audit_report_docx.py
- DOCX QA status: pass
```

## 8. 常见问题

### Q1: 没有完整 manuscript，可以用吗？

可以，但只能做文本级审核。凡是需要 manuscript 或文件包验证的内容都会标记为 `Cannot verify`。

### Q2: 审核 skill 会帮我重写 response 吗？

默认不会。它会指出哪里必须改、为什么要改、需要补什么证据。若需要重写，可以在拿到 audit report 后再单独要求修改。

### Q3: 为什么 verdict 是 Not ready？

常见原因包括：

- reviewer 没有逐条覆盖；
- response 承诺做了某件事，但 manuscript/file package 没有证据；
- 样本量、P value、figure/table 编号等精确事实不一致；
- conclusion 过强；
- source data/data availability/code availability 缺失；
- Word/package 文件不全；
- 还有 `[[FILL: ...]]`、TODO 或占位符残留。

### Q4: 最推荐的工作流是什么？

```text
1. 用 revision-response-drafter 生成或完善 response framework。
2. 作者补完分析、数值、图表、manuscript 修改。
3. 整理完整 revision package。
4. 用 revision-final-auditor 做最终审核并输出 Word report。
5. 按 required fixes 修改。
6. 必要时再次运行 revision-final-auditor，直到 verdict 至少为 Ready after minor fixes。
```
