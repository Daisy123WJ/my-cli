import pytest
from tid import normalize_freq, needs_human,process_row
from clean_data import parse_args,main,log


def test_parse_args():
    #模拟命令行参数
    import sys
    sys.argv=["script.py","--src","input.csv","--out","output.csv"]
    args=parse_args()
    assert args.src=="input.csv"
    assert args.out=="output.csv"
    assert args.dry_run==False
    assert args.verbose==False

def test_exact_hit():
    code,conf=normalize_freq("BID")
    assert code == "BID"
    assert conf == 1.0

def test_needs_human_threshold():
    #置信度1.0 且非UNKNOWN -> 不需要人工复核
    assert needs_human("TID",1.0) is False  
    #置信度0.6 低于默认阈值0.9 -> 必须人工
    assert needs_human("TID",0.6) == True 
    #UNKNOWN -> 必须人工
    assert needs_human("UNKNOWN",0.0) == True

def test_fuzzy_hit():
    code,conf=normalize_freq("QID")
    assert code == "QID"
    assert conf == 1.0

def test_unknown():
    code,conf=normalize_freq("每周一次")
    assert code == "UNKNOWN"
    assert conf == 0.0

def test_add():
    assert 1 + 1 == 2    

def test_boundaries():
    assert normalize_freq(None)[0]=="UNKNOWN"
    assert normalize_freq("")[0]=="UNKNOWN"
    assert normalize_freq(" Tid ")[0]=="TID"
    assert normalize_freq("Tid")[0]=="TID"
    assert normalize_freq("每日三次！")[0]=="TID"

#装饰器 定义参数列表
@pytest.mark.parametrize("raw,exp_code,exp_conf",[
    ("tid",      "TID",  1.0),
    ("每日三次",  "TID",  1.0),
    ("3/日",      "TID",  1.0),
    ("一日三次", "TID",1.0),
    ("每周一次",   "UNKNOWN",0.0),
    (None,        "UNKNOWN",0.0)
]) 
def test_normalize_table(raw,exp_code,exp_conf):
    #调用业务函数
    code,conf=normalize_freq(raw)
    #两个断言,同时校验结果
    assert code == exp_code
    assert conf == exp_conf    

def test_process_row():
    row=process_row("tid")
    assert row["code"]=="TID"
    assert row["needs_human"]==False
   

    
    