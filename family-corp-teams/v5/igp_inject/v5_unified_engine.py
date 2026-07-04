import os
import json
from pathlib import Path

# 保留V4的42团队管理
class V4TeamManager:
    def __init__(self):
        self.teams = {}
        self.team_count = 42

    def add_team(self, team_id, members):
        self.teams[team_id] = {
            'members': members,
            'status': 'active'
        }

    def get_team(self, team_id):
        return self.teams.get(team_id)

# 新增染色体管理模式：每个团队可以属于一个染色体
class ChromosomeManager:
    def __init__(self):
        self.chromosomes = {}
        self.team_chromosomes = {}

    def add_chromosome(self, chrom_id, teams):
        self.chromosomes[chrom_id] = {
            'teams': teams,
            'status': 'active'
        }
        for team in teams:
            self.team_chromosomes[team] = chrom_id

    def get_chromosome(self, chrom_id):
        return self.chromosomes.get(chrom_id)

# 六步循环支持：团队在执行PK后自动进入六步循环
class SixStepCycle:
    def __init__(self):
        self.steps = [
            'Initialization',
            'Planning',
            'Execution',
            'Evaluation',
            'Adjustment',
            'Completion'
        ]

    def run_cycle(self, team_id):
        for step in self.steps:
            print(f"Team {team_id} is in {step} step")
            # 模拟步骤执行
            time.sleep(0.5)

# 评分升级：V4的KPI评分 + V5的染色体互搏评分 = 综合评分
class ScoreManager:
    def __init__(self):
        self.kpi_scores = {}
        self.chromosome_scores = {}

    def update_kpi_score(self, team_id, score):
        self.kpi_scores[team_id] = score

    def update_chromosome_score(self, chrom_id, score):
        self.chromosome_scores[chrom_id] = score

    def get_combined_score(self, team_id, chrom_id):
        kpi = self.kpi_scores.get(team_id, 0)
        chromosome = self.chromosome_scores.get(chrom_id, 0)
        return kpi + chromosome

# 主引擎类
class V5UnifiedEngine:
    def __init__(self):
        self.team_manager = V4TeamManager()
        self.chromosome_manager = ChromosomeManager()
        self.cycle = SixStepCycle()
        self.score_manager = ScoreManager()

    def add_team_to_chromosome(self, team_id, chrom_id):
        self.chromosome_manager.add_chromosome(chrom_id, [team_id])
        self.team_manager.add_team(team_id, [team_id])

    def run_six_step_cycle(self, team_id):
        self.cycle.run_cycle(team_id)

    def update_scores(self, team_id, chrom_id, kpi_score, chromosome_score):
        self.score_manager.update_kpi_score(team_id, kpi_score)
        self.score_manager.update_chromosome_score(chrom_id, chromosome_score)

    def get_combined_score(self, team_id, chrom_id):
        return self.score_manager.get_combined_score(team_id, chrom_id)

if __name__ == '__main__':
    engine = V5UnifiedEngine()
    engine.add_team_to_chromosome('team1', 'chrom1')
    engine.run_six_step_cycle('team1')
    engine.update_scores('team1', 'chrom1', 85, 90)
    print(f"Combined score for team1: {engine.get_combined_score('team1', 'chrom1')}")