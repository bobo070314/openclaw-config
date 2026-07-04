import json

def generate_integration_report(v5_chromosomes, v4_capabilities, mapping):
    report = {
        'v5_chromosomes': v5_chromosomes,
        'v4_capabilities': v4_capabilities,
        'mapping': mapping,
        'upgrade_suggestions': []
    }
    # 生成升级建议
    for chrom in v5_chromosomes:
        if chrom['name'] not in mapping:
            report['upgrade_suggestions'].append(f"{chrom['name']} 可以直接注入 V4 引擎")
        else:
            report['upgrade_suggestions'].append(f"{chrom['name']} 已经在 V4 引擎中存在，建议进行PK优化")
    return report

# 生成家族集团升级地图

def generate_upgrade_map(report):
    map_data = {
        'chromosomes': report['v5_chromosomes'],
        'v4_capabilities': report['v4_capabilities'],
        'mapping': report['mapping'],
        'suggestions': report['upgrade_suggestions']
    }
    return json.dumps(map_data, ensure_ascii=False, indent=2)