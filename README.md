# 📊 交易员看板

> 基于顶级交易员方法论构建的个人股票监控系统。  
> **零成本 · 全自动 · 纯GitHub托管**

---

## ✨ 特性

| 功能 | 说明 |
|------|------|
| 🔄 **自动更新** | 每天北京时间 **08:30** 和 **20:00** 自动拉取行情 |
| 📈 **技术指标** | MA5/10/20/60、RSI、MACD、布林带 |
| 🏷️ **交易信号** | 均线排列、RSI超买超卖、MACD金叉死叉 |
| 🌡️ **情绪温度计** | 基于监控标的涨跌分布估算 |
| 🌐 **在线看板** | 部署在 GitHub Pages，手机/电脑随时访问 |
| 💾 **历史累积** | 数据自动提交回仓库，技术指标越跑越准 |
| 💰 **完全免费** | 不花一分钱，不租服务器 |

---

## 🚀 5分钟搭建（跟着做就行）

### 第1步：创建你的GitHub仓库

1. 打开 [github.com/new](https://github.com/new)
2. Repository name 填 `stock-dashboard`（随便取）
3. 选择 **Public**（Private 也能用，但 Pages 有额外限制）
4. ✅ 勾选 **Add a README file**
5. 点击 **Create repository**

---

### 第2步：上传代码

**方式A：网页上传（最简单）**

1. 进入你刚创建的仓库
2. 点击 **Add file → Upload files**
3. 把本项目的所有文件拖进去（或直接选 `stock-dashboard.zip` 解压后的文件）
4. 点击 **Commit changes**

**方式B：命令行上传**

```bash
# 1. 克隆你的仓库
git clone https://github.com/你的用户名/stock-dashboard.git
cd stock-dashboard

# 2. 把代码文件复制进来
# （把 stock-dashboard.zip 解压后的文件全部复制到这个目录）

# 3. 提交
 git add .
 git commit -m "init: 交易员看板"
 git push origin main
```

---

### 第3步：开启 GitHub Pages

1. 进入仓库 → 点击 **Settings**（顶部标签）
2. 左侧菜单点击 **Pages**
3. **Source** 选择 **Deploy from a branch**
4. **Branch** 选择 `gh-pages` / `(root)`
5. 点击 **Save**
6. 等待1-2分钟，页面会显示访问地址：
   ```
   https://你的用户名.github.io/stock-dashboard/
   ```

> ⚠️ 第一次需要等 Actions 跑完（约2-3分钟）才有内容。

---

### 第4步：开启 Actions 权限（关键！）

1. 仓库 → **Settings** → **Actions** → **General**
2. 找到 **Workflow permissions**
3. 选择 **Read and write permissions**
4. 点击 **Save**

> 这步必须做，否则 Actions 无法提交历史数据，也无法部署 Pages。

---

### 第5步：手动触发第一次运行

1. 仓库 → **Actions**（顶部标签）
2. 点击左侧 **📊 交易员看板 - 每日更新**
3. 点击右侧 **Run workflow** → **Run workflow**
4. 等待约1分钟，看到绿色 ✅ 就是成功了
5. 刷新 GitHub Pages 地址，看板就出来了！

---

## 📁 项目结构

```
stock-dashboard/
├── .github/
│   └── workflows/
│       └── update.yml          # GitHub Actions 定时任务
├── data/
│   └── history.csv             # 历史数据（自动累积）
├── reports/
│   └── index.html              # 生成的看板（自动部署到 Pages）
├── config.py                   # 股票列表配置
├── fetch_data.py               # 数据拉取
├── indicators.py               # 技术指标
├── generate_report.py          # HTML生成
├── main.py                     # 主入口
└── requirements.txt            # Python依赖
```

---

## ⚙️ 自定义股票列表

编辑 `config.py` 里的 `STOCKS` 列表：

```python
STOCKS = [
    {"code": "sh600196", "name": "复星医药", "category": "医药"},
    {"code": "sz000680", "name": "山推股份", "category": "机械"},
    # 添加你自己的...
]
```

**代码格式**：
- 上海股票：`sh` + 6位代码，如 `sh600196`
- 深圳股票：`sz` + 6位代码，如 `sz000680`
- 创业板：`sz` + 6位代码，如 `sz300750`
- 科创板：`sh` + 6位代码，如 `sh688981`

修改后提交到仓库，下次自动更新就生效。

---

## 📊 看板内容

访问 `https://你的用户名.github.io/stock-dashboard/` 可看到：

1. **市场概览** — 涨跌家数、平均涨跌、最强/最弱标的
2. **情绪温度计** — 1-10分评分 + 进度条
3. **涨跌 TOP 5** — 涨幅榜 / 跌幅榜
4. **个股卡片** — 价格、均线、RSI、MACD信号、技术标签

---

## ⏰ 定时任务说明

| 北京时间 | UTC时间 | 触发动作 |
|---------|---------|---------|
| 08:30 | 00:30 | 早盘前更新，生成当日看板 |
| 20:00 | 12:00 | 收盘后更新，生成复盘看板 |

如果需要调整时间，编辑 `.github/workflows/update.yml` 里的 `cron`：

```yaml
schedule:
  - cron: "30 0 * * *"   # 北京时间 08:30
  - cron: "0 12 * * *"   # 北京时间 20:00
```

[cron表达式在线工具](https://crontab.guru/)

---

## 🔧 常见问题

**Q: Actions 显示红色 ❌ 失败了怎么办？**

1. 点击失败的运行记录
2. 查看报错信息（通常是网络问题或权限问题）
3. 确认第4步的 **Read and write permissions** 已开启
4. 点击 **Re-run jobs** 重新运行

**Q: Pages 打开是 404？**

1. 确认 Actions 已经成功运行（绿色 ✅）
2. 确认 Pages 设置里 Branch 选的是 `gh-pages`
3. 等待2-3分钟再刷新
4. 地址格式：`https://你的用户名.github.io/仓库名/`

**Q: 历史数据会丢失吗？**

不会。每次运行后，`data/history.csv` 会自动提交回 `main` 分支永久保存。即使换电脑，数据也在GitHub上。

**Q: 可以监控多少只股票？**

腾讯接口一次最多支持60只。如果超过60只，需要修改 `fetch_data.py` 做分批请求。

**Q: 数据实时吗？**

不是实时，是快照。每次运行拉取的是当前时刻的行情，适合日线级别的跟踪。

---

## 🔒 免责声明

- 本项目仅供个人学习研究使用
- 数据来源于腾讯财经公开接口
- **不构成任何投资建议**，交易风险自担
