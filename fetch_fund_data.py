#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取基金实时数据
"""

import json
import requests
import re
from datetime import datetime

def fetch_fund_data(fund_code):
    """
    从天天基金网获取基金数据
    """
    try:
        url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Referer': 'http://fund.eastmoney.com/'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'

        if response.status_code == 200:
            # 解析JSONP数据
            jsonp_text = response.text
            # 提取JSON部分
            json_match = re.search(r'jsonpgz\((.*?)\);?$', jsonp_text)
            if json_match:
                json_str = json_match.group(1)
                data = json.loads(json_str)
                return {
                    'code': data.get('fundcode'),
                    'name': data.get('name'),
                    'current_nav': float(data.get('gsz', 0) or data.get('dwjz', 0)),
                    'nav_date': data.get('gztime', ''),
                    'day_growth': data.get('gszzl', '0'),
                    'success': True
                }

        return {'code': fund_code, 'success': False, 'error': f'HTTP {response.status_code}'}

    except Exception as e:
        print(f"获取基金{fund_code}数据失败: {str(e)}")
        return {'code': fund_code, 'success': False, 'error': str(e)}

def load_holdings(json_path='fund-holdings.json'):
    """
    读取持仓数据
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('holdings', [])
    except Exception as e:
        print(f"读取持仓文件失败: {str(e)}")
        return []

def parse_day_growth(day_growth):
    """把日涨跌幅字符串转换成浮点数百分比"""
    try:
        return float(day_growth)
    except (TypeError, ValueError):
        return 0.0

def save_fund_data(holdings, fund_data_list, output_path='fund-data.json'):
    """
    保存基金数据到JSON文件
    """
    result = {
        'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'funds': []
    }

    for holding in holdings:
        fund_code = holding['code']
        fund_data = next((f for f in fund_data_list if f.get('code') == fund_code), None)

        if fund_data and fund_data.get('success'):
            day_profit_rate = parse_day_growth(fund_data.get('day_growth', '0'))
            current_nav = fund_data['current_nav']
            day_ratio = day_profit_rate / 100
            denominator = 1 + day_ratio
            previous_nav = (current_nav / denominator) if denominator != 0 else current_nav
            day_profit = holding['shares'] * (current_nav - previous_nav)

            fund_info = {
                'code': fund_code,
                'name': fund_data.get('name', holding['name']),
                'shares': holding['shares'],
                'cost_price': holding['costPrice'],
                'current_nav': current_nav,
                'market_value': holding['shares'] * current_nav,
                'cost': holding['shares'] * holding['costPrice'],
                'profit': holding['shares'] * (current_nav - holding['costPrice']),
                'profit_rate': ((current_nav - holding['costPrice']) / holding['costPrice']) * 100,
                'day_profit': day_profit,
                'day_profit_rate': day_profit_rate,
                'day_growth': fund_data.get('day_growth', '0'),
                'nav_date': fund_data.get('nav_date', '')
            }
        else:
            # 如果获取失败，使用成本价作为当前净值
            fund_info = {
                'code': fund_code,
                'name': holding['name'],
                'shares': holding['shares'],
                'cost_price': holding['costPrice'],
                'current_nav': holding['costPrice'],
                'market_value': holding['shares'] * holding['costPrice'],
                'cost': holding['shares'] * holding['costPrice'],
                'profit': 0,
                'profit_rate': 0,
                'day_profit': 0,
                'day_profit_rate': 0,
                'day_growth': '0',
                'error': fund_data.get('error', '数据获取失败') if fund_data else '未知错误'
            }

        result['funds'].append(fund_info)

    # 计算总计
    total_market_value = sum(f['market_value'] for f in result['funds'])
    total_cost = sum(f['cost'] for f in result['funds'])
    total_profit = total_market_value - total_cost
    total_profit_rate = (total_profit / total_cost * 100) if total_cost > 0 else 0
    total_day_profit = sum(f.get('day_profit', 0) for f in result['funds'])
    total_previous_market_value = total_market_value - total_day_profit
    total_day_profit_rate = (
        total_day_profit / total_previous_market_value * 100
        if total_previous_market_value > 0
        else 0
    )

    result['summary'] = {
        'total_market_value': total_market_value,
        'total_cost': total_cost,
        'total_profit': total_profit,
        'total_profit_rate': total_profit_rate,
        'total_day_profit': total_day_profit,
        'total_day_profit_rate': total_day_profit_rate
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"数据已保存到 {output_path}")
    print(f"总市值: ¥{total_market_value:.2f}")
    print(f"总收益: ¥{total_profit:.2f} ({total_profit_rate:+.2f}%)")
    print(f"当日收益: ¥{total_day_profit:.2f} ({total_day_profit_rate:+.2f}%)")

def main():
    print("开始获取基金数据...")

    # 读取持仓
    holdings = load_holdings()
    if not holdings:
        print("错误: 没有持仓数据")
        return

    print(f"共有 {len(holdings)} 只基金")

    # 获取所有基金数据
    fund_data_list = []
    for holding in holdings:
        fund_code = holding['code']
        print(f"正在获取 {fund_code} - {holding['name']}...")
        fund_data = fetch_fund_data(fund_code)
        fund_data_list.append(fund_data)

        if fund_data.get('success'):
            print(f"  ✓ 成功: 当前净值 ¥{fund_data['current_nav']:.4f}")
        else:
            print(f"  ✗ 失败: {fund_data.get('error')}")

    # 保存数据
    save_fund_data(holdings, fund_data_list)
    print("\n完成!")

if __name__ == '__main__':
    main()
