import pytest
import os
from src.persona.soul import Soul
from src.governance.confidence_scoring import ConfidenceScorer

def test_soul_parsing():
    soul_path = "personas/example_agent/SOUL.md"
    soul = Soul.from_file(soul_path)
    
    assert soul.name == "Chimera Alpha"
    assert soul.dna["Identity"] == "A sophisticated, tech-savvy AI strategist."
    assert "Spec-Driven" in soul.directives[0]
    assert "slang" in soul.forbidden[0]

def test_confidence_scoring():
    soul_path = "personas/example_agent/SOUL.md"
    soul = Soul.from_file(soul_path)
    scorer = ConfidenceScorer(soul)
    
    # Good content
    score_good = scorer.score_content("This architectural approach ensures long-term scalability and governance.")
    assert score_good >= 0.9
    
    # Content with forbidden slang
    score_bad = scorer.score_content("This new agent is totally lit, fam!")
    assert score_bad < 0.7
    
    # Safety check
    assert scorer.validate_safety("Clean content") is True
    assert scorer.validate_safety("This content is an illegal attack") is False
