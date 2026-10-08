import pytest
from _stream import chat,calc_1000_docs_cost

@pytest.mark.api
def test_normal_chat():
    #测试普通非流式对话，拿到回答，token,耗时，token>0
    ans,usage,cost_time=chat("简单介绍token是什么")
    #断言
    assert ans is not None
    assert len(ans)>0
    assert usage.prompt_tokens>0
    assert usage.completion_tokens>0
    assert usage.total_tokens>0
    assert cost_time>0

def test_cost_calc():
    #测试成本估算函数，数学计算正确
    cost = calc_1000_docs_cost(1000,0.002)
    assert cost == 2.0

    cost = calc_1000_docs_cost(500,0.002)
    assert cost ==1.0 



@pytest.mark.api
def test_multi_round():
    #多轮对话测试，AI记住上文
    ans2,usage2,t2=chat("那怎么减少Token消耗？")
    assert "token" in ans2.lower()

@pytest.mark.api
def test_stream_chat():
    #流式对话测试，能返回非空回答+耗时
    ans_stream,t_stream=chat("一句话解释大模型API原理",steram=True)
    assert ans_stream is not None
    assert len(ans_stream) >0
    assert t_stream>0

                            
















