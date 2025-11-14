from operator import not_
import os 
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, List
# 加载.env文件中的环境变量
load_dotenv()

class HelloAgentsLLM:
    """
    为本书”Hello Agents”定制的LLM客户端
    它用于调用任何兼容OpenAI接口的服务，并使用默认流式响应。
    """
    def __init__(self,model:str=None,apikey:str=None,baseurl:str=None,timeout : int=None):
        """
        初始化客户端。优先使用传入参数，如果未提供，则从环境变量加载。
        """
        self.model=model or os.getenv("LLM_MODEL_ID")
        apikey=apikey or os.getenv("LLM_API_KEY")
        baseurl=baseurl or os.getenv("LLM_BASE_URL")
        timeout=timeout or int(os.getenv("LLM_TIMEOUT"),60)
        if not all([self.model,apikey,baseurl]):
            raise ValueError("模型ID、API密钥和服务地址必须被提供或在.env文件中定义。")
        self.client=OpenAI(api_key=apikey,base_url=baseurl,timeout=timeoutxx)
