import os,time,requests


#使用传统的request.post来调用硅基流动API，返回回答+token消耗+耗时
#执行成功 执行命令如下：在 my-cli 这个目录下，1.执行安装requests包的命令：uv pip install requests
# 2.执行命令：uv run python src/first_api.py

#硅基流动（推荐OpenAI兼容，注册送额度）
BASE_URL="https://api.siliconflow.cn/v1/chat/completions"
Model   ="deepseek-ai/DeepSeek-V3"
API_KEY=os.environ.get("LLM_API_KEY")

#非限流 （便于测试/去uage）
def chart(messages):
    to=time.time()
    r=requests.post(
        BASE_URL,
        headers={
            "Content-Type":"application/json",
            "Authorization":f"Bearer {API_KEY}"},
        json={"model":Model,"messages":messages},
        timeout=60,
    )
    r.raise_for_status()
    data=r.json()
    cost=time.time()-to
    usage=data.get("usage",{})
    return data["choices"][0]["message"]["content"],usage,cost

#流式体验
def chart_stream(messages):
    to=time.time()
    r=requests.post(
        BASE_URL,
        headers={
            "Content-Type":"application/json",
            "Authorization":f"Bearer {API_KEY}"},
        json={"model":Model,"messages":messages,"stream":True},
        timeout=60,
        stream=True,
    )
    r.raise_for_status()
    for line in r.iter_lines():
        if not line:
            continue
        line=line.decode("utf-8")
        if line=="data: [DONE]":
            break
        if line.startswith("data: "):
            import json
            chunk=json.loads(line[6:])
            delta=chunk["choices"][0]["delta"].get("content")
            print(delta,end="",flush=True )#逐字打印

#带重试
def chart_safe(messages,retries=3):
    for i in range(retries):
        try:
            return chart(messages)
        except requests.exceptions.Timeout:
            print(f"① 调用超时，第{i+1}次")
        except requests.exceptions.HTTPError  as e:
            if e.response.status_code==429:#限流
                print("触发限流，稍后重试或换本地 0llama");
                break
            else:
                raise  
    return "调用失败",{},0.0
    
if __name__=="__main__":
    msgs=[{"role":"user","content":"用一句话解释什么是 RAG"}]
    ans,usage,cost=chart(msgs)
    #ans=chart_stream(msgs)
    print("AI回答:",ans)
    print(f"耗时: {cost:.2f}秒")
    print(f"使用量: {usage}")

msgs2=[{"role":"system","content":"你是一个严谨的医学术语助手."}]
while True:
    q=input("你")
    if q.lower() in ["exit","quit"]:
        break
    msgs2.append({"role":"user","content":q})
    ans2,usage2,cost2=chart_stream(msgs2)
    #ans2,=chart_stream(msgs2)
    print(f"AI:{ans2} ({usage2.get('total_tokens')} tokens,{cost2:.2f}s)")
    print(f"AI:{ans2} ")
    msgs2.append({"role":"assistant","content":ans2})