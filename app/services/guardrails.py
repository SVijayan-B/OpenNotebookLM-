from typing import List, Dict


class Guardrails:
    @staticmethod
    def validate_retrieval(results: List[Dict]) -> bool:
        """
        Ensures we have at least one strong retrieval result.
        """
        if not results:
            return False

        # If all scores are very low, refuse
        max_score = max(r["score"] for r in results)
        return max_score >= 0.35

    @staticmethod
    def validate_answer(answer: str) -> bool:
        """
        Ensures the LLM produced a meaningful answer.
        """
        if not answer:
            return False

        refusal_phrases = [
            "i don't know",
            "not provided",
            "cannot determine",
            "no information",
        ]

        lower = answer.lower()
        return not any(p in lower for p in refusal_phrases)

    @staticmethod
    def refusal_response() -> Dict:
        return {
            "answer": "I don't know based on the provided documents.",
            "sources": []
        }
