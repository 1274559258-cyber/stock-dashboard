# -*- coding: utf-8 -*-
"""
数据拉取模块 - 使用腾讯财经免费接口
无需注册，无需API Key
"""
import requests
import pandas as pd
import os
from datetime import datetime
from config import STOCKS, DATA_DIR, HISTORY_FILE

def get_realtime_quotes(codes):
    """
    获取实时行情
    codes: list of str, e.g. ["sh600196", "sz000680"]
    返回: DataFrame
    """
    if not codes:
        return pd.DataFrame()

    url = f"http://qt.gtimg.cn/q={','.join(codes)}"
    try:
        response = requests.get(url, timeout=15)
        response.encoding = 'gbk'
        text = response.text
    except Exception as e:
        print(f"[ERROR] 请求失败: {e}")
        return pd.DataFrame()

    data_list = []
    for line in text.strip().split(';'):
        line = line.strip()
        if not line or 'v_' not in line:
            continue
        try:
            # 解析 v_sh600196="1~复星医药~600196~..."
            parts = line.split('="')
            if len(parts) < 2:
                continue
            code_key = parts[0].replace('v_', '')
            content = parts[1].rstrip('"')
            fields = content.split('~')

            if len(fields) < 35:
                continue

            # 字段映射（腾讯接口）
            data_list.append({
                'code': code_key,
                'name': fields[1],
                'price': float(fields[3]) if fields[3] else 0.0,
                'pre_close': float(fields[4]) if fields[4] else 0.0,
                'open': float(fields[5]) if fields[5] else 0.0,
                'high': float(fields[33]) if fields[33] else 0.0,
                'low': float(fields[34]) if fields[34] else 0.0,
                'volume': int(fields[36]) if fields[36] else 0,  # 手
                'amount': float(fields[37]) * 10000 if fields[37] else 0.0,  # 元
                'change_pct': float(fields[32]) if fields[32] else 0.0,
                'turnover': float(fields[38]) if fields[38] else 0.0,
                'pe': float(fields[39]) if fields[39] else 0.0,
                'pb': float(fields[46]) if len(fields) > 46 and fields[46] else 0.0,
                'market_cap': float(fields[45]) if len(fields) > 45 and fields[45] else 0.0,  # 总市值
                'date': datetime.now().strftime('%Y-%m-%d'),
                'time': fields[30] if len(fields) > 30 else datetime.now().strftime('%H:%M:%S'),
            })
        except Exception as e:
            print(f"[WARN] 解析 {line[:50]}... 失败: {e}")
            continue

    df = pd.DataFrame(data_list)
    return df

def save_to_history(df):
    """保存到历史数据文件，用于计算技术指标"""
    if df.empty:
        return

    os.makedirs(DATA_DIR, exist_ok=True)

    # 转换volume为股（腾讯接口是手，1手=100股）
    df['volume'] = df['volume'] * 100

    if os.path.exists(HISTORY_FILE):
        existing = pd.read_csv(HISTORY_FILE)
        # 去重：同一日期同一代码只保留最新
        combined = pd.concat([existing, df], ignore_index=True)
        combined = combined.drop_duplicates(subset=['code', 'date'], keep='last')
        combined = combined.sort_values(['code', 'date']).reset_index(drop=True)
    else:
        combined = df

    combined.to_csv(HISTORY_FILE, index=False)
    print(f"[OK] 历史数据已保存，共 {len(combined)} 条记录")

def load_history():
    """加载历史数据"""
    if not os.path.exists(HISTORY_FILE):
        return pd.DataFrame()
    return pd.read_csv(HISTORY_FILE)

def fetch_all():
    """拉取所有配置的股票"""
    codes = [s['code'] for s in STOCKS]
    print(f"[INFO] 正在拉取 {len(codes)} 只标的...")

    # 腾讯接口一次最多支持60只，分批请求
    batch_size = 60
    all_data = []
    for i in range(0, len(codes), batch_size):
        batch = codes[i:i+batch_size]
        df = get_realtime_quotes(batch)
        if not df.empty:
            all_data.append(df)
        print(f"[INFO] 批次 {i//batch_size + 1}/{(len(codes)-1)//batch_size + 1} 完成")

    if all_data:
        result = pd.concat(all_data, ignore_index=True)
        save_to_history(result)
        return result
    return pd.DataFrame()

if __name__ == "__main__":
    df = fetch_all()
    print(df[['code', 'name', 'price', 'change_pct', 'volume']].head(10))
