import json
fpath = r'D:\bobo\openclaw-foreign\openclaw-minimal.json'
cfg = {
    'tools': {'exec': {'mode': 'full'}},
    'agents': {
        'defaults': {
            'model': 'none',
            'workspace': r'D:\bobo\openclaw-foreign\workspace',
            'timeoutSeconds': 72000,
            'maxConcurrent': 2,
            'memorySearch': {'provider': 'none'}
        },
        'list': [{'id': 'main', 'default': True, 'name': 'OpenClaw Foreign', 'identity': {'name': 'OpenClaw Foreign'}, 'skills': []}]
    },
    'models': {'mode': 'none', 'providers': {}},
    'plugins': {'load': {'paths': []}, 'entries': {}},
    'gateway': {
        'mode': 'local', 'port': 18900, 'bind': 'loopback',
        'auth': {'mode': 'token', 'token': 'foreign18900'},
        'controlUi': {'dangerouslyDisableDeviceAuth': True},
        'http': {'endpoints': {'chatCompletions': {'enabled': True}}},
        'remote': {'token': 'foreign18900'}
    }
}
with open(fpath,'w',encoding='utf-8') as f:
    json.dump(cfg,f,ensure_ascii=False,indent=2)
print('OK')
