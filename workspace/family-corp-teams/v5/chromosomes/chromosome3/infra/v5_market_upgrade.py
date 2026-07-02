import os
import json
import re
from typing import Dict, List, Optional, Tuple, Set

class SkillRegistry:
    def __init__(self):
        self.skills = {}
        self.tags = {}
        self.keywords = {}

    def add_skill(self, skill_id: str, metadata: Dict):
        if skill_id in self.skills:
            raise ValueError(f"Skill {skill_id} already exists")
        
        self.skills[skill_id] = metadata
        
        # Update tags
        for tag in metadata.get('tags', []):
            if tag not in self.tags:
                self.tags[tag] = set()
            self.tags[tag].add(skill_id)
        
        # Update keywords
        for keyword in metadata.get('keywords', []):
            if keyword not in self.keywords:
                self.keywords[keyword] = set()
            self.keywords[keyword].add(skill_id)

    def remove_skill(self, skill_id: str):
        if skill_id not in self.skills:
            raise ValueError(f"Skill {skill_id} not found")
        
        # Remove from tags
        for tag in self.skills[skill_id].get('tags', []):
            self.tags[tag].remove(skill_id)
            if not self.tags[tag]:
                del self.tags[tag]
        
        # Remove from keywords
        for keyword in self.skills[skill_id].get('keywords', []):
            self.keywords[keyword].remove(skill_id)
            if not self.keywords[keyword]:
                del self.keywords[keyword]
        
        del self.skills[skill_id]

    def get_skill(self, skill_id: str) -> Optional[Dict]:
        return self.skills.get(skill_id)

    def search_skills(self, query: str) -> List[Tuple[str, Dict]]:
        # Split query into keywords and tags
        keywords = set(re.findall(r'\b\w+\b', query.lower()))
        tags = set([tag for tag in query.split() if tag.startswith('#')])
        
        # Remove # from tags
        tags = {tag[1:] for tag in tags}
        
        # Find matching skills
        matching_skills = set()
        
        # Match keywords
        for keyword in keywords:
            if keyword in self.keywords:
                matching_skills.update(self.keywords[keyword])
        
        # Match tags
        for tag in tags:
            if tag in self.tags:
                matching_skills.update(self.tags[tag])
        
        # Return sorted by relevance (keyword matches first)
        return [(skill_id, self.skills[skill_id]) for skill_id in matching_skills]

    def list_all_skills(self) -> List[Tuple[str, Dict]]:
        return list(self.skills.items())

    def get_tags(self) -> Dict[str, Set[str]]:
        return self.tags

    def get_keywords(self) -> Dict[str, Set[str]]:
        return self.keywords

class SkillPluginLoader:
    def __init__(self, registry: SkillRegistry):
        self.registry = registry

    def load_skill(self, skill_path: str):
        if not os.path.exists(skill_path):
            raise FileNotFoundError(f"Skill path {skill_path} not found")
        
        # Read SKILL.md
        with open(os.path.join(skill_path, 'SKILL.md'), 'r', encoding='utf-8') as f:
            metadata = self._parse_skill_metadata(f.read())
        
        # Add to registry
        self.registry.add_skill(metadata['id'], metadata)

    def _parse_skill_metadata(self, content: str) -> Dict:
        metadata = {}
        lines = content.split('\n')
        
        # Parse id
        for line in lines:
            if line.startswith('id: '):
                metadata['id'] = line[len('id: '):].strip()
                break
        
        # Parse description
        for line in lines:
            if line.startswith('description: '):
                metadata['description'] = line[len('description: '):].strip()
                break
        
        # Parse location
        for line in lines:
            if line.startswith('location: '):
                metadata['location'] = line[len('location: '):].strip()
                break
        
        # Parse version
        for line in lines:
            if line.startswith('version: '):
                metadata['version'] = line[len('version: '):].strip()
                break
        
        # Parse tags
        tags = []
        for line in lines:
            if line.startswith('tags: '):
                tags = [tag.strip() for tag in line[len('tags: '):].split(',')]
                break
        metadata['tags'] = tags
        
        # Parse keywords
        keywords = []
        for line in lines:
            if line.startswith('keywords: '):
                keywords = [keyword.strip() for keyword in line[len('keywords: '):].split(',')]
                break
        metadata['keywords'] = keywords
        
        return metadata

class SkillVersionManager:
    def __init__(self, registry: SkillRegistry):
        self.registry = registry

    def get_version(self, skill_id: str) -> Optional[str]:
        skill = self.registry.get_skill(skill_id)
        return skill.get('version') if skill else None

    def set_version(self, skill_id: str, version: str):
        skill = self.registry.get_skill(skill_id)
        if not skill:
            raise ValueError(f"Skill {skill_id} not found")
        
        skill['version'] = version

    def get_dependencies(self, skill_id: str) -> Optional[List[str]]:
        skill = self.registry.get_skill(skill_id)
        return skill.get('dependencies', []) if skill else None

    def set_dependencies(self, skill_id: str, dependencies: List[str]):
        skill = self.registry.get_skill(skill_id)
        if not skill:
            raise ValueError(f"Skill {skill_id} not found")
        
        skill['dependencies'] = dependencies

    def check_dependencies(self, skill_id: str) -> bool:
        dependencies = self.get_dependencies(skill_id)
        if not dependencies:
            return True
        
        for dep in dependencies:
            if self.registry.get_skill(dep) is None:
                return False
        
        return True

class SkillSearchEngine:
    def __init__(self, registry: SkillRegistry):
        self.registry = registry

    def search(self, query: str) -> List[Tuple[str, Dict]]:
        return self.registry.search_skills(query)

    def list_all(self) -> List[Tuple[str, Dict]]:
        return self.registry.list_all_skills()

    def get_tags(self) -> Dict[str, Set[str]]:
        return self.registry.get_tags()

    def get_keywords(self) -> Dict[str, Set[str]]:
        return self.registry.get_keywords()

if __name__ == '__main__':
    import time
    reg = SkillRegistry()
    reg.add_skill('test', {'name':'Test','version':'1.0','tags':['demo']})
    assert len(reg.list_all_skills()) == 1, 'Add failed'
    info = reg.get_skill('test')
    assert info is not None, 'Get failed'
    results = reg.search_skills('#demo')
    assert len(results) > 0, 'Search failed'
    print(f'Registry: {reg.list_all_skills()}')
    print(f'Search: {results}')
    print('=== [DONE] Skills market UPGRADE ===')