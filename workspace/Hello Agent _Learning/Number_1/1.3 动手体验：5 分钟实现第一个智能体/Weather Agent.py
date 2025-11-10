#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能旅行助手智能体
基于文档1.3节实现的智能旅行助手
"""

import requests  # 用于发送 HTTP 请求
import os  # 用于文件路径操作
import re  # 用于正则表达式匹配
import sys # 便于之后进行扩展,未使用
from openai import OpenAI  # 用于与 OpenAI API 交互
from tavily import TavilyClient  # 用于与 Tavily API 交互

# ==================== 系统提示词 ====================
def load_system_prompt():
    """
    从外部文件加载系统提示词（多环境兼容版本）
    """
    # 获取当前脚本所在的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 尝试多个可能的文件路径
    possible_paths = [
        os.path.join(script_dir, "system_prompt.md"),  # 同目录下
        "system_prompt.md",  # 当前工作目录
        os.path.join(os.getcwd(), "system_prompt.md"),  # 绝对路径
    ]
    
    # ==================== 通过打印信息区分 ====================
    # 通过控制台输出的路径信息可以清晰区分文件是从哪个代码路径加载成功的：
    # 1. 脚本目录路径：由第20-21行的script_dir计算 + 第24行的os.path.join(script_dir, "system_prompt.md")
    #    - 输出示例：✅ 成功加载系统提示词文件: d:\...\system_prompt.md
    # 2. 当前工作目录路径：直接由第25行的"system_prompt.md"提供
    #    - 输出示例：✅ 成功加载系统提示词文件: system_prompt.md
    # 3. 绝对路径：由第26行的os.path.join(os.getcwd(), "system_prompt.md")提供
    #    - 输出示例：✅ 成功加载系统提示词文件: d:\当前工作目录\system_prompt.md
    # 
    # 搜索优先级：脚本目录 > 当前工作目录 > 绝对路径
    # 实际应用场景：
    # - 从脚本目录运行：通常会从"脚本目录"路径加载成功
    # - 从其他目录运行：可能会从"当前工作目录"或"绝对路径"加载成功
    # - 调试时：通过打印信息可以清楚知道文件是从哪个路径找到的
    
    for prompt_file in possible_paths:
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                prompt_content = f.read().strip()
            print(f"✅ 成功加载系统提示词文件: {prompt_file}")
            return prompt_content
        except FileNotFoundError:
            continue
        except Exception as e:
            print(f"❌ 错误: 读取提示词文件 {prompt_file} 时发生错误 - {e}")
            continue
    
    # 如果所有路径都失败，返回默认提示词
    print("⚠️  警告: 未找到提示词文件，使用内置默认提示词")
    return """你是一个智能旅行助手。你的任务是分析用户的请求，并使用可用工具一步步地解决问题。

# 可用工具:
- `get_weather(city: str)`: 查询指定城市的实时天气。
- `get_attraction(city: str, weather: str)`: 根据城市和天气搜索推荐的旅游景点。

# 行动格式:
你的回答必须严格遵循以下格式。首先是你的思考过程，然后是你要执行的具体行动，每次回复只输出一对Thought-Action：
Thought: [这里是你的思考过程和下一步计划]
Action: [这里是你要调用的工具，格式为 function_name(arg_name="arg_value")]

# 任务完成:
当你收集到足够的信息，能够回答用户的最终问题时，你必须在`Action:`字段后使用 `finish(answer="...")` 来输出最终答案。

