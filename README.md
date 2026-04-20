# 基金实时收益跟踪

基于GitHub Actions自动化的基金收益跟踪系统。

## 功能特点

- ✅ 每天自动更新基金数据（9:30、15:30、21:00）
- ✅ 自动计算收益和收益率
- ✅ 美观的响应式界面
- ✅ 完全免费，无需服务器

## 使用说明

### 添加基金

编辑 `fund-holdings.json` 文件：

```json
{
  "holdings": [
    {
      "code": "基金代码",
      "name": "基金名称",
      "shares": 持有份额,
      "costPrice": 成本价,
      "notes": "备注"
    }
  ]
}
```

### 本地测试

```bash
# 安装依赖
pip install -r requirements.txt

# 获取基金数据
python fetch_fund_data.py

# 生成HTML
python generate_html.py

# 查看生成的 index.html
```

## 自动化

GitHub Actions会自动：
1. 每天定时运行
2. 获取最新基金数据
3. 生成HTML页面
4. 推送到仓库
5. GitHub Pages自动更新

## 访问网址

https://dalinna.github.io/fund-tracker/
