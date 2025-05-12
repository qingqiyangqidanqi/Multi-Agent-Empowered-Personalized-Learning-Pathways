from typing import (
    Dict,
    Any,
    List
)
import yaml
import json
import os

def config_read():
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(current_dir, "configs", "config.yaml")
    fo = open(config_path, 'r', encoding='utf-8')
    res = yaml.load(fo, Loader=yaml.FullLoader)

    return res

def return_config():
    config = config_read()
    return (config["LOG"], config["SERVER"], config["LLM"],
            config["SELECT_SERVER"], config["STUDENT"])

# 读取json文件
def json_read(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# 读取用
def read_lines_to_list(file_path: str) -> List[str]:

    lines_list = []
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                lines_list.append(line)
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到。")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")

    return lines_list


def name_match(name: str, namesList: List[str]) -> bool:
    normalized_product_name = name.lower().strip()

    for product in namesList:
        normalized_product = product.lower().strip()

        # 检查是否匹配
        if normalized_product_name == normalized_product:
            return True

    # 如果没有找到匹配的产品名称，返回 False
    return False

def list2str(lst: List[str]) -> str:
    return ", ".join(lst)

