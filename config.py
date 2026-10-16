# -*- coding: utf-8 -*-
"""
股票看板配置文件
修改 STOCKS 列表即可自定义监控的标的
"""

# 监控股票列表（腾讯财经代码格式）
STOCKS = [
    # === 社保抱团股 ===
    {"code": "sh600196", "name": "复星医药", "category": "社保关注"},
    {"code": "sz000680", "name": "山推股份", "category": "社保抱团"},
    {"code": "sh600176", "name": "中国巨石", "category": "社保抱团"},
    {"code": "sz002396", "name": "星网锐捷", "category": "社保抱团"},
    {"code": "sz002078", "name": "太阳纸业", "category": "社保抱团"},
    {"code": "sh600426", "name": "华鲁恒升", "category": "社保抱团"},
    {"code": "sz000534", "name": "万泽股份", "category": "社保抱团"},

    # === 大盘指数 ===
    {"code": "sh000001", "name": "上证指数", "category": "指数"},
    {"code": "sz399001", "name": "深证成指", "category": "指数"},
    {"code": "sh000300", "name": "沪深300", "category": "指数"},
    {"code": "sh000016", "name": "上证50", "category": "指数"},
    {"code": "sz399006", "name": "创业板指", "category": "指数"},
    {"code": "sh000688", "name": "科创50", "category": "指数"},

    # === 热门板块代表 ===
    {"code": "sh600519", "name": "贵州茅台", "category": "消费"},
    {"code": "sz000858", "name": "五粮液", "category": "消费"},
    {"code": "sh601012", "name": "隆基绿能", "category": "新能源"},
    {"code": "sz300750", "name": "宁德时代", "category": "新能源"},
    {"code": "sh600036", "name": "招商银行", "category": "金融"},
    {"code": "sh601318", "name": "中国平安", "category": "金融"},
    {"code": "sz000002", "name": "万科A", "category": "地产"},
    {"code": "sh600048", "name": "保利发展", "category": "地产"},
    {"code": "sh603259", "name": "药明康德", "category": "医药"},
    {"code": "sz300760", "name": "迈瑞医疗", "category": "医药"},
    {"code": "sh688981", "name": "中芯国际", "category": "半导体"},
    {"code": "sz002371", "name": "北方华创", "category": "半导体"},
    {"code": "sh601127", "name": "赛力斯", "category": "汽车"},
    {"code": "sz002594", "name": "比亚迪", "category": "汽车"},
    {"code": "sh600900", "name": "长江电力", "category": "电力"},
    {"code": "sh601899", "name": "紫金矿业", "category": "有色"},
    {"code": "sh600309", "name": "万华化学", "category": "化工"},
    {"code": "sz002142", "name": "宁波银行", "category": "金融"},
    {"code": "sh600276", "name": "恒瑞医药", "category": "医药"},
    {"code": "sz300124", "name": "汇川技术", "category": "制造"},
    {"code": "sh601888", "name": "中国中免", "category": "消费"},
    {"code": "sz000568", "name": "泸州老窖", "category": "消费"},
    {"code": "sh603288", "name": "海天味业", "category": "消费"},
    {"code": "sz002475", "name": "立讯精密", "category": "电子"},
    {"code": "sh600585", "name": "海螺水泥", "category": "建材"},
    {"code": "sz000001", "name": "平安银行", "category": "金融"},
    {"code": "sh601728", "name": "中国电信", "category": "通信"},
    {"code": "sh600941", "name": "中国移动", "category": "通信"},
    {"code": "sz000063", "name": "中兴通讯", "category": "通信"},
    {"code": "sh601668", "name": "中国建筑", "category": "建筑"},
    {"code": "sh601669", "name": "中国电建", "category": "建筑"},
    {"code": "sz002271", "name": "东方雨虹", "category": "建材"},
    {"code": "sh600031", "name": "三一重工", "category": "机械"},
    {"code": "sz000425", "name": "徐工机械", "category": "机械"},
    {"code": "sh601766", "name": "中国中车", "category": "机械"},
    {"code": "sz300014", "name": "亿纬锂能", "category": "新能源"},
    {"code": "sh600438", "name": "通威股份", "category": "新能源"},
    {"code": "sz002460", "name": "赣锋锂业", "category": "新能源"},
    {"code": "sh603993", "name": "洛阳钼业", "category": "有色"},
    {"code": "sh600111", "name": "北方稀土", "category": "有色"},
    {"code": "sz000933", "name": "神火股份", "category": "有色"},
    {"code": "sh601088", "name": "中国神华", "category": "煤炭"},
    {"code": "sh601225", "name": "陕西煤业", "category": "煤炭"},
    {"code": "sz002128", "name": "露天煤业", "category": "煤炭"},
    {"code": "sh600028", "name": "中国石化", "category": "能源"},
    {"code": "sh601857", "name": "中国石油", "category": "能源"},
    {"code": "sh600256", "name": "广汇能源", "category": "能源"},
    {"code": "sz300498", "name": "温氏股份", "category": "农业"},
    {"code": "sh600298", "name": "安琪酵母", "category": "消费"},
    {"code": "sz000895", "name": "双汇发展", "category": "消费"},
    {"code": "sh603501", "name": "韦尔股份", "category": "半导体"},
    {"code": "sz300433", "name": "蓝思科技", "category": "电子"},
    {"code": "sh600745", "name": "闻泰科技", "category": "电子"},
    {"code": "sz002241", "name": "歌尔股份", "category": "电子"},
]

# 数据存储路径
DATA_DIR = "data"
REPORTS_DIR = "reports"
HISTORY_FILE = f"{DATA_DIR}/history.csv"

# 技术指标参数
MA_PERIODS = [5, 10, 20, 60]
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# 报告生成时间
MORNING_TIME = "08:30"
EVENING_TIME = "20:00"
