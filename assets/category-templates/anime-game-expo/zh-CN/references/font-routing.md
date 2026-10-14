# 字体使用与调度

## 严格字体与排版标准

生成及文字修订前读取[最佳适配参考的字体与排版锁定](strict-reference-typography.md)，实际看图、对照样张并按角色锁定字形与布局。旧候选次序不能代替匹配判断；新增斜体、字族或布局变动须有本案／原图依据。


字体不是按活动大类自动锁死。先依据小类、题材、情绪和信息量选择 assets/fonts/role-profiles.json 的方案，再用真实文案比较样张。包内字族分布与角色索引见 assets/fonts/roles-zh-CN.md 和 roles-en.md；实体文件按字族只存一份，同一字族可以服务多个角色。

## 三种不同结论

- 原字体确认：需要源文件字体元数据、设计者说明或官方规范；普通位图的外观相似不够。
- 风格识别：从笔画、比例、端点、数字、间距和图形改造描述可见类型，可有较高把握。
- 近似替代：包内提供可使用的开源候选。所有本次候选均不宣称与案例原字体相同；候选文件的来源和许可证是真实核验过的。

案例 FEEL、黑白森林、Manga 及IP字标中的图形处理优先视为字标／定制字形待确认，不试图把抠图变成字体。保留原资产身份；在用户需要原创标题时，可按机制制作可辨的定制题名，但正式文字仍逐字核对。

## 调度命令

```powershell
python scripts/font_engine.py --profile PROFILE --language zh-CN --role title --text "真实活动名称"
python scripts/font_engine.py --profile PROFILE --language en --role body --text-file copy.txt
```

将 PROFILE 替换为本类列出的方案ID；text-file 为UTF-8。输出为实际字体路径、内部名称、字重、是否回退和缺字原因。它不安装字体、不联网。根目录默认由脚本位置推导，包可搬移；也可显式 --root 指定技能目录。

选择顺序：用户明确字体或品牌规范 → 可用且允许使用的原资产／原字体 → 风格匹配的本地候选 → 本包近似替代。额外下载字体前核对官方来源和允许用途。未有可用匹配字体时展示现状与候选，不静默更换用户已指定的字形。

## 加载与回退

排版器按返回的实体路径加载，用记录的内部名称或自定义稳定别名；SVG 的字体名不等于已嵌入字体。跨机器编辑时需相同字体，或根据许可嵌入／转曲保留另一份可编辑文字。不要未经核实把系统字体复制进分发包。

脚本为整个字段选择能覆盖全部字符的候选；不按每个字任意切换字族。若包含中英混排或泰文而候选不覆盖，缺字原因可见；需要分段字体时由设计者明确分段并检查基线。找不到覆盖全部字符的候选会失败，不用方框或伪字填充。

包内除 Noto Sans Thai 外均为静态字体。泰文可变字体按内置默认轴加载；排版器不支持可变字体时保持该候选不可用，不擅自伪粗或变形。未经实测不保证所有排版器的可变轴行为。

不通过横向压缩制造窄体；优先选真实窄体或调整文本框。不要为副标题混用自动扣分，不固定主副标题字号比，不把标题层级与构图和谐混为同一检查。

## 许可与复用

每个字族保留 OFL.txt、版权说明、官方提交与SHA-256。字体文件本次未修改。OFL允许按许可条件随软件／技能包捆绑；不能把字体本身单独售卖或忽略保留字体名等限制。正式条款以随包许可证为准。案例海报与Logo的权利不因字体许可证而获得。

## 三案例的实体字体调度
以下是可比较的开源替代，原案例具体字体仍未确认。
- 022：anime-character。英文主标题可比较Archivo Black／Barlow Bold；中文题名比较现有粗黑或活泼候选，日期保持粗而清楚。MANGA定制字标不等于某个实体字体。
- 052：ip-portrait。英文标题比较Bebas Neue与Anton的字面重量，使用真实窄体；中文优先思源黑体Heavy并按自然字宽重排。场地／日期与题名分角色，磨损仅限表现层，不能损坏功能文字。
- 053：artist-alley用于展会名、正文与摊位；英文摊位使用subtitle角色的Barlow BoldItalic，使用真实斜体文件。作者英文署名可调用新增artist-signature的title角色Spectral Italic，再以排版器调真实字距；中文作者名采用其zh-CN角色并按中文阅读重组。日期仍用numeric角色，不因摊位倾斜就全部倾斜。

```powershell
python scripts/font_engine.py --profile artist-signature --language en --role title --text "Actual Creator Name"
python scripts/font_engine.py --profile artist-alley --language en --role subtitle --text "Table F20"
```
F20仅为本案例调度样例，不能填入未来活动。字体检查负责覆盖与实体路径，宽字距、磨损和图文比例由排版实现及审美审核判断。实体文件与许可证随包保留，不新增或伪造原字体确认。

## Verify a locked font, no fallback

```powershell
python scripts/reference_font_check.py --font-id barlow/Barlow-BoldItalic.ttf --text "Table F20"
```
F20 is a specimen, not an event fact. Unknown IDs, checksums or missing glyphs fail visibly. Visual matching still requires the selected reference and the real target text.
