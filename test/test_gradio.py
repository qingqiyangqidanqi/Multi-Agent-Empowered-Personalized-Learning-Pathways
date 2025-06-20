#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@PROJECT_NAME: Multi-Agent-Empowered-Personalized-Learning-Pathways
@File    : test_gradio.py
@Author  : jiesheng
@Date    : 2025/5/29 17:08
@Desc    : 

@Modify History:
         
@Copyright：Copyright(c) 2025-2028. All Rights Reserved
=================================================="""
import gradio as gr


def get_multi_agent_response(msg, chatbot):
    """
    模拟多agent响应函数
    :param msg: 用户输入的消息
    :param chatbot: 聊天机器人组件
    :return: 返回当前选择的assistant和聊天记录
    """
    # 模拟agent选择和状态更新
    selected_agent = "ECS查询助手"
    status = "当前状态：正在处理您的请求..."
    text1 = selected_agent
    text2 = status
    # 更新聊天记录
    chatbot.append((msg, f"您选择了{selected_agent}，正在查询相关信息..."))

    # 模拟返回结果
    response = f"{selected_agent}已收到您的请求，正在查询中..."

    # 更新聊天记录
    chatbot.append((selected_agent, response))

    return text1, chatbot, text2, msg


# 前端界面展示
with gr.Blocks() as demo:
    # 在界面中央展示标题
    gr.HTML('<center><h1>欢迎使用阿里云资源查询bot</h1></center>')
    gr.HTML(
        '<center><h3>支持的功能有指定区域的ecs实例查询、余额查询、实例规格详情查询。您可以在tools.py中添加您需要的工具，并在main.py中配置相关的agent</h3></center>')
    with gr.Row():
        with gr.Column(scale=10):
            chatbot = gr.Chatbot(value=[["hello", "很高兴见到您！您想问关于阿里云资源的哪些问题呢？"]], height=600)
        with gr.Column(scale=4):
            text1 = gr.Textbox(label="assistant选择")
            text2 = gr.Textbox(label="当前assistant状态", lines=22)
    with gr.Row():
        msg = gr.Textbox(label="输入", placeholder="您想了解什么呢？")
    # 一些示例问题
    with gr.Row():
        examples = gr.Examples(examples=[
            '我的阿里云余额还有多少钱啊',
            '我在杭州有哪些ecs实例，把它的实例id，价钱以及实例规格详情告诉我',
            '我想了解ecs.u1-c1m4.xlarge和ecs.gn6i-c4g1.xlarge的指标'], inputs=[msg])
    clear = gr.ClearButton([text1, chatbot, text2, msg])
    msg.submit(get_multi_agent_response, [msg, chatbot], [text1, chatbot, text2, msg])

if __name__ == '__main__':
    demo.launch()
