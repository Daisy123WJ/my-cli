#标准编码 各种脏写法 的同义词表
SYNONYMS:dict[str,list[str]]={
     "QD":["每日一次","每天一次","qd","1/日","一日一次","once daily"],
    "BID":["每日两次","每天两次","bid","2/日","一日两次"], 
    "TID":["每日三次","每天三次","tid","3/日","一日三次"],
    "QID":["每日四次","每天四次","qid","4/日"]
}
#反向索引：脏写法(小写去空格)->标准编码
_LOOKUP:dict[str,str]={}
for _code,_alts in SYNONYMS.items():
    for _alt in _alts:
        _LOOKUP[_alt.lower().strip()]=_code 

def normalize_freq(raw:str|None)->tuple[str,float]:
    """ 返回(标准编码，置信度)。置信度 1.0==精确命中，0.6=模糊命中，0.0=未知"""
    if not raw:
        return "UNKNOWN",0.0
    s=raw.strip().lower()
    if s in _LOOKUP:
        return _LOOKUP[s],1.0
    #模糊兜底：包含关键词（如“三次” 也归一下，但置信度降一档）
    for code,alts in SYNONYMS.items():
        for a in alts:
            if a in s:
                return code,0.6
    return "UNKNOWN",0.0        

def needs_human(code:str,confidence:float,thresthod:float=0.9)->bool:
    """AI/规则都不确定时,必须人工复核--医疗场景的底线"""
    return code=="UNKNOWN" or confidence<thresthod

#把"处理一行"的逻辑抽成纯函数
def process_row(raw:str)->dict:
    code,conf=normalize_freq(raw)
    return {"raw":raw,"code":code,
            "confidence":conf,
            "needs_human":needs_human(code,conf)}

if __name__=="__main__":
    sample_inputs=["tid", "每日三次", "3/日", "一天吃三次", "每周一次",None]
    #测试
    for raw in sample_inputs:
        code,conf=normalize_freq(raw)
        flag="->需要人工复核" if needs_human(code,conf) else ""
        print(f"{raw} => {code} ({conf})")