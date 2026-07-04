"""IGP CLI — 研发部工具箱主入口"""
import argparse
import sys
import os
import json

# ======== 统一路径设置 ========
CLI_DIR = os.path.dirname(os.path.abspath(__file__))
V6_DIR = os.path.abspath(os.path.join(CLI_DIR, '..'))
V5_DIR = os.path.abspath(os.path.join(V6_DIR, '..'))
for p in [V5_DIR, V6_DIR, CLI_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

# 所有染色体 infra 目录
CHROMOSOME_BASE = os.path.join(V5_DIR, 'chromosomes')
if os.path.exists(CHROMOSOME_BASE):
    for d in sorted(os.listdir(CHROMOSOME_BASE)):
        infra = os.path.join(CHROMOSOME_BASE, d, 'infra')
        if os.path.exists(infra) and infra not in sys.path:
            sys.path.insert(0, infra)


def cmd_doctor(args):
    """Bug扫描"""
    try:
        from v5_bug_doctor import BugDoctor
        d = BugDoctor()
        d.scan_directory(args.dir)
        report = d.get_report()
        print(f"BugDoctor scan: {len(report)} issues found")
        for item in report[:10]:
            print(f"  - {item}")
        if len(report) > 10:
            print(f"  ... (+{len(report)-10} more)")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0


def cmd_analyze(args):
    """代码分析"""
    try:
        from v5_code_analyzer import CodeAnalyzer
        ca = CodeAnalyzer(args.dir)
        ca.scan_refactoring()
        ca.scan_bad_patterns()
        ca.scan_mutation_opportunity()
        r = ca.all_results()
        total = sum(len(v) for v in r.values())
        print(f"CodeAnalyzer: {total} issues found")
        for cat, items in r.items():
            if items:
                print(f"  {cat}: {len(items)}")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0


def cmd_complexity(args):
    """复杂度分析"""
    try:
        from v5_complexity_analyzer import ComplexityAnalyzer
        ca = ComplexityAnalyzer()
        result = ca.analyze_file(args.file)
        print(f"Complexity: {args.file}")
        for k, v in result.items():
            print(f"  {k}: {v}")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0


def cmd_lifecycle(args):
    """生命周期管理"""
    try:
        from v6.v6_lifecycle import LifecycleManager
        lm = LifecycleManager(os.path.join(V6_DIR, 'product_registry.json'))
        
        if args.list:
            s = lm.summary()
            print(f"Total: {s['total']} products")
            print(f"Stages: {s['stages']}")
            for stage in ["research", "alpha", "beta", "ga", "deprecated", "eol"]:
                prods = lm.list_products(stage=stage)
                if prods:
                    print(f"\n[{stage.upper()}] {len(prods)}:")
                    for p in prods[:8]:
                        print(f"  {p['key']:<25} v{p['version']}")
                    if len(prods) > 8:
                        print(f"  ... (+{len(prods)-8})")
        
        elif args.upgrade:
            result = lm.upgrade_stage(args.upgrade, args.to or "beta")
            if "error" in result:
                print(f"Error: {result['error']}")
            else:
                print(f"Upgraded: {result['key']} {result['from']} -> {result['to']}")
        
        elif args.version:
            v = lm.get_version(args.version)
            cl = lm.get_changelog(args.version)
            print(f"{args.version}: v{v}")
            for entry in cl[-3:]:
                print(f"  - {entry}")
        
        else:
            print("Usage: lifecycle --list | --upgrade KEY --to stage | --version KEY")
            return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0


def cmd_metrics(args):
    """使用度量"""
    try:
        from v6.v6_lifecycle import LifecycleManager
        lm = LifecycleManager(os.path.join(V6_DIR, 'product_registry.json'))
        p = lm.get_product(args.product)
        if not p:
            print(f"Product '{args.product}' not found")
            return 1
        m = p.get("metrics", {})
        print(f"Metrics: {p.get('display_name', args.product)}")
        print(f"  Calls: {m.get('calls', 0)}")
        print(f"  Avg Latency: {m.get('avg_latency_ms', 0):.1f}ms")
        print(f"  Error Rate: {m.get('error_rate', 0)*100:.1f}%")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0


def cmd_prd(args):
    """PRD需求提交"""
    try:
        from v6.prd.prd_queue import PRDQueue
        queue = PRDQueue(V6_DIR)
        
        if args.new and args.title:
            result = queue.submit(
                department=args.dept or "rd",
                product=args.product or "general",
                title=args.title,
                priority=args.priority or "normal",
                description=args.description or "",
            )
            print(f"PRD submitted: {result['id']}")
            print(f"  Department: {result['department_name']}")
            print(f"  Title: {result['title']}")
            print(f"  Keywords: {queue.auto_search_keywords(result)}")
        elif args.list:
            all_prds = queue.list_all()
            for status, items in all_prds.items():
                print(f"\n[{status.upper()}] {len(items)}:")
                for item in items[:5]:
                    print(f"  {item['id']}: {item['title']}")
        else:
            s = queue.summary()
            print(f"PRD Queue: {s}")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0


def cmd_review(args):
    """三Agent评审"""
    try:
        from v6.review.v6_review_agents import review_file
        result = review_file(args.file)
        print(f"Review: {result['file']}")
        print(f"Score: {result['total_score']}/{result['max_score']} {'PASS' if result['passed'] else 'FAIL'}")
        for issue in result.get("all_issues", [])[:10]:
            print(f"  - {issue}")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0


def cmd_sdk(args):
    """SDK管理"""
    try:
        from commands.sdk import SDKManager
        mgr = SDKManager()
        
        if args.list:
            sdks = mgr.list_sdks()
            print(f"Available SDKs ({len(sdks)}):")
            for s in sdks:
                print(f"  {s['key']:15} v{s['version']:10} {s['description']}")
        elif args.install:
            target = args.target or os.path.join(V5_DIR, 'v6', 'sdk', '_installed')
            result = mgr.install(args.install, target)
            if "error" in result:
                print(f"Error: {result['error']}")
            else:
                print(f"Installed: {result['sdk']} v{result['version']}")
                print(f"  To: {result['installed_to']}")
                print(f"  Files: {result['files_copied']}")
        elif args.update:
            target = args.target or os.path.join(V5_DIR, 'v6', 'sdk', '_installed')
            result = mgr.update(args.update, target)
            if "error" in result:
                print(f"Error: {result['error']}")
            else:
                print(f"Updated: {result['sdk']} v{result['version']}")
        else:
            print("Usage: sdk --list | --install KEY | --update KEY [--target PATH]")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0


def cmd_version(args):
    """查版本"""
    try:
        from v6.v6_lifecycle import LifecycleManager
        lm = LifecycleManager(os.path.join(V6_DIR, 'product_registry.json'))
        v = lm.get_version(args.product)
        cl = lm.get_changelog(args.product)
        p = lm.get_product(args.product)
        print(f"Product: {p.get('display_name', args.product) if p else args.product}")
        print(f"Version: v{v}")
        print(f"Stage: {p.get('stage', 'unknown') if p else 'unknown'}")
        print(f"Changelog:")
        for entry in cl[-5:]:
            print(f"  - {entry}")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0


def main():
    parser = argparse.ArgumentParser(description='IGP 研发部工具箱', add_help=False)
    parser.add_argument('command', nargs='?', help='Command')
    parser.add_argument('--dir', help='Target directory')
    parser.add_argument('--file', help='Target file')
    parser.add_argument('--list', action='store_true', help='List mode')
    parser.add_argument('--upgrade', help='Upgrade product key')
    parser.add_argument('--to', help='Target stage')
    parser.add_argument('--version', help='Product version key')
    parser.add_argument('--product', help='Product key')
    parser.add_argument('--new', action='store_true', help='New PRD')
    parser.add_argument('--title', help='PRD title')
    parser.add_argument('--priority', default='normal', help='PRD priority')
    parser.add_argument('--dept', help='PRD department')
    parser.add_argument('--description', help='PRD description')
    parser.add_argument('--install', help='SDK install')
    parser.add_argument('--update', help='SDK update')
    parser.add_argument('--target', help='SDK target dir')
    parser.add_argument('--help', action='store_true', help='Show help')
    
    args = parser.parse_args()
    
    if args.help or not args.command:
        print("=" * 60)
        print("IGP 研发部工具箱 v6.0")
        print("=" * 60)
        print("Usage: igp <command> [options]")
        print()
        cmds = [
            ("doctor --dir .", "BugDoctor扫描目录"),
            ("analyze --dir .", "CodeAnalyzer全维度分析"),
            ("complexity --file x.py", "复杂度分析"),
            ("lifecycle --list", "产品生命周期列表"),
            ("lifecycle --upgrade KEY --to beta", "升级产品阶段"),
            ("lifecycle --version KEY", "产品变更日志"),
            ("metrics --product KEY", "使用度量数据"),
            ("version --product KEY", "版本号+changelog"),
            ("prd --new --title T --dept market", "提交PRD需求"),
            ("prd --list", "PRD队列"),
            ("review --file x.py", "三Agent评审"),
            ("sdk --list", "可用SDK列表"),
            ("sdk --install KEY", "安装SDK"),
            ("sdk --update KEY", "更新SDK"),
            ("help", "本帮助"),
        ]
        for cmd, desc in cmds:
            print(f"  {cmd:<35} {desc}")
        print()
        print("Examples:")
        print("  igp doctor --dir .")
        print('  igp prd --new --title "需要TS支持" --dept market --priority high')
        print("  igp lifecycle --list")
        print("  igp version --product v5_bug_doctor")
        return 0
    
    commands = {
        'doctor': cmd_doctor,
        'analyze': cmd_analyze,
        'complexity': cmd_complexity,
        'lifecycle': cmd_lifecycle,
        'metrics': cmd_metrics,
        'prd': cmd_prd,
        'review': cmd_review,
        'sdk': cmd_sdk,
        'version': cmd_version,
        'help': lambda a: (print(__doc__), 0)[1],
    }
    
    if args.command in commands:
        return commands[args.command](args)
    else:
        print(f"Unknown command: {args.command}")
        print("Run 'igp --help' for available commands")
        return 1


if __name__ == '__main__':
    sys.exit(main())
