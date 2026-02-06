import os
import re
from typing import Any


class Soul:
    """Representation of an Agent's Persona based on SOUL.md."""

    def __init__(self, name: str, dna: dict[str, str], directives: list[str], forbidden: list[str]):
        self.name = name
        self.dna = dna
        self.directives = directives
        self.forbidden = forbidden

    @classmethod
    def from_file(cls, path: str) -> 'Soul':
        """Parse a SOUL.md file into a Soul object."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"SOUL.md not found at {path}")

        with open(path) as f:
            content = f.read()

        # Simple regex-based parsing for demo purposes
        name_match = re.search(r'# Persona:\s*(.*)', content)
        name = name_match.group(1).strip() if name_match else "Unknown"

        dna = {}
        dna_section = re.search(r'## Character DNA\n(.*?)\n##', content, re.S)
        if dna_section:
            items = re.findall(r'- \*\*(.*?):\*\* (.*)', dna_section.group(1))
            dna = {k.strip(): v.strip() for k, v in items}

        directives = []
        dir_section = re.search(r'## Core Directives\n(.*?)\n##', content, re.S)
        if dir_section:
            directives = [line.strip('- ').strip() for line in dir_section.group(1).split('\n') if line.strip()]

        forbidden = []
        forb_section = re.search(r'## Forbidden Actions\n(.*)', content, re.S)
        if forb_section:
            forbidden = [line.strip('- ').strip() for line in forb_section.group(1).split('\n') if line.strip()]

        return cls(name, dna, directives, forbidden)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "dna": self.dna,
            "directives": self.directives,
            "forbidden": self.forbidden
        }
