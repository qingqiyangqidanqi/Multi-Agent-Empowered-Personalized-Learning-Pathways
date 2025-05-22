import csv
import os
import logging
from typing import Dict, Any, Optional


def read_csv_student_data(id: str = "S00001", file_path: str = './data/student_performance_large_dataset.csv') -> \
Optional[
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


def read_csv_quiz_data(session_id: str = "S00001_01", file_path: str = './data/talks_quiz.csv') -> Optional[
    Dict[str, Any]]:
    """
    通过id读取计算机自适应测试会话CSV文件的指定行，如果不存在文件则返回None,如果不存在指定行则返回一个新行
    Args:
        session_id: 计算机自适应测试会话id
        file_path: CSV文件路径
    Returns:
        Dict[str, Any]: 包含CSV行数据的字典，若未找到则返回False
    """
    if not os.path.exists(file_path):
        print(f"错误: 文件 {file_path} 不存在")
        logging.info(f"错误: 文件 {file_path} 不存在")
        return None

    try:
        # 尝试从会话ID中提取学生ID (假设格式为"S00001_01")
        student_id = session_id.split('_')[0] if '_' in session_id else None

        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)

            # 尝试找到匹配的会话行
            for row in rows:
                if row.get("Session_ID") == session_id:
                    return dict(row)

            # 如果没找到，则返回None
            return None

    except Exception as e:
        print(f"读取CSV文件时出错: {e}")


def is_student_exists_in_csv(student_ID: str, file_path: str = './data/talks_student.csv') -> bool:
    """
    检查CSV文件中是否存在指定学生ID的记录

    Args:
        student_ID: 学生编号
        file_path: CSV文件路径

    Returns:
        bool: 如果学生存在返回True，否则返回False
    """
    # 检查文件是否存在
    if not os.path.isfile(file_path):
        return False

    try:
        # 读取CSV文件
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get("Student_ID") == student_ID:
                    return True
        # 没找到该学生
        return False
    except Exception as e:
        print(f"检查学生是否存在时出错: {e}")
        return False

if __name__ == '__main__':
    # 示例用法
    # csv_file_path = './data/student_performance_large_dataset.csv'
    # csv_file_path ='./data/talks_student.csv'
    # csv_file_path = './data/talks_quiz.csv'
    # student_data = read_csv_student_data(id="S00001", file_path=csv_file_path)
    # print(student_data)

    # is_exist = is_student_exists_in_csv("S00002", file_path='./data/talks_student.csv')
    # print(is_exist)

    # system_promt = read_csv_student_data(id="S00001", file_path='./data/talks_student.csv')
    # print(system_promt)
    # result = system_promt.get('contents')
    # print(result)

    csv_file_path = './data/talks_quiz.csv'
    student_data = read_csv_quiz_data(session_id="S00001_01", file_path=csv_file_path)
    print(student_data)
    student_QA = student_data['QA']
    print(student_QA)
    student_question_num = student_data['question_num']
    print(student_question_num)
    student_QA_list = eval(student_QA)
    print(student_QA_list)
    print(len(student_QA_list))

    # for item in student_QA_list:
    #     print(item)
    #     print(item['order'])
    #     print(item['knowledge_point_type'])
    #     print(item['question'])
    #     print(item['answer'])
    #     print(item['user_answer'])
    #     print(item['is_True'])

