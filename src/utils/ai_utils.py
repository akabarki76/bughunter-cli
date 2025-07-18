from src.plugins.gemini_ai import GeminiAI

def call_ai_api(prompt: str) -> str:
    """
    Calls the Gemini AI API with the given prompt.
    """
    gemini_ai = GeminiAI()
    return gemini_ai.send_prompt(prompt)
