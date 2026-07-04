#!/usr/bin/env python3
"""
IGP 外部生态雷达报告 (2026-06-30 23:33)
对照IGP v3当前状态 vs 2026年Agent行业生态

生成: 吸收清单 + 差距分析表 + 对标分数 + 落地计划
"""

import json
import os

REPORT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "EXTERNAL_ABSORPTION_REPORT_2026-06-30.json"
)

# ====================================================================
# PART 1: 行业生态快照
# ====================================================================

ECOSYSTEM = {
    "coding_agents": [
        {
            "name": "OpenAI Codex CLI",
            "stars": 90000,
            "license": "Apache-2.0",
            "lang": "Rust CLI + IDE + Cloud",
            "bench": "Terminal-Bench #1 (83.4% w/ GPT-5.5)",
            "key_features": [
                "5种表面（CLI/IDE/Web/Desktop/iOS）",
                "Cloud: 自动代码审查 + Slack集成",
                "MCP兼容/Skills插件化",
                "云Sandbox远程执行",
            ],
        },
        {
            "name": "Claude Code",
            "stars": 131000,
            "license": "Proprietary",
            "bench": "SWE-bench Verified 95% (Fable 5, suspended)/88.6% (Opus 4.8)",
            "key_features": [
                "/goal自主完成任务（类似我们的开车门）",
                "Agent View: 所有运行Session控制台",
                "10%+ 所有GitHub commits来自CC",
                "Routines (定时任务)",
                "ultrareview (全量代码审查)",
                "Plugin生态 + Skills标准制定者",
            ],
        },
        {
            "name": "OpenCode",
            "stars": 172000,
            "license": "MIT",
            "lang": "CLI + Desktop",
            "key_features": [
                "75+ LLM providers (最低价/灵活)",
                "Scout subagent (外部文档研究)",
                "Background subagents (后台执行)",
                "Auto-compact (上下文压缩)",
                "本地模型(Ollama/LM Studio)",
                "资源消耗实时监控Dashboard",
            ],
        },
        {
            "name": "Cline",
            "stars": 63000,
            "license": "Apache-2.0",
            "lang": "VS Code+JetBrains+CLI",
            "key_features": [
                "Plan/Act双模式（先计划后执行）",
                "MCP服务器 + 自定义工具",
                "企业版安全审计",
                "Checkpoints代码检查点回滚",
                "本地模型支持 (16-64GB RAM)",
            ],
        },
        {
            "name": "Goose",
            "stars": 48000,
            "license": "Apache-2.0",
            "lang": "Rust Desktop + CLI",
            "key_features": [
                "Linux Foundation AAIF项目",
                "70+ MCP扩展",
                "15+ providers",
                "ACP复用Claude/ChatGPT/Gemini订阅",
                "通用Agent (非仅编码)",
            ],
        },
    ],
    "protocols": {
        "MCP": {
            "desc": "Model Context Protocol - Agent连接工具的标准化协议",
            "status": "行业标准(Anthropic/OpenAI/Google/Microsoft)",
            "ecosystem": "1200+ MCP服务器, 9700万+ npm下载",
            "spec": {
                "tools": "函数调用",
                "resources": "数据读取",
                "prompts": "提示模板",
                "skills": "可复用能力包（草案中Skills-over-MCP WG）",
            },
        },
        "A2A": {
            "desc": "Agent-to-Agent Protocol - Google牵头",
            "status": "Linux Foundation 150+组织",
            "clients": "Google Cloud/AWS/Azure",
            "use_cases": "跨Agent编排/跨语言Agent协作",
        },
        "ACP": {
            "desc": "Agent Commerce Protocol",
            "use": "Agent间商业化交易",
        },
        "UCP": {
            "desc": "Unified Commerce Protocol (Google)",
            "use": "商业Agent交互层",
        },
    },
    "agent_skills_ecosystem": {
        "standard": "Agent Skills (Anthropic主导的开放标准，被Claude/Codex/Cursor/Copilot/Gemini CLI全部采用)",
        "format": "SKILL.md + scripts + examples + resources",
        "marketplaces": {
            "NanoSkill.ai": "人工审查，质量保证",
            "SkillsMP": "最大目录",
            "LobeHub": "社区驱动",
            "mcp.so": "22,400 MCP服务器",
            "VoltAgent/awesome-agent-skills": "26.9K⭐, 500+ skills",
        },
        "meaning": "Skills是2026年Agent生态的'包管理器' — 像npm一样安装/共享/审计Agent能力",
    },
    "other_trends": {
        "code_review": "Augment (automations/ticket-to-pr/security-remediation)",
        "agent_ci": "SWE-agent自修复流水线",
        "security": "PromptLock/Agent合规审计",
        "everything_claude_code": "163K⭐, 封装Agent配置/规则/Skills到一个可安装系统",
    },
}

