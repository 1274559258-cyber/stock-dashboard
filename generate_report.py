# -*- coding: utf-8 -*-
"""
HTML报告生成模块
生成美观的股票看板网页
"""
import pandas as pd
import os
from datetime import datetime
from config import STOCKS, REPORTS_DIR
from indicators import get_latest_signals

def generate_html(df_today, df_history):
    """生成完整HTML报告"""

    if df_today.empty:
        return "<h1>数据获取失败</h1>"

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 计算市场统计
    up_count = len(df_today[df_today['change_pct'] > 0])
    down_count = len(df_today[df_today['change_pct'] < 0])
    flat_count = len(df_today[df_today['change_pct'] == 0])
    avg_change = df_today['change_pct'].mean()
    max_up = df_today['change_pct'].max()
    max_down = df_today['change_pct'].min()

    # 找出涨幅/跌幅前5
    top5_up = df_today.nlargest(5, 'change_pct')[['name', 'change_pct', 'price']]
    top5_down = df_today.nsmallest(5, 'change_pct')[['name', 'change_pct', 'price']]

    # 生成个股卡片
    stock_cards = []
    for _, stock in enumerate(STOCKS):
        code = stock['code']
        name = stock['name']
        cat = stock.get('category', '')

        row = df_today[df_today['code'] == code]
        if row.empty:
            continue
        row = row.iloc[0]

        # 获取历史数据计算更多指标
        hist = df_history[df_history['code'] == code].copy() if not df_history.empty else pd.DataFrame()
        if not hist.empty:
            hist = hist.sort_values('date').tail(60)
            from indicators import calculate_all_indicators
            hist = calculate_all_indicators(hist)
            latest_hist = hist.tail(1)
            if not latest_hist.empty:
                for col in ['MA5', 'MA10', 'MA20', 'MA60', 'RSI', 'MACD', 'MACD_Signal', 'MACD_Hist', 'BOLL_UP', 'BOLL_DOWN']:
                    if col in latest_hist.columns:
                        row[col] = latest_hist[col].values[0]

        price = row.get('price', 0)
        change_pct = row.get('change_pct', 0)
        pre_close = row.get('pre_close', price)
        high = row.get('high', 0)
        low = row.get('low', 0)
        volume = row.get('volume', 0)
        turnover = row.get('turnover', 0)
        pe = row.get('pe', 0)
        pb = row.get('pb', 0)
        market_cap = row.get('market_cap', 0)

        # 颜色
        color_class = "up" if change_pct > 0 else ("down" if change_pct < 0 else "flat")
        change_str = f"+{change_pct:.2f}%" if change_pct > 0 else f"{change_pct:.2f}%"

        # 信号
        signals = get_latest_signals(row)
        signal_tags = ""
        for text, tag_type in signals:
            signal_tags += f'<span class="tag {tag_type}">{text}</span>'

        # 均线数据
        ma5 = row.get('MA5', 0)
        ma20 = row.get('MA20', 0)
        ma60 = row.get('MA60', 0)
        rsi = row.get('RSI', 50)

        ma_display = ""
        if ma5 > 0:
            ma_display += f'<div class="mini-stat">MA5: {ma5:.2f}</div>'
        if ma20 > 0:
            ma_display += f'<div class="mini-stat">MA20: {ma20:.2f}</div>'
        if ma60 > 0:
            ma_display += f'<div class="mini-stat">MA60: {ma60:.2f}</div>'

        # 市值格式化
        cap_str = ""
        if market_cap > 0:
            if market_cap > 100000000:
                cap_str = f"{market_cap/100000000:.0f}亿"
            else:
                cap_str = f"{market_cap/10000:.0f}万"

        card = f"""
        <div class="stock-card {color_class}">
            <div class="card-header">
                <div class="stock-info">
                    <span class="stock-name">{name}</span>
                    <span class="stock-code">{code}</span>
                    <span class="category">{cat}</span>
                </div>
                <div class="stock-price">
                    <span class="price">{price:.2f}</span>
                    <span class="change {color_class}">{change_str}</span>
                </div>
            </div>
            <div class="card-body">
                <div class="price-range">
                    <span>高: {high:.2f}</span>
                    <span>低: {low:.2f}</span>
                    <span>昨收: {pre_close:.2f}</span>
                </div>
                <div class="indicators">
                    {ma_display}
                    <div class="mini-stat">换手: {turnover:.2f}%</div>
                    <div class="mini-stat">PE: {pe:.1f}</div>
                    <div class="mini-stat">PB: {pb:.2f}</div>
                    <div class="mini-stat">市值: {cap_str}</div>
                </div>
                <div class="signals">
                    {signal_tags}
                </div>
            </div>
        </div>
        """
        stock_cards.append(card)

    cards_html = "\n".join(stock_cards)

    # 生成Top5列表
    top5_up_html = ""
    for _, r in top5_up.iterrows():
        top5_up_html += f'<div class="rank-item up"><span>{r["name"]}</span><span>+{r["change_pct"]:.2f}%</span></div>'

    top5_down_html = ""
    for _, r in top5_down.iterrows():
        top5_down_html += f'<div class="rank-item down"><span>{r["name"]}</span><span>{r["change_pct"]:.2f}%</span></div>'

    # 市场温度计HTML
    temp_score = min(10, max(1, int(5 + avg_change / 2)))
    temp_color = "hot" if temp_score >= 8 else ("warm" if temp_score >= 5 else "cold")
    temp_text = "亢奋" if temp_score >= 9 else ("积极" if temp_score >= 7 else ("震荡" if temp_score >= 4 else "谨慎"))

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>交易员看板 - {datetime.now().strftime('%Y-%m-%d')}</title>
    <style>
        :root {{
            --bg: #0f172a;
            --card-bg: #1e293b;
            --text: #e2e8f0;
            --text-dim: #94a3b8;
            --up: #ef4444;
            --down: #22c55e;
            --flat: #64748b;
            --accent: #3b82f6;
            --warning: #f59e0b;
            --success: #10b981;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}

        /* Header */
        .header {{
            text-align: center;
            padding: 30px 0;
            border-bottom: 1px solid #334155;
            margin-bottom: 30px;
        }}
        .header h1 {{ font-size: 2rem; margin-bottom: 10px; }}
        .header .time {{ color: var(--text-dim); font-size: 0.9rem; }}

        /* Market Dashboard */
        .dashboard {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .dash-card {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            border: 1px solid #334155;
        }}
        .dash-card .label {{ color: var(--text-dim); font-size: 0.85rem; margin-bottom: 8px; }}
        .dash-card .value {{ font-size: 1.8rem; font-weight: bold; }}
        .dash-card .value.up {{ color: var(--up); }}
        .dash-card .value.down {{ color: var(--down); }}

        /* Temperature */
        .temp-section {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 30px;
            border: 1px solid #334155;
        }}
        .temp-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        .temp-gauge {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        .temp-score {{
            font-size: 3rem;
            font-weight: bold;
            width: 80px;
            height: 80px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .temp-score.hot {{ background: rgba(239,68,68,0.2); color: var(--up); border: 3px solid var(--up); }}
        .temp-score.warm {{ background: rgba(245,158,11,0.2); color: var(--warning); border: 3px solid var(--warning); }}
        .temp-score.cold {{ background: rgba(59,130,246,0.2); color: var(--accent); border: 3px solid var(--accent); }}
        .temp-bar {{
            flex: 1;
            height: 20px;
            background: #334155;
            border-radius: 10px;
            overflow: hidden;
            position: relative;
        }}
        .temp-fill {{
            height: 100%;
            border-radius: 10px;
            transition: width 0.5s ease;
        }}
        .temp-fill.hot {{ background: var(--up); }}
        .temp-fill.warm {{ background: var(--warning); }}
        .temp-fill.cold {{ background: var(--accent); }}

        /* Rankings */
        .rankings {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }}
        .rank-box {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #334155;
        }}
        .rank-box h3 {{ margin-bottom: 15px; font-size: 1rem; }}
        .rank-item {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #334155;
        }}
        .rank-item:last-child {{ border-bottom: none; }}
        .rank-item.up {{ color: var(--up); }}
        .rank-item.down {{ color: var(--down); }}

        /* Stock Cards Grid */
        .stocks-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 20px;
        }}
        .stock-card {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #334155;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .stock-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        .stock-card.up {{ border-left: 4px solid var(--up); }}
        .stock-card.down {{ border-left: 4px solid var(--down); }}
        .stock-card.flat {{ border-left: 4px solid var(--flat); }}

        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }}
        .stock-name {{ font-size: 1.1rem; font-weight: bold; }}
        .stock-code {{ color: var(--text-dim); font-size: 0.8rem; margin-left: 5px; }}
        .category {{
            display: inline-block;
            background: #334155;
            color: var(--text-dim);
            font-size: 0.7rem;
            padding: 2px 8px;
            border-radius: 4px;
            margin-left: 5px;
        }}
        .stock-price {{ text-align: right; }}
        .price {{ font-size: 1.5rem; font-weight: bold; display: block; }}
        .change {{ font-size: 0.95rem; font-weight: 600; }}
        .change.up {{ color: var(--up); }}
        .change.down {{ color: var(--down); }}

        .card-body {{ margin-top: 10px; }}
        .price-range {{
            display: flex;
            gap: 15px;
            font-size: 0.8rem;
            color: var(--text-dim);
            margin-bottom: 12px;
        }}
        .indicators {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 12px;
        }}
        .mini-stat {{
            background: #334155;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            color: var(--text-dim);
        }}
        .signals {{ display: flex; flex-wrap: wrap; gap: 6px; }}
        .tag {{
            font-size: 0.7rem;
            padding: 3px 8px;
            border-radius: 4px;
            font-weight: 500;
        }}
        .tag.bull {{ background: rgba(34,197,94,0.15); color: var(--success); }}
        .tag.bear {{ background: rgba(239,68,68,0.15); color: var(--up); }}
        .tag.warning {{ background: rgba(245,158,11,0.15); color: var(--warning); }}
        .tag.opportunity {{ background: rgba(59,130,246,0.15); color: var(--accent); }}
        .tag.neutral {{ background: #334155; color: var(--text-dim); }}

        /* Footer */
        .footer {{
            text-align: center;
            padding: 30px;
            color: var(--text-dim);
            font-size: 0.8rem;
            border-top: 1px solid #334155;
            margin-top: 30px;
        }}

        @media (max-width: 768px) {{
            .rankings {{ grid-template-columns: 1fr; }}
            .stocks-grid {{ grid-template-columns: 1fr; }}
            .header h1 {{ font-size: 1.5rem; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 交易员看板</h1>
            <div class="time">生成时间：{now}</div>
        </div>

        <!-- 市场概览 -->
        <div class="dashboard">
            <div class="dash-card">
                <div class="label">上涨家数</div>
                <div class="value up">{up_count}</div>
            </div>
            <div class="dash-card">
                <div class="label">下跌家数</div>
                <div class="value down">{down_count}</div>
            </div>
            <div class="dash-card">
                <div class="label">平盘家数</div>
                <div class="value">{flat_count}</div>
            </div>
            <div class="dash-card">
                <div class="label">平均涨跌</div>
                <div class="value {'up' if avg_change > 0 else 'down'}">{avg_change:+.2f}%</div>
            </div>
            <div class="dash-card">
                <div class="label">最强标的</div>
                <div class="value up">+{max_up:.2f}%</div>
            </div>
            <div class="dash-card">
                <div class="label">最弱标的</div>
                <div class="value down">{max_down:.2f}%</div>
            </div>
        </div>

        <!-- 市场情绪温度计 -->
        <div class="temp-section">
            <div class="temp-header">
                <div>
                    <h2>🌡️ 市场情绪温度计</h2>
                    <p style="color: var(--text-dim); font-size: 0.85rem; margin-top: 5px;">
                        基于监控标的平均涨跌幅估算 · 仅供参考
                    </p>
                </div>
                <div class="temp-gauge">
                    <div class="temp-score {temp_color}">{temp_score}</div>
                    <div style="flex: 1;">
                        <div style="font-size: 1.2rem; font-weight: bold; margin-bottom: 5px;">{temp_text}</div>
                        <div class="temp-bar">
                            <div class="temp-fill {temp_color}" style="width: {temp_score * 10}%"></div>
                        </div>
                        <div style="display: flex; justify-content: space-between; font-size: 0.7rem; color: var(--text-dim); margin-top: 4px;">
                            <span>恐慌</span><span>谨慎</span><span>震荡</span><span>积极</span><span>亢奋</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 涨跌排行 -->
        <div class="rankings">
            <div class="rank-box">
                <h3>🔥 涨幅 TOP 5</h3>
                {top5_up_html}
            </div>
            <div class="rank-box">
                <h3>❄️ 跌幅 TOP 5</h3>
                {top5_down_html}
            </div>
        </div>

        <!-- 个股卡片 -->
        <h2 style="margin-bottom: 20px;">📈 监控标的详情</h2>
        <div class="stocks-grid">
            {cards_html}
        </div>

        <div class="footer">
            <p>交易员看板 · 数据仅供个人参考，不构成投资建议</p>
            <p style="margin-top: 5px;">数据来源：腾讯财经 · 生成时间：{now}</p>
        </div>
    </div>
</body>
</html>"""

    return html

def save_report(html_content, filename=None):
    """保存报告到文件"""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    if filename is None:
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    filepath = os.path.join(REPORTS_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"[OK] 报告已保存: {filepath}")
    return filepath
