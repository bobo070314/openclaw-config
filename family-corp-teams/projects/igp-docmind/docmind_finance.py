"""
IGP 金融风控分支 — DocMind金融版

吸收源: QuantLib（金融计算）+ Black-Scholes（衍生品定价）+ MPT（现代组合理论）
世界观: 文档不是文档，是金融资产的价格序列/风险信号

DNA突变: 把文档当portfolio分析
  - 段落 = 资产
  - 标题层级 = 资产类别
  - 数字密度 = 风险暴露度
  - 语句波动性 = 市场波动率
"""
import os, json, re, math
from datetime import datetime

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'
DOCMIND_DIR = os.path.join(FAMILY, 'projects', 'igp-docmind')
os.makedirs(DOCMIND_DIR, exist_ok=True)


class DocPortfolio:
    """
    文档组合 — 把文档当投资组合评估
    
    每个段落 = 一个资产
    段落的类型 = 资产类别
    段落的信息密度 = 资产价值
    段落之间的关系 = 资产相关性
    """
    
    ASSET_CLASSES = {
        'A': {'name': '标题', 'risk_weight': 0.6, 'category': 'defensive'},
        'T': {'name': '正文', 'risk_weight': 0.4, 'category': 'core'},
        'G': {'name': '数字', 'risk_weight': 0.9, 'category': 'volatile'},
        'C': {'name': '代码', 'risk_weight': 0.7, 'category': 'growth'},
        'U': {'name': '表格', 'risk_weight': 0.5, 'category': 'balanced'},
        'M': {'name': '列表', 'risk_weight': 0.3, 'category': 'stable'},
        'N': {'name': '符号', 'risk_weight': 0.8, 'category': 'speculative'},
    }
    
    def evaluate(self, text, doc_name='unknown'):
        """评估文档资产组合"""
        from docmind_dna import DocDNA
        
        try:
            dna = DocDNA.encode(text)
        except ImportError:
            # fallback
            paragraphs = [p for p in re.split(r'\n\s*\n', text) if p.strip()]
            dna = []
            for p in paragraphs:
                base = 'T'
                if re.match(r'^#+\s', p): base = 'A'
                elif re.search(r'\|.*\|.*\|', p): base = 'U'
                dna.append({'base': base, 'len': len(p), 'text_preview': p[:50]})
        
        if not dna:
            return None
        
        # 构建组合
        portfolio = []
        total_value = 0
        total_risk = 0
        
        for i, b in enumerate(dna):
            base = b['base']
            info = self.ASSET_CLASSES.get(base, self.ASSET_CLASSES['T'])
            
            # 段落价值 = 长度 × 权重
            value = b['len'] * 0.1
            risk = value * info['risk_weight']
            
            # 有数字的段落风险更高
            if base == 'G' or any(c.isdigit() for c in b.get('text_preview', '')):
                risk *= 1.3
            
            asset = {
                'position': i,
                'type': info['name'],
                'category': info['category'],
                'value': round(value, 2),
                'risk': round(risk, 2),
                'preview': b.get('text_preview', '')[:40],
            }
            portfolio.append(asset)
            total_value += value
            total_risk += risk
        
        # 组合指标
        weighted_return = total_value * 0.08  # 假设预期回报8%
        sharpe = weighted_return / max(total_risk, 0.01)
        
        # 集中度风险（是否有太多同类段落）
        type_counts = {}
        for b in dna:
            t = self.ASSET_CLASSES.get(b['base'], self.ASSET_CLASSES['T'])['name']
            type_counts[t] = type_counts.get(t, 0) + 1
        concentration = max(type_counts.values()) / max(len(dna), 1)
        
        return {
            'doc_name': doc_name,
            'portfolio_value': round(total_value, 2),
            'total_risk': round(total_risk, 2),
            'risk_adjusted_return': round(sharpe, 3),
            'concentration': round(concentration, 2),
            'assets': len(portfolio),
            'type_distribution': type_counts,
            'risk_rating': '低' if sharpe > 0.8 else ('中' if sharpe > 0.3 else '高'),
        }


class BlackScholesDoc:
    """
    Black-Scholes文档定价模型
    
    把文档当成金融衍生品定价：
    - 标题 = 执行价
    - 正文 = 标的资产价格
    - 长度波动率 = 隐含波动率
    - 过期时间 = 文档长度
    """
    
    def price(self, text):
        """给文档定价（0依赖Black-Scholes简化版）"""
        paragraphs = [p for p in re.split(r'\n\s*\n', text) if p.strip()]
        
        if not paragraphs:
            return None
        
        n = len(paragraphs)
        
        # S: 标的资产价格（标题权重）
        headers = [p for p in paragraphs if re.match(r'^#+\s', p)]
        S = len(headers) * 10 + len(text) * 0.01
        
        # K: 执行价（文档预期输出长度）
        K = len(text) * 0.5
        
        # T: 到期时间（段落数）
        T = max(1, n / 5)
        
        # sigma: 波动率（段落长度方差）
        lens = [len(p) for p in paragraphs]
        mean_len = sum(lens) / max(n, 1)
        variance = sum((l - mean_len)**2 for l in lens) / max(n, 1)
        sigma = min(1.0, math.sqrt(variance) / max(mean_len, 1))
        
        # d1 和 d2（简化版BS公式）
        d1 = (math.log(max(S / max(K, 0.01), 0.01)) + (sigma**2 / 2) * T) / max(sigma * math.sqrt(T), 0.01)
        d2 = d1 - sigma * math.sqrt(T)
        
        # 标准正态CDF近似
        N_d1 = 0.5 * (1 + math.erf(d1 / math.sqrt(2)))
        N_d2 = 0.5 * (1 + math.erf(d2 / math.sqrt(2)))
        
        call_price = S * N_d1 - K * math.exp(-0.05 * T) * N_d2
        put_price = K * math.exp(-0.05 * T) * (1 - N_d2) - S * (1 - N_d1)
        
        return {
            'call_price': round(call_price, 2),
            'put_price': round(put_price, 2),
            'volatility': round(sigma, 3),
            'underlying_price': round(S, 2),
            'strike_price': round(K, 2),
            'time_to_expiry': round(T, 2),
            'interest_rate': 0.05,
        }


