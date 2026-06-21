import os
import json
import requests

class Comfyui_NanGuangAI_DeepSeek:
    """
    南光AI小助理DK - 通过阿里云百炼调用DeepSeek模型
    """
    CATEGORY = "南光AI/新对话"
    NODE_DISPLAY_NAME = "南光AI小助理DK"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": (
                    ["deepseek-r1", "deepseek-v3"],   # ✅ 修改为百炼实际模型名称
                    {
                        "default": "deepseek-r1",
                        "display_name": "模型选择",
                        "description": "选择要调用的DeepSeek模型版本"
                    }
                ),
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "请在此输入您的问题",
                        "display_name": "问题 / 对话内容",
                        "description": "您想向模型提出的问题或对话内容"
                    }
                ),
                "system_prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "你是一位领域专家，请深入思考并给出详细、准确、有条理的答案。",
                        "display_name": "专家模式系统提示",
                        "description": "用于设定模型行为，可自定义专家指令"
                    }
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "display_name": "API密钥",
                        "description": "阿里云百炼API Key（留空则从环境变量DASHSCOPE_API_KEY读取）"
                    }
                )
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("回复内容",)
    FUNCTION = "generate"
    OUTPUT_NODE = False

    def generate(self, model, prompt, system_prompt, api_key):
        # 1. 获取API Key
        key = api_key.strip() if api_key else os.environ.get("DASHSCOPE_API_KEY") or os.environ.get("ALIYUN_API_KEY")
        if not key:
            error_msg = "❌ 错误：未提供API Key。请填写「API密钥」输入框或设置环境变量 DASHSCOPE_API_KEY。"
            return (error_msg,)

        # 2. 构建请求（阿里云百炼文本生成接口）
        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,   # 现在使用 deepseek-r1 或 deepseek-v3
            "input": {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            },
            "parameters": {
                "result_format": "message"   # 返回标准message格式
            }
        }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()

            if "output" in result and "choices" in result["output"] and len(result["output"]["choices"]) > 0:
                content = result["output"]["choices"][0]["message"]["content"]
                return (content,)
            else:
                error_msg = f"⚠️ API返回格式异常：{json.dumps(result, ensure_ascii=False)}"
                return (error_msg,)

        except requests.exceptions.Timeout:
            return ("⏰ 错误：请求超时，请稍后重试。",)
        except requests.exceptions.RequestException as e:
            return (f"🌐 网络请求错误：{str(e)}",)
        except Exception as e:
            return (f"💥 未知错误：{str(e)}",)