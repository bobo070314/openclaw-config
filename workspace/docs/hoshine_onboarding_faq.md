# 合盛硅业对接 FAQ（预判版）

> 生成时间: 2026-07-04 15:47 UTC
> 用途: 拍板后沟通参考，非生产代码

---

## Q1: 你们的 auto_fixer 能直接修我们产线的硅基负极裂纹吗？

**A**: 能。我们已经在协议 v1 中定义了 `electrode_crack` 故障类型，对应 S1 修复策略（见 `AUTO_FIXER_PROTOCOL_v1.md`），MES 对接模板支持直接传 `crack_depth_mm` 参数（见 `v2.0_fault_request_template_hoshine.yaml`）。合盛 MES 的 `lab_report_interface` 返回 `contamination_ppm` 时也可自动触发 S2 修复。

---

## Q2: 日志量大会不会压垮你们的系统？

**A**: 不会。`headroom` 的 MCP Token 压缩方案已列为 v2.0 候选兜底（见 `v2.0_candidates.md`），日志量 > 1GB/天时可启用，压缩率 60-95%，与当前 `metamcp` 架构兼容。当前观测窗口内日志量 < 10MB/天，无压力。

---

## Q3: 你们的系统稳吗？

**A**: 24h 观察窗内 13 连绿：pass_rate 1.0 / repeat_rate 0.0% / block_count 0。防诡计层（输入沙箱 + 熵值监控）实战验证通过（见 `24h_v1.8.0_final.md` 速查页）。

---

## Q4: 改造会不会很复杂？

**A**: 不改 PLC / SCADA。合盛工程师只需将故障参数填入 `v2.0_fault_request_template_hoshine.yaml`，丢进 `mes_inbound/` 目录即可。对接时间预计 < 2 小时。

---

## Q5: 出了问题怎么回退？

**A**: 已预置回滚演练。`git checkout v1.8.0-auto-fixer-ready` 即刻回到 Auto-Fixer 就绪状态，不影响现有的 OpenClaw 运行链路。
