#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@PROJECT_NAME: Multi-Agent Empowered Personalized Learning Pathways
@File    : main.py
@Author  : jiesheng
@Date    : 2025/5/17 17:30
@Desc    : 

@Modify History:
         
@Copyright：Copyright(c) 2025-2028. All Rights Reserved
=================================================="""
import uvicorn
from utils import return_config

if __name__ == "__main__":
    log_params, server_params, *_ = return_config()
    # 启动服务
    uvicorn.run("server:app", host=server_params["IP"], port=server_params["PORT"], workers=server_params["WORKERS"])