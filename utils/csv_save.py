import csv
import json
import os
from typing import Dict, Any, Optional


def append_messages_to_talks_student(student_ID: str, new_messages: list[dict],
                               file_path: str = './data/talks_student.csv') -> bool:
    """
    将新消息追加到指定学生的现有消息中

    Args:
        student_ID: 学生编号
        new_messages: 要添加的新消息列表
        file_path: CSV文件路径

    Returns:
        bool: 操作成功返回True，否则返回False
    """
    # 检查参数有效性
    if not isinstance(new_messages, list) or not all(isinstance(item, dict) for item in new_messages):
        print("错误: 提供的消息不是有效的列表字典格式")
        return False

    rows = []
    session_id = f"{student_ID}_01"

    try:
        # 读取CSV文件
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)

            # 查找并更新学生记录
            for i, row in enumerate(rows):
                if row.get("Student_ID") == student_ID:
                    try:
                        existing_messages = json.loads(row.get("contents", "[]"))
                        # 直接将新消息追加到现有消息后面
                        existing_messages.extend(new_messages)
                        rows[i]["contents"] = json.dumps(existing_messages, ensure_ascii=False)

                        # 写回文件
                        fieldnames = ["Session_ID", "Student_ID", "contents"]
                        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            writer.writeheader()
                            writer.writerows(rows)
                        return True
                    except json.JSONDecodeError:
                        # 解析失败时使用新message
                        rows[i]["contents"] = json.dumps(new_messages, ensure_ascii=False)

                        # 写回文件
                        fieldnames = ["Session_ID", "Student_ID", "contents"]
                        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            writer.writeheader()
                            writer.writerows(rows)
                        return True
        # 如果执行到这里，说明没有找到学生记录
        # 创建新行
        new_row = {
            "Session_ID": session_id,
            "Student_ID": student_ID,
            "contents": json.dumps(new_messages, ensure_ascii=False)
        }
        rows.append(new_row)

        # 写回文件
        fieldnames = ["Session_ID", "Student_ID", "contents"]
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        return True
    except Exception as e:
        print(f"添加消息时出错: {e}")
        return False


def save_learning_path_to_csv(student_id: int, learning_path: Dict[str, Any],file_path: str = '../data/student_learning_paths.csv') -> None:
    """
    将学习路径规划结果保存到CSV文件中

    Args:
        student_id: 学生编号
        learning_path: 包含学习路径规划的字典
        file_path: 要保存的CSV文件路径
    """
    # 检查是否为有效的学习路径数据
    if not isinstance(learning_path, dict):
        print("错误: 提供的学习路径不是有效的字典格式")
        return

    # 定义表头
    headers = ["学生编号", "当前水平评估", "定制方法", "调整深度", "结构化路径", "可行性建议", "最终目标"]

    # 检查文件是否已存在
    file_exists = os.path.isfile(file_path)

    try:
        with open(file_path, 'a', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)

            # 如果文件不存在，写入表头
            if not file_exists:
                writer.writeheader()

            # 准备要写入的行数据
            row = {"学生编号": student_id}  # 添加学生编号

            # 添加其他字段
            for header in headers[1:]:  # 跳过"学生编号"字段
                if header in learning_path:
                    row[header] = json.dumps(learning_path[header], ensure_ascii=False)
                else:
                    row[header] = ""

            writer.writerow(row)
            print(f"已成功将学习路径规划数据写入到 {file_path}")

    except Exception as e:
        print(f"写入CSV文件时出错: {e}")


if __name__ == "__main__":
    message = [{"role": "user", "content": "你好吗？"},]
    student_id = "S00001"
    append_messages_to_talks_student(student_id, message)
