# B-Line 12:04 续报模板

## 概览

- **时间**: {timestamp}
- **pass_rate**: {pass_rate}
- **repeat_rate**: {repeat_rate}%
- **blocked**: {blocked}
- **injected_count**: {injected_count}
- **轮次数**: {cycle_count}

## 状态

{status_emoji} {status_text}

## 指标趋势

| 时段 | pass_rate | repeat_rate | injected_count |
|---|---|---|---|
| 10:04 | 1.0 | 0.0 | 4 |
| 10:34 | 1.0 | 0.0 | 4 |
| 11:04 | 1.0 | 0.0 | 4 |
| 11:34 | 1.0 | 0.0 | 4 |
| {current_slot} | {pass_rate} | {repeat_rate} | {injected_count} |

## 异常 / 备注

{notes}

## 下轮

```
下一续报: 12:34 (30min后)
无异常 → 静默
```

---

模板使用:
```
python -c "
import json;
d=json.load(open('data/runs/evolution_status.json'));
timestamp=d.get('timestamp','?');
pr=d.get('pass_rate','?');
rr=d.get('repeat_rate','?');
bl=d.get('blocked','?');
ic=d.get('injected_count','?');
print(f'pass_rate: {pr}, repeat_rate: {rr}, blocked: {bl}, injected: {ic}')
"
```
