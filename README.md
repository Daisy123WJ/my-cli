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


-- 用 curl.exe 裸调一次，亲眼看原始 JSON  deepseek-ai/DeepSeek-V3   
--       https://api.siliconflow.cn/v1/chat/completions\
curl.exe https://api.siliconflow.cn/v1/chat/completions `
>>   -H "Authorization: Bearer sk-ooztqgzxbpcybmwbgothatlslihqdrihlbqsvnldlgymplzf" `
>>   -H "Content-Type: application/json" `
>>   -d '{"model":"deepseek-ai/DeepSeek-V3","messages":[{"role":"user","content":"用一句话解释什么是RAG"}]}'

curl.exe https://api.siliconflow.cn/v1/chat/completions -H "Authorization: Bearer sk-ooztqgzxbpcybmwbgothatlslihqdrihlbqsvnldlgymplzf"-H "Content-Type: application/json" 
-d "{`"model`":`"deepseek-ai/DeepSeek-V3`",`"messages`":[{`"role`":`"user`",`"content`":`"用 一句话解释什么是 RAG`"}]}"

curl --request POST \
  --url https://api.siliconflow.cn/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "model": "deepseek-ai/DeepSeek-V4-Flash",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello, please introduce yourself."}
    ]
  }'

curl.exe https://api.siliconflow.cn/v1/chat/completions`
  -H "Content-Type: application/json"`
  -H "Authorization: Bearer sk-ooztqgzxbpcybmwbgothatlslihqdrihlbqsvnldlgymplzf"` 
  -d "{`
    "model": "deepseek-ai/DeepSeek-V3",`
    "messages": [`
      {"role": "system", "content": "You are a helpful assistant."},`
      {"role": "user", "content": "Hello, please introduce yourself."}`
    ]`
  }"`


url.exe https://api.siliconflow.cn/v1/chat/completions -H "Content-Type: application/json" -H "Authorization: Bearer sk-ooztqgxxxxxxxxxxxx" -d "{`"model`":`"deepseek-ai/DeepSeek-V3`",`"messages`":[{`"role`":`"system`",`"content`":`"You are a helpful assistant.`"},{`"role`":`"user`",`"content`":`"Hello, please introduce yourself.`"}]}"

2026-10-8：算一笔账：处理 1000 份文档要花多少（40 min）
步骤	    做法	                                                           产出
取单价	  去硅基流动官网查 DeepSeek-V3 的 输入/输出 单价（元 / 百万 token）	  如 输入 ¥1 / 百万、输出 ¥2 / 百万
估单份量	假设你每份文档平均 800 字进、回 200 字 ≈ 约 1000 + 250 token	     单份 ≈ 1250 token
乘 1000	 1000 × 1250 = 1,250,000 token = 1.25 百万	                      总量
算总价	  输入 1.25M×¥1 + 输出 0.25M×¥2 ≈ ¥1.75（实际不花钱，这是估算练习） 	一份成本结论

所以若一篇为800字的文档，输出为200字，那么需要花费的token大概为1.25百万，合计约1.5元