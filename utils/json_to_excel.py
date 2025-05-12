import pandas as pd
import json
import sys

def json_to_excel(json_file_path, excel_file_path):
    try:
        # 读取JSON文件
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        
        # 检查JSON数据结构，处理嵌套的"data"字段
        if isinstance(json_data, dict) and "data" in json_data:
            data = json_data["data"]
        else:
            data = json_data
        
        # 将JSON数据转换为DataFrame
        df = pd.DataFrame(data)
        
        # 将DataFrame保存为Excel文件
        df.to_excel(excel_file_path, index=False)
        
        print(f"转换成功！Excel文件已保存至: {excel_file_path}")
    
    except Exception as e:
        print(f"转换过程中出现错误: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方法: python json_to_excel.py <json文件路径> <excel文件路径>")
    else:
        json_file_path = sys.argv[1]
        excel_file_path = sys.argv[2]
        json_to_excel(json_file_path, excel_file_path)
    # example for json:
    # {
    #     "data": [
    #         {
    #             "knowledge_point_type": "数据结构基本概念",
    #             "question": "数据结构是一门研究非数值计算的程序设计问题中的操作对象以及它们之间的（）和运算的学科。",
    #             "option_A": "结构",
    #             "option_B": "关系",
    #             "option_C": "运算",
    #             "option_D": "算法",
    #             "answer": "B",
    #             "difficulty": 3,
    #             "bloom_level": "a"
    #         },
    #         {
    #             "knowledge_point_type": "数据结构基本概念",
    #             "question": "在数据结构中，从逻辑上可以把数据结构分成（）。",
    #             "option_A": "动态结构和静态结构",
    #             "option_B": "紧凑结构和非紧凑结构",
    #             "option_C": "线性结构和非线性结构",
    #             "option_D": "逻辑结构和存储结构",
    #             "answer": "C",
    #             "difficulty": 3,
    #             "bloom_level": "a"
    #         },
    # }