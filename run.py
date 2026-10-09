import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RESULTS = BASE_DIR / "temps"                         # 中间数据目录
REPORT_DIR = BASE_DIR / "reports"  /  "allure-report"          # 存放报告的文件夹
#"reports" / "allure-results"
# 你的绝对路径
ALLURE_PATH = r"D:\dev\PycharmProjects\PythonProject1\allure-2.46.1\bin\allure.bat"

def main():
    print("执行测试...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest"],
        cwd=BASE_DIR,
        shell=True
    )
    if result.returncode != 0:
        print(f"测试退出 {result.returncode}，再次生成报告。")

    print("生成报告到指定文件夹...")
    subprocess.run(
        [ALLURE_PATH, "generate", str(RESULTS), "-o", str(REPORT_DIR), "--clean"],
        cwd=BASE_DIR,
        shell=True
    )

    print("打开服务器，正在打开报告...")
    subprocess.run(
        [ALLURE_PATH, "open", str(REPORT_DIR)],
        cwd=BASE_DIR,
        shell=True
    )

if __name__ == "__main__":
    main()
