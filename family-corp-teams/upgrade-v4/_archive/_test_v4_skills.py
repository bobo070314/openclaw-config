import os
import unittest
from pathlib import Path

def test_skill_loader():
    skill_dir = 'D:/bobo/openclaw-foreign/workspace/family-corp-teams/upgrade-v4/skills'
    
    # 检查技能目录是否存在
    assert os.path.exists(skill_dir), f"Skill directory not found: {skill_dir}"
    
    # 检查至少一个SKILL.md文件存在
    skill_files = list(Path(skill_dir).rglob('SKILL.md'))
    assert len(skill_files) > 0, "No SKILL.md files found in the skills directory"
    
    # 检查每个SKILL.md文件的格式
    for file in skill_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否包含必要的部分
        assert '## Description' in content, f"Missing description in {file}"
        assert '## Metadata' in content, f"Missing metadata in {file}"
        assert '## Instructions' in content, f"Missing instructions in {file}"
        
    print("All tests passed!")

if __name__ == "__main__":
    test_skill_loader()