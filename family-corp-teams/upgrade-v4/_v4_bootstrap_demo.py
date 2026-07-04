import os
import sys
import importlib.util
import inspect

def load_v4_unified_engine():
    script_path = os.path.abspath("v4_unified_engine.py")
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"File not found: {script_path}")
    
    spec = importlib.util.spec_from_file_location("v4_unified_engine", script_path)
    v4_unified_engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(v4_unified_engine)
    return v4_unified_engine

def generate_skill(engine, skill_name):
    prompt = f"Generate a new skill named '{skill_name}' that demonstrates self-upgrade capability. Include a description and usage instructions."
    response = engine.providers.chat(prompt)
    return response

def save_skill(engine, skill_name, content):
    skills_dir = os.path.join("upgrade-v4", "skills", skill_name)
    os.makedirs(skills_dir, exist_ok=True)
    skill_path = os.path.join(skills_dir, "SKILL.md")
    with open(skill_path, "w") as f:
        f.write(content)
    return skill_path

def main():
    try:
        # 1. Load V4UnifiedEngine
        engine = load_v4_unified_engine()
        
        # 2. Generate a new skill
        skill_name = "self_upgrade"
        generated_skill = generate_skill(engine, skill_name)
        
        # 3. Save the generated skill
        skill_path = save_skill(engine, skill_name, generated_skill)
        print(f"Skill saved to: {skill_path}")
        
        # 4. Discover and verify the skill
        discovered_skills = engine.skills.discover_skills()
        if skill_name in discovered_skills:
            print(f"Skill '{skill_name}' was successfully loaded.")
        else:
            print(f"Skill '{skill_name}' was NOT loaded. Discovery result: {discovered_skills}")
        
        # 5. Print bootstrapping report
        print("\n--- Bootstrapping Report ---")
        print(f"Generated Skill:\n{generated_skill}")
        print(f"Discovered Skills: {discovered_skills}")
        print("----------------------------")

    except Exception as e:
        print(f"Error during bootstrapping: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()