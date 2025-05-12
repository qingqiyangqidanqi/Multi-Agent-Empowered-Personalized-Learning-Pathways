from typing import (
    Dict,
    Any,
    Union,
    List,
    Optional
)
from openai import OpenAI
import requests


# openai形式调用大模型
def openai_chat(
    headers: [Union[str, Dict]],
    sys_prompt: str,
    user_prompt: str,
    model_name: str,
    base_url: str,
    temperature: float = 0.9,
    timeout:int = 60
):
    headers = headers

    data = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature
    }
    if headers == "":
        response = requests.post(base_url, json=data, timeout=timeout)
    else:
        response = requests.post(base_url, json=data, headers=headers, timeout=timeout)
    return response


# openai形式调用大模型流式返回
def openai_chat_stream(
    headers: [Union[str, Dict]],
    sys_prompt: str,
    user_prompt: str,
    model_name: str,
    base_url: str,
    temperature: float = 0.9,
    timeout:int = 60
):
    headers = headers

    data = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature,
        "stream": True
    }
    if headers == "":
        response = requests.post(base_url, json=data, stream=True, timeout=timeout)
    else:
        response = requests.post(base_url, json=data, headers=headers, stream=True, timeout=timeout)
    return response


def openai_chat_notstream(
    headers: [Union[str, Dict]],
    sys_prompt: str,
    user_prompt: str,
    model_name: str,
    base_url: str,
    temperature: float = 0.9,
    timeout:int = 60
):
    headers = headers

    data = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature,
        "stream": False
    }
    if headers == "":
        # response = requests.post(base_url, json=data, stream=True, timeout=timeout)
        response = requests.post(base_url, json=data, stream=False, timeout=timeout)
    else:
        # response = requests.post(base_url, json=data, headers=headers, stream=True, timeout=timeout)
        response = requests.post(base_url, json=data, headers=headers, stream=False, timeout=timeout)
    return response




