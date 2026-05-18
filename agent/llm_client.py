import requests
import json
from config import Config

class LLMClient:
    def __init__(self):
        self.base_url = Config.MODEL_URL.rstrip('/')
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer dummy-token"
        }
    
    def _try_lmstudio_openai_format(self, prompt):
        payload = {
            "model": Config.MODEL_NAME,
            "messages": [
                {"role": "system", "content": Config.SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": Config.MAX_TOKENS,
            "temperature": Config.TEMPERATURE,
            "top_p": Config.TOP_P,
            "frequency_penalty": Config.FREQUENCY_PENALTY,
            "presence_penalty": Config.PRESENCE_PENALTY,
            "stream": False
        }
        
        response = requests.post(
            f"{self.base_url}/v1/chat/completions",
            headers=self.headers,
            data=json.dumps(payload)
        )
        
        if response.status_code != 200:
            raise Exception(f"LM Studio OpenAI 格式请求失败，状态码：{response.status_code}，响应：{response.text[:200]}")
        
        try:
            result = response.json()
        except json.JSONDecodeError:
            raise Exception(f"LM Studio OpenAI 格式响应不是 JSON 格式：{response.text[:200]}")
        
        if "choices" in result and len(result["choices"]) > 0:
            if "message" in result["choices"][0] and "content" in result["choices"][0]["message"]:
                return result["choices"][0]["message"]["content"].strip()
            elif "text" in result["choices"][0]:
                return result["choices"][0]["text"].strip()
        
        raise Exception(f"LM Studio OpenAI 格式响应解析失败，响应：{json.dumps(result, ensure_ascii=False)[:300]}")
    
    def _try_textgen_format(self, prompt):
        full_prompt = f"{Config.SYSTEM_PROMPT}\n\n用户：{prompt}\n\n助手："
        payload = {
            "prompt": full_prompt,
            "max_new_tokens": Config.MAX_TOKENS,
            "temperature": Config.TEMPERATURE,
            "top_p": Config.TOP_P,
            "frequency_penalty": Config.FREQUENCY_PENALTY,
            "presence_penalty": Config.PRESENCE_PENALTY,
            "stop": ["\n\n用户："],
            "stream": False
        }
        
        response = requests.post(
            f"{self.base_url}/api/v1/generate",
            headers=self.headers,
            data=json.dumps(payload)
        )
        response.raise_for_status()
        result = response.json()
        
        if "results" in result and len(result["results"]) > 0:
            return result["results"][0]["text"].strip()
        raise Exception(f"text-generation-webui 格式响应解析失败")
    
    def _try_simple_format(self, prompt):
        full_prompt = f"{Config.SYSTEM_PROMPT}\n\n{prompt}"
        payload = {
            "prompt": full_prompt,
            "max_tokens": Config.MAX_TOKENS,
            "temperature": Config.TEMPERATURE
        }
        
        response = requests.post(
            f"{self.base_url}/generate",
            headers=self.headers,
            data=json.dumps(payload)
        )
        response.raise_for_status()
        result = response.json()
        
        if "content" in result:
            return result["content"].strip()
        elif "response" in result:
            return result["response"].strip()
        elif "text" in result:
            return result["text"].strip()
        raise Exception(f"简单格式响应解析失败")
    
    def generate(self, prompt):
        endpoints = [
            ("LM Studio OpenAI", self._try_lmstudio_openai_format),
            ("text-generation-webui", self._try_textgen_format),
            ("simple", self._try_simple_format)
        ]
        
        for name, method in endpoints:
            try:
                return method(prompt)
            except Exception as e:
                continue
        
        raise Exception(f"所有端点格式均尝试失败，请检查模型服务配置。当前地址：{self.base_url}")
