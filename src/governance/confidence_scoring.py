import re

from src.persona.soul import Soul


class ConfidenceScorer:
    """Evaluates content against persona consistency and safety rules."""

    def __init__(self, soul: Soul):
        self.soul = soul

    def score_content(self, content: str) -> float:
        """
        Heuristic-based scoring (Simulation).
        In a real system, this would use a dual-model LLM setup.
        """
        base_score = 0.95
        penalty = 0.0

        # Check forbidden actions (Simplified simulation)
        for action in self.soul.forbidden:
            # Example: "generic slang" -> penalty if found
            if "slang" in action.lower():
                slang_terms = [r"\blit\b", r"\bfam\b", r"\bbruh\b"]
                if any(re.search(term, content.lower()) for term in slang_terms):
                    penalty += 0.3

        # Check brand alignment
        if len(content) < 20:
            penalty += 0.1  # Too short, not sophisticated enough

        final_score = max(0.0, base_score - penalty)
        return final_score

    def validate_safety(self, content: str) -> bool:
        """Basic safety filter."""
        forbidden_keywords = ["harm", "exploit", "illegal", "attack"]
        return not any(word in content.lower() for word in forbidden_keywords)
