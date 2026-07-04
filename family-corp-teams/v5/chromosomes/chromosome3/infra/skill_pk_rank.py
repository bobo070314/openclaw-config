class SkillPKRank:
    def __init__(self):
        self.skill_stats = {}

    def update_stats(self, skill_name, success_rate, token_usage):
        self.skill_stats[skill_name] = {
            'success_rate': success_rate,
            'token_usage': token_usage
        }

    def calculate_score(self, skill_name):
        if skill_name in self.skill_stats:
            success_rate = self.skill_stats[skill_name]['success_rate']
            token_usage = self.skill_stats[skill_name]['token_usage']
            return success_rate * 10 - token_usage / 100
        return 0

    def rank_skills(self):
        ranked_skills = sorted(self.skill_stats.items(), key=lambda x: self.calculate_score(x[0]), reverse=True)
        return ranked_skills

    def check_promotion(self, skill_name):
        score = self.calculate_score(skill_name)
        if score > 80:
            return 'Promote'
        elif score < 50:
            return 'Demote'
        else:
            return 'Maintain'