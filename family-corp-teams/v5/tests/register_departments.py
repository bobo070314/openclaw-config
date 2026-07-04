"""IGP 部门注册: 将游离文件全部编入染色体体系"""
import os, shutil

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
CHRO_BASE = os.path.join(V5, 'chromosomes')

# 定义新部门
NEW_DEPARTMENTS = {
    'chromosome13_silicon_memory': {
        'name': '硅胶体记忆部',
        'files': {
            'v6/silicon_memory/v5_silicon_memory.py': 'infra/v5_silicon_memory.py',
        }
    },
    'chromosome16_infrastructure': {
        'name': 'IGP基础设施部',
        'files': {
            'v6/api/igp_api.py': 'infra/igp_api.py',
            'v6/api/igp_api_client.py': 'infra/igp_api_client.py',
            'v6/api/api_runner.py': 'infra/api_runner.py',
            'v6/api/igp_heartbeat.py': 'infra/igp_heartbeat.py',
            'v6/api/start_api.bg.py': 'infra/start_api.bg.py',
            'v6/cli/igp.py': 'infra/igp_cli.py',
            'v6/cli/__main__.py': 'infra/__main__.py',
            'v6/cli/commands/doctor.py': 'infra/commands/doctor.py',
            'v6/cli/commands/analyze.py': 'infra/commands/analyze.py',
            'v6/cli/commands/complexity.py': 'infra/commands/complexity.py',
            'v6/cli/commands/lifecycle.py': 'infra/commands/lifecycle.py',
            'v6/cli/commands/metrics.py': 'infra/commands/metrics.py',
            'v6/cli/commands/prd.py': 'infra/commands/prd.py',
            'v6/cli/commands/review.py': 'infra/commands/review.py',
            'v6/cli/commands/sdk.py': 'infra/commands/sdk.py',
            'v6/cli/commands/version.py': 'infra/commands/version.py',
        }
    },
    'chromosome17_devops': {
        'name': 'DevOps部',
        'files': {
            'v6/ci/pipeline.py': 'infra/pipeline.py',
            'v6/ci/deploy.py': 'infra/deploy.py',
            'v6/ci/ci_pre_push.py': 'infra/ci_pre_push.py',
            'v6/ci/setup_hooks.py': 'infra/setup_hooks.py',
            'v5_absorb_chromosome9.py': 'infra/v5_absorb_chromosome9.py',
            'v5_absorption_plan2.py': 'infra/v5_absorption_plan2.py',
        }
    },
    'chromosome18_core_engine': {
        'name': '核心引擎部',
        'files': {
            'v5_dashboard.py': 'infra/v5_dashboard.py',
            'v5_engine_loop.py': 'infra/v5_engine_loop.py',
            'v5_fission_engine.py': 'infra/v5_fission_engine.py',
            'v5_ghost_patrol.py': 'infra/v5_ghost_patrol.py',
            'v5_pk_battle.py': 'infra/v5_pk_battle.py',
            'v5_pk_arena.py': 'infra/v5_pk_arena.py',
            'v5_closed_loop_pipeline.py': 'infra/v5_closed_loop_pipeline.py',
            'v5_cruise.py': 'infra/v5_cruise.py',
            'v5_defect_audit.py': 'infra/v5_defect_audit.py',
            'v5_final_all.py': 'infra/v5_final_all.py',
            'v5_final_verify.py': 'infra/v5_final_verify.py',
            'v5_verify.py': 'infra/v5_verify.py',
            'v5_health_check.py': 'infra/v5_health_check.py',
            'v5_github_scanner.py': 'infra/v5_github_scanner.py',
            'v5_oneclick.py': 'infra/v5_oneclick.py',
            'v5_skills_registry.py': 'infra/v5_skills_registry.py',
        }
    },
    'chromosome19_product_delivery': {
        'name': '产品交付部',
        'files': {
            'v6/prd/prd_queue.py': 'infra/prd_queue.py',
            'v6/review/v6_review_agents.py': 'infra/v6_review_agents.py',
            'v6/lifecycle/v6_lifecycle.py': 'infra/v6_lifecycle.py',
            'v6/metrics/metrics_collector.py': 'infra/metrics_collector.py',
            'v6/metrics/metrics_reporter.py': 'infra/metrics_reporter.py',
            'v6/hr/generate_report.py': 'infra/generate_report.py',
            'v6/hr/hr_dashboard.py': 'infra/hr_dashboard.py',
            'v6/swat/swat_team.py': 'infra/swat_team.py',
            'v6/scan_registry.py': 'infra/scan_registry.py',
            'v6/closed_loop_demo.py': 'infra/closed_loop_demo.py',
            'v6/full_stack_sprint.py': 'infra/full_stack_sprint.py',
            'v6/v6_final_check.py': 'infra/v6_final_check.py',
            'v6/v6_final_verify.py': 'infra/v6_final_verify.py',
        }
    },
}

# 实际执行：复制文件到染色体目录
def execute():
    actions = []
    for chrom, dept in NEW_DEPARTMENTS.items():
        target_dir = os.path.join(CHRO_BASE, chrom, 'infra')
        os.makedirs(target_dir, exist_ok=True)
        
        for src_rel, dest_rel in dept['files'].items():
            src_path = os.path.join(V5, src_rel.replace('/', '\\'))
            if not os.path.exists(src_path):
                actions.append(f"[SKIP] {src_rel} → 源文件不存在")
                continue
            
            # 确定目标路径
            dest_path = os.path.join(target_dir, os.path.basename(dest_rel))
            if src_path == dest_path:
                actions.append(f"[SKIP] {src_rel} → 已在目录中")
                continue
            
            # 复制
            shutil.copy2(src_path, dest_path)
            actions.append(f"[COPY] {src_rel} → {chrom}/{os.path.basename(dest_rel)}")
        
        # 创建 run.py
        run_path = os.path.join(CHRO_BASE, chrom, 'infra', 'run.py')
        if not os.path.exists(run_path):
            dept_name = dept['name']
            module_list = [os.path.splitext(os.path.basename(p))[0] for p in dept['files'].values()]
            run_content = f'''"""
{chrom}: {dept_name} — 验证运行
"""
import sys, os
BASE = os.path.dirname(os.path.abspath(__file__))
if BASE not in sys.path: sys.path.insert(0, BASE)

def verify():
    results = []
    modules = {mod: True for mod in {os.path.splitext(os.path.basename(p))[0].replace('/', '').replace('\\\\', '') for p in {os.path.basename(p) for p in [
'''
            for p in dept['files'].values():
                run_content += f'        r"{os.path.basename(p)}",\n'
            run_content += '''    ]}}}
    for mod in sorted(modules.keys()):
        try:
            __import__(mod)
            results.append(f"  OK: {mod}")
        except Exception as e:
            results.append(f"  FAIL: {mod}: {e}")
    for r in results: print(r)
    ok = sum(1 for r in results if r.startswith("  OK:"))
    print(f"\\n{chrom}: {ok}/{len(results)}")
    return ok == len(results)

if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
'''
            with open(run_path, 'w', encoding='utf-8') as f:
                f.write(run_content)
            actions.append(f"[CREATE] {chrom}/infra/run.py")
        else:
            actions.append(f"[SKIP] {chrom}/infra/run.py (已存在)")
    
    return actions

actions = execute()
for a in actions:
    print(a)
print(f"\n执行完成: {len(actions)} 操作")