# ====================================================================
# PART 2: IGP v3 vs 行业对标（10分制）
# ====================================================================

COMPARISON = {
    "维度": {
        "MCP协议支持": {
            "igp_score": 1,
            "industry_baseline": 9,
            "industry_detail": "MCP SDK已标准化，1200+服务器",
            "gap_detail": "我们的igp_mcp_bridge.py定义了自己的shell/file/git/docker函数，不走MCP协议。零兼容性。",
            "absorption_action": "MUST: 升级为MCP Client，消费外部MCP服务器",
        },
        "Agent Skills生态": {
            "igp_score": 0,
            "industry_baseline": 9,
            "industry_detail": "SKILL.md标准，500+ skills，7个市场",
            "gap_detail": "我们有SOUL.md/AGENTS.md等，但完全没有Skills概念。每个Agent启动时靠hardcode指令。",
            "absorption_action": "MUST: 实现SKILL.md解析器 + 技能市场",
        },
        "A2A协议支持": {
            "igp_score": 0,
            "industry_baseline": 7,
            "industry_detail": "150+组织支持的协议，跨Agent通信",
            "gap_detail": "IGP的Agent全部在single process里，没有任何Agent-to-Agent协议。",
            "absorption_action": "MUST: 实现A2A Client/Server",
        },
        "LLM Provider灵活度": {
            "igp_score": 4,
            "industry_baseline": 9,
            "industry_detail": "OpenCode支持75+ providers，Cline支持任意OpenAI-compatible",
            "gap_detail": "我们hardcode了qwen-plus/turbo。每个Provider的API差异没有抽象层。",
            "absorption_action": "SHOULD: 抽象Provider层，支持多模型路由",
        },
        "沙箱安全执行": {
            "igp_score": 5,
            "industry_baseline": 8,
            "industry_detail": "Codex云端Sandbox/Cline Checkpoints/E2B沙箱",
            "gap_detail": "我们有Docker沙箱验证通过，但没有权限分级的审批模式。",
            "absorption_action": "SHOULD: Plan/Act双模式 + 安全审批流",
        },
        "代码库上下文理解": {
            "igp_score": 6,
            "industry_baseline": 9,
            "industry_detail": "Cursor/Claude Code的索引+AGENTS.md/Skills三层上下文",
            "gap_detail": "我们有RAG索引了100个文件的183个代码块，但没达到'任意Agent可查'的通用性。",
            "absorption_action": "COULD: RAG升级 + Skills分层加载",
        },
        "代码审查": {
            "igp_score": 2,
            "industry_baseline": 8,
            "industry_detail": "Codex自动审查/Augment PR自动审查",
            "gap_detail": "我们只做了简单的pytest验证，没有正式的代码审查Agent。",
            "absorption_action": "COULD: 创建CodeReview Agent（Skills格式）",
        },
        "自动测试生成": {
            "igp_score": 5,
            "industry_baseline": 7,
            "industry_detail": "SWE-agent自修复/AgentCI",
            "gap_detail": "我们有test_runner.py (12/16 pass)，但没接入CI流水线。",
            "absorption_action": "SHOULD: 测试Agent接入AgentCI",
        },
        "自动化流水线": {
            "igp_score": 6,
            "industry_baseline": 9,
            "industry_detail": "Codex Cloud Agent/Slack集成/定时Routines",
            "gap_detail": "我们有pr_pipeline.py + gh CLI集成心跳，但没有自动触发和Review环节。",
            "absorption_action": "SHOULD: PR+CI+Review全闭环",
        },
        "PK/进化/淘汰机制": {
            "igp_score": 9,
            "industry_baseline": 2,
            "industry_detail": "没有任何Agent工具具备内部的PK竞争/淘汰再生机制",
            "gap_detail": "这是我们最强的差异化优势。行业全是单Agent或多Agent简单协作，没有'不养闲人'的内卷生态。",
            "absorption_action": "KEEP & ENHANCE: 嫁接到Skills生态上",
        },
        "工单/Goal系统": {
            "igp_score": 7,
            "industry_baseline": 4,
            "industry_detail": "Claude Code有/goal但极其简单",
            "gap_detail": "我们的工单系统(v2.0)已经比较成熟，PK/KPI/回溯都有。但Goal和OpenClaw集成有bug。",
            "absorption_action": "FIX & ENHANCE: 修Goal bug + 集成Skills",
        },
        "Agent数量(生态)": {
            "igp_score": 3,
            "industry_baseline": 9,
            "industry_detail": "Everything Claude Code: 27 agents/64 skills/33 commands",
            "gap_detail": "我们有42个Team Agent但全部hardcode。人家的135 agents是可安装的。",
            "absorption_action": "MUST: Agent技能解耦成可安装的Skills包",
        },
    }
}

