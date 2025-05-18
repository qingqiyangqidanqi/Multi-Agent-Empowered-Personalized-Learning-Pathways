import csv
import os
from typing import Dict, Any, Optional


def read_csv_row(id: str = "S00001", file_path: str = './data/student_performance_large_dataset.csv') -> Optional[
    Dict[str, Any]]:
    """
    通过学生ID读取CSV文件的指定行
    - 如果id格式为"S00001"，则提取数字部分作为索引
    - 否则尝试直接按学生ID匹配

    Args:
        id: 学生ID字符串(如"S00001")
        file_path: CSV文件路径

    Returns:
        Dict[str, Any]: 包含CSV行数据的字典，若未找到则返回None
    """
    if not os.path.exists(file_path):
        print(f"错误: 文件 {file_path} 不存在")
        return None

    try:
        # 从学生ID中提取数字部分作为索引
        # 例如从"S00001"中提取出1
        index = None
        if id.startswith('S'):
            # 去掉前缀S并将剩余部分转换为整数，再减1作为索引
            # (因为学生ID通常从1开始，而索引从0开始)
            index = int(id[1:].lstrip('0')) - 1 if id[1:].lstrip('0') else 0

        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)

            # 如果成功提取出索引，则使用索引获取行
            if index is not None and 0 <= index < len(rows):
                return dict(rows[index])

            # 否则，尝试直接按学生ID匹配
            for row in rows:
                if row.get("Student_ID") == id:
                    return dict(row)

            print(f"警告: 未找到ID为 {id} 的学生数据")
            return None
    except Exception as e:
        print(f"读取CSV文件时出错: {e}")
        return None


# def read_data_from_csv(order: int = 0, file_path: str = '../data/student_performance_large_dataset.csv') -> \
# Generator[Dict[str, Any], None, None]:
#     """
#     读取指定CSV文件中的学生数据，每次调用返回一行数据
#
#     Args:
#         order: 从第几行开始读取数据（0表示从第一行开始）
#         file_path: CSV文件路径，默认为'data/student_performance_large_dataset.csv'
#
#     Yields:
#         Dict[str, Any]: CSV文件中的一行数据，表示为字典
#     """
#     # 检查文件是否存在
#     if not os.path.exists(file_path):
#         print(f"错误: 文件 {file_path} 不存在")
#         return
#
#     # 读取所有行数据
#     message = []
#     try:
#         with open(file_path, 'r', encoding='utf-8') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 message.append(row)
#
#         print(f"成功读取{len(message)}条数据")
#
#         # 使用迭代器返回每条数据
#         current_index = order
#         while True:
#             if current_index >= len(message):
#                 current_index = 0  # 循环结束后重新开始
#                 print("已读取完所有学生数据，从头开始")
#
#             yield message[current_index]    # yield语句返回一个值，并且函数执行暂停，保存所有当前的状态(局部变量等),下一次调用next()方法时，函数从上次暂停的地方继续执行
#             current_index += 1
#
#     except Exception as e:
#         print(f"读取CSV文件时出错: {e}")
#         yield None


if __name__ == '__main__':
    # 示例用法
    order = 0
    csv_file_path = './data/student_performance_large_dataset.csv'

    # # 创建学生数据生成器
    # student_data_generator = read_data_from_csv(order=order, file_path=csv_file_path)
    #
    # # 获取下一条学生数据
    # student_data = next(student_data_generator)
    # student_message = json.dumps(student_data)
    # print(f"当前处理的学生数据: {student_message}")

    student_data = read_csv_row(id="S00003", file_path=csv_file_path)
    print(student_data)
