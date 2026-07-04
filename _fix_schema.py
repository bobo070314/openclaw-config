import json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

# 1. 读当前配置
fpath = r'D:\bobo\openclaw-foreign\openclaw-minimal.json'
try:
    with open(fpath, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    print('Read OK, keys:', list(cfg.keys()))
except Exception as e:
    print('Read ERROR:', e)
    sys.exit(1)

# 2. 检查 gateway 是否存在
if 'gateway' not in cfg:
    print('gateway key MISSING - adding it')
    cfg['gateway'] = {
        'mode': 'local',
        'port': 18900,
        'bind': 'loopback',
        'auth': {'mode': 'token', 'token': 'foreign18900'},
        'controlUi': {'dangerouslyDisableDeviceAuth': True},
        'http': {'endpoints': {'chatCompletions': {'enabled': True}}},
        'remote': {'token': 'foreign18900'}
    }
else:
    print('gateway key present:', json.dumps(cfg['gateway'], ensure_ascii=False))
    # 确保 mode 存在
    if 'mode' not in cfg['gateway']:
        cfg['gateway']['mode'] = 'local'
        print('  Added missing mode=local')

# 3. 检查 models.providers 并修复
if 'models' in cfg and 'providers' in cfg['models']:
    provs = cfg['models']['providers']
    print(f'Found {len(provs)} providers')
    for pname, pdata in provs.items():
        # 移除 openclaw 不认识的字段
        removed = pdata.pop('capabilities', None)
        if removed:
            print(f'  {pname}: removed capabilities field')
        # 补充 timeoutSeconds
        if 'timeoutSeconds' not in pdata:
            pdata['timeoutSeconds'] = 120
            print(f'  {pname}: added timeoutSeconds=120')
        # 确保 models 字段完整
        models = pdata.get('models', [])
        for m in models:
            # 确保每个模型有必要的字段
            for field in ['api', 'contextWindow', 'maxTokens']:
                if field not in m:
                    if field == 'api':
                        m[field] = 'openai-completions'
                    elif field == 'contextWindow':
                        m[field] = 128000
                    elif field == 'maxTokens':
                        m[field] = 8192
                    print(f'    {pname}/{m.get("id","?")}: added {field}')
            if 'cost' not in m:
                m['cost'] = {'input': 0, 'output': 0}
                print(f'    {pname}/{m.get("id","?")}: added cost')
            if 'input' not in m:
                m['input'] = ['text']
                print(f'    {pname}/{m.get("id","?")}: added input')
else:
    print('ERROR: models.providers not found')
    sys.exit(1)

# 4. 写回
backup = fpath + '.bak'
if not os.path.exists(backup):
    os.rename(fpath, backup)
    print(f'Backup saved to {backup}')

with open(fpath, 'w', encoding='utf-8') as f:
    json.dump(cfg, f, ensure_ascii=False, indent=2)

# 5. 验证
with open(fpath, 'r', encoding='utf-8') as f:
    v = json.load(f)
print('\nVERIFIED:')
print(f'  gateway.mode: {v["gateway"]["mode"]}')
p = v['models']['providers']
for k, v2 in p.items():
    ms = v2['models']
    sample = ms[0] if ms else {}
    print(f'  {k}: timeout={v2.get("timeoutSeconds")}, models={len(ms)}, sample keys={list(sample.keys())}')
print('\nDONE')
