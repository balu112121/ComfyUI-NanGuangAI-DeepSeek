# 南光AI小助理DK - 插件入口
from .Comfyui_NanGuangAI_DeepSeek import Comfyui_NanGuangAI_DeepSeek

# 将节点类暴露给ComfyUI
NODE_CLASS_MAPPINGS = {
    "Comfyui_NanGuangAI_DeepSeek": Comfyui_NanGuangAI_DeepSeek,
}

# 可选：节点显示名称映射（ComfyUI自动读取NODE_DISPLAY_NAME，此为非必须）
NODE_DISPLAY_NAME_MAPPINGS = {
    "Comfyui_NanGuangAI_DeepSeek": "南光AI小助理DK",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']