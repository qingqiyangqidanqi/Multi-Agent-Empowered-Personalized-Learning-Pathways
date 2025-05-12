#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@PROJECT_NAME: ESOP-HSSC
@File    : jiutian_llm_request.py
@Author  : caixiongjiang
@Date    : 2024/12/24 11:17
@Function: 
    移动九天大模型的请求方式
@Modify History:
         
@Copyright：Copyright(c) 2024-2026. All Rights Reserved
=================================================="""

from typing import Union, Dict

import requests
import base64




client_id = 'yingPanClient'
client_secret = '32bGKy5EgY'
url = 'http://maas.zj.chinamobile.com/maas-sso/oauth2/token'


def get_jiu_tian_token(
    get_token_url: str,
    get_token_client_id: str,
    get_token_client_secret: str
) -> str:

    # 对客户端ID和客户端密钥进行Base64编码
    auth_str = f"{get_token_client_id}:{get_token_client_secret}"
    encoded_auth = base64.b64encode(auth_str.encode()).decode()

    # 设置请求头
    headers = {
        'Authorization': f"Basic {encoded_auth}",
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # 设置查询参数
    params = {
        'grant_type': 'client_credentials'
    }

    # 发送POST请求
    response = requests.post(url=get_token_url, headers=headers, params=params)
    access_token = response.json()['access_token']
    # print(access_token)
    return access_token


def jiu_tian_chat(
    headers: [Union[str, Dict]],
    sys_prompt: str,
    user_prompt: str,
    model_name: str,
    access_token: str,
    url: str,
    temperature: float = 0.9,
    timeout:int = 60
):

    headers["Authorization"] = f"Bearer {access_token}"

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
        response = requests.post(url, json=data, stream=False, timeout=timeout)
    else:
        response = requests.post(url, json=data, headers=headers, stream=False, timeout=timeout)
    return response


def jiu_tian_chat_stream(
    headers: [Union[str, Dict]],
    sys_prompt: str,
    user_prompt: str,
    model_name: str,
    access_token: str,
    url: str,
    temperature: float = 0.9,
    timeout:int = 60
):
    headers["Authorization"] = f"Bearer {access_token}"

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
        response = requests.post(url, json=data, stream=True, timeout=timeout)
    else:
        response = requests.post(url, json=data, headers=headers, stream=True, timeout=timeout)
    return response