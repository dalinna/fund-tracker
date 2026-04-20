#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成基金收益展示HTML
"""

import json
from datetime import datetime

def format_money(value):
    """格式化金额"""
    return f"¥{value:,.2f}"

def format_percent(value):
    """格式化百分比"""
    sign = '+' if value >= 0 else ''
    return f"{sign}{value:.2f}%"

def load_fund_data(json_path='fund-data.json'):
    """读取基金数据"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"读取数据文件失败: {str(e)}")
        return None

def generate_html(data, output_path='index.html'):
    """生成HTML文件"""

    summary = data.get('summary', {})
    funds = data.get('funds', [])
    update_time = data.get('update_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    total_market_value = summary.get('total_market_value', 0)
    total_profit = summary.get('total_profit', 0)
    total_profit_rate = summary.get('total_profit_rate', 0)

    profit_class = 'positive' if total_profit >= 0 else 'negative'

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <title>基金实时收益</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }}

        .container {{
            max-width: 600px;
            margin: 0 auto;
        }}

        .header {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}

        .header h1 {{
            font-size: 24px;
            margin-bottom: 20px;
            color: #333;
        }}

        .summary {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-bottom: 16px;
        }}

        .summary-item {{
            text-align: center;
        }}

        .summary-label {{
            font-size: 14px;
            color: #999;
            margin-bottom: 8px;
        }}

        .summary-value {{
            font-size: 24px;
            font-weight: bold;
        }}

        .summary-value.positive {{
            color: #f5222d;
        }}

        .summary-value.negative {{
            color: #52c41a;
        }}

        .refresh-btn {{
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: opacity 0.3s;
        }}

        .refresh-btn:active {{
            opacity: 0.8;
        }}

        .fund-card {{
            background: white;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}

        .fund-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 1px solid #f0f0f0;
        }}

        .fund-name {{
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }}

        .fund-code {{
            font-size: 14px;
            color: #999;
        }}

        .fund-info {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 12px;
        }}

        .info-item {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
        }}

        .info-label {{
            color: #666;
            font-size: 14px;
        }}

        .info-value {{
            font-weight: 500;
            font-size: 14px;
        }}

        .fund-profit {{
            background: #f5f5f5;
            border-radius: 8px;
            padding: 12px;
            text-align: center;
            margin-top: 12px;
        }}

        .profit-label {{
            font-size: 12px;
            color: #999;
            margin-bottom: 4px;
        }}

        .profit-value {{
            font-size: 20px;
            font-weight: bold;
        }}

        .profit-value.positive {{
            color: #f5222d;
        }}

        .profit-value.negative {{
            color: #52c41a;
        }}

        .update-time {{
            text-align: center;
            color: rgba(255,255,255,0.8);
            font-size: 12px;
            margin-top: 16px;
        }}

        .error-badge {{
            background: #fff1f0;
            color: #cf1322;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            margin-left: 8px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>基金实时收益</h1>
            <div class="summary">
                <div class="summary-item">
                    <div class="summary-label">总市值</div>
                    <div class="summary-value">{format_money(total_market_value)}</div>
                </div>
                <div class="summary-item">
                    <div class="summary-label">总收益</div>
                    <div class="summary-value {profit_class}">
                        {format_money(total_profit)}
                    </div>
                </div>
            </div>
            <div class="summary-item">
                <div class="summary-label">收益率</div>
                <div class="summary-value {profit_class}">
                    {format_percent(total_profit_rate)}
                </div>
            </div>
            <button class="refresh-btn" onclick="location.reload()">刷新数据</button>
        </div>
"""

    # 生成每只基金的卡片
    for fund in funds:
        code = fund.get('code', '')
        name = fund.get('name', '')
        shares = fund.get('shares', 0)
        cost_price = fund.get('cost_price', 0)
        current_nav = fund.get('current_nav', 0)
        market_value = fund.get('market_value', 0)
        profit = fund.get('profit', 0)
        profit_rate = fund.get('profit_rate', 0)
        error = fund.get('error', '')

        fund_profit_class = 'positive' if profit >= 0 else 'negative'
        error_badge = f'<span class="error-badge">{error}</span>' if error else ''

        html += f"""
        <div class="fund-card">
            <div class="fund-header">
                <div>
                    <div class="fund-name">{name}{error_badge}</div>
                    <div class="fund-code">{code}</div>
                </div>
            </div>
            <div class="fund-info">
                <div class="info-item">
                    <span class="info-label">持有份额</span>
                    <span class="info-value">{shares:.2f}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">成本价</span>
                    <span class="info-value">{format_money(cost_price)}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">当前净值</span>
                    <span class="info-value">{format_money(current_nav)}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">市值</span>
                    <span class="info-value">{format_money(market_value)}</span>
                </div>
            </div>
            <div class="fund-profit">
                <div class="profit-label">持有收益</div>
                <div class="profit-value {fund_profit_class}">
                    {format_money(profit)} ({format_percent(profit_rate)})
                </div>
            </div>
        </div>
"""

    html += f"""
        <div class="update-time">更新时间：{update_time}</div>
        <div class="update-time" style="margin-top: 8px;">每天自动更新 | GitHub Actions驱动</div>
    </div>
</body>
</html>
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"HTML已生成: {output_path}")

def main():
    print("开始生成HTML...")

    data = load_fund_data()
    if not data:
        print("错误: 无法读取基金数据")
        return

    generate_html(data)
    print("完成!")

if __name__ == '__main__':
    main()
