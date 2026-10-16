# -*- coding: utf-8 -*-
"""
技术指标计算模块
"""
import pandas as pd
import numpy as np
from config import MA_PERIODS, RSI_PERIOD, MACD_FAST, MACD_SLOW, MACD_SIGNAL

def calculate_ma(df, periods=None):
    """计算移动平均线"""
    if periods is None:
        periods = MA_PERIODS
    df = df.sort_values('date').copy()
    for p in periods:
        df[f'MA{p}'] = df['price'].rolling(window=p, min_periods=1).mean()
    return df

def calculate_rsi(df, period=RSI_PERIOD):
    """计算RSI"""
    df = df.sort_values('date').copy()
    delta = df['price'].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta).where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()
    rs = avg_gain / (avg_loss + 1e-10)
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def calculate_macd(df, fast=MACD_FAST, slow=MACD_SLOW, signal=MACD_SIGNAL):
    """计算MACD"""
    df = df.sort_values('date').copy()
    ema_fast = df['price'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['price'].ewm(span=slow, adjust=False).mean()
    df['MACD'] = ema_fast - ema_slow
    df['MACD_Signal'] = df['MACD'].ewm(span=signal, adjust=False).mean()
    df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
    return df

def calculate_bollinger(df, period=20, std_dev=2):
    """计算布林带"""
    df = df.sort_values('date').copy()
    df['BOLL_MID'] = df['price'].rolling(window=period, min_periods=1).mean()
    df['BOLL_STD'] = df['price'].rolling(window=period, min_periods=1).std()
    df['BOLL_UP'] = df['BOLL_MID'] + std_dev * df['BOLL_STD']
    df['BOLL_DOWN'] = df['BOLL_MID'] - std_dev * df['BOLL_STD']
    return df

def calculate_all_indicators(df):
    """为每只股票计算所有技术指标"""
    if df.empty or len(df) == 0:
        return df

    results = []
    for code in df['code'].unique():
        sub = df[df['code'] == code].copy()
        if len(sub) < 2:
            results.append(sub)
            continue
        sub = calculate_ma(sub)
        sub = calculate_rsi(sub)
        sub = calculate_macd(sub)
        sub = calculate_bollinger(sub)
        results.append(sub)

    return pd.concat(results, ignore_index=True)

def get_latest_signals(row):
    """根据最新数据生成交易信号"""
    signals = []

    # 均线排列
    ma5 = row.get('MA5', 0)
    ma10 = row.get('MA10', 0)
    ma20 = row.get('MA20', 0)
    price = row.get('price', 0)

    if price > ma5 > ma10 > ma20:
        signals.append(("均线多头排列", "bull"))
    elif price < ma5 < ma10 < ma20:
        signals.append(("均线空头排列", "bear"))
    elif price > ma5 and ma5 > ma10:
        signals.append(("短期趋势向上", "bull"))
    elif price < ma5 and ma5 < ma10:
        signals.append(("短期趋势向下", "bear"))

    # RSI
    rsi = row.get('RSI', 50)
    if rsi > 70:
        signals.append((f"RSI超买({rsi:.1f})", "warning"))
    elif rsi < 30:
        signals.append((f"RSI超卖({rsi:.1f})", "opportunity"))
    elif 30 <= rsi <= 50:
        signals.append((f"RSI偏弱({rsi:.1f})", "neutral"))
    else:
        signals.append((f"RSI偏强({rsi:.1f})", "bull"))

    # MACD
    macd = row.get('MACD', 0)
    macd_signal = row.get('MACD_Signal', 0)
    macd_hist = row.get('MACD_Hist', 0)

    if macd > macd_signal and macd_hist > 0:
        signals.append(("MACD金叉上行", "bull"))
    elif macd < macd_signal and macd_hist < 0:
        signals.append(("MACD死叉下行", "bear"))

    # 价格位置（布林带）
    boll_up = row.get('BOLL_UP', 0)
    boll_down = row.get('BOLL_DOWN', 0)
    if boll_up > 0 and price > boll_up:
        signals.append(("突破布林上轨", "warning"))
    elif boll_down > 0 and price < boll_down:
        signals.append(("跌破布林下轨", "opportunity"))

    return signals