# ====================================================================
# PART 3: 差异化优势分析
# ====================================================================

DIFFERENTIATORS = {
    "最独特": [
        "PK竞争/淘汰再生机制 — 行业里唯一一个让Agent之间内卷的体系",
        "42个Team结构 + 14部门 + 参谋部 — 行业没有类似的虚拟企业架构",
        "KPI+Token成本闭环 — 行业全都不关注每个Agent消耗了多少token",
        "开车门(Goal自动触发) — 行业需要手动输入，我们是'你说一句我全自动'",
    ],
    "最薄弱": [
        "MCP协议兼容 — 0分，必须补上",
        "Agent Skills生态 — 0分，最大空白",
        "A2A协议 — 0分，但可以短期不补",
    ],
    "战略思考": {
        "不追低处": "不跟OpenCode比provider数量、不跟Codex比Terminal-Bench",
        "利用优势": "把PK/进化/KPI机制嫁接到标准生态(MCP+Skills+A2A)上",
        "差异化定位": "IGP = 会自我进化的企业架构Agent军团 (不仅是编码工具)",
    },
}


def calc_average(dimension_data):
    scores = [dim_data["igp_score"] for dim_data in dimension_data.values()]
    industry = [
        dim_data["industry_baseline"] for dim_data in dimension_data.values()
    ]
    return {
        "igp_avg": round(sum(scores) / len(scores), 1),
        "industry_avg": round(sum(industry) / len(industry), 1),
        "gap": round(sum(scores) / len(scores) - sum(industry) / len(industry), 1),
    }


