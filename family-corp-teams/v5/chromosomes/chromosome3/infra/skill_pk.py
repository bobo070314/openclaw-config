import os
import json
from typing import Dict, List, Optional, Tuple, Set

class SkillPackage:
    def __init__(self, skill_id: str, version: str, dependencies: List[str], metadata: Dict):
        self.skill_id = skill_id
        self.version = version
        self.dependencies = dependencies
        self.metadata = metadata

    def to_dict(self) -> Dict:
        return {
            'skill_id': self.skill_id,
            'version': self.version,
            'dependencies': self.dependencies,
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'SkillPackage':
        return cls(
            data['skill_id'],
            data['version'],
            data['dependencies'],
            data['metadata']
        )

    def validate(self) -> bool:
        # Check if skill_id is valid
        if not self.skill_id or not re.match(r'^[a-zA-Z0-9_-]+$', self.skill_id):
            return False
        
        # Check if version is valid
        if not self.version or not re.match(r'^v\d+\.\d+\.\d+$', self.version):
            return False
        
        # Check if dependencies are valid
        for dep in self.dependencies:
            if not re.match(r'^[a-zA-Z0-9_-]+$', dep):
                return False
        
        # Check if metadata is valid
        if not isinstance(self.metadata, dict):
            return False
        
        return True

class SkillPackageLoader:
    def __init__(self, package_dir: str):
        self.package_dir = package_dir

    def load_package(self, package_name: str) -> Optional[SkillPackage]:
        package_path = os.path.join(self.package_dir, package_name)
        if not os.path.exists(package_path):
            return None
        
        # Load package info
        with open(os.path.join(package_path, 'package.json'), 'r', encoding='utf-8') as f:\n            package_data = json.load(f)\n        \n        # Load metadata\n        with open(os.path.join(package_path, 'SKILL.md'), 'r', encoding='utf-8') as f:\n            metadata = self._parse_skill_metadata(f.read())\n        \n        return SkillPackage(\n            package_data['skill_id'],\n            package_data['version'],
            package_data['dependencies'],
            metadata
        )

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

class SkillPackageManager:
    def __init__(self, package_dir: str):
        self.package_dir = package_dir

    def create_package(self, skill_id: str, version: str, dependencies: List[str], metadata: Dict) -> bool:
        package_path = os.path.join(self.package_dir, f"{skill_id}-{version}")
        if os.path.exists(package_path):
            return False
        
        os.makedirs(package_path)
        
        # Create package.json
        package_data = {
            'skill_id': skill_id,
            'version': version,
            'dependencies': dependencies
        }
        with open(os.path.join(package_path, 'package.json'), 'w', encoding='utf-8') as f:\n            json.dump(package_data, f, ensure_ascii=False, indent=4)\n        \n        # Create SKILL.md\n        with open(os.path.join(package_path, 'SKILL.md'), 'w', encoding='utf-8') as f:\n            f.write(f"id: {metadata['id']}\n")
            f.write(f"description: {metadata['description']}\n")
            f.write(f"location: {metadata['location']}\n")
            f.write(f"version: {metadata['version']}\n")
            f.write(f"tags: {','.join(metadata['tags'])}\n")
            f.write(f"keywords: {','.join(metadata['keywords'])}\n")
        
        return True

    def delete_package(self, skill_id: str, version: str) -> bool:
        package_path = os.path.join(self.package_dir, f"{skill_id}-{version}")
        if not os.path.exists(package_path):
            return False
        
        # Remove package directory
        os.rmdir(package_path)
        return True

    def list_packages(self) -> List[Tuple[str, str]]:
        packages = []
        for item in os.listdir(self.package_dir):
            if os.path.isdir(os.path.join(self.package_dir, item)):
                # Extract skill_id and version from directory name
                parts = item.split('-')
                if len(parts) == 2:
                    skill_id, version = parts
                    packages.append((skill_id, version))
        return packages