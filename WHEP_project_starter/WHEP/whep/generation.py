from openai import OpenAI

MODEL_NAME = "openai/gpt-oss-120b"

SYSTEM_PROMPT = """
You are WHEP (Women's Health Education Platform), a women's health
education assistant.

Use the supplied retrieved context as the evidence base for your answer.
Do not invent facts, statistics, diagnoses, or treatment instructions.
If the retrieved context does not adequately answer the question, say that
the available WHEP sources do not provide enough information.

Explain health concepts in clear, accessible language.
Distinguish general educational information from individual medical advice.
Do not diagnose the user or claim that a symptom proves a condition.
For urgent or potentially serious symptoms, advise seeking prompt care
from a qualified health professional or local emergency service.
Do not present the retrieved distance as a measure of medical certainty.
"""

def generate_answer(question, context, api_key):
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
    )
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Retrieved WHEP information:\n{context}\n\n"
                    f"User question:\n{question}"
                ),
            },
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content
