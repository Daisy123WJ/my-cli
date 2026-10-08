from openai import OpenAI
import os

#测试成功 执行指令：uv run python test_silicon.py
try:

    client=OpenAI(
    api_key=os.environ["LLM_API_KEY"],
    base_url="https://api.siliconflow.cn/v1"
    )
    print("开始请求硅基流动API....")
    #消息列表，初始带上system
    messages=[{"role":"system","content":"你是简洁的小助手，回答简短."}]

    #第一轮提问
    messages.append({"role":"user","content":"介绍一下token"})
    resp=client.chat.completions.create(model="deepseek-ai/DeepSeek-V3",messages=messages)
    ans1=resp.choices[0].message.content
    print("收到返回结果：")
    print("AI回答：",ans1)
    
    #把AI的回答塞回messages
    messages.append({"role":"assistant","content":ans1})

    #第二轮提问(AI能看到第一轮对话)
    messages.append({"role":"user","content":"那怎么减少token消耗？"})
    resp2=client.chat.completions.create(model="deepseek-ai/DeepSeek-V3", messages=messages) 
    ans2=resp2.choices[0].message.content
    print("AI回答2：",ans2)
    messages.append({"role":"assistant","content":ans2})

    print("\n====== 消息数组全部内容 ===")

    #打印token消耗
    # usage=resp.usage
    # print("\n====== token 消耗统计 ===")
    # print(f"prompt_tokens(输入):{usage.prompt_tokens}")
    # print(f"completion_tokens(输出):{usage.completion_tokens}")
    # print(f"total_tokens(总计):{usage.total_tokens}")

except Exception as e:
    print(f"出错了，调用失败:{e}")