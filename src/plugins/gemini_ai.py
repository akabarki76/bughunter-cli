from src.utils.tool_registration import register_tool, BaseTool
import google.generativeai as genai
import os

@register_tool("gemini_ai")
class GeminiAI(BaseTool):
    name = "gemini_ai"
    description = "AI-powered text generation using Google Gemini."

    def __init__(self):
        super().__init__(self.name, self.description)
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if gemini_api_key:
            genai.configure(api_key=gemini_api_key)
        else:
            raise ValueError("GEMINI_API_KEY not configured. Please set it in your .env file.")

    def run(self, prompt: str, output_file: str = None, **kwargs):
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            if output_file:
                with open(output_file, "w") as f:
                    f.write(response.text)
            return response.text
        except Exception as e:
            return f"Error calling Gemini API: {e}"
