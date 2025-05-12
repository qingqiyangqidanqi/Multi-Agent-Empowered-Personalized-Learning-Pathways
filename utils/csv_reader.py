import csv
import os
import json
from typing import Dict, Any, Generator, Optional


def read_data_from_csv(order: int = 0, file_path: str = '../data/student_performance_large_dataset.csv') -> \
Generator[Dict[str, Any], None, None]:
    """
    读取指定CSV文件中的学生数据，每次调用返回一行数据

    Args:
        order: 从第几行开始读取数据（0表示从第一行开始）
        file_path: CSV文件路径，默认为'data/student_performance_large_dataset.csv'

    Yields:
        Dict[str, Any]: CSV文件中的一行数据，表示为字典
    """
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"错误: 文件 {file_path} 不存在")
        return

    # 读取所有行数据
    message = []
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                message.append(row)

        print(f"成功读取{len(message)}条数据")

        # 使用迭代器返回每条数据
        current_index = order
        while True:
            if current_index >= len(message):
                current_index = 0  # 循环结束后重新开始
                print("已读取完所有学生数据，从头开始")

            yield message[current_index]    # yield语句返回一个值，并且函数执行暂停，保存所有当前的状态(局部变量等),下一次调用next()方法时，函数从上次暂停的地方继续执行
            current_index += 1

    except Exception as e:
        print(f"读取CSV文件时出错: {e}")
        yield None


if __name__ == '__main__':
    # 示例用法
    order = 0
    csv_file_path = '../data/student_performance_large_dataset.csv'

    # 创建学生数据生成器
    student_data_generator = read_data_from_csv(order = order, file_path=csv_file_path)

    # 获取下一条学生数据
    student_data = next(student_data_generator)
    student_message = json.dumps(student_data)
    print(f"当前处理的学生数据: {student_message}")