请开始吧！"""

# 加载系统提示词
AGENT_SYSTEM_PROMPT = load_system_prompt()

# ==================== 工具函数 ====================

def get_weather(city: str) -> str:
    """
    通过调用 wttr.in API 查询真实的天气信息。
    """
    # API端点，我们请求JSON格式的数据
    url = f"https://wttr.in/{city}?format=j1"
    
    try:
        # 发起网络请求
        response = requests.get(url)
        # 检查响应状态码是否为200 (成功)
        response.raise_for_status() 
        # 解析返回的JSON数据
        data = response.json()
        
        # 提取当前天气状况
        current_condition = data['current_condition'][0]
        weather_desc = current_condition['weatherDesc'][0]['value']
        temp_c = current_condition['temp_C']
        
        # 格式化成自然语言返回
        return f"{city}当前天气:{weather_desc}，气温{temp_c}摄氏度"
        
    except requests.exceptions.RequestException as e:
        # 处理网络错误
        return f"错误:查询天气时遇到网络问题 - {e}"
    except (KeyError, IndexError) as e:
        # 处理数据解析错误
        return f"错误:解析天气数据失败，可能是城市名称无效 - {e}"


def get_attraction(city: str, weather: str) -> str:
    """
    根据城市和天气，使用Tavily Search API搜索并返回优化后的景点推荐。
    """
    # 1. 从环境变量中读取API密钥
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return "错误:未配置TAVILY_API_KEY环境变量。"

    # 2. 初始化Tavily客户端
    tavily = TavilyClient(api_key=api_key)
    
    # 3. 构造一个精确的查询
    query = f"'{city}' 在'{weather}'天气下最值得去的旅游景点推荐及理由"
    
    try:
        # 4. 调用API，include_answer=True会返回一个综合性的回答
        response = tavily.search(query=query, search_depth="basic", include_answer=True)
        
        # 5. Tavily返回的结果已经非常干净，可以直接使用
        # response['answer'] 是一个基于所有搜索结果的总结性回答
        if response.get("answer"):
            return response["answer"]
        
        # 如果没有综合性回答，则格式化原始结果
        formatted_results = []
        for result in response.get("results", []):
            formatted_results.append(f"- {result['title']}: {result['content']}")
        
        if not formatted_results:
             return "抱歉，没有找到相关的旅游景点推荐。"

        return "根据搜索，为您找到以下信息:\n" + "\n".join(formatted_results)

    except Exception as e:
        return f"错误:执行Tavily搜索时出现问题 - {e}"


# ==================== OpenAI兼容客户端 ====================

class OpenAICompatibleClient:
    """
    一个用于调用任何兼容OpenAI接口的LLM服务的客户端。
    """
    def __init__(self, model: str, api_key: str, base_url: str):
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate(self, prompt: str, system_prompt: str) -> str:
        """调用LLM API来生成回应。"""
        print("正在调用大语言模型...")
        try:
            messages = [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}
            ]
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False
            )
            answer = response.choices[0].message.content
            print("大语言模型响应成功。")
            return answer
        except Exception as e:
            print(f"调用LLM API时发生错误: {e}")
            return "错误:调用语言模型服务时出错。"


# ==================== 主程序 ====================

def main():
    """智能体主循环"""
    
    # 将所有工具函数放入一个字典，方便后续调用
    available_tools = {
        "get_weather": get_weather,
        "get_attraction": get_attraction,
    }
    
    # --- 1. 配置LLM客户端 ---
    # 检查是否已配置API密钥，如果没有则等待用户输入
    API_KEY = "sk-5f77f27d6364440aa85c8c410a7c270a"
    BASE_URL = "https://api.deepseek.com/v1"  # 例如: "https://api.openai.com/v1"
    MODEL_ID = "deepseek-reasoner"  # 例如: "gpt-3.5-turbo"
    TAVILY_API_KEY = "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"
    
    # 如果没有配置API密钥，等待用户输入
    if API_KEY == "YOUR_API_KEY":
        print("⚠️  警告: 未检测到有效的API密钥配置。")
        print("=" * 50)
        print("请配置您的LLM服务信息：")
        
        # 获取用户输入的API密钥
        while True:
            api_key_input = input("请输入您的API密钥: ").strip()
            if api_key_input and api_key_input != "YOUR_API_KEY":
                API_KEY = api_key_input
                break
            else:
                print("❌ API密钥不能为空或使用默认值，请重新输入。")
        
        # 获取用户输入的Base URL
        while True:
            base_url_input = input("请输入API服务地址 (例如: https://api.openai.com/v1): ").strip()
            if base_url_input and base_url_input != "YOUR_BASE_URL":
                BASE_URL = base_url_input
                break
            else:
                print("❌ API服务地址不能为空或使用默认值，请重新输入。")
        
        # 获取用户输入的模型ID
        while True:
            model_id_input = input("请输入模型名称 (例如: gpt-3.5-turbo): ").strip()
            if model_id_input and model_id_input != "YOUR_MODEL_ID":
                MODEL_ID = model_id_input
                break
            else:
                print("❌ 模型名称不能为空或使用默认值，请重新输入。")
        
        print("✅ 配置完成！")
        print("=" * 50)
    
    # 配置Tavily API密钥
    if TAVILY_API_KEY == "YOUR_TAVILY_API_KEY":
        print("⚠️  警告: 未检测到有效的Tavily API密钥配置。")
        print("=" * 50)
        print("请配置您的Tavily API密钥：")
        
        # 获取用户输入的Tavily API密钥
        while True:
            tavily_api_key_input = input("请输入您的Tavily API密钥: ").strip()
            if tavily_api_key_input and tavily_api_key_input != "YOUR_TAVILY_API_KEY":
                TAVILY_API_KEY = tavily_api_key_input
                break
            else:
                print("❌ Tavily API密钥不能为空或使用默认值，请重新输入。")
        
        print("✅ Tavily API配置完成！")
        print("=" * 50)
    
    # 设置Tavily API密钥到环境变量
    os.environ['TAVILY_API_KEY'] = TAVILY_API_KEY
    
    # 使用配置的LLM服务
    llm = OpenAICompatibleClient(
        model=MODEL_ID,
        api_key=API_KEY,
        base_url=BASE_URL
    )
    
    # --- 2. 初始化 ---
    user_prompt = "你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。"
    prompt_history = [f"用户请求: {user_prompt}"]

    print(f"用户输入: {user_prompt}")
    print("=" * 50)

    # --- 3. 运行主循环 ---
    for i in range(5):  # 设置最大循环次数
        print(f"--- 循环 {i+1} ---")
        
        # 3.1. 构建Prompt
        full_prompt = "\n".join(prompt_history)
        
        # 3.2. 调用LLM进行思考
        llm_output = llm.generate(full_prompt, system_prompt=AGENT_SYSTEM_PROMPT)
        # 模型可能会输出多余的Thought-Action，需要截断
        match = re.search(r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)', llm_output, re.DOTALL)
        if match:
            truncated = match.group(1).strip()
            if truncated != llm_output.strip():
                llm_output = truncated
                print("已截断多余的 Thought-Action 对")
        print(f"模型输出:\n{llm_output}")
        prompt_history.append(llm_output)
        
        # 3.3. 解析并执行行动
        action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
        if not action_match:
            print("解析错误:模型输出中未找到 Action。")
            break
        action_str = action_match.group(1).strip()

        if action_str.startswith("finish"):
            final_answer_match = re.search(r'finish\(answer="(.*)"\)', action_str)
            if final_answer_match:
                final_answer = final_answer_match.group(1)
                print(f"任务完成，最终答案: {final_answer}")
                break
            else:
                print("解析错误:finish函数格式不正确。")
                break
        
        # 解析工具调用
        tool_match = re.search(r"(\w+)\(", action_str)
        if not tool_match:
            print("解析错误:无法识别工具名称。")
            break
        tool_name = tool_match.group(1)
        
        # 解析参数
        args_match = re.search(r"\((.*)\)", action_str)
        if args_match:
            args_str = args_match.group(1)
            kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))
        else:
            kwargs = {}

        if tool_name in available_tools:
            observation = available_tools[tool_name](**kwargs)
        else:
            observation = f"错误:未定义的工具 '{tool_name}'"

        # 3.4. 记录观察结果
        observation_str = f"Observation: {observation}"
        print(f"{observation_str}")
        print("=" * 50)
        prompt_history.append(observation_str)
    else:
        print("达到最大循环次数，任务未完成。")


if __name__ == "__main__":
    main()