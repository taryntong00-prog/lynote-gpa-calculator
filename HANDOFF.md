# GPA Calculator 页面交付说明

## 版本与范围

- 最终设计：v25，2026-10-29。
- 页面语言：英文；顶部产品功能区保留中文交接占位。
- 桌面页面内容最大宽度 1160px，采用 Inter 字体，资源随包提供。
- 本交付包含营销页视觉与交互，不包含真实计算器的集成、登录、计费或后台服务。

## 设计确认要点

1. 顶部计算器只保留占位框“产品功能区，以 Molly 为准”。开发需接入 Molly 确认的产品稿。
2. 无左侧目录导航；宽屏采用左右布局和完整组合版块。
3. How to 为三步：Add your classes → Set the credits → Calculate and review。Previous GPA 属于可选操作。
4. How GPA is calculated 已合并公式、课程示例和结果，避免重复讲解。
5. GPA scale 左侧表格，右侧标题和说明。
6. Semester vs. cumulative GPA 已删除底部两条补充说明。
7. Weighted vs. unweighted GPA 重点突出两列：未加权为蓝色，加权为紫色，与右侧结果对应；跨学年示例已删除。
8. Why choose 已调整为用户收益和产品优点，而非功能清单。
9. FAQ 使用现有品牌折叠样式；底部推荐使用品牌图标卡片轮播。
10. Review 版块为六张示例卡片轮播：浅底色、橙色星形、斜体文案和字母头像；桌面三张、平板两张、手机一张，支持按钮、分页点、触摸滑动和键盘切换。星形仅为示例设计，不代表真实用户评分。

## 页面顺序

Hero / 产品占位 → What is a GPA calculator → How to use → How GPA is calculated → GPA scale → Semester vs. cumulative GPA → Weighted vs. unweighted GPA → What is a good GPA → Why your GPA differs from your transcript → Who needs this GPA calculator → What our users say → Why choose our GPA calculator → FAQ → Related tools → Footer。

## 开发文件映射

| 文件 | 用途 |
| --- | --- |
| `gpa-calculator/index.html` | 完整静态页面，可作为样式和布局参考 |
| `assets/gpa.css` | GPA 页样式，包括响应式规则 |
| `assets/guide.js` | 导航、示例表格选中、FAQ 和推荐轮播交互 |
| `design-source/guide.html` | 说明、公式、表格、FAQ 等主体结构 |
| `design-source/marketing.html` | Who needs、评价示例、Why choose 三个版块 |
| `design-source/gpa.css` | 可编辑页面样式源文件 |
| `design-source/guide.js` | 可编辑交互源文件 |
| `design-source/build_page.py` | 组装页面、生成 FAQ 结构化数据和资源版本号 |
| `design-source/source/` | 构建保留资源：品牌导航、字体、图标、原始 demo 依赖 |
| `design-previews/` | 最近确认的重点版块截图；以根目录完整静态页为最终版本 |

## 交互与接入

- 已实现：品牌导航菜单、移动端菜单、课程示例选中与计算明细切换、FAQ 展开收起、推荐工具及六张评价轮播。
- 产品相关 CTA 当前滚动到顶部占位区；`gpa-guide-action` 事件提供 action，需在真实计算器集成时绑定到对应产品操作。
- CSV / Print / PDF / 评分配置等是营销文案描述的产品能力；本页面顶部占位框不能执行这些功能。
- `design-source/source/demo/` 是构建时保留的原始参考，不作为已确认的产品区实现交付。
- 导航和推荐工具部分链接指向现有线上页面；GPA 页面正式上线时需统一正式域名及产品按钮目标。

## 文案与上线确认

- 评价是明确标注的示例文案。没有提供真实用户反馈，不应添加真实姓名、五星评分、Review 或 AggregateRating 标记；正式发布时使用真实授权评价或保留示例说明。
- 顶部工具接入后，确认免费、免注册、导出和评分规则等文案与真实产品一致。
- 当前元信息及 FAQ JSON-LD 已随页面提供；正式域名确定后由开发补充正式 canonical 和站点索引配置。
- 表格为 HTML 文本；手机上较宽表格保留区域内横向滚动。

## 资源

字体、图片和图标均随包保留。相关工具图标来源见 `design-source/source/related/ATTRIBUTION.txt`。原始第三方依赖许可随对应 vendor 文件保留。