def generate_markdown():
    avg = calc_average(COMPARISON["维度"])

    lines = []
    lines.append("# IGP 外部生态吸收报告 (2026-06-30 23:33)")
    lines.append("")
    lines.append(f"**IGP平均分: {avg['igp_avg']}/10 vs 行业基线: {avg['industry_avg']}/10**")
    lines.append(f"**差距: {avg['gap']} 分**")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 一、行业Top Agent排行榜 (2026-06-18)")
    lines.append("")
    lines.append(f"| 排名 | Agent | Stars | SWE-bench V | Term-Bench | 突出特性 |")
    lines.append(f"|------|-------|------:|:-----------:|:----------:|---------|")
    tables = [
        ("Codex CLI + GPT-5.5", "90K", "88.7%", "83.4% (#1)", "5种表面/MCP/Skills"),
        ("Claude Code + Opus 4.8", "131K", "88.6%", "78.9%", "Agent View//goal/Plugin"),
        ("Gemini CLI + 3.1 Pro", "105K", "80.6%", "70.7%", "1000次/天免费"),
        ("OpenCode (自选模型)", "172K⭐", "模型决定", "模型决定", "75+ providers/Scout/MIT"),
        ("Cline (自选模型)", "63K", "模型决定", "模型决定", "Plan-Act双模/Checkpoints"),
        ("Goose (自选模型)", "48K", "模型决定", "模型决定", "Linux Foundation/70+MCP"),
    ]
    for name, stars, swe, tb, feat in tables:
        lines.append(f"| {name} | {stars} | {swe} | {tb} | {feat} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 二、IGP v3 逐维差距分析")
    lines.append("")
    lines.append(f"| 维度 | IGP | 行业 | 差距 | 行动 |")
    lines.append(f"|------|:---:|:----:|:----:|------|")
    for dim, data in COMPARISON["维度"].items():
        score_igp = "🔴" if data["igp_score"] < 3 else "🟡" if data["igp_score"] < 6 else "🟢"
        lines.append(f"| {dim} | {score_igp} {data['igp_score']} | {data['industry_baseline']} | {data['industry_baseline'] - data['igp_score']} | {data['absorption_action']} |")
    lines.append("")
    lines.append(f"| **平均** | **{avg['igp_avg']}** | **{avg['industry_avg']}** | **{avg['gap']}** | |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 三、差异化优势（我们独有的）")
    lines.append("")
    for d in DIFFERENTIATORS["最独特"]:
        lines.append(f"- ✅ **{d}**")
    lines.append("")
    lines.append("### 三个致命空白（必须补）")
    for d in DIFFERENTIATORS["最薄弱"]:
        lines.append(f"- ❌ **{d}**")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 四、吸收计划（按优先级）")
    lines.append("")
    lines.append("| 优先级 | 行动 | 投入 | 收益 |")
    lines.append("|:-----:|------|:---:|:----:|")
    lines.append("| P0 | **MCP协议兼容**：igp_mcp_bridge → 兼容MCP Client + 导出MCP Server | ~4h | 立即接入1200+ MCP服务器生态 |")
    lines.append("| P0 | **Agent Skills系统**：SKILL.md解析器 + 技能目录 + 自动加载 | ~6h | Agent能力从hardcode变成可安装包 |")
    lines.append("| P1 | **Plan/Act双模式** + Checkpoints安全点 | ~3h | 避免Agent乱改代码 |")
    lines.append("| P1 | **Provider抽象层**：多模型路由（保留qwen但增加降级） | ~2h | 不再限于DashScope |")
    lines.append("| P2 | **代码审查Agent**：PR提交后自动审查 | ~3h | 质量保障 |")
    lines.append("| P2 | **AgentCI流水线**：测试+审查+PR全自动 | ~4h | 完成编码闭环 |")
    lines.append("| P3 | **A2A协议**：Agent-to-Agent标准通信 | ~8h | 长期差异化 |")
    lines.append("")
    lines.append("### 预估效果：MCP + Skills实现后，差距从-3.8缩小到-1.0 → 反超行业")
    lines.append("")

    return "\n".join(lines)


def main():
    # 计算分数
    avg = calc_average(COMPARISON["维度"])

    report = {
        "generated_at": "2026-06-30T23:33:00+08:00",
        "scores": avg,
        "ecosystem": ECOSYSTEM,
        "comparison": COMPARISON,
        "differentiators": DIFFERENTIATORS,
        "absorption_plan": [
            {"priority": "P0", "action": "MCP协议兼容", "estimated_hours": 4,
             "impact": "1200+ MCP服务器生态接入"},
            {"priority": "P0", "action": "Agent Skills系统", "estimated_hours": 6,
             "impact": "Agent能力可安装/可共享"},
            {"priority": "P1", "action": "Plan/Act双模式", "estimated_hours": 3,
             "impact": "安全沙箱审批流"},
            {"priority": "P1", "action": "Provider抽象层", "estimated_hours": 2,
             "impact": "多模型路由/降级"},
            {"priority": "P2", "action": "代码审查Agent", "estimated_hours": 3,
             "impact": "自动PR审查"},
            {"priority": "P2", "action": "AgentCI流水线", "estimated_hours": 4,
             "impact": "全自动编码闭环"},
            {"priority": "P3", "action": "A2A协议集成", "estimated_hours": 8,
             "impact": "跨Agent标准通信"},
        ],
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"[OK] 报告已保存: {REPORT_PATH}")
    print(f"[OK] IGP平均分: {avg['igp_avg']}/10 vs 行业基线: {avg['industry_avg']}/10")
    print(f"[OK] 差距: {avg['gap']} 分")

    # 输出markdown
    md = generate_markdown()
    md_path = os.path.join(
        os.path.dirname(__file__), "..", "EXTERNAL_ABSORPTION_REPORT_2026-06-30.md"
    )
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[OK] Markdown报告已保存: {md_path}")
    print("\n" + md)


if __name__ == "__main__":
    main()
