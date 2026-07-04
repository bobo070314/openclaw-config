class SkillMarket:
    def __init__(self):
        self.skills = {}
        self.skill_ratings = {}

    def add_skill(self, skill_name, metadata, instructions):
        self.skills[skill_name] = {
            'metadata': metadata,
            'instructions': instructions
        }

    def rate_skill(self, skill_name, score):
        self.skill_ratings[skill_name] = score

    def get_top_skills(self, limit=5):
        sorted_skills = sorted(self.skill_ratings.items(), key=lambda x: x[1], reverse=True)
        return sorted_skills[:limit]

    def install_skill(self, skill_name):
        if skill_name in self.skills:
            print(f"✅ Installed skill: {skill_name}")
        else:
            print(f"❌ Skill not found: {skill_name}")

    def uninstall_skill(self, skill_name):
        if skill_name in self.skills:
            del self.skills[skill_name]
            print(f"✅ Uninstalled skill: {skill_name}")
        else:
            print(f"❌ Skill not found: {skill_name}")