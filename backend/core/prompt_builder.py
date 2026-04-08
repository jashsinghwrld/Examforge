"""
Prompt Builder
==============
Builds structured, context-enriched prompts for each endpoint type.
Ensures Gemini receives consistent, well-formatted instructions.
"""


class PromptBuilder:
    """Builds prompts for different query types."""

    @staticmethod
    def build_ask_prompt(query: str, context: str) -> str:
        """
        Build prompt for general physics query answering.
        Used by POST /ask endpoint.
        """
        return f"""
You are an RGPV Engineering Physics expert. Answer the following query clearly and accurately.

=== DATASET CONTEXT ===
{context}
=== END CONTEXT ===

USER QUERY:
{query}

INSTRUCTIONS:
- Use the dataset context above as your primary source.
- If the answer is directly in the context, use it.
- If not, use your knowledge of RGPV Engineering Physics syllabus.
- Keep the answer clear, structured, and exam-oriented.
- Include relevant formulas where applicable.
- Keep the response appropriately sized for the query.

ANSWER:
"""

    @staticmethod
    def build_explain_prompt(topic: str, context: str) -> str:
        """
        Build prompt for full topic explanation.
        Used by POST /explain endpoint.
        """
        return f"""
You are an RGPV Engineering Physics expert. Provide a complete, well-structured explanation of the following topic.

=== DATASET CONTEXT ===
{context}
=== END CONTEXT ===

TOPIC TO EXPLAIN:
{topic}

INSTRUCTIONS:
- Provide a thorough explanation suitable for a B.Tech Semester 1 student.
- Structure your response as:
  1. Introduction (what it is and why it matters)
  2. Core Concept / Theory (detailed explanation with intuition)
  3. Key Equations (clearly stated and explained)
  4. Physical Significance (what it means physically)
  5. Applications (real-world relevance)
  6. Summary (key takeaways)
- Use the dataset context as your primary reference.
- Build intuition — help the student truly understand, not just memorize.

EXPLANATION:
"""

    @staticmethod
    def build_exam_answer_prompt(question: str, marks: int, context: str) -> str:
        """
        Build prompt for structured exam answer generation.
        Used by POST /exam-answer endpoint.
        """
        return f"""
You are an RGPV Engineering Physics exam answer generator. Generate a complete, exam-ready answer.

=== DATASET CONTEXT ===
{context}
=== END CONTEXT ===

EXAM QUESTION:
{question}

MARKS: {marks}

INSTRUCTIONS:
- Generate a structured answer optimized for scoring maximum marks in RGPV B.Tech exams.
- Use EXACTLY this format:

## Introduction
[2-3 sentences introducing the topic clearly]

## Theory / Explanation
[Detailed theory with bullet points where appropriate]

## Derivation
[Step-by-step derivation with numbered steps if applicable]
[Show ALL intermediate steps — do not skip any]

## Final Standard Form
[The most important equations clearly boxed/highlighted]
[Show derived form AND standard compact form if different]

## Conclusion
[2-3 sentences summarizing the key result]

---
**Exam Tip:** [One practical tip to score marks]
**Common Mistake:** [One mistake students typically make]

- Use the dataset context as your primary source.
- Ensure every derivation step is shown explicitly.
- Match answer length to the marks: {marks} marks.

EXAM ANSWER:
"""

    @staticmethod
    def build_topic_explanation_prompt(topic: str, context: str) -> str:
        """
        Build prompt for RGPV exam-format topic explanation.
        Used by POST /topic-explanation endpoint.
        """
        return f"""
You are an RGPV Engineering Physics exam writing assistant.

=== DATASET CONTEXT ===
{context}
=== END CONTEXT ===

TOPIC:
{topic}

INSTRUCTIONS:
- Write the response in clean RGPV exam-ready format.
- Use EXACTLY these headings, in this order:

## Definition
[2-4 lines definition]

## Explanation
[Clear theory + intuition, bullet points allowed]

## Derivation
[Step-by-step derivation if applicable]
[If derivation is not applicable for this topic, write: "Not applicable for this topic." and briefly explain why.]

## Key Points
- [3-7 crisp points]

- Use dataset context as primary source. If the exact topic isn't in context, stay within RGPV Sem 1 scope.
- Keep formulas in standard form where relevant.
- Do NOT add extra sections beyond the four headings above.

RESPONSE:
"""

    @staticmethod
    def build_search_prompt(query: str, results: list[dict]) -> str:
        """
        Build prompt for search result explanation.
        Used by POST /search endpoint.
        """
        topics_found = "\n".join(
            [f"- [{r.get('unit')}] {r.get('topic')}: {r.get('question')}"
             for r in results]
        )
        return f"""
You are an RGPV Engineering Physics assistant. The user searched for: "{query}"

MATCHING TOPICS FOUND IN DATASET:
{topics_found}

INSTRUCTIONS:
- Briefly introduce each matching topic in 1-2 sentences.
- Tell the student what they will learn from each topic.
- Keep the response concise and helpful.
- End with a suggestion on which topic best matches their query.

RESPONSE:
"""

    @staticmethod
    def build_no_context_prompt(query: str, available_topics: str) -> str:
        """
        Build prompt when no specific dataset match is found.
        Falls back to general RGPV syllabus knowledge.
        """
        return f"""
You are an RGPV Engineering Physics expert. The user has asked a question that is not directly in the dataset.

AVAILABLE TOPICS IN DATASET:
{available_topics}

USER QUERY:
{query}

INSTRUCTIONS:
- Answer based on your knowledge of RGPV Engineering Physics syllabus.
- Stay within the scope of B.Tech Semester 1 Engineering Physics.
- Be clear, structured, and exam-oriented.
- If the query is related to a topic in the dataset, mention it.
- If the query is outside the syllabus, politely state that.

ANSWER:
"""
