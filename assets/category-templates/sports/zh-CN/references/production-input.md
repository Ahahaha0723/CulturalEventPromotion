# 制作输入与分工

本Skill接收母本处理Skill已经批准的上版文字、locked_copy、运动项目与主题、现有Logo/图像素材。它不定义文案筛选范围，不重新排除报名、奖项等某一内容类别。上游未提供某字段时不自行填造。

渲染器常用数据键为year、title_lines、subtitle、slogan、location、date_lines、venue_lines、organizers、sponsor_lines，属于布局槽位，不是可上版内容白名单。其他已批准文字可写入extra_text_blocks，每项含id、lines和style；style使用x、top、size、font、align、width、lineHeight。不能因数据键未映射就无声忽略文案；先完成布局映射，必要时调整整体布局。

示例中赞助角色和Logo状态用于排版，不承担资料筛选。锁定文案与实际文字图层逐项比对，所有已批准文字都需要落位。制作后保存layout-input、layout-plan、visual-plan、layout-metrics和quality-report。
