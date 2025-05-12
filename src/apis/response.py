from typing import (
    Any,
    List
)
from fastapi.responses import JSONResponse, StreamingResponse
import json
import time
from logging import Logger


# 九天使用
def stream_response(
    response,
    logger: Logger,
    requestId: str,
    start_time: float
) -> Any:

    first_token_time = None
    llm_response = ""

    for line in response.iter_lines():  # 遍历流式响应的每一行
        if line:
            line_str = line.decode("utf-8")  # 将字节解码为字符串
            print(line_str)  # 打印原始行内容（调试用）
            if first_token_time is None:
                first_token_time = time.time()
            try:
                data = json.loads(line_str.split(":", 1)[1])  # 解析 JSON 数据
                if "choices" in data and data["choices"][0].get("finish_reason") != "stop":
                    if "content" in data["choices"][0]["delta"]:  # 检查是否有内容
                        llm_response += data["choices"][0]["delta"]["content"]  # 累加文本内容
                yield line_str + "\n"
            except Exception as e:
                end_time = time.time()
                if first_token_time is not None:
                    logger.info(f"Request ID: {requestId}, 请求大模型开始到第一个token开始返回时间花费：{first_token_time - start_time:.2f} s\n")
                logger.info(f"Request ID: {requestId}, 请求大模型开始到返回结束时间花费：{end_time - start_time:.2f} s\n")
                logger.info(f"Request ID: {requestId}, 大模型返回内容如下：\n{llm_response}\n")
                yield line_str + "\n"




# 非大模型接口正常返回
def server_response(
    data: str
) -> JSONResponse:
    response = JSONResponse(content={"errorcode": 1,
                                     "result": 1,
                                     "msg" :"Server success",
                                     "data": data})
    return response

# 大模型流式接口返回
def llm_stream_response(
    data
) -> StreamingResponse:
    response = StreamingResponse(data)
    return response


# 入参错误返回
def params_error_response(
    data: str
) -> JSONResponse:
    response = JSONResponse(content={"errorcode": 0,
                                     "result": 1000,
                                     "msg": "There is an error in the request parameter",
                                     "data": data})
    return response

# 服务内部逻辑错误返回(只有代码的逻辑出错了才返回500，其余只要正确处理都返回200)
def server_error_response(
    data: str
) -> JSONResponse:
    response = JSONResponse(content={"errorcode": 0,
                                     "result": 1099,
                                     "msg": "Program running exception",
                                     "data": data})
    return response

# 子服务接口调用错误返回
def child_server_error_response(
    data: str
) -> JSONResponse:
    response = JSONResponse(content={"errorcode": 0,
                                     "result": 108,
                                     "msg": "The atomic service is running abnormally",
                                     "data": data})
    return response
