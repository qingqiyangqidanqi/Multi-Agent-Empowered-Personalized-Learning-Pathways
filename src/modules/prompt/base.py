#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@PROJECT_NAME: Multi-Agent-Empowered-Personalized-Learning-Pathways
@File    : base.py
@Author  : jiesheng
@Date    : 2025/5/18 11:39
@Desc    : 

@Modify History:
         
@Copyright：Copyright(c) 2025-2028. All Rights Reserved
=================================================="""
from abc import ABC, abstractmethod

# 抽象基类
class PromptTemplateBase(ABC):
    """
    提示词模版基类
    """
    @abstractmethod
    def __init__(self, *args, **kwargs):
        """
        初始化方法，子类必须实现
        """
        pass

    @abstractmethod
    def create_prompt(self, *args, **kwargs):
        """
        创建提示词的方法，子类必须实现
        """
        pass
