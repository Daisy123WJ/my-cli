import time
from openai import OpenAI

#使用OpenAI库来调用硅基流动API，返回回答+token消耗+耗时
client = OpenAI(
    api_key="LLM_API_KEY",
    base_url="https://api.siliconflow.cn/v1"
)

#消息历史
messages = [{"role": "system", "content": "你是简洁的小助手，回答简短."}] 

def chat(user_input,stream=False): 
    messages.append({"role": "user", "content": user_input})
    start=time.time()
    resp = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3", 
        messages=messages,
        stream=stream
    )
    if stream:
        #流式输出
        full_ans=""
        print("AI: ",end="")
        for chunk in resp:
            piece=chunk.choicesp[0].delta.content
            if piece:
                full_ans+=piece
                print(piece,end="")
        print()
        cost_time=time.time()-start
        messages.append({"role": "assistant", "content": full_ans})
        print(f"本次对话耗时: {cost_time:.2f}秒")
        return full_ans
    else:
        #非流式输出
        ans = resp.choices[0].message.content
        cost_time=time.time()-start
        usage=resp.usage
        print("AI:",ans)
        print(f"\ntoken统计：prompt={usage.prompt_tokens},complition={usage.complition_tokens},total={usage.total_tokens}")
        print(f"耗时：{cost_time:.2f}s")
        messages.append({"role": "assistant", "content": ans})
        return ans,usage
    
    #成本估算函数，输入单篇total_tokens,1000篇总花费
def calc_1000_docs_cost(single_total_token,price_per_1k=0.002):
    total_token_1000=single_total_token*1000
    total_cost=total_token_1000/1000*price_per_1k
    print(f"单篇token：{single_total_token},1000篇总token:{total_token_1000},预计费用：{total_cost:.4f}元")
    return total_cost

if __name__=="__main__":

#----------------测试---------------
 ans,usage=chat("简单介绍token是什么")
 calc_1000_docs_cost(usage.total_tokens)
 #第二轮多轮对话测试
 chat("刚才说的token，怎么减少消耗")
 #流式测试
 chat("用一句话总结大模型API原理",stream=True)
