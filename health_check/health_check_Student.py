import requests
import sys
import json
from config.prompt import *

header = {"appId": "yxcptj_ydy", "requestId": "80088208820",
          "requestTime": "2021-03-16 23:15:00"}

url = 'http://localhost:10007/student'  # 测试


def check_health(student_id: str, talk: str = ""):
    # 不加统一接口
    http_body = {"student_id": student_id, "talk": talk}

    try:
        exception = 0
        response = requests.post(url, json=http_body, headers=header)
        print(response.text)

        if response.status_code == 200:

            res = '11'


        else:
            exception = 1


    except Exception as e:
        exception = 1
        print(e)
    if exception == 1:
        sys.exit(1)
    return exception


# 示例用法
if __name__ == "__main__":
    student_id = "S00001"
    talk = """
问题 10/10:
[难度: 10] 折半查找具有 n 个元素的线性表，其时间复杂度为 ( ) 。
A. O (n)
B. O (log₂n)
C. O (n²)
D. O (nlog₂n)
    """
    print(check_health(student_id,talk))
