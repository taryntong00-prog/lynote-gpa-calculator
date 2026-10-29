# Lynote GPA Calculator — 设计与开发交付

最终设计版本：v25 · 2026-10-29。此仓库包含可直接预览的静态页面、可编辑源码、资源和交付说明。

- [在线页面](https://taryntong00-prog.github.io/lynote-gpa-calculator/gpa-calculator/)
- [原始设计预览 v24（历史版本）](https://lynote-gpa-calculator-guide.banhpigat19.chatgpt.site/gpa-calculator/?v=24)
- [设计与开发交付说明](HANDOFF.md)
- [重点版块截图](design-previews/)

## 本地查看

在仓库根目录执行（无需安装前端依赖）：

```sh
python3 -m http.server 8765
```

打开 http://localhost:8765/gpa-calculator/ 。静态成品位于 `gpa-calculator/index.html` 和 `assets/`。

## 修改与重新构建

Python 3，构建依赖为 lxml。建议使用虚拟环境：

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python build.py
```

编辑 `design-source/` 中的文件，运行 `build.py` 后根目录静态页面会更新。无需 Node、npm 或后端服务。

## 交付边界

这是营销落地页设计。顶部保留“产品功能区，以 Molly 为准”，并未接入实际计算器。评价内容明确标为示例，不能当作真实客户证言使用。详见 HANDOFF.md。
