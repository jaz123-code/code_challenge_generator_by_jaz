import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import Dict, Any
import json

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_mcq_challenge(difficulty: str) -> Dict[str, Any]:
    """
    Generates a coding challenge with multiple-choice answers using an AI model.
    """
    model = genai.GenerativeModel(
        'gemini-pro-latest',
        generation_config=genai.types.GenerationConfig(
            response_mime_type="application/json"
        )
    )
    prompt = f"""
    Generate a multiple-choice coding challenge for a '{difficulty}' level.
    The output must be a single, valid JSON object that follows this exact structure:
    {{
        "question": "The question text, including any code snippets formatted correctly for JSON.",
        "options": {{
            "A": "Option A",
            "B": "Option B",
            "C": "Option C",
            "D": "Option D"
        }},
        "answer": "The key of the correct option (e.g., 'A')",
        "explanation": "A detailed explanation of why the answer is correct."
    }}
    """
    response = model.generate_content(prompt)
    try:
        # The response may already be parsed, or it might be a string.
        if hasattr(response, 'text') and isinstance(response.text, str):
            return json.loads(response.text)
        elif isinstance(response, str):
            return json.loads(response)
        else:
            # If the response is not a string, it might be an object with a text attribute
            # that needs parsing, or something else. This handles the case where it's already loaded.
            # This part is tricky because the library behavior can vary.
            # A common pattern is that the content is in response.parts[0].text
            # but let's stick to response.text for now as it's the most common.
            # The error logs will tell us more if this fails.
            # Assuming the library sometimes returns a dict-like object directly
            # For now, let's assume response.text is the primary source.
            # The previous error suggests response.text is sometimes a dict.
            # Let's refine the logic to handle that.
            if hasattr(response, 'text'):
                if isinstance(response.text, dict):
                    return response.text
                return json.loads(response.text)
            raise ValueError("Response object does not have a 'text' attribute.")

    except (json.JSONDecodeError, TypeError, AttributeError, ValueError) as e:
        print(f"Error processing response from Gemini: {e}")
        print(f"Received response object: {response}")
        raise ValueError("Failed to get a valid JSON response from the AI model.") from e
