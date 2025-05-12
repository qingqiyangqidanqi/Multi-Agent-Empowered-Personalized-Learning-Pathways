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