def demo_finance():
    """金融风控演示"""
    print('= ' * 30)
    print('  IGP 金融风控分支')
    print('  世界观: 文档 = 金融资产组合')
    print('  吸收: QuantLib + Black-Scholes + MPT')
    print('= ' * 30)
    print()
    
    portfolio = DocPortfolio()
    bs = BlackScholesDoc()
    
    test_doc = '''# 2026-Q2 风险管理报告

Author: Risk Committee | Date: 2026-07-01

## 1. 市场风险概览

全球市场波动率指数(VIX)从Q1的18.5上升至Q2的24.3，增长31.4%。
主要风险因素包括：
- 美联储利率决议（7月预期加息25bp）
- 欧洲主权债务利差扩大至180bp
- 新兴市场汇率波动加剧

## 2. 组合风险敞口

| 资产类别 | 敞口($M) | VaR(95%) | 占比 |
|---------|---------|---------|------|
| 固收     | 42.5    | 1.8      | 35%  |
| 权益     | 38.2    | 3.2      | 32%  |
| 大宗商品  | 18.0    | 2.1      | 15%  |
| 外汇     | 12.3    | 1.5      | 10%  |
| 衍生品   | 9.0     | 2.8      | 8%   |

## 3. 风险调整后收益

组合夏普比率0.85，低于目标值1.2。
建议：降低权益占比5%，增加固收配置。

## 4. 特别关注

- 信用风险：BBB级债券利差扩大42bp
- 操作风险：新交易系统上线需加强监控
- 流动性风险：小盘股流动性下降至Q1的65%'''
    
    # 1. 组合评估
    print('1️⃣ 文档投资组合分析')
    print('-' * 40)
    result = portfolio.evaluate(test_doc, '风险报告')
    if result:
        print(f'  文档: {result["doc_name"]}')
        print(f'  组合价值: ¥{result["portfolio_value"]}')
        print(f'  总风险: ¥{result["total_risk"]}')
        print(f'  风险调整收益: {result["risk_adjusted_return"]}')
        print(f'  风险评级: {result["risk_rating"]}')
        print(f'  集中度: {result["concentration"]:.0%}')
        print(f'  资产构成:')
        for t, c in sorted(result['type_distribution'].items(), key=lambda x: -x[1]):
            print(f'    {t}: {c}个')
    print()
    
    # 2. BS定价
    print('2️⃣ Black-Scholes文档定价')
    print('-' * 40)
    price = bs.price(test_doc)
    if price:
        print(f'  Call价格: ¥{price["call_price"]}')
        print(f'  Put价格: ¥{price["put_price"]}')
        print(f'  波动率: {price["volatility"]:.1%}')
        print(f'  标的价: ¥{price["underlying_price"]}')
        print(f'  执行价: ¥{price["strike_price"]}')
        print(f'  到期时间: {price["time_to_expiry"]}期')
        print()
        print(f'  金融含义:')
        print(f'  看涨价值¥{price["call_price"]} > 看跌¥{price["put_price"]}')
        print(f'  → 市场对该文档持乐观态度（资产重估空间大）')
    print()
    
    # 3. DNA视角交叉验证
    print('3️⃣ DNA基因交叉验证')
    print('-' * 40)
    # 找3种不同文档DNA看差异
    samples = {
        '风险报告': test_doc,
        '简单笔记': '# 待办\n- 开会\n- 写代码\n- 吃饭',
        '技术文档': 'def main():\n    print("hello")\n    return True\n\n# EOF',
    }
    for name, text in samples.items():
        try:
            from docmind_dna import DocDNA
            dna = DocDNA.encode(text)
            seq = ''.join(b['base'] for b in dna)
        except:
            seq = 'N/A'
        print(f'  {name}: {seq}')
    print()
    
    print('= ' * 30)
    print('  ✅ 金融风控分支就绪')
    print(f'  状态: {datetime.now().strftime("%H:%M:%S")}')
    print('  下一步: 接入Ollama让分支真正理解风险语义')
    print('= ' * 30)
    
    # 保存
    with open(os.path.join(DOCMIND_DIR, 'finance_branch.json'), 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat()[:19],
            'branch': 'financial_risk',
            'models': ['MPT(组合理论)', 'Black-Scholes(定价)', 'DNA(基因交叉)'],
        }, f)


def main():
    demo_finance()


if __name__ == '__main__':
    main()
