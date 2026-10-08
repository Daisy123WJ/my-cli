import argparse,logging
import pandas as pd
import os

def setup_logger():
    #创建logger对象
    log=logging.getLogger(__name__)
    log.setLevel(logging.INFO)

    #防止重复添加Handler
    if log.handlers:
        return log
    #日志格式
    log_format=logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    #1.控制台输出
    console_handler=logging.StreamHandler()
    console_handler.setFormatter(log_format)

    #2.文件输出，日志保存到run.log
    file_handler=logging.FileHandler("run.log",encoding="utf-8")
    file_handler.setFormatter(log_format)

    #把两个处理器添加到logger
    log.addHandler(console_handler)
    log.addHandler(file_handler)
    return log

#初始化日志
log=setup_logger()    

def parse_args():
    p=argparse.ArgumentParser(description="清洗主业务表T1的脏数据(频次字段归一体)")
    p.add_argument("--src",required=True,help="输入 csv 路径")
    p.add_argument("--out",required=True,help="输出 csv 路径")
    p.add_argument("--dry-run",action="store_true",help="只打印将要做的改动，不写文件")
    p.add_argument("--verbose",action="store_true",help="开启详细DEBUG日志")
    return p.parse_args()

def main():

    keys=os.environ["LLM_API_KEY"]
    print("KEY:",keys)

    args=parse_args()
    log.info("开始读取文件: %s",args.src)

    #开启调试模式
    if args.verbose:
        log.setLevel(logging.DEBUG)
        log.debug("调试模式开启")
    
    #自动创建输出文件夹
    out_dir=os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir,exist_ok=True)
        log.info(f"输出目录检查完成：{out_dir}")    

    #读取csv
    df=pd.read_csv(args.src)
    log.info("读取完成，一共 %d 行",len(df)+1)

    #删除空值行
    df=df.dropna()
    log.info("清洗后剩下 %d 行",len(df)+1)

    if args.dry_run:
        log.info("dry-run 模式，不会写入文件") 
        return

   #这一行才是真正创建/保存文件的关键
    df.to_csv(args.out,index=False)
    log.info("文件成功写入: %s",args.out)

if __name__=="__main__":
    try:     
        main()
    except Exception as e:
        log.error("程序运行出错: %s",e,exc_info=True)