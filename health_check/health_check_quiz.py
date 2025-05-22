import requests
import sys
import json
from config.prompt import *

header = {"appId": "yxcptj_ydy", "requestId": "80088208820",
          "requestTime": "2021-03-16 23:15:00"}

url = 'http://localhost:10007/quiz/question'  # 测试


def check_health(student_id: str, session_id: str = ""):
    # 不加统一接口
    http_body = {"student_id": student_id, "session_id": session_id}

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


if __name__ == '__main__':
    student_id   = "S00002"
    session_id = student_id + "_01"
    print(check_health(student_id, session_id))
