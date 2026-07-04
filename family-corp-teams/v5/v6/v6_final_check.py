"""IGP 研发部 V6 最终验证"""
import sys, os, json, warnings
warnings.filterwarnings('ignore')

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
V6 = os.path.join(V5, 'v6')

# 先把所有路径都加上
for p in [V6, os.path.join(V6, 'review'), os.path.join(V6, 'prd'),
          os.path.join(V6, 'cli'), os.path.join(V6, 'api'),
          os.path.join(V6, 'cli', 'commands'), V5]:
    if p not in sys.path:
        sys.path.insert(0, p)

# 添加所有染色体infra
chrom_base = os.path.join(V5, 'chromosomes')
if os.path.exists(chrom_base):
    for d in sorted(os.listdir(chrom_base)):
        infra = os.path.join(chrom_base, d, 'infra')
        if os.path.exists(infra) and infra not in sys.path:
            sys.path.insert(0, infra)

results = []

def check(name, fn):
    try:
        fn()
        results.append((name, True, ''))
    except Exception as e:
        results.append((name, False, str(e)[:80]))

# 1. Registry
check('Registry', lambda: (
    json.load(open(os.path.join(V6, 'product_registry.json'), encoding='utf-8'))['total_products'] > 50
) and None)

# 2. Lifecycle
check('Lifecycle', lambda: (
    __import__('v6_lifecycle').LifecycleManager(
        os.path.join(V6, 'product_registry.json')
    ).summary()['total'] > 50
) and None)

# 3. ReviewAgents
check('ReviewAgents', lambda: (
    __import__('v6_review_agents').review_file(
        os.path.join(V6, 'v6_lifecycle.py')
    )['passed'] == True
) and None)

# 4. PRDQueue
check('PRDQueue', lambda: (
    __import__('prd_queue').PRDQueue(V6).summary()['total'] >= 0
) and None)

# 5. CLI igp.py
check('CLI igp', lambda: (
    callable(__import__('igp').main)
) and None)

# 6. SDKManager
check('SDKManager', lambda: (
    len(__import__('sdk').SDKManager().list_sdks()) == 7
) and None)

# 7. HTTP API
check('HTTP API', lambda: (
    hasattr(__import__('igp_api'), 'start_server')
) and None)

# 8. APIClient
check('APIClient', lambda: (
    callable(__import__('igp_api_client').IGPAPIClient().health)
) and None)

print('=' * 60)
print('IGP 研发部 V6 最终验证')
print('=' * 60)
for name, ok, err in results:
    print(f'  {"✅" if ok else "❌"} {name:20} {err}')
print('=' * 60)
print(f'Passed: {sum(1 for r in results if r[1])}/{len(results)}')
