# -*- coding: utf-8 -*-
"""
交易员看板 - 主入口
"""
import os
import sys
import shutil

from config import DATA_DIR, REPORTS_DIR
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

from fetch_data import fetch_all, load_history
from generate_report import generate_html, save_report

def run():
    print("=" * 60)
    print("🚀 交易员看板 - 数据更新")
    print("=" * 60)

    print("\n[1/3] 拉取实时行情...")
    df_today = fetch_all()
    if df_today.empty:
        print("[ERROR] 数据拉取失败")
        sys.exit(1)
    print(f"[OK] 成功获取 {len(df_today)} 只标的")

    print("\n[2/3] 加载历史数据...")
    df_history = load_history()
    if df_history.empty:
        print("[WARN] 历史数据为空，技术指标可能不准确")
    else:
        print(f"[OK] 历史数据共 {len(df_history)} 条记录")

    print("\n[3/3] 生成HTML看板...")
    html = generate_html(df_today, df_history)
    filepath = save_report(html, "index.html")

    # GitHub Pages 需要 404.html 也指向首页
    shutil.copy(filepath, os.path.join(REPORTS_DIR, "404.html"))

    print("\n" + "=" * 60)
    print(f"✅ 完成！报告已生成: {filepath}")
    print("=" * 60)

if __name__ == "__main__":
    run()
