# clean-data · 主业务表 T1 脏数据清洗工具

## 功能
把某三甲医院主业务表 T1 里「频次字段」的非标准写法
（"每日三次" / "tid" / "3/日" 混用）归一化为标准编码。

## 环境
- Python 3.11+
- 依赖见 requirements.txt

## 安装
```bash
uv venv
uv pip install -r requirements.txt
```

## 运行
```bash
python src/clean_data.py --src input.csv --out output.csv
python src/clean_data.py --src input.csv --out output.csv --dry-run
```

## 输入 / 输出
- 输入：含「频次」列的 CSV（列名脱敏为 freq）
- 输出：归一化后的 CSV + 控制台日志（跳过/异常的行列号）

## 示例
```bash
python src/clean_data.py --src sample/raw.csv --out sample/clean.csv
```

## 注意事项
- 涉及给药安全，归一化后建议人工复核；本工具仅做建议，不自动写库。
- 不提交任何真实数据，sample/ 下只用脱敏样例。