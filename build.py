from pathlib import Path
import runpy
import shutil
ROOT = Path(__file__).resolve().parent
runpy.run_path(str(ROOT / "design-source/build_page.py"), run_name="__main__")
for item in (ROOT / "design-source/dist").iterdir():
    target = ROOT / item.name
    if item.is_dir():
        shutil.copytree(item, target, dirs_exist_ok=True)
    else:
        shutil.copy2(item, target)
print("Updated root static files. Serve this folder to preview /gpa-calculator/.")
