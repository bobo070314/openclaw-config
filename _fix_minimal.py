import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'D:\bobo\openclaw-foreign\openclaw-minimal.json'

providers = {
  "deepseek": {
    "baseUrl": "https://api.deepseek.com/v1",
    "apiKey": "${DEEPSEEK_API_KEY}",
    "api": "openai-completions",
    "capabilities": {"tools": False},
    "models": [{"id": "deepseek-v4-flash", "name": "DeepSeek V4-Flash"}]
  },
  "zhipu": {
    "baseUrl": "https://open.bigmodel.cn/api/paas/v4/",
    "apiKey": "${ZHIPU_API_KEY}",
    "api": "openai-completions",
    "models": [
      {"id": "glm-4-flash", "name": "GLM-4-Flash"},
      {"id": "glm-4-flash-250315", "name": "GLM-4.7-Flash"},
      {"id": "glm-4-flashx", "name": "GLM-4-FlashX"},
      {"id": "glm-z1-air", "name": "GLM-Z1-Air"}
    ]
  },
  "siliconflow": {
    "baseUrl": "https://api.siliconflow.cn/v1",
    "apiKey": "${SILICONFLOW_API_KEY}",
    "api": "openai-completions",
    "models": [
      {"id": "Qwen/Qwen2.5-7B-Instruct", "name": "Qwen2.5-7B"},
      {"id": "Qwen/Qwen2.5-14B-Instruct", "name": "Qwen2.5-14B"},
      {"id": "THUDM/GLM-4-9B-0414", "name": "GLM-4-9B"},
      {"id": "deepseek-ai/DeepSeek-V3", "name": "DeepSeek-V3"}
    ]
  },
  "huoshan": {
    "baseUrl": "https://ark.cn-beijing.volces.com/api/v3",
    "apiKey": "${HUOSHAN_API_KEY}",
    "api": "openai-completions",
    "models": [
      {"id": "doubao-lite-32k", "name": "Doubao-Lite"},
      {"id": "doubao-seed-2-0-code-preview-260215", "name": "Doubao-Code"}
    ]
  },
  "aliyun": {
    "baseUrl": "https://dashscope.aliyun.com/compatible-mode/v1",
    "apiKey": "${ALIYUN_API_KEY}",
    "api": "openai-completions",
    "models": [{"id": "qwen-plus", "name": "Qwen-Plus"}]
  },
  "tencent": {
    "baseUrl": "https://api.hunyuan.cloud.tencent.com/v1",
    "apiKey": "${TENCENT_API_KEY}",
    "api": "openai-completions",
    "models": [{"id": "hunyuan-lite", "name": "Hunyuan-lite"}]
  },
  "baidu": {
    "baseUrl": "https://qianfan.baidubce.com/v2",
    "apiKey": "${BAIDU_API_KEY}",
    "api": "openai-completions",
    "models": [
      {"id": "ernie-4.5-turbo-128k", "name": "ERNIE-4.5-Turbo"},
      {"id": "deepseek-v4-flash", "name": "DeepSeek-V4-Flash"},
      {"id": "deepseek-v3.2", "name": "DeepSeek-V3.2"}
    ]
  }
}

config = {
    "tools": {"exec": {"mode": "full"}},
    "agents": {
        "defaults": {
            "model": "deepseek/deepseek-v4-flash",
            "workspace": r"D:\bobo\openclaw-foreign\workspace",
            "timeoutSeconds": 72000,
            "maxConcurrent": 2,
            "memorySearch": {"provider": "none"}
        },
        "list": [{"id": "main", "default": True, "name": "OpenClaw Foreign", "identity": {"name": "OpenClaw Foreign"}, "skills": []}]
    },
    "models": {"mode": "merge", "providers": providers},
    "plugins": {"load": {"paths": []}, "entries": {}},
    "gateway": {
        "mode": "local", "port": 18900, "bind": "loopback",
        "auth": {"mode": "token", "token": "foreign18900"},
        "controlUi": {"dangerouslyDisableDeviceAuth": True},
        "http": {"endpoints": {"chatCompletions": {"enabled": True}}},
        "remote": {"token": "foreign18900"}
    }
}

with open(path, 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)
    f.write(chr(10))

with open(path, 'r', encoding='utf-8') as f:
    v = json.load(f)
    p = v['models']['providers']
    print('OK - written model providers: ' + ', '.join(f'{k}({len(p[k]["models"])})' for k in p))
    print('gateway: mode=' + v['gateway']['mode'] + ' port=' + str(v['gateway']['port']))
