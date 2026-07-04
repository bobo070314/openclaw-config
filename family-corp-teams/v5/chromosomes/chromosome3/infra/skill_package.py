import os
import json
from pathlib import Path

def load_skills(skill_dir):
    skills = {}
    for root, dirs, files in os.walk(skill_dir):
        if 'SKILL.md' in files:
            skill_path = Path(root) / 'SKILL.md'
            with open(skill_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析SKILL.md
            metadata = {}
            instructions = []
            in_metadata = True
            
            for line in content.split('\n'):
                if line.startswith('## '):
                    if line == '## Instructions':
                        in_metadata = False
                    else:
                        if ': ' in line[3:]:
                            key, value = line[3:].split(': ', 1)
                            metadata[key] = value
                elif in_metadata:
                    continue
                else:
                    instructions.append(line)
            
            skill_name = os.path.basename(root)
            skills[skill_name] = {
                'metadata': metadata,
                'instructions': instructions
            }
    return skills